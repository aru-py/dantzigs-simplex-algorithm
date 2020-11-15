"""
test_cases.py

Collection of Linear Programming Problems from (1) `Linear Programming` by
James P. Ignizio, (2) homework problems assigned by `Boshi Yang` at Clemson
University, and (3) few created by me.
"""

test_cases = {}

# LP, pg. 96
# simple problem
test_cases[1] = {
    'obj_func': [2, 3, 0, 0, 0],
    'coeffs': [
        [1, -2, 1, 0, 0],
        [2, 1, 0, 1, 0],
        [0, 1, 0, 0, 1]
    ],
    'constraints': [4, 18, 10],
    'solution': [4, 10, 20]
}

# BY, hw.5, #6
# Klee Minty Cube
test_cases[2] = {
    'obj_func': [100, 10, 1, 0, 0, 0],
    'coeffs': [
        [1, 0, 0, 1, 0, 0],
        [20, 1, 0, 0, 1, 0],
        [200, 20, 1, 0, 0, 1]
    ],
    'constraints': [1, 100, 10000],
    'solution': [0, 0, 10000, 1, 100]
}

# BY, hw.6, #5
# problem with cycling
test_cases[3] = {
    'obj_func': [10, -57, -9, -24, 0, 0, 0],
    'coeffs': [
        [.5, -5.5, -2.5, 9, 1, 0, 0],
        [.5, -1.5, -.5, 1, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 1]
    ],
    'constraints': [0, 0, 1],
    'solution': [1, 0, 1, 0, 2]
}

# unbounded case
test_cases[4] = {
    'obj_func': [2, -1, 0, 0],
    'coeffs': [
        [1, -1, 1, 0],
        [-2, -1, 0, 1]
    ],
    'constraints': [1, -6],
    'solution': None
}


# infeasible case
test_cases[5] = {
    'obj_func': [1, 0, 0],
    'coeffs': [
        [1, 1, 0],
        [-1, 0, 1]
    ],
    'constraints': [-1, -1],
    'solution': None
}

# LP, pg. 103
# problem without existing basis
test_cases[6] = {
    'obj_func': [8, 10, 0, 0],
    'coeffs': [
        [1, -1, 0, 0],
        [1, 1, 1, 0],
        [1, .5, 0, -1]
    ],
    'constraints': [1, 9, 4],
    'solution': [5, 4, 0, 3]
}
