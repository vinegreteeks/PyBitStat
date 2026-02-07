import time
from PyBitStat import NumberAnalyzer


def run_benchmark():
    print("Генерация данных (100,000,000 чисел)...")
    data = list(range(100_000_000))
    target = 99_999_999
    analyzer = NumberAnalyzer(data)

    print("\n--- НАЧАЛО БИТВЫ ---")
    print(f"Ищем число {target} перебором (как раньше)...")
    start_time = time.perf_counter()

    found_index = -1
    for i in range(len(analyzer.data)):
        if analyzer.data[i] == target:
            found_index = i
            break

    end_time = time.perf_counter()
    linear_time = end_time - start_time
    print(f"Линейный поиск (O(N)): {linear_time:.6f} сек.")
    print(f"Ищем число {target} бинарным поиском (мой новый метод)...")
    start_time = time.perf_counter()
    idx = analyzer.find_number(target)
    end_time = time.perf_counter()
    binary_time = end_time - start_time
    print(f"Бинарный поиск (O(logN)): {binary_time:.6f} сек.")

    # ИТОГ
    print("-" * 30)
    if binary_time > 0:
        # Считаем во сколько раз быстрее
        speedup = int(linear_time / binary_time)
        print(f">>> ПОБЕДА: Бинарный поиск быстрее в {speedup} раз! <<<")
    else:
        print("Бинарный поиск отработал мгновенно (0.000000 сек).")


if __name__ == "__main__":
    run_benchmark()
