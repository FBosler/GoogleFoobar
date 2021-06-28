from __future__ import division
from fractions import Fraction, gcd
from itertools import starmap
from operator import mul


# swap i,j rows/columns of a square matrix `m`
def swap(m, i, j):
    if i == j:
        return m

    n = []

    for r in range(len(m)):
        res_row = []
        temp_row = m[r]
        if r == i:
            temp_row = m[j]
        if r == j:
            temp_row = m[i]
        for c in range(len(m)):
            temp_cell = temp_row[c]
            if c == i:
                temp_cell = temp_row[j]
            if c == j:
                temp_cell = temp_row[i]
            res_row.append(temp_cell)
        n.append(res_row)

    return n


def sort(m):
    zero_row = -1
    for row in range(len(m)):

        if not any(m[row]):
            zero_row = row

        if any(m[row]) and zero_row > -1:
            swapped = swap(m, row, zero_row)
            return sort(swapped)

    return m


def decompose(m):
    t = sum([any(row) for row in m])
    Q = [row[:t] for row in m][:t]
    R = [row[t:] for row in m][:t]
    return Q, R


def identity(t):
    return [[1 if col == row else 0 for col in range(t)] for row in range(t)]


def subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]


def transpose(m):
    return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]


def multiply(A, B):
    return [[sum(starmap(mul, zip(A_row, B_col))) for B_col in transpose(B)] for A_row in A]


def swap_row(m, i, j):
    m[i], m[j] = m[j], m[i]


def gauss_elmination(m, values):
    mat = [[elem for elem in row] for row in m]
    for i in range(len(mat)):

        # swap rows
        index = -1
        for j in range(i, len(mat)):
            if mat[j][i] != 0:
                index = j
                break
        if index == -1:
            raise ValueError('Gauss elimination failed!')

        swap_row(mat, i, index)
        swap_row(values, i, index)

        # scale values
        for j in range(i + 1, len(mat)):
            if mat[j][i] == 0:
                continue
            ratio = -mat[j][i] / mat[i][i]
            for k in range(i, len(mat)):
                mat[j][k] += ratio * mat[i][k]
            values[j] += ratio * values[i]

    # solve for upper triangular matrix
    res = [0 for i in range(len(mat))]
    for i in range(len(mat)):
        index = len(mat) - 1 - i
        end = len(mat) - 1
        while end > index:
            values[index] -= mat[index][end] * res[end]
            end -= 1
        res[index] = values[index] / mat[index][index]
    return res


def matrix_inverse(mat):
    tmat = transpose(mat)
    mat_inv = []
    for i in range(len(tmat)):
        values = [1 if i == j else 0 for j in range(len(mat))]
        mat_inv.append(gauss_elmination(tmat, values))
    return mat_inv


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def format_solution(arr):
    arr = [Fraction(state).limit_denominator() for state in arr]
    denom = reduce(lcm, [state.denominator for state in arr])
    return [
               int(state.numerator)
               if state.denominator == denom else
               int(state.numerator * denom / state.denominator)
               for state in arr
           ] + [denom]


def normalize(m):
    return [[elem / sum(row) if elem else 0 for elem in row] if sum(row) != 0 else row for row in m]


def solution(m):
    if len(m) == 1:
        return [1, 1]

    m = normalize(m)
    m = sort(m)

    Q, R = decompose(m)

    # https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter11.pdf
    # terminal probabilities are determined as:
    # B = (I - Q)^-1 * R

    terminal_states = multiply(matrix_inverse(subtract(identity(len(Q)), Q)), R)[0]
    terminal_states = [Fraction(state).limit_denominator() for state in terminal_states]

    return format_solution(terminal_states)


test = [
    [0, 2, 1, 0, 0],
    [0, 0, 0, 3, 4],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]
assert solution(test) == [7, 6, 8, 21]

test = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
assert solution(test) == [0, 3, 2, 9, 14]
