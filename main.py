from analyzer import NumberAnalyzer
from utils import normalize_path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def main() -> None:
    while True:
        show_menu()
        choice = input("\nВыбери пункт меню (0-6): ").strip()
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
        elif choice == "5":
            run_binary_search_mode()
        elif choice == "6":
            run_recursion_mode()


def run_list_analysis_mode() -> None:
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
        if sc:
            print(
                f"Положительных: {sc['pos']}, отрицательных: {sc['neg']}, нулей: {sc['zero']}"
            )
        else:
            print("Знаков нет (список пуст).")
    print("\nВозвращаюсь в главное меню...")
    print()


def run_save_report_mode() -> None:
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
            logging.warning(f"Некорретный ввод пользователя: {raw}")
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
            logging.error(f"Ошибка записи файла {path}: {e}")
            if e.errno == 13:
                print(r"Нет прав. Выбери другу папку (например D:\data\report.txt)")
            else:
                print(f"Ошибка записи: {e}")
            continue
        if ok:
            print("Сохранил.")
            logging.info(f"Файл успещно сохранён: {path}")
            break
        else:
            print("Не сохранил.")
            continue
    print("Возвращаюсь в главное меню...")
    return


def run_to_binary_mode() -> None:
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


def run_bit_calc_mode() -> None:
    num_base = 0
    while True:
        print()
        print(
            "0 - Новое число/Выход\n1 - Показать бит\n2 - Поменять бит на 1\n3 - Обнулить бит\n4 - Поменять бит на противоположный"
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


def show_menu() -> None:
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
    print("5 - Бинарный поиск")
    print()
    print("6 - Рекурсия")
    print()
    print("0 - Выход")


def run_recursion_mode() -> None:
    print("Режим: Рекурсия")
    while True:
        raw = input("Введи число (0 - выход): ").strip()
        if raw == "0":
            print("Выход в главное меню...")
            return
        elif raw:
            try:
                num_fact = int(raw)
            except (ValueError, TypeError) as e:
                print(e)
                continue
            try:
                result = NumberAnalyzer.get_factorial(num_fact)
                print(f"Факториал: {result}")
            except RecursionError:
                print("Ошибка: Слишком большое число для рекурсии (Stack Overflow).")
            except ValueError as e:
                print(f"Ошибка: {e}")
        else:
            continue


def run_binary_search_mode() -> None:
    print("\nРежим: Бинарный поиск")
    raw = input("Введите список чисел через пробел: ").strip()
    try:
        nums = [int(x) for x in raw.split()]
    except ValueError:
        print("Ошибка ввода")
        return
    analyzer = NumberAnalyzer(nums)
    print(f"Список отсортирован: {analyzer.data}")

    target_raw = input("Какое число ищем? ").strip()
    try:
        target = int(target_raw)
    except ValueError:
        return

    idx = analyzer.find_number(target)

    if idx != -1:
        print(f"Найдено! Индекс в отсортированном списке: {idx}")
    else:
        print("Число не найдено.")


if __name__ == "__main__":
    analyzer = NumberAnalyzer([1, 2, 3, 4, "bad"])
    print(analyzer)
    print("Чётные:", analyzer.get_even_numbers())
    print("Статистика:", analyzer.get_even_stats())
    print("знаки:", analyzer.get_sign_counts())
    main()
