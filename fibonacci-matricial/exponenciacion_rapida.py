def exponenciacion_rapida(x, n):
    """
    Calcula x^n con exponentiation by squaring para un entero n >= 0.

    Devuelve la potencia de la base numérica x.
    Tiempo: O(log n). Espacio auxiliar: O(log n) por la recursión.
    Los casos base tienen costo constante. Se cuentan operaciones aritméticas.
    """
    if type(n) is not int:
        raise TypeError("n debe ser un entero de Python.")
    if n < 0:
        raise ValueError("n debe ser mayor o igual que cero.")

    if n == 0:
        return 1
    if n == 1:
        return x
    if n == 2:
        return x * x

    # Caso par: (x^2)^(n/2). La llamada interior usa el caso base n == 2.
    if n % 2 == 0:
        return exponenciacion_rapida(exponenciacion_rapida(x, 2), n // 2)
    # Caso impar: x * (x^2)^((n-1)/2).
    else:
        return x * exponenciacion_rapida(
            exponenciacion_rapida(x, 2), (n - 1) // 2
        )


def probar(nombre, obtenido, esperado):
    assert obtenido == esperado, (
        f"{nombre} falló\n"
        f"Esperado: {esperado}\n"
        f"Obtenido: {obtenido}"
    )
    print(f"[OK] {nombre}: {obtenido}")


if __name__ == "__main__":
    probar("2^0", exponenciacion_rapida(2, 0), 1)
    probar("2^10", exponenciacion_rapida(2, 10), 1024)
    probar("5^3", exponenciacion_rapida(5, 3), 125)

    print("\nTodas las pruebas de exponenciacion_rapida.py pasaron.")
