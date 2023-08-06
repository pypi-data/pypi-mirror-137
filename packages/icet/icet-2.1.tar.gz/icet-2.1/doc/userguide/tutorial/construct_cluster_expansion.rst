.. _tutorial_construct_cluster_expansion:
.. highlight:: python
.. index::
   single: Tutorial; Constructing a cluster expansion

Constructing a cluster expansion
================================

In this step we will construct a cluster expansion using a dataset of Ag-Pd structures, which have been relaxed using density functional theory calculations.

General preparations
--------------------

A number of `ASE <https://wiki.fysik.dtu.dk/ase>`_ and :program:`icet` functions are needed in order to set up and train the cluster expansion.
Since the reference data is provided in the form of an `ASE <https://wiki.fysik.dtu.dk/ase>`_ database we require the :func:`ase.db.connect() <ase.db.core.connect>` function.
Furthermore, the :program:`icet` classes :class:`ClusterSpace <icet.ClusterSpace>`, :class:`StructureContainer <icet.StructureContainer>`, :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>` and :class:`ClusterExpansion <icet.ClusterExpansion>` are used, :ref:`in sequence <workflow>`, during preparation, compilation and training of the cluster expansion followed by the extraction of information in the form of predicted energies from the latter.

.. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
   :end-before: # step 1

Then we open a connection to the reference database and use the first structure in the database as the primitive structure as we happen to have prepared the database in this way.

.. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
   :start-after: # step 1
   :end-before: # step 2

Preparing a cluster space
-------------------------

In order to be able to build a cluster expansion, it is first necessary to create a :class:`ClusterSpace <icet.ClusterSpace>` object based on a prototype structure.
When initiating the former, one must also provide cutoffs and the chemical elements that are allowed to occupy different lattice sites.

The *cutoffs* are specified in the form of a list with the different elements
corresponding to clusters of increasing order (pairs, triplets, quadruplets,
etc). The values then specify the longest distance allowed between any two
atoms in clusters of the respective order. In the example below, the cluster
space will contain all pairs of atoms that are 13.5 Å or closer to each other,
all triplets among which the longest distance is 6.0 Å or less, and all
quadruplets among which the longest distance is 5.5 Å or less. If higher-order
clusters (quintuplets etc.) are to be included, one would simply extend the
list.

The *allowed chemical elements* are specified as a list. Two formats are
possible. If all sites in the structure are to be occupied identically, it
suffices to provide a simple list of chemical symbols, e.g., ``['Ag', 'Pd']``
in the case below. If there are multiple sites that are to be occupied in
different fashion, one has to provide instead a list of lists, where the outer
list must contain as many elements as there are sites in the primitive
structure and each "inner" list specifies the occupation for the respective
site. Examples for this approach can be found in the :class:`ClusterSpace
<icet.ClusterSpace>` documentation.


.. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
   :start-after: # step 2
   :end-before: # step 3

.. note::

  Here, we include *all* structures from the database with six or less atoms in
  the unit cell. This approach has been adopted in this basic tutorial for the
  sake of simplicity. In general this is *not* the preferred approach to
  assembling a data set.

As with many other :program:`icet` objects, it is possible to print core
information in a tabular format by simply calling the :func:`print` function
with the instance of interest as input argument. For the case at hand, the
output should look as follows::

  ====================================== Cluster Space =======================================
   space group                            : Fm-3m (225)
   chemical species                       : ['Ag', 'Pd'] (sublattice A)
   cutoffs                                : 13.5000 6.0000 5.5000
   total number of parameters             : 55
   number of parameters by order          : 0= 1  1= 1  2= 25  3= 12  4= 16
   fractional_position_tolerance          : 2e-06
   position_tolerance                     : 1e-05
   symprec                                : 1e-05
  --------------------------------------------------------------------------------------------
  index | order |  radius  | multiplicity | orbit_index | multi_component_vector | sublattices
  --------------------------------------------------------------------------------------------
     0  |   0   |   0.0000 |        1     |      -1     |           .            |      .
     1  |   1   |   0.0000 |        1     |       0     |          [0]           |      A
     2  |   2   |   1.4460 |        6     |       1     |         [0, 0]         |     A-A
     3  |   2   |   2.0450 |        3     |       2     |         [0, 0]         |     A-A
     4  |   2   |   2.5046 |       12     |       3     |         [0, 0]         |     A-A
     5  |   2   |   2.8921 |        6     |       4     |         [0, 0]         |     A-A
     6  |   2   |   3.2334 |       12     |       5     |         [0, 0]         |     A-A
     7  |   2   |   3.5420 |        4     |       6     |         [0, 0]         |     A-A
     8  |   2   |   3.8258 |       24     |       7     |         [0, 0]         |     A-A
     9  |   2   |   4.0900 |        3     |       8     |         [0, 0]         |     A-A
   ...
    45  |   4   |   2.1691 |        8     |      44     |      [0, 0, 0, 0]      |   A-A-A-A
    46  |   4   |   2.2295 |       24     |      45     |      [0, 0, 0, 0]      |   A-A-A-A
    47  |   4   |   2.3434 |       48     |      46     |      [0, 0, 0, 0]      |   A-A-A-A
    48  |   4   |   2.4193 |        8     |      47     |      [0, 0, 0, 0]      |   A-A-A-A
    49  |   4   |   2.4222 |       24     |      48     |      [0, 0, 0, 0]      |   A-A-A-A
    50  |   4   |   2.5046 |        6     |      49     |      [0, 0, 0, 0]      |   A-A-A-A
    51  |   4   |   2.5657 |       48     |      50     |      [0, 0, 0, 0]      |   A-A-A-A
    52  |   4   |   2.7676 |       48     |      51     |      [0, 0, 0, 0]      |   A-A-A-A
    53  |   4   |   2.7940 |       12     |      52     |      [0, 0, 0, 0]      |   A-A-A-A
    54  |   4   |   2.8921 |        6     |      53     |      [0, 0, 0, 0]      |   A-A-A-A
  ============================================================================================

.. note::

  The ``radius`` is *not* the same as the longest distance between atoms in
  the cluster (which was the measure used for initialization via ``cutoffs``),
  but is the average distance from all atoms to the center of mass (assuming
  all atoms have the same mass).


Compiling a structure container
-------------------------------

Once a :class:`ClusterSpace <icet.ClusterSpace>` has been prepared, the next
step is to compile a :class:`StructureContainer <icet.StructureContainer>`. To
this end, we first initialize an empty :class:`StructureContainer
<icet.StructureContainer>` and then add the structures from the database
prepared previously including for each structure the mixing energy in the
property dictionary.

.. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
   :start-after: # step 3
   :end-before: # step 4

.. note::

  While here we add only *one* property, the :class:`StructureContainer
  <icet.StructureContainer>` allows the addition of *several* properties. This
  can be useful e.g., when constructing (and sampling) CEs for a couple of
  different properties.

By calling the :func:`print` function with the :class:`StructureContainer
<icet.StructureContainer>` as input argument, one obtains the following
result::

  ========================== Structure Container ==========================
  Total number of structures: 137
  -------------------------------------------------------------------------
  index |       user_tag        | natoms | chemical formula | mixing-energy
  -------------------------------------------------------------------------
     0  | Ag                    |     1  | Ag               |      0.000
     1  | Pd                    |     1  | Pd               |      0.000
     2  | AgPd_0002             |     2  | AgPd             |     -0.040
     3  | AgPd_0003             |     3  | AgPd2            |     -0.029
     4  | AgPd_0004             |     3  | Ag2Pd            |     -0.049
     5  | AgPd_0005             |     3  | AgPd2            |     -0.018
     6  | AgPd_0006             |     3  | Ag2Pd            |     -0.056
     7  | AgPd_0007             |     3  | AgPd2            |     -0.030
     8  | AgPd_0008             |     3  | Ag2Pd            |     -0.048
     9  | AgPd_0009             |     4  | AgPd3            |     -0.017
   ...
   127  | AgPd_0127             |     6  | Ag5Pd            |     -0.032
   128  | AgPd_0128             |     6  | AgPd5            |     -0.012
   129  | AgPd_0129             |     6  | Ag2Pd4           |     -0.026
   130  | AgPd_0130             |     6  | Ag2Pd4           |     -0.024
   131  | AgPd_0131             |     6  | Ag4Pd2           |     -0.059
   132  | AgPd_0132             |     6  | Ag4Pd2           |     -0.054
   133  | AgPd_0133             |     6  | Ag3Pd3           |     -0.046
   134  | AgPd_0134             |     6  | Ag3Pd3           |     -0.048
   135  | AgPd_0135             |     6  | Ag5Pd            |     -0.040
   136  | AgPd_0001             |     2  | AgPd             |     -0.063
  =========================================================================

Training CE parameters
----------------------

Since the :class:`StructureContainer <icet.StructureContainer>` object created
in the previous section, contains all the information required for
constructing a cluster expansion, the next step is to train the parameters,
i.e. to fit the *effective cluster interactions* (:term:`ECIs`) using the
target data. More precisely, the goal is to achieve the best possible
agreement with a set of training structures, which represent a subset of all
the structures in the :class:`StructureContainer
<trainstation.StructureContainer>`. In practice, this is a two step process
that involves the initiation of an optimizer object (here a
:class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>`)
with a list of target properties produced by the :func:`get_fit_data()
<icet.StructureContainer.get_fit_data>` method of the
:class:`StructureContainer <icet.StructureContainer>` as input argument.

.. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
   :start-after: # step 4
   :end-before: # step 5

The :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>` optimizer used here is intended to provide a reliable estimate for the cross validation score.
This is achieved by calling the :func:`validate <trainstation.CrossValidationEstimator.validate>` method.
With the default settings used here the :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>` then randomly splits the available data into a training and a validation set.
Here, the effective cluster interactions (:term:`ECIs`) are obtained using the
`LASSO <https://en.wikipedia.org/wiki/Lasso_(statistics)>`_ method (``fit_method``).
This procedure is repeated 10 times (the default value for ``number_of_splits``).

.. note::

   The optimized parameters returned by the optimizer are actually
   *not* the :term:`ECIs` but the :term:`ECIs` times the multiplicity
   of the respective orbit. The distinction is handled internally but
   it is something to be aware of when inspecting the parameters
   directly.

.. note::

   You will likely see a few "Convergence errors" when executing this command.
   For the present purpose these can be ignored.
   They arise since the internal scikit-learn optimization loops have exceeded the number of iterations without reaching the default target accuracy.
   It is possible to extend the iterations but this increases the run time without a marked improvement in the quality of the cluster expansion.

The "final" CE is ultimately constructed using *all* available data by calling the :func:`train <trainstation.CrossValidationEstimator.train>` method.
Once it is finished, the results can be displayed by providing the :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>` object to the :func:`print` function, which gives the output shown below::

  ============== CrossValidationEstimator ==============
  alpha_optimal                  : 0.001944862
  fit_method                     : lasso
  n_nonzero_parameters           : 40
  n_parameters                   : 55
  n_splits                       : 10
  n_target_values                : 625
  parameters_norm                : 0.06954891
  rmse_train                     : 0.002077373
  rmse_train_final               : 0.002085274
  rmse_validation                : 0.002267498
  seed                           : 42
  shuffle                        : True
  standardize                    : True
  target_values_std              : 0.01486413
  validation_method              : k-fold
  ======================================================

We have thus constructed a CE with an average root mean square error (RMSE,
``rmse_validation``) for the validation set of only 2.4 meV/atom. The original
cluster space included 173 parameters (``number_of_parameters``), 54 of which
are non-zero (``number_of_nonzero_parameters``) in the final CE. The efficiency
of the LASSO method for finding sparse solutions is evident from the
number of non-zero parameters (54) being much smaller than the total number of
parameters (173).

.. note::

  Here we have used the :class:`CrossValidationEstimator <trainstation.CrossValidationEstimator>` from the :program:`trainstation` package.
  More information can be found in the `documentation of this package <https://trainstation.materialsmodeling.org/>`_.


