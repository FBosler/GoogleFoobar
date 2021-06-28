from collections import deque


class Point(object):
    def __init__(self, x, y, layer=0):
        self.x = x
        self.y = y
        self.layer = layer
        self.up = x, y + 1, layer
        self.down = x, y - 1, layer
        self.right = x + 1, y, layer
        self.left = x - 1, y, layer

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def neighbours(self):
        return [self.up, self.down, self.right, self.left]


class Node(object):
    def __init__(self, pt, dist):
        self.pt = pt
        self.dist = dist


def is_valid(row, col, h, w):
    return (0 <= row < h) and (0 <= col < w)


def solution(mat):
    """
    solution solves for the shortest path from 0,0 (src) to h-1,w-1 (destination) and returns
    number of steps required (incl. src and destination), while going through at most one wall.

    Implementation via a breadth-first-search approach with a double layered graph.
    This should in theory yield a linear time complexity as every node is in the two layers is
    visited only once.

    Graphs:
        - base graph (i.e. layer 0) represents paths, where no walls have been hit.
        - shadow graph (i.e. layer 1) represents paths, where exactly one wall has been hit.

    Discovery of nodes:
        - in layer 0 walls can be discovered.
        - in layer 1 walls are ignored (as a wall has already been hit)

    Marking nodes as visited
        - node discovered during the traversal of the base graph -> mark visited for layer 0 and layer 1
          (as it is strictly better to discover a node without hitting a wall first)
        - node discovered during traversal of the shadow graph -> mark visited for layer 1 only

    Transitions between layers:
        - from layer 0 to layer 1 is possible exactly and only when a wall is hit.
        - back from layer 1 to layer 0 is not possible.

    arguments:
    mat -- a map of a maze (i.e.:
            mat = [
                [0, 1, 1, 0],
                [0, 0, 0, 1],
                [1, 1, 0, 0],
                [1, 1, 1, 0]
            ])
            1's represent walls, 0's are passable
    """

    h, w = (len(mat), len(mat[0]))
    src = Point(x=0, y=0)
    dest = Point(x=w - 1, y=h - 1)

    # visited[0] = layer 0; visited[1] = layer 1
    visited = [
        [[False for i in range(w)] for j in range(h)],
        [[False for i in range(w)] for j in range(h)]
    ]

    q = deque([Node(src, 0)])
    while q:
        curr = q.popleft()
        pt = curr.pt

        if pt == dest:
            return curr.dist + 1

        for x, y, layer in pt.neighbours():
            if layer == 0:
                if is_valid(y, x, h, w) and not visited[0][y][x]:
                    visited[0][y][x] = True
                    visited[1][y][x] = True

                    # move up to layer 1 when hitting a wall
                    adj_cell = Node(Point(x=x, y=y, layer=mat[y][x]), curr.dist + 1)
                    q.append(adj_cell)
            elif layer == 1:
                if is_valid(y, x, h, w) and mat[y][x] == 0 and not visited[1][y][x]:
                    visited[1][y][x] = True
                    adj_cell = Node(Point(x=x, y=y, layer=1), curr.dist + 1)
                    q.append(adj_cell)
            else:
                raise ValueError('Invalid layer: {}'.format(layer))


if __name__ == "__main__":
    mat = [
        [0, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 1, 0, 0],
        [1, 1, 1, 0]
    ]
    assert solution(mat) == 7

    mat = [
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0],
    ]
    assert solution(mat) == 11

    mat = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert solution(mat) == 29

    mat = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    assert solution(mat) == 31

    mat = [
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    ]
    assert solution(mat) == 47

    mat = [[0, 1], [1, 0]]
    assert solution(mat) == 3