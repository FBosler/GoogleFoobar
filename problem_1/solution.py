from collections import Counter


def solution(data, n):
    counted = Counter(data)
    return [k for k, v in counted.items() if v <= n]


assert solution([1, 2, 3], 0) == []
assert solution([1, 2, 2, 3, 3, 3, 4, 5, 5], 1) == [1, 4]
