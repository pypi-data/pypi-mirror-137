import atexit
import base64
import hashlib
import json
import logging
import os
import os.path
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.parse
import uuid
from http import HTTPStatus

import click
import coloredlogs
import halo
import inquirer
import pandas as pd
import requests
import tabulate
import yaml
from dateutil import parser
from tinynetrc import Netrc

logger = logging.getLogger("elbo.client")
coloredlogs.install(level='DEBUG',
                    logger=logger,
                    fmt='%(name)s %(message)s'
                    )

__version__ = "0.3"


# noinspection PyMethodMayBeStatic
class ElboConnector:
    #
    # Server endpoints
    #
    UPLOAD_URL_ENDPOINT = "upload_url"
    SCHEDULE_ENDPOINT = "schedule"
    PROVISION_ENDPOINT = "provision"
    CREATE_ENDPOINT = "create"
    LOGS_ENDPOINT = "logs"
    RESOURCE_ENDPOINT = "resource"
    DASHBOARD_ENDPOINT = "dashboard"
    STATUS_ENDPOINT = "status"
    TASKS_ENDPOINT = "tasks"
    SHOW_ENDPOINT = "show"
    REMOVE_ENDPOINT = "rm"
    CANCEL_ENDPOINT = "cancel"

    ELBO_TOKEN_FILE = os.path.expanduser("~/.elbo/token")

    # TODO: Add back SSL in Cloud fare after fixing HTTP error 524 -- Long polling
    # noinspection HttpUrlsUsage
    ELBO_HOST = "http://bayes.elbo.ai"
    ELBO_STAGING_HOST = "https://rbm.elbo.ai"
    ELBO_TEST_HOST = "http://localhost:5006"

    def __init__(self):
        self._host_name = ElboConnector.get_elbo_host()

    @staticmethod
    def get_elbo_host():
        if os.getenv('ELBO_TEST_MODE') is not None:
            return ElboConnector.ELBO_TEST_HOST
        elif os.getenv('ELBO_STAGING_MODE') is not None:
            return ElboConnector.ELBO_STAGING_HOST
        else:
            return ElboConnector.ELBO_HOST

    def get_auth_token(self):
        """
        Get the ELBO service authentication tokens using NETRC
        :return: The auth tokens
        """
        netrc = Netrc()
        host_name = self._host_name
        tokens = netrc.get(host_name)
        if tokens['password'] is None:
            logger.error(f"please login to elbo service by running `elbo login`")
            exit(0)
        else:
            return tokens['password']

    def request(self, end_point, params=None, host=None):
        """
        Call the rest API get
        """
        if not host:
            host = self._host_name
        url = host + "/" + end_point
        token = self.get_auth_token()
        headers = {
            # Flask does not like `_` in header keys
            'TOKEN': token
        }

        try:
            # Keep a high timeout
            response = requests.get(url, headers=headers, params=params, timeout=5 * 60)
        except requests.exceptions.ConnectionError as _connection_error:
            logger.error(f"Unable to connect to ELBO Server -- {_connection_error}")
            return None

        if response.ok:
            response_json = response.text
            response = json.loads(response_json)
        else:
            if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
                logger.error(f"🚨 {response.text}")
            elif response.status_code == HTTPStatus.UNAUTHORIZED:
                logger.error(f"🚨 we are not able to authorize you, could you try `elbo login` again?")
                exit(-1)
            elif response.status_code == HTTPStatus.NOT_FOUND:
                logger.error(f"🚨 got resource not found error")
            elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                print("")
                logger.error(f"🚨 we hit a glitch --> {response.text}")
                logger.error(f"Please email this to contact@elbo.ai")
            else:
                logger.error(f"received unknown error code - {response.status_code} with message - {response.text}")
            response = None

        return response


__elbo_connector = ElboConnector()


def read_config(config_file):
    """
    Read the config file and verify that is valid and has all the requirements parameters
    :param config_file: The input config file
    :return: Python dictionary of YAML
    """
    with open(config_file) as fd:
        task_config = yaml.load(fd, Loader=yaml.FullLoader)

    keys = task_config.keys()

    valid_config = True
    if 'task_dir' not in keys:
        logger.error(f"needs 'task_dir' to be specified in '{config_file}'. This is the directory "
                     f"where your source code is present.")
        valid_config = False

    if 'run' not in keys:
        logger.error(f"needs 'run' to be specified in '{config_file}'. This is the command that should be "
                     f"run to start the task.")
        valid_config = False

    if 'artifacts' not in keys:
        logger.error(
            f"needs 'artifacts to be specified in '{config_file}'. This directory would be tar-balled and saved "
            f"as output for your task.")
        valid_config = False

    if not valid_config:
        return None

    return task_config


