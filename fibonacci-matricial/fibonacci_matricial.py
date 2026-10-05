import pandas as pd


MATRIZ_FIBONACCI = pd.DataFrame([[0, 1], [1, 1]], dtype=object)


def potencia_matriz(M, n):
    """
    Calcula M^n con exponentiation by squaring para un entero n >= 0.

    M es un DataFrame 2x2 de enteros con índices y columnas 0, 1.
    Devuelve un DataFrame 2x2; dtype=object conserva enteros de Python.
    Tiempo: O(log n). Espacio auxiliar: O(log n) por la recursión.
    Estas cotas cuentan operaciones aritméticas con matrices de tamaño fijo.
    """
    if type(n) is not int:
        raise TypeError("n debe ser un entero de Python.")
    if n < 0:
        raise ValueError("n debe ser mayor o igual que cero.")
    if M.shape != (2, 2):
        raise ValueError("M debe ser una matriz 2x2.")

    # Evita que pandas use int64 y desborde al calcular términos grandes.
    M = M.astype(object)

    # Casos base: identidad, matriz original y cuadrado.
    if n == 0:
        return pd.DataFrame([[1, 0], [0, 1]], dtype=object)

    if n == 1:
        return M

    if n == 2:
        return M @ M

    # Caso par: (M^2)^(n/2). La llamada interior tiene costo constante.
    if n % 2 == 0:
        return potencia_matriz(potencia_matriz(M, 2), n // 2)
    # Caso impar: M @ (M^2)^((n-1)/2).
    else:
        return M @ potencia_matriz(
            potencia_matriz(M, 2), (n - 1) // 2
        )


def fibonacci_matricial(n):
    """
    Calcula F(n) extrayendo la posición [0, 1] de MATRIZ_FIBONACCI^n.

    Recibe un entero n >= 0 y devuelve un entero de Python.
    Para n >= 1, M^n = [[F(n-1), F(n)], [F(n), F(n+1)]].
    Para n == 0, M^0 es la identidad y su posición [0, 1] contiene cero.
    Tiempo y espacio auxiliar: O(log n), contando operaciones aritméticas.
    """
    matriz = potencia_matriz(MATRIZ_FIBONACCI, n)
    return matriz.iloc[0, 1]


def probar(nombre, obtenido, esperado):
    assert obtenido == esperado, (
        f"{nombre} falló\n"
        f"Esperado: {esperado}\n"
        f"Obtenido: {obtenido}"
    )
    print(f"[OK] {nombre}: {obtenido}")


if __name__ == "__main__":
    probar("Fibonacci matricial n=0", fibonacci_matricial(0), 0)
    probar("Fibonacci matricial n=5", fibonacci_matricial(5), 5)
    probar("Fibonacci matricial n=10", fibonacci_matricial(10), 55)

    print("\nTodas las pruebas de fibonacci_matricial.py pasaron.")
