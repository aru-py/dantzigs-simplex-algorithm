"""
example.py

Simple script to show basic functionality.
"""

from simplex.solver import SimplexSolver
from test.test_cases import test_cases

# the classic Klee-Minty cube problem
problem = test_cases[2]

# initialize solver
solver = SimplexSolver(obj_func=problem['obj_func'],
                       coeffs=problem['coeffs'],
                       constraints=problem['constraints'])


# run solver
print("Beginning solve...\n")
sol = solver.solve(use_blands_rule=False,
                   print_tableau=True)

print('\n', sol)
