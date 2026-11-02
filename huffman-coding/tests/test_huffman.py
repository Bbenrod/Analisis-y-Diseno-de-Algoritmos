"""Pruebas del árbol y de sus códigos binarios."""

import unittest

from huffman import Node, build_tree, evaluate_tree


class TestConstruirArbol(unittest.TestCase):
    def test_estructura(self):
        root = build_tree(list("abc"), [2, 5, 1])
        self.assertIsNone(root.character)
        self.assertEqual(root.left.character, "b")
        self.assertIsNone(root.right.character)
        self.assertEqual(root.right.left.character, "a")
        self.assertEqual(root.right.right.character, "c")
        for hoja in [root.left, root.right.left, root.right.right]:
            self.assertIsNone(hoja.left)
            self.assertIsNone(hoja.right)

    def test_vacio(self):
        self.assertIsNone(build_tree([], []))

    def test_un_caracter(self):
        root = build_tree(["a"], [3])
        self.assertIsNone(root.character)
        self.assertEqual(root.left.character, "a")
        self.assertIsNone(root.right)
        self.assertEqual(evaluate_tree(root), {"a": "0"})

    def test_empates_conservan_orden_de_entrada(self):
        root = build_tree(list("zab"), [2, 2, 2])
        self.assertEqual(evaluate_tree(root), {"z": "0", "a": "10", "b": "11"})

    def test_entradas_invalidas(self):
        casos = [(["a"], []), (["a", "a"], [1, 2]), ([""], [1]),
                 (["ab"], [1]), ([None], [1])]
        casos += [(["a"], [f]) for f in
                  [0, -1, True, None, "2", float("inf"), float("nan")]]
        for characters, frequencies in casos:
            with self.subTest(datos=(characters, frequencies)):
                with self.assertRaises(ValueError):
                    build_tree(characters, frequencies)


class TestEvaluarArbol(unittest.TestCase):
    def test_recorrido_de_arbol_manual(self):
        root = Node(left=Node("f"), right=Node(
            left=Node("a"), right=Node("b")))
        self.assertEqual(evaluate_tree(root), {"f": "0", "a": "10", "b": "11"})

    def test_recorrido_de_otra_estructura(self):
        root = Node(left=Node(left=Node("x"), right=Node("y")),
                    right=Node("z"))
        self.assertEqual(evaluate_tree(root), {"x": "00", "y": "01", "z": "1"})

    def test_vacio(self):
        self.assertEqual(evaluate_tree(None), {})

    def test_prueba_local_con_datos_del_ejercicio(self):
        root = build_tree(list("ABCDEFGHI"), [5, 12, 35, 3, 8, 14, 21, 1, 39])
        codigos = evaluate_tree(root)
        self.assertEqual(codigos, {
            "I": "0", "C": "10", "G": "110", "F": "1110",
            "B": "11110", "E": "111110", "A": "1111110",
            "D": "11111110", "H": "11111111",
        })
        for character, codigo in codigos.items():
            for otro, otro_codigo in codigos.items():
                if character != otro:
                    self.assertFalse(otro_codigo.startswith(codigo))


if __name__ == "__main__":
    unittest.main()
