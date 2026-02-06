import time
from PyBitStat import NumberAnalyzer


def run_benchmark():
    # 1. Готовим данные: 1 миллион чисел (от 0 до 999,999)
    print("Генерация данных (1,000,000 чисел)...")
    data = list(range(1_000_000))

    # Ищем самое последнее число — это худший случай для обычного поиска
    target = 999_999

    # Создаем наш анализатор (он внутри сделает self.data.sort())
    analyzer = NumberAnalyzer(data)

    print("\n--- НАЧАЛО БИТВЫ ---")

    # ЗАМЕР 1: Линейный поиск (имитация твоего старого подхода)
    # Мы просто перебираем циклом каждое число по порядку
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

    # ЗАМЕР 2: Твой Бинарный поиск
    print(f"Ищем число {target} бинарным поиском (твой новый метод)...")
    start_time = time.perf_counter()

    # Вызываем твой метод find_number
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
