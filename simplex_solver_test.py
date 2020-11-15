"""
test_solver.py

Test cases for `SimplexSolver` class. Runs all tests from
`test_cases.py`. To be used with `Pytest`.
"""

from simplex.solver import SimplexSolver
from test_cases import test_cases

def test_simplex_solver():
    for index, test in test_cases.items():
        expected_sol = test['solution']
        del test['solution']  # to avoid unexpected keyword argument
        actual_sol = SimplexSolver(**test).solve().solution
        assert actual_sol == expected_sol