def get_upload_url():
    """
    Get the upload URL for the token
    """
    response = __elbo_connector.request(ElboConnector.UPLOAD_URL_ENDPOINT)
    if response is None:
        return None

    upload_url = response.get('uploadUrl')
    user_id = response.get('user_id')
    authorization_token = response.get('authorizationToken')
    session_id = response.get('session_id')
    show_low_balance_alert = response.get('add_low_balance_alert')
    user_first_name = response.get('user_first_name')
    return upload_url, user_id, authorization_token, session_id, show_low_balance_alert, user_first_name


def get_task_id_from_file_name(file_name):
    """
    Get the task id from the file name
    :param file_name: The file name
    :return: The task id
    """
    return file_name.split('-')[2].split('.')[0]


def download_file(download_url, download_directory, authorization=None, file_name=None):
    """
    TODO: This is copied over from common/utils in elbo-server Repo. Need to expose this in a common
    package

    Download the file at URL to the download directory. This stores the file in memory and writes to file system.
    This can be used for really large files which may not fit in memory.

    :param file_name:
    :param authorization: The download authorization token
    :param download_url: The download URL
    :param download_directory: The download directory
    :return: Path to file if download is successful, None otherwise
    """
    if not download_url:
        logger.error(f"No download URL")
        return

    if file_name is None:
        file_name = download_url.split('/')[-1]
        if file_name is None:
            logger.error(f"Could not infer filename from {download_url}")
            return None
    local_filename = os.path.join(download_directory, file_name)
    headers = {}
    if authorization is not None:
        headers = {
            'Authorization': authorization
        }

    try:
        with requests.get(download_url, stream=True, headers=headers) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == HTTPStatus.NOT_FOUND:
            logger.warning(f"{download_url} file does not exists.")
        else:
            logger.error(f"Unable to request {download_url} exception - {e}")
        return None

    if os.path.exists(local_filename):
        return local_filename
    else:
        return None


def upload_file(file_path, upload_url, user_id, authorization_token):
    """
    Upload a file to the URL specified
    :param file_path: The file to upload
    :param upload_url: The upload URL
    :param user_id: The user id
    :param authorization_token: The auth token
    :return: The bucket key and the SHA256 hash of the uploaded file
    """
    content_type = "application/tar+gzip"
    with open(file_path, mode='rb') as fd:  # b is important -> binary
        file_contents = fd.read()

    file_hash = hashlib.sha1(file_contents).hexdigest()
    file_name = os.path.basename(file_path)
    bucket_key = os.path.join(user_id, file_name)
    headers = {
        'Authorization': authorization_token,
        'X-Bz-File-Name': bucket_key,
        'Content-Type': content_type,
        'X-Bz-Content-Sha1': file_hash,
        'X-Bz-Info-Author': 'None',
        'X-Bz-Server-Side-Encryption': 'AES256'
    }

    session = requests.Session()
    upload_response = session.post(upload_url, headers=headers, data=file_contents)
    if upload_response.status_code == 200:
        task_id = get_task_id_from_file_name(file_name)
        logger.info(f"upload successful.")
    else:
        logger.error(f"failed task upload, response: {upload_response}")
        return None

    return bucket_key, file_hash, task_id


def request_task_run(bucket_key, file_hash, task_config, session_id):
    """
    Request the receiver to run the task.

    :param bucket_key: The bucket key - The file path in the Bucket
    :param file_hash: The file hash. The receiver will check if the file hash on the Bucket is the same as specified
    :param task_config: The task config provided by the user in the YAML file
    :param session_id: The session id
    here.
    :return: None
    """
    params = {
        'session_id': session_id,
        'bucket_key': bucket_key,
        'file_hash': file_hash,
        'task_config': base64.b64encode(bytes(json.dumps(task_config), 'utf-8'))
    }

    response = __elbo_connector.request(ElboConnector.SCHEDULE_ENDPOINT, params=params)
    return response


def request_machine_create():
    """
    Request the receiver to run the task.
    :return: None
    """
    params = {}
    response = __elbo_connector.request(ElboConnector.CREATE_ENDPOINT, params=params)
    return response


