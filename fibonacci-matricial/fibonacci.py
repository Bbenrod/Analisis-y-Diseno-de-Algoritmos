import pandas as pd


MATRIZ_FIBONACCI = pd.DataFrame([[0, 1], [1, 1]], dtype=object)


def fibonacci(n):
    """
    Calcula F(n) mediante multiplicación matricial lineal.

    Recibe un entero n >= 0 y devuelve un entero de Python.
    Realiza n - 1 productos por la matriz base cuando n >= 1.

    Tiempo: O(n). Espacio auxiliar: O(1) matrices de tamaño fijo.
    Estas cotas cuentan operaciones aritméticas, no el tamaño de los enteros.
    """
    if type(n) is not int:
        raise TypeError("n debe ser un entero de Python.")
    if n < 0:
        raise ValueError("n debe ser mayor o igual que cero.")

    if n == 0:
        return 0

    matriz = MATRIZ_FIBONACCI
    for _ in range(n - 1):
        # Cada producto avanza una potencia: M, M^2, ..., M^n.
        matriz = matriz @ MATRIZ_FIBONACCI
    return matriz.iloc[0, 1]


def probar(nombre, obtenido, esperado):
    assert obtenido == esperado, (
        f"{nombre} falló\n"
        f"Esperado: {esperado}\n"
        f"Obtenido: {obtenido}"
    )
    print(f"[OK] {nombre}: {obtenido}")


if __name__ == "__main__":
    probar("Fibonacci n=0", fibonacci(0), 0)
    probar("Fibonacci n=5", fibonacci(5), 5)
    probar("Fibonacci n=10", fibonacci(10), 55)

    print("\nTodas las pruebas de fibonacci.py pasaron.")