Finalizing the cluster expansion
--------------------------------

At this point, the task of constructing the cluster expansion is almost
complete. The only step that remains is to tie the parameter values obtained
from the optimization to the cluster space. This is achieved through the
initiation of a :class:`ClusterExpansion <icet.ClusterExpansion>` object using
the previously created :class:`ClusterSpace <icet.ClusterSpace>` instance and
the list of parameters, available via the :class:`parameters
<trainstation.Optimizer.parameters>` attribute of the optimizer, as input arguments.

.. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
   :start-after: # step 5

Information regarding the parameters and associated cluster space
can be displayed by using the :func:`print` function with the
:class:`ClusterExpansion <icet.ClusterExpansion>` object as input argument::

  ================================================ Cluster Expansion =================================================
   space group                            : Fm-3m (225)
   chemical species                       : ['Ag', 'Pd'] (sublattice A)
   cutoffs                                : 13.5000 6.0000 5.5000
   total number of parameters             : 55
   number of parameters by order          : 0= 1  1= 1  2= 25  3= 12  4= 16
   fractional_position_tolerance          : 2e-06
   position_tolerance                     : 1e-05
   symprec                                : 1e-05
   total number of nonzero parameters     : 40
   number of nonzero parameters by order  : 0= 1  1= 1  2= 19  3= 10  4= 9 
  --------------------------------------------------------------------------------------------------------------------
  index | order |  radius  | multiplicity | orbit_index | multi_component_vector | sublattices | parameter |    ECI   
  --------------------------------------------------------------------------------------------------------------------
     0  |   0   |   0.0000 |        1     |      -1     |           .            |      .      |    -0.045 |    -0.045
     1  |   1   |   0.0000 |        1     |       0     |          [0]           |      A      |   -0.0353 |   -0.0353
     2  |   2   |   1.4460 |        6     |       1     |         [0, 0]         |     A-A     |    0.0285 |   0.00475
     3  |   2   |   2.0450 |        3     |       2     |         [0, 0]         |     A-A     |    0.0134 |   0.00447
     4  |   2   |   2.5046 |       12     |       3     |         [0, 0]         |     A-A     |    0.0172 |   0.00144
     5  |   2   |   2.8921 |        6     |       4     |         [0, 0]         |     A-A     |        -0 |        -0
     6  |   2   |   3.2334 |       12     |       5     |         [0, 0]         |     A-A     |        -0 |        -0
     7  |   2   |   3.5420 |        4     |       6     |         [0, 0]         |     A-A     |    0.0029 |  0.000724
     8  |   2   |   3.8258 |       24     |       7     |         [0, 0]         |     A-A     |  -0.00178 | -7.41e-05
     9  |   2   |   4.0900 |        3     |       8     |         [0, 0]         |     A-A     | -0.000288 |  -9.6e-05
   ...
    45  |   4   |   2.1691 |        8     |      44     |      [0, 0, 0, 0]      |   A-A-A-A   |         0 |         0
    46  |   4   |   2.2295 |       24     |      45     |      [0, 0, 0, 0]      |   A-A-A-A   |        -0 |        -0
    47  |   4   |   2.3434 |       48     |      46     |      [0, 0, 0, 0]      |   A-A-A-A   |        -0 |        -0
    48  |   4   |   2.4193 |        8     |      47     |      [0, 0, 0, 0]      |   A-A-A-A   |   0.00101 |  0.000127
    49  |   4   |   2.4222 |       24     |      48     |      [0, 0, 0, 0]      |   A-A-A-A   |         0 |         0
    50  |   4   |   2.5046 |        6     |      49     |      [0, 0, 0, 0]      |   A-A-A-A   | -0.000682 | -0.000114
    51  |   4   |   2.5657 |       48     |      50     |      [0, 0, 0, 0]      |   A-A-A-A   |        -0 |        -0
    52  |   4   |   2.7676 |       48     |      51     |      [0, 0, 0, 0]      |   A-A-A-A   |  -0.00395 | -8.23e-05
    53  |   4   |   2.7940 |       12     |      52     |      [0, 0, 0, 0]      |   A-A-A-A   |  0.000196 |  1.63e-05
    54  |   4   |   2.8921 |        6     |      53     |      [0, 0, 0, 0]      |   A-A-A-A   | -0.000411 | -6.85e-05
  ====================================================================================================================

Note that in the table above the parameters obtained from the
optimizer and the :term:`ECIs` are shown separately, with the
multiplication factor being the multiplicity of the respective orbit.

Finally, the CE is written to file in order to be reused in the
following steps of the tutorial.


Source code
-----------

.. container:: toggle

    .. container:: header

       The complete source code is available in
       ``examples/tutorial/1_construct_cluster_expansion.py``

    .. literalinclude:: ../../../examples/tutorial/1_construct_cluster_expansion.py
