# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:

import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        add a vertex to a directed graph in the form of an adjacency matrix
        """
        self.adj_matrix = [[0 for i in range(self.v_count + 1)] for j in range(self.v_count + 1)]
        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Add an edge wih an associated weight to a directed graph
        """
        if not (0 <= src < self.v_count and 0 <= dst < self.v_count):
            return None
        else:
            if weight > 0:
                if src is not dst:
                    self.adj_matrix[src][dst] = weight


    def remove_edge(self, src: int, dst: int) -> None:
        """
        Remove an edge from a directed graph by setting the weight to 0
        """
        if not (0 <= src < self.v_count and 0 <= dst < self.v_count):
            return None
        else:
            if src is not dst:
                self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Return a list of vertices from a directed graph
        """
        return [i for i in range(self.v_count)]

    def get_edges(self) -> []:
        """
        return the edges between 2 vertices and those edge's associated weights
        """
        list = []
        for i in range(self.v_count):
            for j in range(self.v_count):
                if (i and j) >= 0 and self.adj_matrix[i][j] > 0:
                    list.append((i, j, self.adj_matrix[i][j]))

        return list

    def is_valid_path(self, path: []) -> bool:
        """
        return True if there is a way to get from a starting vertex to another through the given vertices
        """
        if len(path) == 0:
            return True
        edges = self.get_edges()
        for i in range(0, len(path) - 1):
            if (path[i], path[i + 1], self.adj_matrix[path[i]][path[i + 1]]) not in edges:
                return False

        return True


    def dfs(self, v_start, v_end=None) -> []:
        """
        Do a depth first search on a directed graph
        """
        if v_start not in range(0, self.v_count):
            return []
        if v_end not in range(0, self.v_count):
            v_end = None
        visited = []
        stack = deque([v_start])
        while len(stack) is not 0:
            v = stack.pop()
            if v not in visited:
                visited += [v]
                for i in range(len(self.adj_matrix[v]) - 1, -1, -1):
                    if self.adj_matrix[v][i] > 0:
                        stack.append(i)
            if v == v_end:
                break
        return visited


    def bfs(self, v_start, v_end=None) -> []:
        """
        Do a breadth first search on a directed graph
        """
        if v_start not in range(0, self.v_count):
            return []
        if v_end not in range(0, self.v_count):
            v_end = None
        visited = []
        queue = deque([v_start])
        while len(queue) is not 0:
            v = queue.popleft()
            if v not in visited:
                visited += [v]
                if v == v_end:
                    break
                for i in range(len(self.adj_matrix[v])):
                    if i not in visited and self.adj_matrix[v][i] > 0:
                        queue.append(i)
        return visited

    def has_cycle(self):
        """
        Check if there is a cycle in a directed graph
        """
        visited = []
        for i in range(self.v_count - 1):
            visited += [i]
            for j in self.dfs(i):
                if self.adj_matrix[j][i] > 0:
                    return True

        return False
    def dijkstra(self, src: int) -> []:
        """
        Return the shortest possible route from a given vertex to all other vertices in a directed graph, return 'inf'
        for vertices that don't have a path from given vertex to another
        """
        # initialize parent,neighbors, and shortest distance dictionaries
        distance = {}
        parent = {}
        vertices = self.get_vertices()
        for i in range(self.v_count):
            distance[i] = float('inf')
            parent[i] = None
        distance[src] = 0
        neighbors = {}
        for x in vertices:
            neighbors[x] = []
            for y in range(len(self.adj_matrix[x])):
                if self.adj_matrix[x][y] > 0:
                    neighbors[x].append(y)
        v = src
        # loop through all vertices of a directed graph, starting with the source vertex and continuing with the vertex
        # with the lowest cost to the source until no vertices are left unvisited
        while len(vertices) != 0:
            for k in vertices:
                if distance[v] > distance[k]:
                    v = k
            vertices.remove(v)
            for z in neighbors[v]:
                if z in vertices:
                    route = distance[v] + self.adj_matrix[v][z]
                    if route < distance[z]:
                        distance[z] = route
                        parent[z] = v
            if len(vertices) > 0:
                v = vertices[0]

        dijkstra = []
        for a in distance.values():
            dijkstra += [a]
        return dijkstra





if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(12, 11, 9), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
