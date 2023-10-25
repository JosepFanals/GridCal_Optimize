.. _optimization_candidates:

Optimization of candidates
========================

Introduction
------------

Planning power grids involves determining an appropriate set of assets that makes sense from both the
technical and economical optics. This challenge can be understood as an optimization problem, where one tries to
minimize the total cost `C =` CAPEX+OPEX, while simultaneously minimizing the technical restrictions `f_o`. While
apparently simple to comprehend, such a problem in its original form is arduous to solve and a satisfying solution
may not even be reached.

At this point we have to ask ourselves what the underlying issue is. If the puzzle is rigorously formulated, it
becomes of the type MINLP. Not only it can include continuous variables (such as the rating of a substation), but
also a wide set of integer variables (the potential investments to make). It is well-known that even solving a
single-period OPF with only continuous variables becomes a very complicated problem, to the point where the
original scenario is often convexified to solve it with acceptable precision and time. Now imagine we have to find a
solution to such a problem, but considering the full 8760 hours in a year and thousands of investment combinations.
The result would be catastrophic given the astronomically high computational time.

Hence, it is clear we desire an algorithm that can provide us with a list of optimal investments and not suffer from
the curse of dimensionality. The methodology we have adopted here consists of:

#. Building a machine-learning model that captures the behavior of the grid under diverse scenarios.
#. Optimizing such a model in a matter of a few seconds.



Formulation
-------------

Testing
------------
.. check for the IEEE 118 with 2 areas