import logging
from datetime import timedelta, datetime, date
from dotmap import DotMap
from es_stats.exceptions import MissingArgument, NotFound
from es_stats.utils import fix_key, get_value, status_map

class Stats():
    """Stats Parent Class"""

    def __init__(self, client, cache_frequency=60):
        self.logger = logging.getLogger(__name__)
        self.client = client
        self.cache = {}
        self.cache_frequency = cache_frequency
        # Get the _local nodeid to initialize
        localinfo = self.client.nodes.info(node_id='_local')['nodes']
        self.nodeid = list(localinfo.keys())[0]
        self.nodename = localinfo[self.nodeid]['name']
        self.logger.debug('Initialized nodeid = {0}'.format(self.nodeid))
        self.logger.debug('Initialized nodename = {0}'.format(self.nodename))

    def epochnow(self):
        return int(datetime.utcnow().strftime('%s'))

    def pull_stats(self, k):
        statsmap = {
            'health': self.client.cluster.health(),
            'clusterstate': self.client.cluster.state(),
            'clusterstats': self.client.cluster.stats(),
            'nodeinfo': self.client.nodes.info(),
            'nodestats': self.client.nodes.stats(),
        }
        if not k in self.cache:
            self.cache[k] = {}
        self.cache[k]['lastvalue'] = statsmap[k]
        self.cache[k]['lastcall'] = self.epochnow()

    def cached_read(self, kind):
        """Cache stats calls to prevent hammering the API"""
        if not kind in self.cache:
            self.pull_stats(kind)
        if self.epochnow() - self.cache[kind]['lastcall'] > self.cache_frequency:
            self.pull_stats(kind)
        return self.cache[kind]['lastvalue']

    def find_name(self):
        # The idea here is to recheck for the node 'name' after
        # the other child class has re-assigned ``self.nodename``
        nodestats = self.cached_read('nodestats')['nodes']
        found = False
        for node in nodestats:
            if nodestats[node]['name'] == self.nodename:
                self.logger.debug('Found node name "{0}"'.format(self.nodename))
                self.logger.debug('Replacing nodeid "{0}" with "{1}"'.format(self.nodeid, node))
                self.nodeid = node
                found = True
        if not found:
            msg = 'Node with name {0} not found.'.format(self.nodename)
            self.logger.critical(msg)
            raise NotFound(msg)

    def get(self, key, name=None):
        """Return value for specific key"""
        if name is not None:
            self.logger.debug('Replacing nodename "{0}" with "{1}"'.format(self.nodename, name))
            self.nodename = name
        self.find_name()
        return get_value(self.stats(), fix_key(key))

    def stats(self):
        """
        Extend in each child class.
        Must return dotmap of expected stats.
        """
        pass

class ClusterHealth(Stats):
    """Cluster Health Child Class"""

    def stats(self):
        # health = DotMap(self.cached_read('health'))
        # # Remap to numerical output for Zabbix.
        # health.status = status_map(health['status'])
        # return health
        return DotMap(self.cached_read('health'))


class ClusterState(Stats):

    def stats(self):
        cs = DotMap(self.cached_read('clusterstate'))
        master = cs['master_node']
        cs['master_node'] = self.cached_read('nodestats')['nodes'][master]['name']
        return cs

class ClusterStats(Stats):

    def stats(self):
        return DotMap(self.cached_read('clusterstats'))

class NodeInfo(Stats):

    def stats(self):
        return DotMap(self.cached_read('nodeinfo')['nodes'][self.nodeid])

class NodeStats(Stats):

    def stats(self):
        return DotMap(self.cached_read('nodestats')['nodes'][self.nodeid])

 
