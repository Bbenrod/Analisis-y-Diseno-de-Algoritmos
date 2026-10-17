import unittest

from dfs_connected_components.connected_components import (
    EDGES,
    N,
    construir_grafo,
    encontrar_componentes,
)


def normalize_components(components):
    """Compare components without depending on vertex or component order."""
    return {frozenset(component) for component in components}


class TestGraphConstruction(unittest.TestCase):
    def test_undirected_graph(self):
        graph = construir_grafo()
        self.assertEqual(len(graph), N)
        for source, destination in EDGES:
            self.assertIn(destination, graph[source])
            self.assertIn(source, graph[destination])

    def test_official_graph_has_all_vertices_and_edges(self):
        graph = construir_grafo(EDGES)
        self.assertEqual(len(graph), 50)
        self.assertEqual(len(EDGES), 84)
        self.assertEqual(sum(map(len, graph)), 2 * len(EDGES))
        self.assertEqual(set(range(N)), set(range(len(graph))))


class TestConnectedComponents(unittest.TestCase):
    def assert_components(self, n, edges, expected):
        # Small cases define adjacency lists directly, independently of the
        # official graph constructor.
        graph = [[] for _ in range(n)]
        for source, destination in edges:
            graph[source].append(destination)
            graph[destination].append(source)
        actual = encontrar_componentes(graph)
        self.assertEqual(normalize_components(actual), normalize_components(expected))
        vertices = [vertex for component in actual for vertex in component]
        self.assertEqual(len(vertices), len(set(vertices)))
        self.assertEqual(set(vertices), set(range(n)))

    def test_connected_graph(self):
        self.assert_components(4, [(0, 1), (1, 2), (2, 3)], [{0, 1, 2, 3}])

    def test_multiple_components(self):
        self.assert_components(5, [(0, 1), (2, 3)], [{0, 1}, {2, 3}, {4}])

    def test_isolated_vertices(self):
        self.assert_components(3, [], [{0}, {1}, {2}])

    def test_graph_with_cycles(self):
        self.assert_components(
            5,
            [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)],
            [{0, 1, 2, 3, 4}],
        )

    def test_empty_graph(self):
        self.assert_components(0, [], [])

    def test_official_components_are_disjoint_and_cover_all_vertices(self):
        graph = construir_grafo(EDGES)
        components = encontrar_componentes(graph)
        vertices = [vertex for component in components for vertex in component]
        self.assertEqual(len(vertices), len(set(vertices)))
        self.assertEqual(set(vertices), set(range(N)))


if __name__ == "__main__":
    unittest.main()
