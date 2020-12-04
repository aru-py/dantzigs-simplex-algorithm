# Author: Aru Bhoop
# Copyright: This module has been placed in the public domain.

import logging
import sys
from typing import List

import numpy as np

from .exceptions import LinearlyDependentError
from .exceptions import SizeMismatchError
from .exceptions import UnsolvableError
from .tableau import Tableau


class SimplexSolver:
    """
    Solves a Linear Programming problem using Dantzig's Simplex Method
    by manipulating the `Tableau` class.

    Methods
    -------
    solve(max_iterations=100, use_blands_rule=False) : solves problem and
    returns `Solution` object

    """

    def __init__(self, obj_func: List[float], coeffs: List[List[float]], constraints: List[float]):
        """
        Assigns internal variables after performing basic checks.

        Parameters
        ----------
        obj_func: values af the objective function, in order. Must be of
           size *n* (n = number of variables).
        coeffs: values of technological coefficients (params), row-major.
          Must be size *m x n* (m = number of constraints)
        constraints: values of the constraint column-vector (right-hand
        side). Must be size *m*.
        """

        # validate dimensions
        m = len(constraints)  # rows
        n = len(obj_func)  # columns

        if len(coeffs) != m:
            raise SizeMismatchError
        for coeff in coeffs:
            if len(coeff) != n:
                raise SizeMismatchError

        # full rank assumption
        if m > n:
            raise LinearlyDependentError

        # create corresponding tableau
        self.tableau = Tableau(
            obj_func=obj_func,
            coeffs=coeffs,
            constraints=constraints
        )

    def solve(self, max_iterations=100, use_blands_rule=False, print_tableau=True):
        """
        Solves Linear Programming Problem. Returns `Solution` instance`.

        Parameters
        ----------
        max_iterations : int
           number of times to pivot before resorting to Bland's rule
        use_blands_rule : bool
           whether to use Bland's Rule for anti-cycling
        print_tableau : bool
           whether to print the tableau at every iteration
        """

        # configure logging
        logging.basicConfig(stream=sys.stdout,
                            format='%(message)s',
                            level=logging.DEBUG if print_tableau else logging.INFO)

        with self.tableau as t:
            # if incomplete basis, use two-phase method
            if -1 in t.basis:
                logging.info("No identifiable basis. Using two-phase method.")

                # solve phase 1 problem
                t.add_artificial_variables()
                logging.debug(f"\nPhase I Tableau:")
                sol = self.solve(max_iterations=max_iterations)

                # if phase I is infeasible
                if not sol.solution:
                    return sol

                # begin solving phase II
                t.drop_artificial_variables()
                logging.debug(f'\nPhase II Tableau:')

            # print starting/phase 2 tableau
            logging.debug(f'{t}\n')

            iterations = 0
            # keep pivoting until exception is raised or max iterations
            while iterations < max_iterations:
                t.pivot(use_blands_rule=use_blands_rule)
                logging.info(f"[{iterations + 1}] Pivoted around "
                             f"{t.pivot_idx[0] - 1, t.pivot_idx[1]}")  # log pivots
                logging.debug(f'{t}\n')  # log tableau
                iterations += 1

            # resort to Bland's rule if necessary
            if not use_blands_rule:
                logging.info("Possible Cycling detected. Resorting to Bland's Rule.")
                return self.solve(use_blands_rule=True)

            # if no solution if found
            raise UnsolvableError(max_iterations)

        return Solution(state=t.state, basis=t.basis,
                        solution=t.solution, obj_value=t.obj_value)


class Solution:
    """
    Converts Tableau parameters into a human-readable solution.
    """

    def __init__(self, state: str, obj_value: float,
                 basis: List[int], solution: List[float]):
        """
        Calculates objective value and basic solution.

        Parameters
        ----------
        state : final state of the tableau
        obj_value : final objective value of tableau
        basis : indices of the basis variables
        solution : raw solution from tableau
        """
        self.state = state

        # objective value
        self.obj_value = {
            "Optimal": obj_value,
            "Unbounded": np.inf,
            "Infeasible": np.NaN
        }[self.state]

        # calculate solution if optimal
        if self.state == "Optimal":
            self.solution = [0.0] * (max(basis) + 1)  # start from zero vector
            for i, j in zip(basis, solution):
                self.solution[i] = j
        else:
            self.solution = None

    def __repr__(self):
        """
        Returns string representation of solution.
        """
        return 'Solution: ' + {
            "Optimal": f"z*={self.obj_value}, x*={self.solution}",
            "Unbounded": "The problem is unbounded.",
            "Infeasible": "The problem is infeasible."
        }[self.state]