def provision_machine_create_compute(compute_type, session_id, open_ports):
    """
    Request to provision the chosen to compute type.
    """
    params = {
        'chosen_compute_type': base64.b64encode(bytes(json.dumps(compute_type), 'utf-8')),
        'session_id': session_id,
        'open_ports': open_ports
    }

    response = __elbo_connector.request(ElboConnector.CREATE_ENDPOINT, params=params)
    return response


def provision_compute(compute_type, session_id, task_config, config_file_path):
    """
    Request to provision the chosen to compute type.

    :param task_config: The task config
    :param config_file_path: The config file path
    :param compute_type: To compute type
    :param session_id The session id
    :return:
    """
    params = {
        'chosen_compute_type': base64.b64encode(bytes(json.dumps(compute_type), 'utf-8')),
        'session_id': session_id,
        'config_file_path': config_file_path,
        'task_config': base64.b64encode(bytes(json.dumps(task_config), 'utf-8'))
    }

    response = __elbo_connector.request(ElboConnector.PROVISION_ENDPOINT, params=params)
    return response


def prompt_user(compute_options):
    """
    Prompt the user with compute options and get the selection
    :param compute_options: The list of compute options
    :return: The selected option
    """
    options = []
    mapping = {}
    for k, v in compute_options.items():
        v = json.loads(v)
        option = f"~ ${round(v['cost'], 4):>6}/hour > {v['provider']:>10} {k:>24} ({v['name']})"
        options.append(option)
        mapping[option] = v

    # TODO: Inquirer supports themes, use an ELBO theme ?
    logger.info("Please choose the compute for your task -")
    if len(options) > 1:
        questions = [inquirer.List('ComputeType',
                                   message="Selection >",
                                   choices=options)]
        chosen = inquirer.prompt(questions)
        if chosen is None:
            logger.warning(f"None selected, exiting.")
            exit(0)
            return None
        logger.info(f"chosen compute type - {chosen['ComputeType']}")
        chosen_compute_type = mapping[chosen['ComputeType']]
    elif len(options) == 0:
        logger.error(
            f"was unable to find compute options at the moment. Please email support@elbo.ai if this continues.")
        return None
    else:
        chosen_compute_type = list(mapping.values())[0]

    return chosen_compute_type


@click.group()
def cli():
    """elbo.ai - Train more, pay less
    """
    pass


@cli.command(name='login')
@click.option('--token',
              prompt='Please enter or paste your token from https://elbo.ai/welcome',
              hide_input=True)
def login(token):
    """
    Login to the ELBO service.
    """
    netrc = Netrc()
    host_name = ElboConnector.get_elbo_host()
    netrc[host_name]['password'] = token
    netrc.save()

    logger.info(f"ELBO token saved to ~/.netrc")


@cli.command(name='status')
def status():
    """
    Get ELBO server status.
    """
    member_status = "❌"
    db_status = "❌"
    server_status = "❌"

    response = __elbo_connector.request(ElboConnector.STATUS_ENDPOINT)
    if response is not None:
        db_status = '✅' if response.get('db') is True else db_status
        member_status = '✅' if response.get('membership') is True else db_status
        server_status = '✅' if response.get('server') is True else db_status

    logger.info(f"Membership: {member_status}")
    logger.info(f"Database  : {db_status}")
    logger.info(f"Server    : {server_status}")


@cli.command(name='ls')
@click.option('-r', '--running', help='Show only running tasks', flag_value='Running')
@click.option('-c', '--completed', help='Show only completed tasks', flag_value='Completed')
def ls(running, completed):
    """
    Show list of all tasks.
    """
    if running:
        logger.info(f"your running tasks:")
    else:
        logger.info(f"your tasks list: ")
    response = __elbo_connector.request(ElboConnector.TASKS_ENDPOINT)
    if response is None:
        logger.error(f"is unable to get tasks list")
        return

    tasks_list = response['records']
    task_list = [x['fields'] for x in tasks_list]
    df = pd.DataFrame(task_list)
    df = df.fillna('')
    del df['Artifacts URL']
    del df['Logs URL']
    del df['SSH']
    del df['Source URL']
    del df['last']

    df['Start Time'] = df['Start Time'].apply(transform_date())
    df['Submission Time'] = df['Submission Time'].apply(transform_date())
    df['Completion Time'] = df['Completion Time'].apply(transform_date())

    df = df.sort_values(by=['Task ID'])
    df = df.set_index('Task ID')
    if running == "Running":
        df = df.loc[df['Status'] == running]
    elif completed == "Completed":
        df = df.loc[df['Status'] == completed]
    if len(df) == 0:
        logger.info(f"no running tasks...")
    else:
        print(tabulate.tabulate(df, headers="keys", tablefmt="pretty"))
    print("")
    print("")
    print(f"Related task commands: \n")
    print("\telbo show     --task_id [task_id]")
    print("\telbo cancel   --task_id [task_id]")
    print("\telbo ssh      --task_id [task_id]")
    print("\telbo download --task_id [task_id]\n")


