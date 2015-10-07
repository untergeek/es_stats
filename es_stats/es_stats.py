import sys
import elasticsearch
from dotmap import DotMap
from .utils import *
import logging

logger = logging.getLogger(__name__)

class ClusterHealth():
    """Cluster Health Object"""

    def __init__(self, client):
        self.health = DotMap(client.cluster.health())
        self.health["status"] = status_map(self.health["status"])

    def get(self, key):
        """Return value for specific key"""
        return get_value(self.health, key)

class ClusterStats():
    """Cluster Stats Object"""

    def __init__(self, client):
        self.stats = DotMap(client.cluster.stats())

    def get(self, key):
        """Return value for specific key"""
        return get_value(self.stats, key)

class ClusterState():
    """Cluster State Object"""

    def __init__(self, client):
        self.state = DotMap(client.cluster.state())

    def get(self, key):
        """Return value for specific key"""
        # Remap the key to show master_node name, rather than nodeid
        if key == "master_node":
            nodeid = get_value(self.state, key)
            key = "nodes." + nodeid + ".name"
        return get_value(self.state, key)

class NodeStats():
    """NodeStats object"""

    def __init__(self, client, name=None):
        self.nodeid = None
        self.rawstats = client.nodes.stats()
        # Must provide node "name"
        if not name:
            logger.error('Node name not provided')
            sys.exit(1)
        else:
            self.nodename = name
            self.by_name()

    def by_name(self):
        for node in self.rawstats["nodes"]:
            if self.rawstats["nodes"][node]["name"] == self.nodename:
                self.nodeid = node
        if not self.nodeid:
            logger.error('Node with name {0} not found.'.format(self.nodename))
            sys.exit(1)
        self.stats = DotMap(self.rawstats["nodes"][self.nodeid])

    def get(self, key):
        """Return value for specific key"""
        return get_value(self.stats, key)

class NodeInfo():
    """NodeInfo object"""

    def __init__(self, client, name=None):
        self.nodeid = None
        self.rawinfo = client.nodes.info()
        # Must provide node "name"
        if not name:
            logger.error('Node name not provided')
            sys.exit(1)
        else:
            self.nodename = name
            self.by_name()

    def by_name(self):
        for node in self.rawinfo["nodes"]:
            if self.rawinfo["nodes"][node]["name"] == self.nodename:
                self.nodeid = node
        if not self.nodeid:
            logger.error('Node with name {0} not found.'.format(self.nodename))
            sys.exit(1)
        self.info = DotMap(self.rawinfo["nodes"][self.nodeid])

    def get(self, key):
        """Return value for specific key"""
        return get_value(self.info, key)
