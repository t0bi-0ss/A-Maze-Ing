"""Custom exceptions used during maze generation."""


class EmptyVisitedList(Exception):
    """Raised when a visited-cell list is unexpectedly empty."""


class InvalidDirection(Exception):
    """Raised when a direction leaves the maze bounds or is invalid."""


class InvalidNeighbor(Exception):
    """Raised when a neighbor cell cannot be used for expansion."""


class NoValidNeighbors(Exception):
    """Raised when no valid neighboring cells are available."""


class DeadEnd(Exception):
    """Raised when a dead-end condition is encountered during generation."""
