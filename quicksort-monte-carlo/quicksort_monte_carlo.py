"""Experimento Monte Carlo de QuickSort con pivote aleatorio.

Ejecutar con ``python quicksort_monte_carlo.py``. Los CSV y la gráfica se
regeneran junto a este archivo. La semilla fija repite las decisiones
seudoaleatorias, aunque el tiempo de ejecución depende de la máquina.
"""

import csv
import math
import platform
import random
import statistics
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SIZES = (100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000)
REPETITIONS = 50
SEED = 20261005
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = BASE_DIR / "images"


class Solution(object):
    """QuickSort in-place con partición Lomuto y pivote aleatorio."""

    def sortArray(self, nums):
        self.quickSort(nums, 0, len(nums) - 1)
        return nums

    def quickSort(self, A, low, high):
        if low < high:
            p = self.partition(A, low, high)
            self.quickSort(A, low, p - 1)
            self.quickSort(A, p + 1, high)

    def partition(self, A, low, high):
        # Elegir un elemento al azar y trasladarlo a la posición del pivote.
        random_index = random.randint(low, high)
        A[random_index], A[high] = A[high], A[random_index]
        pivot = A[high]
        i = low

        for j in range(low, high):
            if A[j] <= pivot:
                A[i], A[j] = A[j], A[i]
                i += 1

        A[i], A[high] = A[high], A[i]
        return i


def run_experiment():
    random.seed(SEED)
    sorter = Solution()
    measurements = []
    expected = {n: list(range(n)) for n in SIZES}

    # Intercalar tamaños distribuye entre ellos los cambios de carga del equipo.
    for run in range(1, REPETITIONS + 1):
        for n in SIZES:
            numbers = list(range(n))
            random.shuffle(numbers)

            start = time.perf_counter()
            sorter.sortArray(numbers)
            elapsed = time.perf_counter() - start

            if numbers != expected[n]:
                raise AssertionError(f"QuickSort falló para n={n}, repetición={run}")
            measurements.append((n, run, elapsed))

    return measurements


def calculate_statistics(measurements):
    means = {}
    for n in SIZES:
        times = [elapsed for size, _run, elapsed in measurements if size == n]
        if len(times) != REPETITIONS:
            raise ValueError(f"Se esperaban {REPETITIONS} mediciones para n={n}")
        means[n] = statistics.mean(times)

    reference_time = means[1000]
    k1 = reference_time / (1000 * math.log(1000))
    k2 = reference_time / (1000**2)
    return means, k1, k2


def save_data(measurements, means):
    DATA_DIR.mkdir(exist_ok=True)
    with (DATA_DIR / "tiempos_quicksort.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("n", "run", "time_seconds"))
        writer.writerows((n, run, repr(elapsed)) for n, run, elapsed in measurements)

    with (DATA_DIR / "medias_quicksort.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(("n", "mean_time_seconds"))
        writer.writerows((n, repr(means[n])) for n in SIZES)


def plot_results(means, k1, k2):
    IMAGES_DIR.mkdir(exist_ok=True)
    domain = range(SIZES[0], SIZES[-1] + 1)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(SIZES, [means[n] for n in SIZES], "o-", linewidth=2, label="QuickSort: media de 50 ejecuciones")
    ax.plot(domain, [k1 * n * math.log(n) for n in domain], linewidth=2, label=r"$k_1 n\ln(n)$")
    ax.plot(domain, [k2 * n**2 for n in domain], linewidth=2, label=r"$k_2 n^2$")
    ax.axvline(1000, color="0.45", linestyle=":", linewidth=1)
    ax.scatter([1000], [means[1000]], color="black", zorder=5)
    ax.annotate("Coincidencia en n = 1000", (1000, means[1000]),
                xytext=(1080, 0.0015), fontsize=9,
                arrowprops={"arrowstyle": "->", "color": "0.3"})
    ax.set(title="QuickSort aleatorizado: comparación de crecimiento",
           xlabel="Tamaño del arreglo (n)", ylabel="Tiempo medio de ordenamiento (s)")
    ax.set_xlim(SIZES[0], SIZES[-1])
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    output = IMAGES_DIR / "quicksort_monte_carlo_comparacion.png"
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output


def main():
    measurements = run_experiment()
    means, k1, k2 = calculate_statistics(measurements)
    save_data(measurements, means)
    image_path = plot_results(means, k1, k2)

    print(f"Python: {platform.python_version()} | Sistema: {platform.platform()}")
    print(f"Semilla: {SEED} | Ordenamientos validados: {len(measurements)}")
    print("n,media_segundos")
    for n in SIZES:
        print(f"{n},{means[n]:.12g}")
    print(f"k1 = {k1:.12g} s/(n ln n)")
    print(f"k2 = {k2:.12g} s/n²")
    print(f"T(1000) = {means[1000]:.12g} s")
    print(f"k1·1000·ln(1000) = {k1 * 1000 * math.log(1000):.12g} s")
    print(f"k2·1000² = {k2 * 1000**2:.12g} s")
    print(f"Datos: {DATA_DIR}")
    print(f"Gráfica: {image_path}")


if __name__ == "__main__":
    main()
