def solution(l, t):
    # l: [int in (1,100)] not [] (1 to 100 elements)
    # t: 250 > int > 0
    # solution verifies if there sequence within l such that sum(l[start:end]) == t
    # if multiple (start,end) satisfy condition -> return min(start,end)
    # if no solutions -> [-1,-1]
    if sum(l) < t:
        return [-1, -1]

    for idx, val in enumerate(l):
        if val == t:
            return [idx, idx]

        if val > t:
            continue

        rolling_sum = val
        curr_start = idx
        for remaining_value in l[idx + 1:]:
            rolling_sum += remaining_value
            curr_start += 1
            if rolling_sum == t:
                return [idx, curr_start]

            if rolling_sum > t:
                break

    else:
        return [-1, -1]


assert solution([1, 2, 3, 4], 15) == [-1, -1]
assert solution([4, 3, 10, 2, 8], 12) == [2, 3]
assert solution([4, 3, 5, 7, 8], 12) == [0, 2]
