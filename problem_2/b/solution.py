def max_value(h):
    # total number of elements in the tree
    return sum([2 ** level for level in range(h)])


def find_root(to_check, root_value, height):
    if to_check >= root_value:
        return -1

    left_leaf = root_value - 2 ** (height - 1)
    right_leaf = root_value - 1

    while (to_check != left_leaf) and (to_check != right_leaf):
        if to_check < left_leaf:
            root_value = left_leaf
        else:
            root_value = right_leaf
        height -= 1

        left_leaf = root_value - 2 ** (height - 1)
        right_leaf = root_value - 1

    return root_value


def solution(h, q):
    base_root = max_value(h)
    return [find_root(to_check=elem, root_value=base_root, height=h) for elem in q]


assert solution(3, [7, 3, 5, 1]) == [-1, 7, 6, 3]
assert solution(5, [19, 14, 28]) == [21, 15, 29]
