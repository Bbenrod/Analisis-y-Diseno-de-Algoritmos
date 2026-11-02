"""Construcción y evaluación del árbol binario por frecuencias."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


CHARACTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
FREQUENCIES = [5, 12, 35, 3, 8, 14, 21, 1, 39]


@dataclass
class Node:
    character: str | None = None
    left: Node | None = None
    right: Node | None = None


def build_tree(characters, frequencies):
    """Devolver la raíz del árbol; None si las entradas están vacías.

    Respuesta esperada: un objeto Node (la raíz), o None para entrada vacía.
    Ejemplo con dos caracteres: Node(left=Node('f'), right=Node('a')).

    Pseudocódigo:
        Validar longitudes iguales, caracteres únicos de longitud uno y
        frecuencias numéricas positivas y finitas (sin booleanos).
        Ordenar por frecuencia descendente; conservar el orden en empates.
        Si no hay caracteres, devolver None.
        Si hay uno, crear una raíz con ese carácter como hoja izquierda.
        En otro caso, crear una raíz interna y recorrer los datos ordenados:
            Colocar el siguiente carácter como hoja izquierda.
            Si solo queda un carácter, colocarlo como hoja derecha y terminar.
            Crear un nodo interno derecho y continuar desde él.
        Devolver la raíz.
    """
    characters = list(characters)
    frequencies = list(frequencies)
    if len(characters) != len(frequencies):
        raise ValueError("Debe haber una frecuencia por carácter.")

    seen = set()
    for character, frequency in zip(characters, frequencies):
        if not isinstance(character, str) or len(character) != 1:
            raise ValueError("Cada carácter debe ser una cadena de longitud uno.")
        if character in seen:
            raise ValueError("Los caracteres no deben repetirse.")
        seen.add(character)
        if (isinstance(frequency, bool)
                or not isinstance(frequency, (int, float))
                or frequency <= 0
                or (isinstance(frequency, float) and not isfinite(frequency))):
            raise ValueError("Las frecuencias deben ser números positivos y finitos.")

    if not characters:
        return None

    characters_by_frequency = zip(characters, frequencies)
    characters_by_frequency = sorted(characters_by_frequency, key=lambda pair: pair[1], reverse=True)

    root = Node()
    if len(characters_by_frequency) == 1:
        root.left = Node(character=characters_by_frequency[0][0])
        return root

    current = root
    for character, _ in characters_by_frequency[:-1]:
        current.left = Node(character=character)
        next_node = Node()
        current.right = next_node
        current = next_node

    current.character = characters_by_frequency[-1][0]
    return root


def evaluate_tree(root):
    """Devolver un diccionario de códigos, por ejemplo {'f': '0', 'a': '10'}.

    Respuesta esperada: dict[str, str], con carácter como clave y código como valor.
    Para los datos del trabajo:
        {'I': '0', 'C': '10', 'G': '110', 'F': '1110', 'B': '11110',
         'E': '111110', 'A': '1111110', 'D': '11111110', 'H': '11111111'}
    Para un árbol vacío: {}.

    Pseudocódigo:
        Crear un diccionario vacío.
        Recorrer el árbol desde la raíz con un camino inicialmente vacío.
        Agregar 0 al bajar a la izquierda y 1 al bajar a la derecha.
        Al llegar a una hoja, guardar su carácter y el camino en el diccionario.
        Devolver el diccionario; si la raíz es None, devolver {}.
    """
    output = {}
    pending = [(root, 0, 0)] if root is not None else []
    while pending:
        current, code, depth = pending.pop()
        if current.left is None and current.right is None:
            if current.character is not None:
                output[current.character] = format(code, f"0{max(depth, 1)}b")
        else:
            if current.right is not None:
                pending.append((current.right, code * 2 + 1, depth + 1))
            if current.left is not None:
                pending.append((current.left, code * 2, depth + 1))
    return output


def main():
    """Probar el ejemplo del trabajo con los caracteres y frecuencias dados."""
    tree = build_tree(CHARACTERS, FREQUENCIES)
    print(evaluate_tree(tree))


if __name__ == "__main__":
    main()
