import os
import numpy as np

def even_only(lst):
    """
    Возвращает чётные целые числа из lst, сохраняя порядок.
    Args:
        lst: Последовательность значений (int/float/любой тип).

    Returns:
        list[int]: Список чётных целых. Пустой, если чётных нет.

    Notes:
        - Берём int и float с целым значением (x.is_integer()).
        - Игнорируем bool и любые нечисловые типы.
    """
    res = []
    for x in lst:
        if isinstance(x, bool):
            continue
        if not isinstance(x, (int, float)):
            continue
        if isinstance(x, float) and not x.is_integer():
            continue
        xi = int(x)
        if xi % 2 == 0:
            res.append(xi)
    return res


def even_stats(lst):
    """
Возвращает сводную статистику по чётным целым из lst.

Args:
    lst: Последовательность значений любых типов.

Returns:
    dict[str, int | float] | None: Словарь с ключами:
        - "sum" (int): сумма;
        - "min" (int): минимум;
        - "max" (int): максимум;
        - "avg" (float): среднее арифметическое.
    Возвращает None, если после отбора чётных целых список пуст.

Notes:
    - Отбор делает even_only(lst).
    - Учитываются int и float с целым значением (x.is_integer()).
    - Игнорируются bool и любые нечисловые типы.
    - "avg" всегда float (даже если делится нацело).
"""
    ei = even_only(lst)
    if not ei:
        return None
    arr = np.array(ei)
    return {
        "sum": int(arr.sum()),
        "min": int(arr.min()),
        "max": int(arr.max()),
        "avg": float(arr.mean())
    } 


def sign_counts(lst):
    """
Возвращает количество положительных, отрицательных и нулей.
    
    """
    if not lst:
        return {"plus": 0, "minus": 0, "zeros": 0}
    lst = [x for x in lst if isinstance(x, (int, float)) and not isinstance(x , bool)]
    arr = np.array(lst)
    pos = (arr > 0).sum()
    neg = (arr < 0).sum()
    zeros = (arr == 0).sum()
    return {
        "pos": int(pos),
        "neg": int(neg),
        "zero": int(zeros)
    }

