# Árbol binario por frecuencias

Ejercicio en Python 3.10 o posterior, sin dependencias
externas. Hay dos funciones, con pseudocódigo en `huffman.py`:

- `build_tree(characters, frequencies)`: devuelve la raíz del árbol.
- `evaluate_tree(root)`: recorre el árbol y devuelve los códigos en un diccionario,
  por ejemplo `{"f": "0", "a": "10", "b": "11"}`.

`Node` representa un carácter o un nodo interno con hijos izquierdo y derecho.

Ordena por frecuencia descendente. En empates, conserva el orden de entrada.
Coloca hojas a la izquierda y continúa por nodos internos a la derecha. Al quedar
los dos últimos caracteres, coloca uno a la izquierda y el último a la derecha:
los códigos siguen `0`, `10`, `110`, … y el último termina solo con unos.
Un carácter único tiene código `0`; una entrada vacía produce `None` y `{}`.
Las entradas inválidas deben lanzar `ValueError`.

Este procedimiento sigue el árbol en cadena del ejercicio, no Huffman clásico,
que combina repetidamente los dos nodos de menor frecuencia.

Desde la raíz del repositorio:

```bash
python3 huffman-coding/huffman.py
python3 -m unittest discover -s huffman-coding -p 'test_*.py' -v
```

Las pruebas con `unittest` validan la estructura, el recorrido, el ejemplo y los
casos límite.

Los datos del ejemplo y la prueba local están en `tests/test_huffman.py`.
`huffman.py` contiene los datos del trabajo (`CHARACTERS` y `FREQUENCIES`), el nodo
y las dos funciones.
Para ejecutar solo la prueba local desde la carpeta del ejercicio:

```bash
cd huffman-coding
python3 -m unittest tests.test_huffman.TestEvaluarArbol.test_prueba_local_con_datos_del_ejercicio -v
```
