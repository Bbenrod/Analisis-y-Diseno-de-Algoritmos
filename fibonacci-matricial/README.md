# ADA — Fibonacci matricial y exponenciación rápida

Actividad de **Análisis y Diseño de Algoritmos (007343)**, Universidad Autónoma de Guadalajara.

El proyecto calcula términos de Fibonacci mediante multiplicación matricial directa y mediante exponentiation by squaring. También implementa la exponenciación rápida de números. Conserva la recursión que primero eleva la base al cuadrado y después reduce el exponente aproximadamente a la mitad.

## Algoritmos

| Script / función | Estrategia | Tiempo | Espacio auxiliar |
| --- | --- | --- | --- |
| `fibonacci.py` / `fibonacci(n)` | Multiplicación matricial directa, lineal | O(n) | O(1) |
| `exponenciacion_rapida.py` / `exponenciacion_rapida(x, n)` | Divide y vencerás | O(log n) | O(log n) |
| `fibonacci_matricial.py` / `fibonacci_matricial(n)` | Matrices + divide y vencerás | O(log n) | O(log n) |

La primera implementación es **Fibonacci matricial lineal**, no el método de dos acumuladores escalares. Para `n >= 1`, comienza con la matriz base y realiza `n - 1` productos por esa misma base.

```text
M = [0 1]
    [1 1]

Para n >= 1:
M^n = [F(n-1)  F(n)  ]
      [F(n)    F(n+1)]
```

Se obtiene `F(n)` con `matriz.iloc[0, 1]`. Para `n == 0`, la versión lineal devuelve cero; la rápida obtiene cero de la matriz identidad.

Las potencias rápidas mantienen los casos base `n == 0`, `n == 1` y `n == 2`. Para exponentes pares calculan `(base²)^(n/2)`; para impares, `base * (base²)^((n-1)/2)`, usando `@` en el caso matricial. La llamada interior con exponente `2` termina en un caso base: solo una llamada por nivel reduce el problema.

**Modelo del análisis:** `n` es el índice de Fibonacci o el exponente. Se cuentan operaciones aritméticas de costo constante y matrices de tamaño fijo 2×2. Una multiplicación tradicional de matrices genéricas k×k cuesta O(k³). Con enteros grandes, el costo de cada operación y el almacenamiento de sus dígitos aumentan; por eso estas cotas no son una medición del tiempo real ni del espacio en bytes. Los casos base tienen costo constante.

Las matrices usan `dtype=object` para conservar enteros de Python y evitar el desbordamiento de `int64`. No se utilizan números de punto flotante para Fibonacci.

## Estructura

```text
ADA-fibonacci-matricial/
├── fibonacci.py
├── exponenciacion_rapida.py
├── fibonacci_matricial.py
├── README.md
├── requirements.txt
└── .gitignore
```

El directorio local puede conservar el nombre `fibonacci-exponenciacion`; los comandos se ejecutan desde su raíz.

## Requisitos e instalación

- Python 3.10 o posterior.
- pandas 2.3.3, declarado en `requirements.txt`.

Crear el entorno:

```bash
python -m venv .venv
```

Activarlo en Linux/macOS:

```bash
source .venv/bin/activate
```

O en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar la dependencia:

```bash
python -m pip install -r requirements.txt
```

## Ejecución y pruebas

```bash
python fibonacci.py
python exponenciacion_rapida.py
python fibonacci_matricial.py
```

Cada script ejecuta **tres casos con `assert`**, muestra `[OK]` por caso y termina con un mensaje de confirmación. Los mensajes de fallo incluyen nombre, esperado y obtenido. No ejecutar con `python -O`, porque desactiva los asserts.

| Scripts de Fibonacci | Resultados esperados |
| --- | --- |
| `fibonacci.py` y `fibonacci_matricial.py` | F(0) = 0, F(5) = 5, F(10) = 55 |

| Exponenciación numérica | Resultado esperado |
| --- | --- |
| 2⁰ | 1 |
| 2¹⁰ | 1024 |
| 5³ | 125 |

El índice/exponente debe ser un entero de Python no negativo; las funciones rechazan tipos incorrectos con `TypeError` y negativos con `ValueError`. `potencia_matriz(M, n)` trabaja con un DataFrame entero 2×2, con índices y columnas `0, 1`, y conserva sus valores sin modificar la entrada.
