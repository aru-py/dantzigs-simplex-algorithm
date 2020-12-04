from simplex.solver import SimplexSolver

obj_func = [2, 3, 0, 0, 0]
coeffs = [
    [1, -2, 1, 0, 0],
    [2, 1, 0, 1, 0],
    [0, 1, 0, 0, 1]
	]
constraints = [4, 18, 10]


solver = SimplexSolver(obj_func, coeffs, constraints)
sol = solver.solve()
print(sol)

