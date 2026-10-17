# Report figures

Run the generator from the repository root:

```bash
.venv/bin/python report_assets/generate_graph_figures.py
```

It writes three figures as both 300-DPI PNGs and vector PDFs to `report_assets/figures/`:

- `undirected_graph.png`: the official unweighted graph.
- `directed_weighted_graph.png`: the official digraph, with direction shown by arrows. Edge weights are shown in the adjacency matrix figure.
- `adjacency_matrices.png`: adjacency matrices for both official graphs.

The figures use only the official edge lists. The script does not run DFS or Dijkstra and does not calculate or display an answer to either exercise.

In Overleaf, upload the PDF files for vector quality and include one with `\includegraphics[width=\textwidth]{directed_weighted_graph.pdf}` (add `\usepackage{graphicx}` to the preamble).
