class EmptyUnvisitedListError(Exception):
    """Exception raised when the unvisited list is empty."""


class UnreachableCellsError(Exception):
    """Exception raised when all cells in the unvisited list are unreachable"""
