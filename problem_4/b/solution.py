from itertools import combinations


def solution(num_buns, num_required):
    """
    Number of copies per key:
    -------------------------
    Select any group of "num_required - 1" bunnies. By specification they can not open the door.
    However, if we were to add any one of the remaining "num_buns - (num_required - 1)" bunnies,
    we would be able to open the door.

    => every one of the remaining "num_buns - num_required + 1" bunnies has exactly one key that
       is not in the union of keys of the selected "num_required - 1".

    This means that every key has exactly
    num_buns - num_required + 1
    copies (called copies_per_key)

    Total keys:
    -----------
    Based on the above logic, there are exactly
    /      num_buns    \
    \ num_required - 1 /
    different sets of bunnies that miss one key to being able to open the door.

    => there is a total number of distinct keys =
    /      num_buns    \
    \ num_required - 1 /
    =
    /            num_buns         \
    \ num_buns - num_required + 1 /
    = len(combinations(range(num_buns), copies_per_key))
    """
    key_sets = [[] for _ in range(num_buns)]

    copies_per_key = num_buns - num_required + 1

    for key, bunnies in enumerate(combinations(range(num_buns), copies_per_key)):
        for bunny in bunnies:
            key_sets[bunny].append(key)

    return key_sets


assert solution(2, 1) == [[0], [0]]
assert solution(4, 4) == [[0], [1], [2], [3]]
assert solution(5, 3) == [
    [0, 1, 2, 3, 4, 5],
    [0, 1, 2, 6, 7, 8],
    [0, 3, 4, 6, 7, 9],
    [1, 3, 5, 6, 8, 9],
    [2, 4, 5, 7, 8, 9]
]

