import math
import unittest

from dijkstra_shortest_path.dijkstra import (
    DESTINATION,
    EDGES,
    N,
    SOURCE,
    construir_grafo,
    dijkstra,
)


class TestGraphConstruction(unittest.TestCase):
    def test_defaults_to_directed_edges(self):
        graph = construir_grafo([(0, 5, 1)])
        self.assertEqual(len(graph), N)
        self.assertEqual(graph[0], [(5, 1)])
        self.assertEqual(graph[5], [])

    def test_preserves_edge_weights_and_does_not_add_reverse_edges(self):
        graph = construir_grafo(EDGES)
        self.assertEqual(len(EDGES), 59)
        for source, target, weight in EDGES:
            self.assertIn((target, weight), graph[source])
            self.assertNotIn((source, weight), graph[target])
        self.assertEqual(sum(map(len, graph)), len(EDGES))

    def test_includes_vertices_without_outgoing_edges(self):
        graph = construir_grafo([(0, 1, 7)])
        self.assertEqual(len(graph), N)
        self.assertEqual(graph[1], [])
        self.assertEqual(graph[19], [])

    def test_can_explicitly_build_an_undirected_graph(self):
        graph = construir_grafo([(0, 5, 1)], directed=False)
        self.assertEqual(graph[0], [(5, 1)])
        self.assertEqual(graph[5], [(0, 1)])


class TestDijkstra(unittest.TestCase):
    """Algorithm cases raise NotImplementedError until Dijkstra is implemented."""

    def assert_valid_path(self, graph, path, cost, source, destination):
        self.assertTrue(path)
        self.assertEqual(path[0], source)
        self.assertEqual(path[-1], destination)
        calculated_cost = 0
        for origin, target in zip(path, path[1:]):
            connections = dict(graph[origin])
            self.assertIn(target, connections)
            calculated_cost += connections[target]
        self.assertEqual(cost, calculated_cost)

    @staticmethod
    def directed_graph(n, edges):
        graph = [[] for _ in range(n)]
        for source, target, weight in edges:
            graph[source].append((target, weight))
        return graph

    def test_known_shortest_path(self):
        graph = self.directed_graph(4, [(0, 1, 2), (1, 3, 2), (0, 3, 9)])
        path, cost = dijkstra(graph, 0, 3)
        self.assert_valid_path(graph, path, cost, 0, 3)
        self.assertEqual(cost, 4)

    def test_multiple_routes_with_different_weights(self):
        graph = self.directed_graph(
            4, [(0, 1, 1), (1, 3, 8), (0, 2, 3), (2, 3, 2), (0, 3, 10)]
        )
        path, cost = dijkstra(graph, 0, 3)
        self.assertEqual(tuple(path), (0, 2, 3))
        self.assertEqual(cost, 5)

    def test_equal_cost_alternative_paths_are_accepted(self):
        graph = self.directed_graph(
            4, [(0, 1, 1), (1, 3, 2), (0, 2, 2), (2, 3, 1)]
        )
        path, cost = dijkstra(graph, 0, 3)
        self.assertIn(tuple(path), {(0, 1, 3), (0, 2, 3)})
        self.assertEqual(cost, 3)

    def test_source_equals_destination(self):
        path, cost = dijkstra([[]], 0, 0)
        self.assertEqual(path, [0])
        self.assertEqual(cost, 0)

    def test_unreachable_destination(self):
        path, cost = dijkstra([[], []], 0, 1)
        self.assertEqual(path, [])
        self.assertTrue(math.isinf(cost))

    def test_uses_only_directed_connections(self):
        graph = [[(1, 4)], []]
        forward_path, forward_cost = dijkstra(graph, 0, 1)
        self.assertEqual(forward_path, [0, 1])
        self.assertEqual(forward_cost, 4)
        reverse_path, reverse_cost = dijkstra(graph, 1, 0)
        self.assertEqual(reverse_path, [])
        self.assertTrue(math.isinf(reverse_cost))

    def test_official_route_is_from_source_to_destination(self):
        graph = construir_grafo(EDGES)
        path, cost = dijkstra(graph, SOURCE, DESTINATION)
        self.assert_valid_path(graph, path, cost, 0, 14)


if __name__ == "__main__":
    unittest.main()
