[![Build Status](https://travis-ci.org/corbinmcneill/SNF.svg?branch=master)](https://travis-ci.org/corbinmcneill/SNF)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/smithnormalform)
[![PyPI version](https://badge.fury.io/py/smithnormalform.svg)](https://badge.fury.io/py/smithnormalform)
[![Coverage Status](https://coveralls.io/repos/github/corbinmcneill/SNF/badge.svg)](https://coveralls.io/github/corbinmcneill/SNF)

# Generalized Python Smith Normal Form 

This project is a python package implementing the calculation of smith normal
forms (SNFs) for matrices defined over arbitrary principle ideal domains.

Currently, this SNF library can calculate the SNF of matrices over either the
integers or the gaussian integers. Additionally it can be easily extended to
any principle ideal domain. 


What are Principle Ideal Domains?
---------------------------------

Generally speaking [principle ideal
domains](https://en.wikipedia.org/wiki/Principal_ideal_domain)(PID) is a class
of mathematical structures that are more structured than a commutative ring,
but not necessarily structured as a field. Two items in a PID will always have
a greatest common denominator and they will always have a unique factorization.
Elements of a PID do not necessarily have inverses though. For example,
integers do not generally speaking have integer inverses.

Some examples of PIDs include:

- integers
- gaussian integers
- fields (finite fields, rational numbers, real numbers, complex numbers)
- single variable polynomials over a field


What is the Smith Normal Form of a matrix?
------------------------------------------

The Smith Normal form of a matrix is cannonical way to represent a matrix
defined over a PID. The smith normal form of a matrix `A` is a matrix `J` such that:

- all non-diagonal elements of `J` are zero
- along the diagonal of `J`, every element divides evenly into its predecessor until a zero is encounterd and then all future diagonal elements are zero
- there exists unimodular matrices `S` and `T` such that `S*A*T = J`.

As an example if the matrix `A` is
```
A = [ 1 2 3 ]
    [ 4 5 6 ],
```
the Smith Normal Form of this matrix would be
```
J = [ 1 0 0 ]
    [ 0 3 0 ]
```
with complementary matrices
```
S = [ 1  0 ]
    [ 4 -1 ]
```
and
```
T = [ 1 -1  1 ]
    [ 0 -1 -2 ]
    [ 0  1  1 ].
```


Example Usage
-------------

The following is an example of how to set up a Smith Normal Form problem over the integers, run the computation, and interpret the results.

```python
>>> from smithnormalform import matrix, snfproblem, z
>>> original_matrix = matrix.Matrix(2, 2, [z.Z(1), z.Z(2), z.Z(3), z.Z(4)])
>>> prob = snfproblem.SNFProblem(original_matrix)
>>> prob.computeSNF()
>>> print(prob.isValid())
True
>>> print(prob.A)
[ 1 2 ]
[ 3 4 ]
>>> print(prob.J)
[ -2 1 ]
[ 3 -1 ]
>>> print(prob.S * prob.A * prob.T == prob.J)
True
```



Adding New Principle Ideal Domains
----------------------------------

The Smith Normal Form algorithm can be run on any subclass of the principle ideal domain class `smithnormalform.pid.PID`. In order to subclass `PID`, you will need to define several basic operations that are well defined on PIDs such as addition, multiplication, division, negation, and GCD.

Since every PID is a [GCD Domain](https://en.wikipedia.org/wiki/GCD_domain), greatest common divisor is a well defined operation for two elements of PID. Just because GCD is well-defined, however, does not mean it is easy (or even tractible) to compute. One way to find the GCD of two elements is the [Euclidean algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm); however, the Euclidean algorithm can only be applied to [Euclidean domains](https://en.wikipedia.org/wiki/Euclidean_domain). While all Euclidean domains are PIDs, not all PIDs are Euclidean domains.

This leaves us in an unfortunate position. While the Smith Normal Form algorithm implemented here is efficient in-and-of-itself and works for all PIDs, it is only efficient if GCD can be computed efficiently, which is not generally speaking true for all PIDs.

We resolve this conflict in the following way: We provide an abstract class for Euclidean domains (`smithnormalform.ed.ED`) that implements the euclidean algorithm for you. Extending this class requires you define a norm for your Euclidean domain; however, once you do so the GCD function required for PIDs will be completed for you without you needing to implement the Euclidian algorithm for yourself.

If you would like to run this algorithm on a PID that is not a Euclidean domain, you can extend the PID class `smithnormalform.pid.PID` directly, bypassing the Euclidean domain class. Doing this will require you to implement the GCD function directly. Please note that GCDs are requested frequently during the Smith Normal Form calculation so if the GCD function isn't efficient the Smith Normal Form computation may be intractible.


Contributors
------------

1. Corbin McNeill
2. Elias Schomer
