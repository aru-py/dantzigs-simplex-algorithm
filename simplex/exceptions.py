"""
exceptions.py

Contains exceptions for the `SimplexSolver` and `Tableau` classes.
"""


class SolverException(Exception):
    """
    Base class for `SimplexSolver` exceptions.
    """
    pass


class SizeMismatchError(SolverException):
    """
    Raised if Tableau dimensions are incompatible.
    """
    pass


class LinearlyDependentError(SolverException):
    """
    Raised if full-rank condition has not been met.
    """
    pass


class UnsolvableError(SolverException):
    """
    Raised if problem cannot be solved.
    """

    def __init__(self, max_iterations):
        message = f"Solver could not find a solution. Try increasing the " \
                  f"max iterations (currently {max_iterations})."
        super().__init__(message)


class TableauException(BaseException):
    """
    Base class for Tableau exceptions.
    """

    def __init__(self):
        message = "Make sure you are operating on tableau inside" \
                  "a context manager."
        super(TableauException, self).__init__(message)


class ReachedOptimality(TableauException):
    """
    Raised if tableau has reached optimality.
    """
    pass


class UnboundedProblem(TableauException):
    """
    Raised if problem is unbounded.
    """
    pass


class InfeasibleProblem(TableauException):
    """
    Raised if problem is infeasible.
    """
    pass
