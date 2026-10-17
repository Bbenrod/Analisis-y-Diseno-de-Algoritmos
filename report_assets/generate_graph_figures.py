"""Generate graph diagrams and adjacency-matrix figures for the report."""

from pathlib import Path
import os
import sys
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ada-matplotlib-config")
)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from dfs_connected_components.connected_components import EDGES as DFS_EDGES, N as DFS_N
from dijkstra_shortest_path.dijkstra import (
    DESTINATION,
    EDGES as DIJKSTRA_EDGES,
    N as DIJKSTRA_N,
    SOURCE,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "figures"
BACKGROUND = "#FAFAF7"
NODE_COLOR = "#315C72"
EDGE_COLOR = "#87949A"
TEXT_COLOR = "#24343B"
SOURCE_COLOR = "#27866B"
DESTINATION_COLOR = "#C56A42"


def save_figure(figure, filename: str) -> None:
    """Save each report figure as a raster PNG and vector PDF."""
    figure.savefig(
        OUTPUT_DIR / f"{filename}.png",
        dpi=300,
        bbox_inches="tight",
        facecolor=BACKGROUND,
    )
    figure.savefig(
        OUTPUT_DIR / f"{filename}.pdf",
        bbox_inches="tight",
        facecolor=BACKGROUND,
    )


def circular_positions(vertex_count: int) -> list[tuple[float, float]]:
    """Return deterministic circular coordinates for vertices 0..vertex_count-1."""
    from math import cos, pi, sin

    return [
        (cos(pi / 2 - 2 * pi * index / vertex_count),
         sin(pi / 2 - 2 * pi * index / vertex_count))
        for index in range(vertex_count)
    ]


def draw_undirected_graph() -> None:
    positions = circular_positions(DFS_N)
    figure, axis = plt.subplots(figsize=(12, 12), facecolor=BACKGROUND)
    axis.set_facecolor(BACKGROUND)

    for source, target in DFS_EDGES:
        x_values = [positions[source][0], positions[target][0]]
        y_values = [positions[source][1], positions[target][1]]
        axis.plot(x_values, y_values, color=EDGE_COLOR, alpha=0.3, linewidth=0.8, zorder=1)

    axis.scatter(
        [position[0] for position in positions],
        [position[1] for position in positions],
        s=190,
        color=NODE_COLOR,
        edgecolors=BACKGROUND,
        linewidths=1.2,
        zorder=2,
    )
    for vertex, (x_coord, y_coord) in enumerate(positions):
        axis.text(
            x_coord,
            y_coord,
            str(vertex),
            color="white",
            fontsize=7,
            ha="center",
            va="center",
            zorder=3,
        )

    axis.set_title("Undirected graph · 50 vertices · 84 edges", color=TEXT_COLOR, pad=22)
    axis.set_aspect("equal")
    axis.axis("off")
    save_figure(figure, "undirected_graph")
    plt.close(figure)


def draw_directed_weighted_graph() -> None:
    positions = circular_positions(DIJKSTRA_N)
    figure, axis = plt.subplots(figsize=(12, 12), facecolor=BACKGROUND)
    axis.set_facecolor(BACKGROUND)

    for edge_index, (source, target, _weight) in enumerate(DIJKSTRA_EDGES):
        start = positions[source]
        end = positions[target]
        curve = ((edge_index % 3) - 1) * 0.06
        arrow = FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=0.9,
            color=EDGE_COLOR,
            alpha=0.72,
            shrinkA=13,
            shrinkB=13,
            connectionstyle=f"arc3,rad={curve}",
            zorder=1,
        )
        axis.add_patch(arrow)

    node_colors = [NODE_COLOR] * DIJKSTRA_N
    node_colors[SOURCE] = SOURCE_COLOR
    node_colors[DESTINATION] = DESTINATION_COLOR
    axis.scatter(
        [position[0] for position in positions],
        [position[1] for position in positions],
        s=520,
        color=node_colors,
        edgecolors=BACKGROUND,
        linewidths=1.5,
        zorder=3,
    )
    for vertex, (x_coord, y_coord) in enumerate(positions):
        axis.text(
            x_coord,
            y_coord,
            str(vertex),
            color="white",
            fontsize=9,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=4,
        )

    axis.set_title("Directed graph structure · 20 vertices · 59 edges", color=TEXT_COLOR, pad=22)
    axis.set_aspect("equal")
    axis.axis("off")
    save_figure(figure, "directed_weighted_graph")
    plt.close(figure)


def draw_adjacency_matrices() -> None:
    undirected_matrix = [[0] * DFS_N for _ in range(DFS_N)]
    for source, target in DFS_EDGES:
        undirected_matrix[source][target] = 1
        undirected_matrix[target][source] = 1

    weighted_matrix = [[0] * DIJKSTRA_N for _ in range(DIJKSTRA_N)]
    for source, target, weight in DIJKSTRA_EDGES:
        weighted_matrix[source][target] = weight

    figure, axes = plt.subplots(1, 2, figsize=(15, 7), facecolor=BACKGROUND)
    for axis in axes:
        axis.set_facecolor(BACKGROUND)

    left = axes[0].imshow(undirected_matrix, cmap="Blues", interpolation="nearest", vmin=0, vmax=1)
    axes[0].set_title("Undirected adjacency matrix")
    axes[0].set_xlabel("Vertex")
    axes[0].set_ylabel("Vertex")
    axes[0].set_xticks(range(0, DFS_N, 5))
    axes[0].set_yticks(range(0, DFS_N, 5))
    figure.colorbar(left, ax=axes[0], fraction=0.046, pad=0.04, ticks=[0, 1])

    right = axes[1].imshow(weighted_matrix, cmap="YlGnBu", interpolation="nearest", vmin=0)
    axes[1].set_title("Directed weighted adjacency matrix")
    axes[1].set_xlabel("Target vertex")
    axes[1].set_ylabel("Source vertex")
    axes[1].set_xticks(range(DIJKSTRA_N))
    axes[1].set_yticks(range(DIJKSTRA_N))
    axes[1].tick_params(axis="both", labelsize=7)
    figure.colorbar(right, ax=axes[1], fraction=0.046, pad=0.04, label="Edge weight (0 = no edge)")

    figure.suptitle("Adjacency matrices of the official graphs", color=TEXT_COLOR)
    figure.tight_layout()
    save_figure(figure, "adjacency_matrices")
    plt.close(figure)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    draw_undirected_graph()
    draw_directed_weighted_graph()
    draw_adjacency_matrices()
    print(f"Figures saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
