# Camino mínimo con Dijkstra

## Componentes conexos mediante DFS

El grafo no dirigido y no conexo se recorre mediante DFS para obtener sus componentes conexos. La implementación y las pruebas están en `../dfs_connected_components/`.

## Grafo ponderado dirigido

El grafo tiene 20 vértices. El módulo `dijkstra.py` contiene las 59 aristas de entrada. Cada tupla `(u, v, w)` representa la conexión dirigida `u → v` con peso `w`. `construir_grafo` conserva esa dirección por defecto. `dijkstra` devuelve el camino mínimo de `SOURCE = 0` a `DESTINATION = 14` y su costo.

El enunciado denomina al segundo grafo *dígrafo*, aunque su representación visual no muestra flechas. Se adopta la interpretación `u → v` para cada arista `(u, v, w)`, pendiente de confirmación con el profesor.

Ejecuta el ejercicio desde la raíz del repositorio:

```bash
.venv/bin/python dijkstra_shortest_path/dijkstra.py
```

Ejecuta solo las pruebas de construcción del grafo:

```bash
.venv/bin/python -m unittest dijkstra_shortest_path.tests.test_dijkstra.TestGraphConstruction -v
```

La suite completa incluye también los casos de Dijkstra:

```bash
.venv/bin/python -m unittest dijkstra_shortest_path.tests.test_dijkstra -v
```

Para generar diagramas y matrices de adyacencia para el reporte, consulta `../report_assets/README.md`.
