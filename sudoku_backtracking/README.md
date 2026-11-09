# Sudoku mediante Backtracking

Resolver los dos Sudokus regulares (9×9) del enunciado mediante búsqueda exhaustiva con poda y vuelta atrás. Es un problema de satisfacción de restricciones (CSP); no se requieren técnicas adicionales.

Cada fila, columna y bloque de 3×3 debe contener los números del 1 al 9 sin repetir. Los ceros representan celdas vacías y las pistas originales no pueden modificarse.

`sudoku.py` contiene ambos tableros y tres funciones con pseudocódigo: `find_empty`, `is_valid` y `solve_sudoku`. Las coordenadas comienzan en 0. El solucionador modifica el tablero recibido y devuelve `True` si lo resuelve, o `False` si no existe solución; en este último caso debe restaurar el tablero inicial. Se asumen entradas 9×9 con valores 0..9 y pistas sin conflictos.

Desde la raíz del repositorio:

```bash
.venv/bin/python sudoku_backtracking/sudoku.py
.venv/bin/python -m unittest sudoku_backtracking.tests.test_sudoku -v
```

El `main` evalúa ambos casos por separado e imprime sus resultados. Las pruebas verifican ambos casos, conservación de pistas, filas, columnas, bloques, búsqueda de vacíos, candidatos válidos, tablero completo, una celda vacía, tablero vacío y un caso sin solución.

Para la entrega, reporta tu código y los dos tableros obtenidos al ejecutar el programa. Las soluciones se obtienen al ejecutar el programa.
