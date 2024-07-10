import doctest


def average(l):
    """
    Returns average of the provided list

    >>> print(round(average([20,30,70])))
    40
    """
    return sum(l)/(len(l))

doctest.testmod()