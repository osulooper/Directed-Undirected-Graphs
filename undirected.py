# Course: 261
# Author: Nicholas Tucker
# Assignment: 6
# Description: implemenet an undirected graph


import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        self.adj_list[v] = []
        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        if u is not v:
            if u not in self.adj_list:
                self.add_vertex(u)
            if v not in self.adj_list:
                self.add_vertex(v)

            if u not in self.adj_list[v]:
                self.adj_list[v] += u
                self.adj_list[u] += v
    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[v].remove(u)
            self.adj_list[u].remove(v)


    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        vertices = []
        if v in self.adj_list:
            for i in self.adj_list[v]:
                vertices += i
            for j in vertices:
                self.remove_edge(v, j)
            del(self.adj_list[v])

    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        keys = []
        for key in self.adj_list:
            keys += key
        return keys
    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        edges = []
        keys = self.get_vertices()
        for key in self.adj_list:
            for value in self.adj_list[key]:
                if value in keys:
                    edges.append((key,value))
            keys.remove(key)
        return edges
    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        if len(path) == 0:
            return True
        if len(path) == 1:
            if path[0] in self.adj_list:
                return True
            else:
                return False
        edges = self.get_edges()
        for i in range(len(path) - 1):
            if (path[i], path[i+1]) not in edges and (path[i+1], path[i]) not in edges:
                # print((path[i]), path[i+1])
                return False
        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        if v_end not in self.adj_list:
            v_end = None
        visited = []
        stack = deque(v_start)
        while len(stack) is not 0:
            v = stack.pop()
            if v not in visited:
                visited += v
                for i in reversed(sorted(self.adj_list[v])):
                    stack.append(i)
            if v == v_end:
                break
        return visited



    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        if v_start not in self.adj_list:
            return []
        if v_end not in self.adj_list:
            v_end = None
        visited = []
        queue = deque(v_start)
        while len(queue) is not 0:
            v = queue.popleft()
            if v not in visited:
                visited += v
                if v == v_end:
                    break
                for i in sorted(self.adj_list[v]):
                    if i not in visited:
                        queue.append(i)
        return visited

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        count = 0
        vertices = self.get_vertices()
        while len(vertices) != 0:
            visited = self.dfs(vertices[0])
            count += 1
            for i in visited:
                if i in visited:
                    vertices.remove(i)
        return count

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        stack = deque()
        visited = []
        vertices = self.get_vertices()
        parent = {}
        for x in range(len(self.adj_list)):
            if len(self.adj_list[vertices[x]]) > 0:
                v = vertices[x]
                break
        visited.append(v)
        stack.append(v)
        # vertices.remove(v)
        while len(stack) != 0:
            v1 = stack.pop()
            if v1 not in visited:
                visited.append(v1)
            for i in self.adj_list[v1]:
                if i not in visited:
                    visited.append(i)
                    stack.append(i)
                    parent[i] = v1
                elif parent[v1][0] != i:
                    return True
            if v1 in vertices:
                vertices.remove(v1)
            if len(stack) == 0 and len(vertices) > 0:
                stack.append(vertices[0])

        return False

if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)
    #
    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)
    #
    # g.add_vertex('A')
    # print(g)
    #
    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)
    #
    #
    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)
    #
    #
    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    #
    #
    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))
    #
    #
    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = 'ABCDEGH'
    # for case in test_cases:
    #     print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    # print('-----')
    # for i in range(1, len(test_cases)):
    #     v1, v2 = test_cases[i], test_cases[-1 - i]
    #     print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    # print(g.count_connected_components())


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print('{:<10}'.format(case), g.has_cycle())
