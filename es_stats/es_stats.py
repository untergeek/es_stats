import sys
import elasticsearch
from dotmap import DotMap
from .exceptions import *
from .utils import *
import re
import logging

logger = logging.getLogger(__name__)

class ClusterHealth():
    """Cluster Health Object"""

    def __init__(self, client):
        self.health = DotMap(client.cluster.health())
        self.health["status"] = status_map(self.health["status"])

    def get(self, key, name=None):
        """Return value for specific key"""
        return get_value(self.health, fix_key(key))

class ClusterStats():
    """Cluster Stats Object"""

    def __init__(self, client):
        self.stats = DotMap(client.cluster.stats())

    def get(self, key, name=None):
        """Return value for specific key"""
        return get_value(self.stats, fix_key(key))

class ClusterState():
    """Cluster State Object"""

    def __init__(self, client):
        self.state = DotMap(client.cluster.state())

    def get(self, key, name=None):
        """Return value for specific key"""
        # Remap the key to show master_node name, rather than nodeid
        if key == "master_node":
            nodeid = get_value(self.state, fix_key(key))
            key = "nodes." + nodeid + ".name"
        return get_value(self.state, fix_key(key))

class NodeStats():
    """NodeStats object"""

    def __init__(self, client):
        self.nodeid = None
        self.rawstats = client.nodes.stats()

    def by_name(self):
        for node in self.rawstats["nodes"]:
            if self.rawstats["nodes"][node]["name"] == self.nodename:
                self.nodeid = node
        if not self.nodeid:
            raise NotFound('Node with name {0} not found.'.format(self.nodename))
        self.stats = DotMap(self.rawstats["nodes"][self.nodeid])

    def get(self, key, name=None):
        """Return value for specific key"""
        # Must provide node "name"
        if not name:
            raise MissingArgument('Node name not provided')
        else:
            self.nodename = name
            self.by_name()
        return get_value(self.stats, fix_key(key))

class NodeInfo():
    """NodeInfo object"""

    def __init__(self, client):
        self.nodeid = None
        self.rawinfo = client.nodes.info()

    def by_name(self):
        for node in self.rawinfo["nodes"]:
            if self.rawinfo["nodes"][node]["name"] == self.nodename:
                self.nodeid = node
        if not self.nodeid:
            raise NotFound('Node with name {0} not found.'.format(self.nodename))
        self.info = DotMap(self.rawinfo["nodes"][self.nodeid])

    def get(self, key, name=None):
        """Return value for specific key"""
        # Must provide node "name"
        if not name:
            raise MissingArgument('Node name not provided')
        else:
            self.nodename = name
            self.by_name()
        return get_value(self.info, fix_key(key))
