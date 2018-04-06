#!/usr/bin/env python
import elasticsearch
import socket
import sys
from dotmap import DotMap
from es_stats.classes import ClusterHealth, ClusterState, ClusterStats, NodeInfo, NodeStats
from es_stats.utils import fix_key, get_value

KEYS = [
    'health', 
    'clusterstate',
    'clusterstats',
    'nodeinfo',
    'nodestats',
]

SKIP_THESE = [
    'get', 
    'os', 
    'update', 
    'keys', 
    'items', 
    'mappings', 
    'snapshots', 
    'metadata', 
    'type.default'
]
# 'get', 'update', 'keys', and 'items' are a protected methods in DotMap
# 'os' level stats are easier to get in other ways
# 'mappings' & 'metadata' should not be tracked in this way
# 'type.default' is a dotted notation, but single key. Very weird.

def dotty(dm, notation='', retval=[]):
    for i in list(dm.keys()):
        if i in SKIP_THESE:
            continue
        if isinstance(dm[i], DotMap):
            nestlevel = notation[:]
            if notation == '':
                notation += i
            else:
                notation += '.' + i
            try:
                val = eval('dm' + '.' + i)
            except (NameError, SyntaxError):
                val = dm[i]
            dotty(val, notation, retval=retval)
            notation = nestlevel
        elif isinstance(dm[i], list):
            pass
        else:
            if notation == '':
                retval.append('{0}'.format(i))
            else:
                retval.append('{0}.{1}'.format(notation, i))
    return retval

def main():

    usage = '''
USAGE: quicktest.py (API_TYPE)

    API_TYPE must be one of {0}
    '''.format(KEYS)

    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print(usage)
        sys.exit(0)
    elif sys.argv[1] not in KEYS:
        print()
        print('ERROR: "{0}" is not an accepted API_TYPE'.format(sys.argv[1]))
        print(usage)
        sys.exit(1)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('127.0.0.1',9200)) != 0:
        print('  ERROR: Unable to connect to 127.0.0.1:9200')
        print('  quicktest.py expects an unencrypted instance of elasticsearch to be running locally.')
        sys.exit(1)

    client = elasticsearch.Elasticsearch()
    nodesdump = client.nodes.stats()['nodes']
    nodeid = list(nodesdump.keys())[0] # Just take the first
    nodename = nodesdump[nodeid]['name']

    if sys.argv[1] == 'health':
        data = client.cluster.health()
        stats = ClusterHealth(client)
    elif sys.argv[1] == 'clusterstate':
        data = client.cluster.state()
        stats = ClusterState(client)
    elif sys.argv[1] == 'clusterstats':
        data = client.cluster.stats()
        stats = ClusterStats(client)
    elif sys.argv[1] == 'nodeinfo':
        data = client.nodes.info()['nodes'][nodeid]
        stats = NodeInfo(client)
    elif sys.argv[1] == 'nodestats':
        data = client.nodes.stats()['nodes'][nodeid]
        stats = NodeStats(client)

    all_lines = []
    for line in dotty(DotMap(data)):
        value = stats.get(line, name=nodename)
        if value == DotMap():
            continue
        all_lines.append('{0} = {1}'.format(line, value))

    for line in sorted(all_lines):
        print(line)

    print()
    print('======================================================')
    print('The above are the available dotted keys obtained from:')
    print(' --- API: {0}'.format(sys.argv[1]))
    print(' --- node name: {0}'.format(nodename))
    print(' --- nodeid: {0}'.format(nodeid))
    print(' --- Elasticsearch version: {0}'.format(client.nodes.info()['nodes'][nodeid]['version']))
    print('======================================================')
    print()
    print('Results may differ when run with different versions of Elasticsearch.')

if __name__ == "__main__":
    main()