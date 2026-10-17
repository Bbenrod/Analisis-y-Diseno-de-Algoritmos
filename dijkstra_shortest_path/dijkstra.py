"""Find a shortest path using Dijkstra's algorithm."""

N = 20
SOURCE = 0
DESTINATION = 14

EDGES = [
    (0, 5, 1), (0, 7, 9), (0, 11, 11), (0, 16, 11), (0, 17, 3), (0, 18, 9),
    (1, 5, 5), (1, 7, 1), (1, 9, 10), (1, 15, 1), (1, 16, 6), (1, 19, 12),
    (2, 12, 14), (2, 16, 4), (2, 19, 13), (3, 7, 5), (3, 15, 1), (3, 16, 10),
    (3, 18, 4), (4, 7, 3), (4, 8, 11), (4, 11, 12), (4, 13, 13), (4, 16, 9),
    (4, 18, 8), (5, 7, 2), (5, 8, 2), (5, 9, 13), (5, 11, 1), (5, 14, 12),
    (6, 7, 8), (6, 10, 6), (6, 13, 13), (6, 15, 5), (6, 18, 13), (7, 8, 2),
    (7, 11, 13), (7, 16, 4), (7, 17, 6), (7, 19, 7), (8, 13, 8), (8, 14, 10),
    (8, 16, 14), (9, 16, 9), (10, 17, 7), (10, 19, 5), (11, 13, 12), (11, 14, 13),
    (11, 15, 2), (12, 13, 9), (12, 15, 7), (12, 17, 8), (13, 15, 1), (13, 18, 9),
    (13, 19, 6), (14, 18, 9), (15, 18, 2), (17, 18, 14), (17, 19, 13),
]

def construir_grafo(
    edges: list[tuple[int, int, int]] = EDGES, directed: bool = True
) -> list[list[tuple[int, int]]]:
    """Build a weighted adjacency list, directed by default."""
    graph = [[] for _ in range(N)]
    for source, target, weight in edges:
        graph[source].append((target, weight))
        if not directed:
            graph[target].append((source, weight))
    return graph


def dijkstra(
    graph: list[list[tuple[int, int]]], source: int, destination: int
) -> tuple[list[int], int | float]:
    """Return a shortest path and its cost, or ([], infinity) if unreachable."""
    # Return: tuple[list[int], int | float]
    vertex_count = len(graph)
    visited = [False] * vertex_count
    distances = [float("inf")] * vertex_count
    previous = [-1] * vertex_count
    if source == destination:
        return [source], 0

    distances[source] = 0
    # Repeat once per vertex.
    for _ in range(vertex_count):
        minimum_distance = float("inf")
        current_node = -1

        for node in range(vertex_count):
            if not visited[node] and distances[node] < minimum_distance:
                current_node = node
                minimum_distance = distances[node]

        if current_node == -1:
            break

        visited[current_node] = True
        if current_node == destination:
            break

        for neighbor, weight in graph[current_node]:
            candidate_distance = distances[current_node] + weight
            if candidate_distance < distances[neighbor]:
                distances[neighbor] = candidate_distance
                previous[neighbor] = current_node

    if distances[destination] == float("inf"):
        return ([], float("inf"))

    current = destination
    path = []

    while current != source:
        if current == -1:
            return ([], float("inf"))
        path.append(current)
        current = previous[current]

    path.append(source)
    path.reverse()
    output = (path, distances[destination])

    return output



if __name__ == "__main__":
    graph = construir_grafo(EDGES)
    print(dijkstra(graph, SOURCE, DESTINATION))
