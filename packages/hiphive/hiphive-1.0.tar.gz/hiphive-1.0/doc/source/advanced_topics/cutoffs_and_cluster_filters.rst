.. _cutoffs_and_cluster_filters:
.. highlight:: python
.. index::
   single: Cutoffs and cluster filters


Cutoffs and cluster filters
===========================

In this tutorial the usage of cutoffs and cluster filters will be discussed.

Cutoffs
-------

A cluster of lattice sites `(i,j,k,...)` is defined to be inside a
cutoff if *all* pairwise interatomic distances in the cluster are less
than the cutoff.

Cutoffs can be set for each expansion order as well as for each
*n*-body interaction. This can be seen as a matrix of cutoffs, i.e.

  +------------+-----+-----+-----+-----+-----+
  | body/order |  2  |  3  |  4  |  5  |  6  |
  +============+=====+=====+=====+=====+=====+
  |      2     | 6.0 | 6.0 | 6.0 | 5.0 | 5.0 |
  +------------+-----+-----+-----+-----+-----+
  |      3     |  -  | 5.0 | 5.0 | 5.0 | 4.0 |
  +------------+-----+-----+-----+-----+-----+
  |      4     |  -  |  -  | 4.0 | 4.0 | 3.5 |
  +------------+-----+-----+-----+-----+-----+


The order of a cluster `(i.j,k,...)` is given by the number of lattice
sites in the cluster, whereas the body (*n*-body interaction) is given
by the number of unique lattice sites in the cluster.


Cluster filters
---------------

Hiphive allows users to use custom cluster filters. These can be used
to reduce the number of clusters that full within the given
cutoffs. The cluster filter has one main function, which given a
cluster `(i,j,k,...)` is to return True or False depending on whether
the cluster should be kept or not. The ``BaseClusterFilter`` code
looks like this::

    class BaseClusterFilter:
        def __init__(self):
            pass

        def setup(self, atoms):
            """ The filter is passed the environment of the primitive cell. """
            self._atoms = atoms

        def __call__(self, cluster):
            """ Returns True or False when a cluster is proposed. """
            return True

Where the setup function can be used to pre-define or pre-calculate
quantities that are needed for the subsequent filter. Filtering can be
based on both geometrical aspects, e.g., include a cluster if it
involves atoms close to a defect.  It can also be based on the atomic
species, for example the following filter will only consider higher
order clusters if they contain at least one oxygen atom.::

    class MyOxygenFilter(BaseClusterFilter):

        def __call__(self, cluster):
            """ Returns True or False when a cluster is proposed. """
            order = len(cluster)
            if order == 2:
                return True
            else:
                if any(self._atoms[i].symbol == 'O' for i in cluster):
                    return True
                else:
                    return False

    cf = MyOxygenFilter()
    cs = ClusterSpace(prim, [6.0, 6.0, 6.0], cluster_filter=cf)


In ``examples/advanced_topics/cluster_filters`` an example is provided that
demonstrates how to generate a higher-order model for atoms on the
surface while "bulk" atoms are treated harmonically.

Please note that the cutoffs from the ``Cutoffs`` object are always
enforced first, *after* which the cluster filter is applied.


Source code
-----------

.. |br| raw:: html

   <br />

.. container:: toggle

    .. container:: header

       Usage of max triplet distance filter |br|
       ``examples/advanced_topics/cluster_filters/surface_filter.py``

    .. literalinclude:: ../../../examples/advanced_topics/cluster_filters/surface_filter.py
