def trailing_zeros(s):
    return len(s) - len(s.rstrip('0'))


def solution(n):
    """
    solution uses binary representation of the n and the fact that
    the number of trailing zeros (in binary) represents the number of
    times we can divide n by 2.
    When there are no trailing zeros (i.e. n is not divisible by 2),
    we check if we get more trailing zeros for the next loop by adding
    or subtracting one pellet.
    """
    n = int(n)
    steps = 0
    while n > 1:
        if n == 3:
            steps += 2
            break

        num_zeros = trailing_zeros(bin(n))

        if num_zeros == 0:
            steps += 1
            upper = trailing_zeros(bin(n + 1))
            lower = trailing_zeros(bin(n - 1))
            # add pellet
            if upper > lower:
                n = n + 1
            # remove pellet
            else:
                n = n - 1
        else:
            # is equivalent to dividing by two**num_zeros
            steps += num_zeros
            n = int(bin(n)[:-num_zeros], 2)

    return steps


assert solution('15') == 5
assert solution('4') == 2
