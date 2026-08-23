class EmptyVisitedList(Exception):
    """
    Exception in case of an empty 'visited' list
    """


class InvalidDirection(Exception):
    """
    Exception for an invalid Direction
    """


class InvalidNeighbor(Exception):
    """
    Exception in case of an invalid neighbor's index
    """


class NoValidNeighbors(Exception):
    """
    Exception in case no valid neighbors are found
    """


class DeadEnd(Exception):
    """
    Exception when a 'dead end' has been reached
    """
