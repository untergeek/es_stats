.. _changelog:

Changelog
=========

1.1.2 (20 April 2018)
---------------------

**Changes**

  * Renamed ``cache_frequency`` to ``cache_timeout`` as `frequency` didn't
    make as much sense.
  * Renamed ``_version.py`` to ``version.py`` for project consistency's sake.

1.1.1 (17 April 2018)
---------------------

**Bug Fixes**

  * Refactor how the instance attributes ``nodeid`` and ``nodename`` are
    initialized, and treated when/if a node name is passed to a child class.

1.1.0 (17 April 2018)
---------------------

**New**

  * Update to only get the `_local` node information at initialization time and
    set the instance attributes ``nodeid`` and ``nodename`` from the `_local`
    node.  The previous behavior was to just take the first in the list.
  * Allow any ``elasticsearch-py`` version >= 5.5.2

1.0.1 (6 April 2018)
--------------------

**Bug Fixes**

  * Fix incorrect version in ``_version.py`` for PyPI release

1.0.0 (4 April 2018)
--------------------

**New**

  * Redundant code removed by making classes children of a parent class,
    ``Stats``.
  * Caching of stats calls.  Configurable with ``cache_frequency`` kwarg in
    class initialization.  This should make repeated calls to crowded APIs
    like NodeStats much faster, without hammering the cluster.  Default value
    is 60 seconds.
  * Improved linting helped clean things up.  Removed many unnecessary import
    statements.
  * Added ``quicktest.py`` which should test against a local, unencrypted node.

**Breaking**

  * Cluster health used to be mapped in this module from green/yellow/red to
    0/1/2, respectively.  This is no longer done here.  It will respond with
    ``green``, ``yellow``, and ``red`` as the API does.  For those of you who
    are Zabbix users, the ``es_stats_zabbix`` module will handle the change, as
    it should be mapped on that end.


0.2.1 (22 June 2016)
--------------------

**Bug Fixes**

  * Not only can the key "key" not appear in a DotMap, dashes in a key are also
    bad.  The ``fix_key()`` method corrects this by translating all dotted
    notation keys into dict notation.

0.2.0 (22 June 2016)
--------------------

**New**

  * Switch to exception-based termination instead of ``sys.exit(#)``

**Bug Fixes**

  * The key "get" cannot appear normally in a DotMap without it being
    translated as function "get."  This fix corrects this by way of a regex to
    use dict notation for "get" only. Fixes #1 (untergeek)

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

  * Have ClusterState master_node calls return the node name, rather than the
    nodeid

**Bug Fixes**

  * Found out why Elasticsearch-py 1.7.0 was buggy.  It doesn't affect this
    module at all. Fixed dependencies to allow 1.7.0 to be used.

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
