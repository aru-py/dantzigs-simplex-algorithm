==========
Quickstart
==========


Introduction
=============

This library is a robust implementation of `Dantzig’s Simplex method <https://en.wikipedia.org/wiki/Simplex_algorithm>`_ for solving problems in Linear Programming. It supports a wide variety of problems including cycling (using Bland’s rule) and Two-Phase problems and handles unbounded and infeasible cases.

Getting Started
================

Prerequisites
--------------
This tutorial requires a working understanding of Python and the Simplex Method.

.. note:: This library requires Python >= 3.7.6.

Basics
-------
If you haven’t already, obtain a copy of the `source code <https://github.com/aru-py/dantzigs-simplex-algorithm>`_ and place the `simplex` package in your working directory. Included in this package are three modules, but only the `solver` module is necessary for high-level usage (See `Digging Deeper` below for a deeper understanding of the program workings). It can be imported as follows.
::
from simplex.solver import SimplexSolver``.

Take the following standard-form Linear Programming problem, which can be found in `test_cases.py`.

.. math::

	max\;z = 2x_1 + 3x_2\\subject\;to \\
	x_1 - 2x_2 + x_3 = 4 \\
	2x_1 + x_2 + x_4 = 18 \\
	x_2 + x_5 = 10


Decomposing the problem into the objective function, technological coefficients, and the constraints, we get the following code.
::
		obj_func = [2, 3, 0, 0, 0]
		coeffs = [
	        [1, -2, 1, 0, 0],
	        [2, 1, 0, 1, 0],
	        [0, 1, 0, 0, 1]]
		constraints = [4, 18, 10]

Let’s instantiate `Solver` with these parameters and call its method `solve`.
::
	solver = SimplexSolver(obj_func, coeffs, constraints)
	sol = solver.solve()
	print(sol)

Running the script, you should get the following output.
::
             1x  2x  3x  4x  5x RHS
	z   [-2. -3.  0.  0.  0.  0.]
	x3  [ 1. -2.  1.  0.  0.  4.]
	x4  [ 2.  1.  0.  1.  0. 18.]
	x5  [ 0.  1.  0.  0.  1. 10.]

	[1] Pivoted around (2, 1)
	     1x  2x  3x  4x  5x RHS
	z   [-2.  0.  0.  0.  3. 30.]
	x3  [ 1.  0.  1.  0.  2. 24.]
	x4  [ 2.  0.  0.  1. -1.  8.]
	x2  [ 0.  1.  0.  0.  1. 10.]

	[2] Pivoted around (1, 0)
	     1x   2x   3x   4x   5x  RHS
	z   [ 0.   0.   0.   1.   2.  38. ]
	x3  [ 0.   0.   1.  -0.5  2.5 20. ]
	x1  [ 1.   0.   0.   0.5 -0.5  4. ]
	x2  [ 0.   1.   0.   0.   1.  10. ]

	Solution: z*=38.0, x*=[4.0, 10.0, 20.0]

That’s it! If you want to learn more about this library, check out the `references` or keep reading to get a better understanding of the program’s workings.


Digging Deeper
===============
This section is for those interested in what’s going on under the hood. The library is composed of three modules, `solver`, `tableau`, and `exceptions`.

The `solver` module contains the `Solver` class, which provides high-level instructions on how to manipulate the simplex tableau. It also is responsible for determining the solve state of the problem and whether the problem is infeasible or unbounded. The `Solution` class is also provided in this module and contains the state of the problem, the optimal objective value, and the solution (if any).

The `tableau` module provides only the `Tableau` class, which stores data for the simplex tableau and handles all low-level manipulations, such as pivoting and adding artificial variables. It also allows for printing the tableau in a readable format.

.. Note:: This section needs expanding and is looking for contributors. Submit a pull request if you would like help contribute. See `Contributing.md` for further details.