def median_even(lst):
    """
    Возвращает медиану чётных целых из lst или None, если после отбора пусто.
    Agrs:
        lst: Последовательность значений любых типов.

    Returns: 
        int | float | None: Медиана отсортированного списка чётных целых.
            При нечётной длине - средний элемент (int).
            При чётной - среднее двух средних (float).
            Если подходящих значений нет - None.
    Notes:
        - Отбор делает even_only(lst): учитывает int и float с целым значением, игнориует bool и нечисловые.
        - Порядок: отбор -> сортировка -> вычисление медианы.
    """
    ei = even_only(lst)
    if not ei:
        return None
    ei = sorted(ei)
    
    n = len(ei)
    if n % 2 == 1:
        return ei[n//2]
    else:
        return (ei[n//2-1] + ei[n//2])/2


def format_even_stats(lst):
    """
    Кратко: строка отчёт по чётным числам из lst; если нет чётных - специальная фраза.
    Agrs:
        lst: последовательность любых значений.
    Returns:
        str: 'sum=..., min:..., max:..., avg:..."
    Notes:
        - Использует evem_stats(lst).
    """
    es = even_stats(lst)
    if es is None:
        return "нет чётных чисел"
    return f"sum={es['sum']}, min={es['min']}, max={es['max']}, avg={es['avg']}"


def to_binary_divmod(n):
    """
    Возвращает двоичную запись неотрицательного целого n строкой.
    >>> to_binary_divmod(0)
    '0'
    >>> to_binary_divmod(37)
    '100101'
    >>> to_binary_divmod(26)
    '11010'
    >>> to_binary_divmod(-1)
    Traceback (most recent call last):
    ...
    ValueError: n must be a non-negative integer

    """
    if n == 0:
        return "0"
    bits = []
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    while n > 0: 
        q, r = divmod(n, 2)
        bits.append(str(r))
        n = q
    return ''.join(reversed(bits))



def save_even_report(lst, path, fmt="txt"):
    """
    Сохраняет отчёт по чётным числам из lst в файл.

    Agrs:
        lst: последовательность любых значений.
        path: путь к файлу (str).
        fmt: "txt" или "csv".
    
    Returns:
        True при успешной записи.
    
    Notes:
        - Статистику берём через even_stats/format_even_stats.
        - TXT: одна строка из format_even_stats + '\n'.
        - CSV: первая строка "sum, min, max, avg"; если чётных нет - только заголовок;
            иначе строка
        "sum,min,max,avg\nS,M,X,A\n
        - При неверном fmt -> ValueError.
    """
    if fmt not in ("txt", "csv"):
        raise ValueError("fmt must be 'txt' or 'csv' ")
    es = even_stats(lst)
    if fmt == 'txt':
        line = "нет чётных целых" if es is None else format_even_stats(lst)
        with   open(path, "w", encoding="utf-8") as f:
            f.write(line + "\n")
    elif fmt == 'csv':
        header = "sum,min,max,avg\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(header)
            if es is not None:
                f.write(f"{es['sum']},{es['min']},{es['max']},{es['avg']}\n")
    return True     



def last_bit(n):
    """
    Возвращает последний бит (0 или 1) для неотрицательного целого n.
    >>> last_bit(0)
    0
    >>> last_bit(7)
    1
    >>> last_bit(8)
    0
    >>> last_bit(-1)
    Traceback (most recent call last):
    ...
    ValueError: n must be a non-negative integer
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    return n & 1


def count_ones(n):
    """
    Считает количество единичных битов в двоичной записи неотрицательного целого n.
    Agrs:
        n: int - неотрицательное целое.
    Returns:
        int - число единичных битов.
    Notes:
        При неверном входе выбрасывает ValueError.
    >>> count_ones(0)
    0
    >>> count_ones(7)
    3
    >>> count_ones(255)
    8
    >>> count_ones(-1)
    Traceback (most recent call last):
    ...
    ValueError: n must be a non-negative integer
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    cnt = 0
    while n > 0:
        cnt += n & 1
        n //= 2
    return cnt

def is_power_of_two(n):
    """
    Принимает int n; if n <= 0 -> False; не-int -> TypeError; возвращает bool.
    """
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n <= 0:
        return False
    return (n & (n - 1)) == 0

def count_ones_fast(n):
    """
    Принимает int n >= 0; не-int -> TypeError; n < 0 -> ValueError; возвращает int - число единичных бит.
    """
    _check_non_negative_int("n", n)
    cnt = 0
    while n:
        cnt += 1
        n &= n - 1
    return cnt

def parity(n):
    """
    Принимает int n>=0; не-int -> TyprError; n<0 -> ValueError; возвращает bool: нечётное число единичных бит.
    >>> parity('10')
    Traceback (most recent call last):
    ...
    TypeError: n must be int
    >>> parity(-1)
    Traceback (most recent call last):
    ...
    ValueError: n must be a non-negative integer
    """
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    return True if count_ones_fast(n) % 2 == 1 else False

def highest_bit_index(n):
    """
    Принимает int n>=0; не-int -> TypeError; n<0 -> ValueError; возвращает int|None - индекс старшего установленного бита; для 0 -> None.
    >>> highest_bit_index(0) is None
    True
    >>> highest_bit_index(32)
    5
    >>> highest_bit_index('10')
    Traceback (most recent call last):
    ...
    TypeError: n must be int
    >>> highest_bit_index(-1)
    Traceback (most recent call last):
    ...
    ValueError: n must be a non-negative integer
    """
    if not isinstance(n, int):
        raise TypeError("n must be int")
    if n == 0:
        return None
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    return n.bit_length() - 1

def is_kth_bit_set(n,k):
    """
    Принимает int n >= 0 и int k >= 0; не-int -> TypeError; отрицательные -> ValueError; возвращает bool - установлен-ли k-й бит.
    >>> is_kth_bit_set(22, 2)
    True
    >>> is_kth_bit_set(0, 5)
    False
    """
    _check_non_negative_int("n", n)
    _check_non_negative_int("k", k)
    return (n & (1 << k)) != 0

def clear_kth_bit(n, k):
    """
    Принимает int n>=0 и int k>=0; не-int -> TypeError; n < 0 или k < 0 -> ValueError; возвращает int: n с очищенным k-м битом.
    """
    _check_non_negative_int("n", n)
    _check_non_negative_int("k", k)
    return n & ~(1 << k)

def set_kth_bit(n, k):
    """
    Кратко: "Включает k-й бит числа n".
    Agrs: n (int, >= 0, bool не принимаем), k (int, >=0).
    Returns: int.
    Raises: TypeError(не int/bool), ValueError(n<0 или k<0)
    Notes: маска 1 << k.
    """
    _check_non_negative_int("n", n)
    _check_non_negative_int("k", k)
    return n | (1 << k)

def toggle_kth_bit(n, k):
    """
    Инвертирует k-й бит числа n.
    Agrs: 
        n (int, >= 0), k (int, >= 0)
    Returns:
        int: n с инвертированным k-м битом.
    Raises:
        TypeError: если n или k не int
        ValueErrorL если n < 0 или k < 0
    Notes: 
        Маска 1 << k; операция XOR (^)
    """
    _check_non_negative_int("n", n)
    _check_non_negative_int("k", k)
    return n ^ (1 << k)

def _check_non_negative_int(name, value):
    """
    Внутренняя функция-проверка: name(str), value - должен быть int >= 0. 
    TypeError - если не int; 
    ValueError - если < 0.
    """
    if type(value) is not int:
        raise TypeError(f"{name} must be int")
    if value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    
def main():
    while True:
        show_menu()
        choice = input("\nВыбери пункт меню (0-4): ").strip()
        if choice == "0":
            print("Выход из программы.")
            break
        elif choice == "1":
            run_list_analysis_mode()
        elif choice == "2":
            run_save_report_mode()
        elif choice == "3":
            run_to_binary_mode()
        elif choice == "4":
            run_bit_calc_mode()

def run_list_analysis_mode():
    print("\nРежим: анализ списка чисел.")
    print("Введи целые числа через пробел. Например: 1 2 3 10 -5 0")
    print()
    raw = input("\nТвой список: ").strip()
    parts = raw.split()
    if not parts:
        print("Пустой ввод. Введи хотя бы одно число.")
        return
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        print("Ошибка: введи только целые числа через пробел. Пример: 1 2 3 10 -5 0")
        return
    print("Ок, распознал числа: ", nums)
    evens = even_only(nums)
    if not evens:
        print("Чётных нет.")
        return
    else:
        print("Чётные числа:", evens)
        print("Считаю статистику...")
        stats = even_stats(evens)
        print(format_even_stats(evens))
        sc = sign_counts(nums)
        print(f"Положительных: {sc['pos']}, отрицательных: {sc['neg']}, нулей: {sc['zero']}")
    print("\nВозвращаюсь в главное меню...")
    print()

def run_save_report_mode():
    while True:
        print("Введи целые числа через пробел (или 0 чтобы выйти)")
        raw = input("Твой список: ").strip()
        if raw == "0":
            print("Возвращаюсь в главное меню...")
            return
        parts = raw.split()
        if not parts:
            print("пустой ввод. Введи хотя бы одно число. Например: 1 2 3 10 -5 0")
            continue
        try:
            nums = [int(p) for p in parts]
        except ValueError:
            print("Ошибка: введи только целые числа через пробел.")
            continue
        path = input("Путь к файлу (например report.txt): ").strip()
        fmt = input("Формат txt/csv (по умолчанию txt): ").strip().lower()
        if fmt == "":
            fmt = "txt"
        if fmt not in ("txt", "csv"):
            print("формат только txt/csv")
            continue
        if path == "":
            print("пустой путь.")
            continue
        try:
            path, fmt = normalize_path(path, fmt)
        except ValueError as e:
            print(e)
            continue
        print(f"Сохраняю в: {path}")
        ok = False
        try:
            ok = save_even_report(nums, path, fmt)
        except OSError as e:
            print(f"Не сохранил: {e}")
            if e.errno == 13:
                print("Нет прав. Выбери другу папку (например D:\data\report.txt)")
            else:
                print(f"Ошибка записи: {e}")
            continue
        if ok:
            print("Сохранил.")
            break
        else:
            print("Не сохранил.")
            continue
    print("Возвращаюсь в главное меню...")
    return

def run_to_binary_mode():
    while True:
        raw = input("введи неотрицательное целое (0 = выход): ").strip()
        if raw == "0": 
            print("Возвращаюсь в меню...")
            return
        try:
            n = int(raw)
            b = to_binary_divmod(n)
        except ValueError as e:
            print(f"Ошибка: {e}")
            continue
        print(f"Двоичное: {b}")

def run_bit_calc_mode():
    num_base = 0
    while True:
        print()
        print("1 - Показать бит\n2 - Поменять бит на 1\n3 - Обнулить бит\n4 - Поменять бит на противоположный\n0 - Новое число/Выход")
        print()
        raw = input("Твой вариант: ").strip()
        if raw == "0":
            x = 0
            while x != 1:
                print()
                print("1 - Новое число\n0 - Выход")
                exit_or_num = input("Твой вариант: ").strip()
                if exit_or_num == "0":
                    print("Возвращаюсь в меню...")
                    return
                elif exit_or_num == "1":
                    try:
                        print()
                        print("Твоё число?")
                        num_base = int(input("число: ").strip())
                        if num_base >= 0:
                            print()
                            print(f"Число: {num_base} (двочное: {bin(num_base)[2:]})")
                            x += 1
                    except (ValueError, TypeError) as e:
                        print(f"Ошибка: {e}")
                        continue
                else:
                    print("Выбери 0 - 1")
                    continue
        elif raw == "1":
            try:
                print()
                print("Показать бит")
                if num_base >= 0:
                    print(f"Число: {num_base} (двочное: {bin(num_base)[2:]})")
                    pos_bit = int(input("Позиция(с правого края, счет с нуля): ").strip())
                    if pos_bit >= 0:
                        print()
                        print(f"Бит: {(num_base >> pos_bit) & 1}")
                    else:
                        print("Число должно быть больше нуля.")
                        continue
                else:
                    print("Число должно быть больше нуля.")
                    continue
            except (ValueError, TypeError) as e:
                print(f"Ошибка: {e}")
                continue
        elif raw == "2":
            try:
                print()
                print(("Поменять бит на 1"))
                if num_base >= 0:
                    print(f"Число: {num_base}, (двочное: {bin(num_base)[2:]})")
                    pos_bit = int(input("Позиция(с правого края счет с нуля): ").strip())
                    if pos_bit >= 0:
                        print()
                        print(f"Получилось число: {set_kth_bit(num_base, pos_bit)} (двоичное: {bin(set_kth_bit(num_base, pos_bit))[2:]})")
                    else:
                        print("Число должно быть больше нуля.")
                        continue
                else:
                    print("Число должно быть больше нуля.")
                    continue
            except (ValueError, TypeError) as e:
                print(f"Ошибка: {e}")
                continue
        elif raw == "3":
            try:
                print()
                print("Обнулить бит")
                if num_base >= 0:
                    print(f"Число: {num_base} (двочное: {bin(num_base)[2:]})")
                    pos_clear = int(input("позиция(с правого края счет с нуля): ").strip())
                    if pos_clear >= 0:
                        print()
                        print(f"Получилось число: {clear_kth_bit(num_base, pos_clear)} (двоичное: {bin(clear_kth_bit(num_base, pos_clear))[2:]})")
                    else:
                        print("Число должно быть больше нуля.")
                        continue
                else:
                    print("Число должно быть больше нуля.")
                    continue
            except (ValueError, TypeError) as e:
                print(f"Ошибка: {e}")
                continue
        elif raw == "4":
            try:
                print()
                print("Поменять бит на противоположный")
                if num_base >= 0:
                    print(f"Число: {num_base} (двочное: {bin(num_base)[2:]})")
                    pos_toggle = int(input("Позиция(с правого края счет с нуля): ").strip())
                    if pos_toggle >= 0:
                        print()
                        print(f"Получилось число: {toggle_kth_bit(num_base, pos_toggle)} (двоичное: {bin(toggle_kth_bit(num_base, pos_toggle))[2:]})")
                    else:
                        print("Число должно быть больше нуля.")
                        continue
                else:
                    print("Число должно быть больше нуля.")
                    continue
            except (ValueError, TypeError) as e:
                print(f"Ошибка: {e}")
                continue
        else:
            print()
            print("Выбери вариант 0-4")
            continue

def show_menu():
    print("\n1 - Анализ  списка чисел")
    print("    Введёшь список - покажу  чётные числа, и их сумму, минимум, максимум, среднее  и сколько там + / - / нулей")
    print()
    print("2 - Сохранение  отчёта по  чётным числам")
    print("    Сохраняю твой  отчёт в читаемый  файл")
    print()
    print("3 - Переводчик в  двоичную систему  счисления")
    print("    Введешь число - получишь  его в двоичном  коде")
    print()
    print("4 - Битовый калькулятор")
    print("    Ты можешь тут  играться с двоичными числами:  узнать, что на определенной  позиции - определённое число (0 или 1), и поменять это")
    print()
    print("0 - Выход")


def normalize_path(path: str, fmt: str):
    path = path.strip()
    if not os.path.dirname(path):
        path = os.path.join(os.getcwd(), path)
    root, ext = os.path.splitext(path)
    fmt = fmt.strip().lower()
    if fmt == "":
        fmt = "txt"
    if fmt not in ("txt", "csv"):
        raise ValueError("Формат только txt/csv")
    need_ext = "." + fmt
    if not ext:
        path = root + need_ext
    elif ext.lower() != need_ext:
        raise ValueError("Расширение не совпадает с форматом.")
    return path, fmt


if __name__ == "__main__":
    main()
