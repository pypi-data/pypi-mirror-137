def divide_round_up(n, d):
    """
    Avoids rounding errors that other methods may cause with inputs such as:
        n = 10000000000000001
        d = 10000000000000000
    ; the result should be 2 in this case.
    """

    lowest_possible = n // d
    if lowest_possible * d == n:
        return lowest_possible
    else:
        return lowest_possible + 1