@cli.command(name='cancel')
@click.option('--task_id',
              required=True,
              hide_input=False)
def cancel(task_id):
    """
    Stop the task.
    """
    logger.info(f"Stopping task - {task_id}")
    params = {
        'task_id': task_id
    }
    response = __elbo_connector.request(ElboConnector.CANCEL_ENDPOINT,
                                        params=params)
    if response is not None:
        logger.info(f"Task with id={task_id} is marked for cancellation.")


@cli.command(name='show')
@click.option('--task_id',
              required=True,
              hide_input=False)
def show(task_id):
    """
    Show the task.
    """
    logger.info(f"Fetching task - {task_id}")
    params = {
        'task_id': task_id
    }
    response = __elbo_connector.request(ElboConnector.SHOW_ENDPOINT,
                                        params=params)
    if response is not None:
        logger.info(f"Task with id = {task_id}:")
        record = response['records']['fields']
        is_running = record['Status'].lower() == "running"
        for k, v in response['records']['fields'].items():
            # TODO: Present these fields in a better way
            if k == "SSH":
                if not is_running:
                    continue
            if 'Time' in k:
                v = format_date(v)
            if 'URL' not in k and k != 'last':
                print(f"{k:<15}: {v}")


@cli.command(name='rm')
@click.option('--task_id',
              required=True,
              hide_input=False)
def rm(task_id):
    """
    Permanently delete the task.
    """
    logger.info(f"Removing task - {task_id}")
    params = {
        'task_id': task_id
    }
    response = __elbo_connector.request(ElboConnector.REMOVE_ENDPOINT,
                                        params=params)
    if response is not None:
        logger.info(f"Task with id={task_id} is marked for removal.")


@cli.command(name='download')
@click.option('--task_id',
              required=True,
              hide_input=False)
def download(task_id):
    """
    Download the artifacts for the task.
    """
    logger.info(f"Downloading Artifacts for - {task_id}")
    params = {
        'task_id': task_id
    }
    response = __elbo_connector.request(ElboConnector.RESOURCE_ENDPOINT,
                                        params=params)
    if response is None:
        logger.info(f"Could not retrieve artifact download URL for {task_id}")
        return

    artifact_auth = response['client_artifact_auth']
    artifact_url = urllib.parse.unquote(response['client_url'])
    temp_dir = tempfile.mkdtemp()
    local_file_name = download_task_artifacts(artifact_url, temp_dir, artifact_auth, None)
    if local_file_name is not None and os.path.exists(local_file_name):
        logger.info(f"Artifacts for task id = {task_id} downloaded to {local_file_name}")


@cli.command(name='ssh')
@click.option('--task_id',
              required=True,
              hide_input=False)
def ssh_task(task_id):
    """
    SSH into the machine running the task.
    """
    logger.info(f"Trying to SSH into task {task_id}...")
    params = {
        'task_id': task_id
    }
    response = __elbo_connector.request(ElboConnector.SHOW_ENDPOINT,
                                        params=params)

    if response is not None:
        ssh_command = response['records']['fields']['SSH']
        logger.info(f"SSH:")
        logger.info(f"Running Command : {ssh_command}")
        logger.info(f"Enter this password when prompted: elbo")
        os.system(ssh_command)


# TODO: Enable once we get this working
# @cli.command(name='logs')
# @click.option('--task_id',
#              required=True,
#              hide_input=False)
def logs(task_id):
    """
    Show logs from the task.
    """
    # TODO:
    logger.info(f"Getting logs of {task_id}...")
    params = {
        'task_id': task_id
    }
    response = __elbo_connector.request(ElboConnector.LOGS_ENDPOINT,
                                        params=params)
    if response is not None:
        logger.info(response)


