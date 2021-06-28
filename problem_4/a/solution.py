from fractions import gcd


def is_dead_lock(a, b):
    sm = (a + b) // gcd(a, b)
    return not (sm & (sm - 1)) == 0


def solution(banana_list):
    pairs = [[is_dead_lock(x, y) for y in banana_list] for x in banana_list]
    return maximum_matching(pairs)


def maximum_matching(graph):
    """
    Original approach was to use Edwards Blossom Algorithm,
    but investigation into the performance showed that
    a depth first search for augmenting paths without considering blossoms,
    yields far better results, which does not come as a suprise given that
    Edwards Blossom has Complexity of O(|V||E|^2), whereas the algorithm
    at hand should have a complexity of O(|V|^2).
    :param graph: nxn matrix where a value of 1 in a cell (i,j) represents an edge between vertex i and vertex j
     e.ge. [
        [0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ]
    :return: number of unmatched edges
    """
    nonmatching_edges = [[x, y] for x in range(len(graph)) for y in range(len(graph[x])) if graph[x][y] == 1]
    matching_edges = []

    # all vertices are unmatched
    unmatched_vertices = [x for x in range(len(graph))]

    augmenting_path_found = True
    while augmenting_path_found:
        augmenting_path_found = False
        while unmatched_vertices:
            visited = []
            path = []
            vertex = unmatched_vertices.pop()
            # we will flip this depending on what we need to extend path
            looking_in_matching = False
            while 1:
                # determine if we need to find edge in matching_edges or nonmatching_edges
                found_alternating_extension = False
                visited.append(vertex)
                neighbouring_vertex = None
                # all connections
                for i in range(len(graph[vertex])):
                    if i not in visited and graph[vertex][i] != 0:
                        if (not looking_in_matching and [vertex, i] in nonmatching_edges) or (
                                looking_in_matching and [vertex, i] in matching_edges
                        ):
                            looking_in_matching = not looking_in_matching
                            neighbouring_vertex = i
                            found_alternating_extension = True
                            break

                if found_alternating_extension:
                    # extend path, go to new vertex
                    path.append(vertex)
                    vertex = neighbouring_vertex
                elif not path:
                    # did not find unvisited vertex, path empty (i.e. cant backtrace)
                    break
                else:
                    # backtrace, as current vertex was a dead-end
                    vertex = path.pop()
                    looking_in_matching = not looking_in_matching

                if vertex in unmatched_vertices:
                    path.append(vertex)
                    augmenting_path_found = True
                    update_edges(path, matching_edges, nonmatching_edges)
                    unmatched_vertices.remove(path[len(path) - 1])
                    break

    return len(graph) - len(matching_edges)


def update_edges(path, matching_edges, nonmatching_edges):
    for i in range(len(path) - 1):
        if [path[i], path[i + 1]] in matching_edges:
            a, b = matching_edges, nonmatching_edges
        else:
            a, b = nonmatching_edges, matching_edges
        symmetric_removal(a, path[i], path[i + 1])
        symmetric_addition(b, path[i], path[i + 1])

def symmetric_removal(lst, i, j):
    lst.remove([i, j])
    lst.remove([j, i])


def symmetric_addition(lst, i, j):
    lst.append([i, j])
    lst.append([j, i])


assert solution([1, 1]) == 2
assert solution([1, 7, 3, 21, 13, 19]) == 0
