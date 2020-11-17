# Author: Aru Bhoop
# Copyright: This module has been placed in the public domain.

from typing import List

import numpy as np

from .exceptions import InfeasibleProblem
from .exceptions import ReachedOptimality
from .exceptions import UnboundedProblem


class Tableau:
    """
    `Simplex Tableau` contains and performs basic operations such as pivoting
    on the problem data.

    There is one primary use case for this class, which is employed by the
    `Solver` class:

    1. Intialize Tableau (see `__init__()`) with program data in **standard
       form**.
    2. Open Tableau as a Context Manager and operate on it using the
       `pivot()` method.
    3. The pivot method will raise an exception once a termination point
       has been reached (optimality, unboundedness, or infeasibility).
    4. Extract Tableau data by directly accessing its attributes (see
       below).

    Attributes
    ----------
    obj_value : float
       linear program objective value, arbitrary if problem is unbounded
    solution : List[float]
       solution to the linear program, if any.
    basis : List[float]
       indices of the basis matrix.


    Methods
    -------
    pivot(use_blands_rule=False)
        determines entering and departing variables and pivots tableau.
    """

    # todo phase 1 or phase 2?

    def __init__(self, obj_func: List[float], coeffs: List[List[float]], constraints: List[float]):
        """
        Creates tableau object `(self.tab)` from program data in **standard
        form**.

        Parameters
        ----------
        obj_func: values af the objective function, in order. Must be of
           size *n* (n = number of variables).
        coeffs: values of technological coefficients (params), row-major.
          Must be size *m x n* (m = number of constraints)
        constraints: values of the contraint column-vector (right-hand
        side). Must be size *m*.
        """

        # calculate reduced costs
        self.obj_func = obj_func
        obj_func = [-v for v in obj_func]

        # tableau object is a single large m + 1 x n + 1 matrix
        obj_value = 0
        self.tab = np.r_[
            np.r_[obj_func, obj_value][np.newaxis, :],
            np.c_[coeffs, constraints]]

        # float type is necessary for future conversions
        self.tab = self.tab.astype(float)

        # useful for calculations (m, n)
        self.shape = (len(constraints), len(obj_func))

        # state of tableau (None, Optimal, Unbounded, or Infeasible)
        self.state = None

    def __repr__(self):
        """
        Returns string representation of tableau.
        """

        # suppress scientific notation
        np.set_printoptions(suppress=True)

        # convert tableau to string
        top = np.arange(1, self.tab.shape[1] + 1)
        top[-1] = -1  # used as a placeholder
        tab = np.r_[top[np.newaxis, :], self.tab]
        rows = str(tab).split('\n')

        # strip off extra bracket off last row
        rows[-1] = rows[-1][:-1]

        # top row with variables
        top = "     " + rows[0].replace('.', 'x').replace('-1x', 'RHS')[2:-1]

        # add basis variables
        return '\n'.join([top] + [f'{f"x{var + 1}" if var != "" else "z "} {row}'
                                  for row, var in zip(rows[1:], [''] + self.basis)])

    def __enter__(self):
        """ Enter method for context manager. Returns self."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Exit method for context manager. """

        # if context exits without an exception (no solution found)
        if not exc_type:
            return

        try:
            # exception is mapped to the following states
            self.state = {
                ReachedOptimality: "Optimal",
                UnboundedProblem: "Unbounded",
                InfeasibleProblem: "Infeasible"
            }[exc_type]
        except KeyError:
            # if it is another exception, let it be raised
            return False
        return True

    @property
    def obj_value(self) -> float:
        """
        Returns the objective value.
        """
        return self.tab[0][-1]

    @property
    def solution(self) -> List[float]:
        """
        Returns the solution vector.
        """
        return self.tab[1:, -1]

    @property
    def basis(self) -> List[float]:
        """
        Returns indices of basis vector.

        Looks for each basic vector in the tableau, and stores index in
        the basis. -1 is stored in the absence of a corresponding basis
        column.
        """

        # identity shifted over so top row is zeroes
        identity = np.identity(self.shape[0] + 1)[1:]

        # default basis has all -1's
        basis = np.full(self.shape[0], -1)

        for i, row in enumerate(identity):
            for j, col in enumerate(self.tab.T):
                if np.all(row == col):
                    basis[i] = j

        return list(basis)

    def pivot(self, use_blands_rule=False):
        """
        Calculates departing and entering variables and calls
        `_pivot_around()`. Raises exception upon termination condition.

        Raises
        ------
        ReachedOptimality
           If optimality conditions have been reached.
        InfeasibleProblem
           If problem is feasible and unable to pivot.
        UnboundedProblem
           If problem is unbounded.
        """

        try:
            entering_var = np.argwhere(self.tab[0][:-1] < 0).min()  # use value with smallest index
        except ValueError:  # all values are positive
            feasible_sol = np.all(self.tab[1:, -1] >= 0)  # b >= 0
            raise ReachedOptimality if feasible_sol else InfeasibleProblem
        if not use_blands_rule:
            entering_var = self.tab[0][:-1].argmin()  # use value that is most negative

        # minimum ratio test
        col = self.tab[1:, entering_var]  # column of entering variable
        ratios = np.divide(self.tab[1:, -1], col, out=np.full_like(col, np.inf, dtype=float), where=col > 0)
        departing_var = ratios.argmin()  # index of smallest positive value
        if use_blands_rule:
            val = ratios[departing_var]
            departing_var = self.basis.index(
                np.min(np.array(self.basis)[ratios == val]))  # smallest index

        # if all departing variables are negative
        if col[departing_var] <= 0:
            raise UnboundedProblem  # problem in unbounded

        departing_var += 1  # since top of tableau is offset by one

        # pivot index, useful for debugging
        self.pivot_idx = (departing_var, entering_var)

        # actually pivot
        self._pivot_around(*self.pivot_idx)

    def _pivot_around(self, r: int, c: int) -> None:
        """
        Pivots tableau object given a row and column.

        Parameters
        ----------
        r : index of departing variable
        c : index of entering variable

        Notes
        -----
        Indices are relative to the tableau; they are not the constraint
        or variable indices.
        """

        # divide row by pivot
        self.tab[r] /= self.tab[r, c]

        # zero out column, except for pivot
        self.tab -= [self.tab[r] * self.tab[i, c] if i != r else np.zeros_like(self.tab[r])
                     for i, row in enumerate(self.tab)]

    def add_artificial_variables(self):
        """
        Inserts artificial columns in tableau and calculates new reduced
        costs.
        """

        # store basis so only single calculation is needed
        basis = np.array(self.basis)

        # calculate new reduced costs
        new_basic_cost = -1 * (basis == -1)
        self.tab[0] = [np.dot(new_basic_cost, r[1:]) for r in self.tab.T]

        # identity shifted over so top row is zeroes
        identity = np.identity(self.shape[0] + 1)[1:]

        # add artificial variable columns
        args = np.nonzero(basis == -1)[0]
        self.artificial_vars = range(self.shape[1], self.shape[1] + args.size)  # indices of artificial variables
        self.tab = np.insert(self.tab, -1, identity[args], axis=1)

    def drop_artificial_variables(self):
        """
        Removes artificial variables that have been driven out of the
        basis.

        Raises
        ------
        InfeasibleProblem
            if artificial variable is in basis with positive value

        Returns
        -------
        Function does not return anything.
        """

        # check basis for artificial vars
        for var in self.basis:
            if var in self.artificial_vars:
                if self.tab[v][-1] > 0:
                    raise InfeasibleProblem
                # todo keep in basis and test this

        # drop artificial variables
        drop_cols = self.artificial_vars
        self.tab = np.delete(self.tab, drop_cols, axis=1)

        # calculate new costs
        costs = [self.obj_func[i] for i in self.basis]
        self.tab[0] = [np.dot(costs, r[1:]) - c for c, r in
                       zip(self.obj_func + [0], self.tab.T)]