def get_real_time_logs(server_ip):
    # noinspection HttpUrlsUsage
    log_address = f"http://{server_ip}/stream"
    connection_errors = 0
    while True:
        try:
            request = requests.get(log_address, stream=True)
            if request.encoding is None:
                request.encoding = 'utf-8'

            for line in request.iter_lines(decode_unicode=True):
                if line and line != "0":
                    logger.info(f"{server_ip}> {line}")
            time.sleep(2)
        except requests.exceptions.ConnectionError as _:
            # Connection errors can happen when SSH is trying to get established
            print('.', end='')
            time.sleep(5)
            connection_errors = connection_errors + 1
            if connection_errors > 10:
                print("*")
                break
            pass
        except Exception as _e:
            logger.error(f"Hit {_e}")
            break


def download_task_artifacts(artifact_url, output_directory, artifact_auth, artifact_file):
    local_file_name = download_file(artifact_url, output_directory, artifact_auth, artifact_file)
    return local_file_name


# noinspection HttpUrlsUsage
def process_compute_provisioned_response(response_json, keep_alive=False, ssh_only=False):
    """
    Process the response from the server for provisioned compute
    :param ssh_only: Is this task SSH only?
    :param keep_alive: Will the machine be kept alive?
    :param response_json: The response json
    :return: None
    """
    response = response_json
    server_ip = response['ip']
    task_id = response['task_id']
    # TODO we need separate end point for this
    # artifact_auth = response['client_artifact_auth']
    # artifact_url = response['client_url']
    # artifact_file = response['file_name']

    logger.info(f"compute node ip {server_ip}")
    #
    # TODO: Could we route the traffic through CloudFare so we get https endpoint?
    # One problem may be the use of port 2222 for SSH which will not work if we proxy through CloudFare
    #
    if not ssh_only:
        logger.info(f"here are URLS for task logs, these may take a few minutes to start ...")
        logger.info(f"setup logs - http://{server_ip}/setup")
        logger.info(f"requirements logs - http://{server_ip}/requirements")
        logger.info(f"task logs - http://{server_ip}/task")
        logger.info(f"task with ID {task_id} is submitted successfully.")
        logger.info(f"task details command:")
        logger.info(f"elbo show --task_id {task_id}")

    if keep_alive:
        logger.info(f"ssh using - ssh root@{response['ip']} -p 2222")
        logger.info(f"scp using - scp root@{response['ip']} -p 2222")
        logger.info(f"password: elbo")
        logger.info(f"💡 copy your SSH public key to the server for password less login using:")
        logger.info(f"ssh-copy-id -p 2222 root@{response['ip']}")
        logger.info(f"task cancellation command:")
        logger.info(f"elbo cancel --task_id {task_id}")


def say_hello(user_first_name=None):
    # TODO: Add fortune? Random greetings?
    if user_first_name is None:
        logger.info(f"Hey there 👋")
    else:
        logger.info(f"Hey {user_first_name} 👋, welcome!")


@cli.command(name='create')
@click.option('--open_port',
              '-p',
              type=list,
              multiple=True,
              help='The port(s) that should be opened on the instance')
def create(open_port):
    """
    Create an instance and get SSH access to it
    """
    spinner = halo.Halo(text='elbo.client is finding compute options (this may take a while)',
                        spinner='bouncingBall',
                        placement='left')
    print("")
    spinner.start()
    response = request_machine_create()
    if not response:
        logger.error(f"Unable to get compute type options")
        return

    options = response['results']
    session_id = response['session_id']
    user_first_name = response['user_first_name']
    spinner.stop()
    say_hello(user_first_name)
    if options is not None:
        chosen_type = prompt_user(options)
        spinner = halo.Halo(text='elbo.client is provisioning compute (usually takes ~ 4 minutes, ☕️ time!)',
                            spinner='bouncingBall',
                            placement='left')
        spinner.start()
        response_json = provision_machine_create_compute(chosen_type, session_id, open_ports=open_port)
        spinner.stop()
        if response_json is not None:
            process_compute_provisioned_response(response_json, keep_alive=True, ssh_only=True)
        else:
            logger.error(f"something went wrong with provisioning, please try again ...")
    else:
        logger.error(f"is unable to get compute options from ELBO servers")


@cli.command(name='run')
@click.option('--config',
              type=click.Path(),
              default="elbo.yaml", help='The path of the ELBO yaml configuration file')
