.. _changelog:

Changelog
=========

=======
0.2.0 (22 June 2016)
--------------------

**New**

  * Switch to exception-based termination instead of ``sys.exit(#)``

**Bug Fixes**

  * The key "get" cannot appear normally in a DotMap without it being translated
    as function "get."  This fix corrects this by way of a regex to use dict
    notation for "get" only. Fixes #1 (untergeek)

**General**

  * Pruned incorrect docs from the as yet unfinished docs.

0.1.0 (7 October 2015)
----------------------

**New**

  * Change NodeStats and NodeInfo to do by_name lookup in get method.
    Additionally, all get methods now have name=None.
    This helps simplify es_stats_zabbix use.

0.0.4 (6 October 2015)
----------------------

**New**

  * Have ClusterState master_node calls return the node name, rather than the nodeid

**Bug Fixes**

  * Found out why Elasticsearch-py 1.7.0 was buggy.  It doesn't affect this module at all.
    Fixed dependencies to allow 1.7.0 to be used.

0.0.3 (6 October 2015)
----------------------

**Announcement**

  * Project/Module rename.  Should have checked first.

0.0.2 (6 October 2015)
----------------------

**Announcement**

  * Yay!  First patch release!

0.0.1 (6 October 2015)
----------------------

**Announcement**

  * Initial release
