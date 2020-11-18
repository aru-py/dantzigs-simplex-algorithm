# dantzigs-simplex-algorithm
This is an Python implementation of the [Simplex Algorithm](https://en.wikipedia.org/wiki/Simplex_algorithm) used in [Linear Programming](https://en.wikipedia.org/wiki/Linear_programming). The program requires specification of the objective function, technological coefficients, and the constraints of a linear programming problem and outputs the optimal solution and objective value (if any).


## Features
- Fast Numpy implementation
- Bland's Rule for anti-cycling
- Two-Phase Method
- Supports infeasible and unbounded problems
- Extensive documentation


## Usage
#### Code
```python
from simplex.solver import SimplexSolver
from test_cases import test_cases

problem = test_cases[1]

# initialize solver
solver = SimplexSolver(obj_func=problem['obj_func'],
                       coeffs=problem['coeffs'],
                       constraints=problem['constraints'])

# run solver
sol = solver.solve(use_blands_rule=False,
                   print_tableau=True)
```

#### Output
```
[0] Initial Tableau
      1x  2x  3x  4x  5x RHS
z   [-2. -3.  0.  0.  0.  0.]
x3  [ 1. -2.  1.  0.  0.  4.]
x4  [ 2.  1.  0.  1.  0. 18.]
x5  [ 0.  1.  0.  0.  1. 10.]
```
```
[1] Pivoted around (2, 1)
      1x  2x  3x  4x  5x RHS
z   [-2.  0.  0.  0.  3. 30.]
x3  [ 1.  0.  1.  0.  2. 24.]
x4  [ 2.  0.  0.  1. -1.  8.]
x2  [ 0.  1.  0.  0.  1. 10.]
```
```
[2] Pivoted around (1, 0)
      1x  2x  3x  4x  5x  RHS 
z   [ 0.  0.  0.  1.  2.  38.]
x3  [ 0.  0.  1. -.5  2.5 20.]
x1  [ 1.  0.  0.  .5 -0.5  4.]
x2  [ 0.  1.  0.  0.  1.  10.]
```

```
Solution: 
z*=38.0, 
x*=[4.0, 10.0, 20.0]
```
## Contributing
All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome. Please make sure to adhere to the code style and add sufficient documenation.