def run(config):
    """
    Submit a task specified by the config file.
    """
    if not os.path.exists(config):
        logger.error(f"is unable to find '{config}', is the path correct?")
        exit(-1)

    task_config = read_config(config)
    if task_config is None:
        exit(-2)

    if 'name' in task_config:
        logger.info(f"is starting '{task_config['name']}' submission ...")
    else:
        logger.error(f"please specify a task `name` in {config} file.")
        exit(-3)

    url_response = get_upload_url()
    if url_response is None:
        logger.error(f"is unable to authenticate with server..")
        exit(-6)
    upload_url, user_id, authorization_token, session_id, show_low_balance_alert, user_first_name = url_response
    if user_first_name:
        say_hello(user_first_name)

    if show_low_balance_alert:
        #
        # Allow user to continue scheduling. The job will complete even if balance is low
        #
        logger.warning(f"The balance on your account is too low, please deposit funds 🙏")

    if upload_url is not None and user_id is not None and authorization_token is not None:
        temp_file_name = get_temp_file_path(tgz=True)
        # Get directory path relative to config file
        config_directory = os.path.dirname(config)
        task_dir = os.path.join(config_directory, task_config['task_dir'])
        create_tar_gz_archive(temp_file_name, task_dir)
        logger.info(f"is uploading sources from {task_dir}...")
        bucket_key, file_hash, task_id = upload_file(temp_file_name, upload_url, user_id, authorization_token)
        if bucket_key is not None and file_hash is not None:
            spinner = halo.Halo(text='elbo.client is finding compute options (this may take a while)',
                                spinner='bouncingBall',
                                placement='left')
            print("")
            spinner.start()
            response = request_task_run(bucket_key, file_hash, task_config, session_id)
            spinner.stop()
            if response is not None:
                chosen_type = prompt_user(response)
                spinner = halo.Halo(text='elbo.client is provisioning compute (usually takes ~ 4 minutes, ☕️ time!)',
                                    spinner='bouncingBall',
                                    placement='left')
                spinner.start()
                response_json = provision_compute(chosen_type, session_id, task_config, config)
                spinner.stop()
                if response_json is not None:
                    process_compute_provisioned_response(response_json, keep_alive=task_config.get('keep_alive'),
                                                         ssh_only=False)
                else:
                    logger.error(f"something went wrong with provisioning, please try again ...")
            else:
                logger.error(f"is unable to get compute options from ELBO servers")
        else:
            logger.info(f":(. something went wrong with upload, please send us a bug report at bugs@elbo.ai")

    else:
        if user_id is None:
            logger.error(f"is unable to verify your membership.")
            logger.error("please obtain your token from https://elbo.ai/welcome, and run `elbo login`")
        else:
            logger.info(f"is unable to obtain upload url. Please report this to bugs@elbo.ai.")


def create_tar_gz_archive(output_filename, source_dir):
    """
    Create a tar gzip file

    :param output_filename: The name of the output file
    :param source_dir: The directory to tar and gzip
    :return: None
    """
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def generate_short_rand_string():
    """
    Generate a short random string
    :return: The random string
    """
    return str(uuid.uuid4())[:8]


def get_temp_file_path(tgz=False):
    """
    Generate a name for temp file
    :return: A random temp file name
    """
    rand_string = f"elbo-archive-{generate_short_rand_string()}"
    if tgz:
        rand_string = f"{rand_string}.tgz"

    path = os.path.join(tempfile.mkdtemp(), rand_string)
    return path


def is_elbo_outdated():
    output = subprocess.check_output([sys.executable, '-m', 'pip', 'show', 'elbo'])
    output = str(output, encoding='utf-8').split('\n')
    installed_version = 0
    for line in output:
        if "Version:" in line:
            installed_version = line.split(" ")[1]
    response = requests.get(f'https://pypi.org/pypi/elbo/json')
    latest_version = response.json()['info']['version']
    return installed_version != latest_version, latest_version


def exit_handler():
    is_outdated, latest_version = is_elbo_outdated()
    if is_outdated:
        logger.warning(f"A new version of elbo is available, please install using:")
        logger.warning(f"pip3 install elbo=={latest_version}")


def format_date(date):
    if len(date) > 0:
        return parser.parse(date).strftime("%m/%d/%Y %H:%M %p")
    return ""


def transform_date():
    return lambda x: format_date(x)


atexit.register(exit_handler)

if __name__ == '__main__':
    cli()
