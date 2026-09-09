"""Custom exceptions for pathfinding failures."""


class EmptyUnvisitedListError(Exception):
    """
    Raised when the unvisited list is empty before path resolution completes.
    """


class UnreachableCellsError(Exception):
    """Raised when no reachable cells remain in the unvisited frontier."""
