# Componentes conexos mediante DFS

El grafo es simple, no dirigido y no conexo, con 50 vértices y 84 aristas. `connected_components.py` contiene los datos de entrada. `construir_grafo` produce su lista de adyacencia; `dfs` recorre los vértices y `encontrar_componentes` agrupa cada componente conexo.

Ejecuta el ejercicio desde la raíz del repositorio:

```bash
.venv/bin/python dfs_connected_components/connected_components.py
```

Ejecuta sus pruebas:

```bash
.venv/bin/python -m unittest dfs_connected_components.tests.test_connected_components -v
```
