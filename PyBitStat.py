import os


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
    analyzer = NumberAnalyzer(nums)
    evens = analyzer.get_even_numbers()
    if not evens:
        print("Чётных нет.")
        return
    else:
        print("Чётные числа:", evens)
        print("Считаю статистику...")
        stats = analyzer.get_even_stats()
        print(stats)
        sc = analyzer.get_sign_counts()
        print(
            f"Положительных: {sc['pos']}, отрицательных: {sc['neg']}, нулей: {sc['zero']}"
        )
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
        analyzer = NumberAnalyzer(nums)
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
            ok = analyzer.save_to_file(path, fmt)
        except OSError as e:
            print(f"Не сохранил: {e}")
            if e.errno == 13:
                print(r"Нет прав. Выбери другу папку (например D:\data\report.txt)")
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
            b = NumberAnalyzer.to_binary_divmod(n)
        except ValueError as e:
            print(f"Ошибка: {e}")
            continue
        print(f"Двоичное: {b}")


def run_bit_calc_mode():
    num_base = 0
    while True:
        print()
        print(
            "1 - Показать бит\n2 - Поменять бит на 1\n3 - Обнулить бит\n4 - Поменять бит на противоположный\n0 - Новое число/Выход"
        )
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
                    pos_bit = int(
                        input("Позиция(с правого края, счет с нуля): ").strip()
                    )
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
                    pos_bit = int(
                        input("Позиция(с правого края счет с нуля): ").strip()
                    )
                    if pos_bit >= 0:
                        print()
                        print(
                            f"Получилось число: {NumberAnalyzer.set_kth_bit(num_base, pos_bit)} (двоичное: {bin(NumberAnalyzer.set_kth_bit(num_base, pos_bit))[2:]})"
                        )
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
                    pos_clear = int(
                        input("позиция(с правого края счет с нуля): ").strip()
                    )
                    if pos_clear >= 0:
                        print()
                        print(
                            f"Получилось число: {NumberAnalyzer.clear_kth_bit(num_base, pos_clear)} (двоичное: {bin(NumberAnalyzer.clear_kth_bit(num_base, pos_clear))[2:]})"
                        )
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
                    pos_toggle = int(
                        input("Позиция(с правого края счет с нуля): ").strip()
                    )
                    if pos_toggle >= 0:
                        print()
                        print(
                            f"Получилось число: {NumberAnalyzer.toggle_kth_bit(num_base, pos_toggle)} (двоичное: {bin(NumberAnalyzer.toggle_kth_bit(num_base, pos_toggle))[2:]})"
                        )
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
    print(
        "    Введёшь список - покажу  чётные числа, и их сумму, минимум, максимум, среднее  и сколько там + / - / нулей"
    )
    print()
    print("2 - Сохранение  отчёта по  чётным числам")
    print("    Сохраняю твой  отчёт в читаемый  файл")
    print()
    print("3 - Переводчик в  двоичную систему  счисления")
    print("    Введешь число - получишь  его в двоичном  коде")
    print()
    print("4 - Битовый калькулятор")
    print(
        "    Ты можешь тут  играться с двоичными числами:  узнать, что на определенной  позиции - определённое число (0 или 1), и поменять это"
    )
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


class NumberAnalyzer:
    def __init__(self, data):
        """
        Конструктор. Запускается один раз при создании.
        Здесь мы сохраняем данные и валидируем их.
        """
        self.data = []
        for x in data:
            if self._is_valid_number(x):
                self.data.append(int(x))

    def _is_valid_number(self, x):
        if isinstance(x, bool):
            return False
        if not isinstance(x, (int, float)):
            return False
        if isinstance(x, float) and not x.is_integer():
            return False
        return True

    def get_even_numbers(self):
        evens = []
        for x in self.data:
            if x % 2 == 0:
                evens.append(x)
        return evens

    def get_even_stats(self):
        evens = self.get_even_numbers()
        if not evens:
            return None
        sm = sum(evens)
        mn = min(evens)
        mx = max(evens)
        num = len(evens)
        return {"sum": sm, "min": mn, "max": mx, "avg": sm / num}

    def get_sign_counts(self):
        summa = 0
        pos = 0
        neg = 0
        zero = 0
        for x in self.data:
            xi = int(x)
            if xi > 0:
                pos += 1
            elif xi < 0:
                neg += 1
            else:
                zero += 1
        summa = pos + neg + zero
        if summa == 0:
            return None
        else:
            return {"pos": pos, "neg": neg, "zero": zero}

    def save_to_file(self, path, fmt="txt"):
        stats = self.get_even_stats()
        if fmt == "txt":
            if stats is None:
                content = "Нет чётных целых чисел для анализа."
            else:
                content = f"Статистика чётных чисел:\nСумма: {stats['sum']}\nМинимум: {stats['min']}\nМаксимум: {stats['max']}\nСреднее: {stats['avg']}"

            with open(path, "w", encoding="utf-8") as f:
                f.write(content + "\n")

        elif fmt == "csv":
            header = "sum,min,max,avg\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(header)
                if stats is not None:
                    f.write(
                        f"{stats['sum']},{stats['min']},{stats['max']},{stats['avg']}\n"
                    )
        else:
            raise ValueError("Формат должен быть 'txt' или 'csv'")

        return True

    def __str__(self):
        return f"NumberAnalyzer: обработано {len(self.data)} чисел. Данные: {self.data}"

    @staticmethod
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
        return "".join(reversed(bits))

    @staticmethod
    def set_kth_bit(n, k):
        """
        Кратко: "Включает k-й бит числа n".
        Agrs: n (int, >= 0, bool не принимаем), k (int, >=0).
        Returns: int.
        Raises: TypeError(не int/bool), ValueError(n<0 или k<0)
        Notes: маска 1 << k.
        """
        NumberAnalyzer._check_non_negative_int("n", n)
        NumberAnalyzer._check_non_negative_int("k", k)
        return n | (1 << k)

    @staticmethod
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
        NumberAnalyzer._check_non_negative_int("n", n)
        NumberAnalyzer._check_non_negative_int("k", k)
        return n ^ (1 << k)

    @staticmethod
    def clear_kth_bit(n, k):
        """
        Принимает int n>=0 и int k>=0; не-int -> TypeError; n < 0 или k < 0 -> ValueError; возвращает int: n с очищенным k-м битом.
        """
        NumberAnalyzer._check_non_negative_int("n", n)
        NumberAnalyzer._check_non_negative_int("k", k)
        return n & ~(1 << k)

    @staticmethod
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


if __name__ == "__main__":
    analyzer = NumberAnalyzer([1, 2, 3, 4, "bad"])
    print(analyzer)
    print("Чётные:", analyzer.get_even_numbers())
    print("Статистика:", analyzer.get_even_stats())
    print("знаки:", analyzer.get_sign_counts())
    main()
