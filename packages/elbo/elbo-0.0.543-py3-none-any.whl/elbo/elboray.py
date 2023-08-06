"""
The RAY provider for ELBO
"""
from typing import Optional, Dict, Any, List


# TODO:
# Hitting:
# ImportError:
# dlopen(/Users/joy/.venv/lib/python3.8/site-packages/ray/thirdparty_files/setproctitle.cpython-38-darwin.so,
# 0x0002): symbol not found in flat namespace '_Py_GetArgcArgv'
# from ray.autoscaler.node_provider import NodeProvider
# Extend class once that is fixed

# noinspection PyUnresolvedReferences
class ElboRayProvider:
    """
    Implementation of ELBO's Ray Provider. Ray's auto-scalar calls methods in this class to provision
    cluster nodes.

    A key assumption in Ray is that all nodes are on a secure private network. With ELBO we can get nodes
    that span across providers and connect over public IP. Thus exposing the attack surface of these nodes.

    TODO: Figure out a gateway mechanism that allows nodes across providers to talk to each other
    """

    def __init__(self, provider_config: Dict[str, Any], cluster_name: str):
        super().__init__(provider_config, cluster_name)

    def non_terminated_nodes(self, tag_filters: Dict[str, str]) -> List[str]:
        """Return a list of node ids filtered by the specified tag's dict.
        This list must not include terminated nodes. For performance reasons,
        providers are allowed to cache the result of a call to
        non_terminated_nodes() to serve single-node queries
        (e.g. is_running(node_id)). This means that non_terminate_nodes() must
        be called again to refresh results.
        Examples:
            >>> provider.non_terminated_nodes({TAG_RAY_NODE_KIND: "worker"})
            ["node-1", "node-2"]
        """
        pass

    def is_running(self, node_id: str) -> bool:
        """Return whether the specified node is running."""
        pass

    def is_terminated(self, node_id: str) -> bool:
        """Return whether the specified node is terminated."""
        pass

    def node_tags(self, node_id: str) -> Dict[str, str]:
        """Returns the tags of the given node (string dict)."""
        pass

    def external_ip(self, node_id: str) -> str:
        """Returns the external ip of the given node."""
        pass

    def internal_ip(self, node_id: str) -> str:
        """Returns the internal ip (Ray ip) of the given node."""
        pass

    def create_node(self, node_config: Dict[str, Any], tags: Dict[str, str], count: int) -> Optional[Dict[str, Any]]:
        """Creates a number of nodes within the namespace.
        Optionally returns a mapping from created node ids to node metadata.
        """
        pass

    def set_node_tags(self, node_id: str, tags: Dict[str, str]) -> None:
        """Sets the tag values (string dict) for the specified node."""
        pass

    def terminate_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Terminates the specified node.
        Optionally return a mapping from deleted node ids to node
        metadata.
        """
        pass
