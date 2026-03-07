import logging
from typing import List, Dict, Optional, Union, Sequence, Any
from dataclasses import dataclass
from utils import time_it


@dataclass
class EvenStats:
    sum: int
    min: int
    max: int
    avg: float


class NumberAnalyzer:
    def __init__(self, data: Sequence[Union[int, float, str, bool]]) -> None:
        """
        Конструктор. Запускается один раз при создании.
        Здесь мы сохраняем данные и валидируем их.
        """
        self.data = []
        for x in data:
            if self._is_valid_number(x):
                self.data.append(int(x))
        self.data.sort()
        logging.info(f"Инициализация NumberAnalyzer: загружено {len(self.data)} чисел.")

    @time_it
    def find_number(self, target: int) -> int:
        left = 0
        right = len(self.data) - 1
        while left <= right:
            mid = (left + right) // 2
            current = self.data[mid]
            if current == target:
                return mid
            elif current < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1

    def _is_valid_number(self, x: Union[int, float, str, bool]) -> bool:
        if isinstance(x, bool):
            return False
        if not isinstance(x, (int, float)):
            return False
        if isinstance(x, float) and not x.is_integer():
            return False
        return True

    def get_even_numbers(self) -> List[int]:
        evens = []
        for x in self.data:
            if x % 2 == 0:
                evens.append(x)
        return evens

    def get_even_stats(self) -> Optional[EvenStats]:
        evens = self.get_even_numbers()
        if not evens:
            return None
        sm = sum(evens)
        mn = min(evens)
        mx = max(evens)
        avg_val = sm / len(evens)
        return EvenStats(sum=sm, min=mn, max=mx, avg=avg_val)

    def get_sign_counts(self) -> Optional[Dict[str, int]]:
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

    def save_to_file(self, path: str, fmt: str = "txt") -> bool:
        stats = self.get_even_stats()
        if fmt == "txt":
            if stats is None:
                content = "Нет чётных целых чисел для анализа."
            else:
                content = f"Статистика чётных чисел:\nСумма: {stats.sum}\nМинимум: {stats.min}\nМаксимум: {stats.max}\nСреднее: {stats.avg}"

            with open(path, "w", encoding="utf-8") as f:
                f.write(content + "\n")

        elif fmt == "csv":
            header = "sum,min,max,avg\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(header)
                if stats is not None:
                    f.write(f"{stats.sum},{stats.min},{stats.max},{stats.avg}\n")
        else:
            raise ValueError("Формат должен быть 'txt' или 'csv'")

        return True

    def __str__(self) -> str:
        return f"NumberAnalyzer: обработано {len(self.data)} чисел. Данные: {self.data}"

    @staticmethod
    def to_binary_divmod(n: int) -> str:
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
    def set_kth_bit(n: int, k: int) -> int:
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
    def toggle_kth_bit(n: int, k: int) -> int:
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
    def clear_kth_bit(n: int, k: int) -> int:
        """
        Принимает int n>=0 и int k>=0; не-int -> TypeError; n < 0 или k < 0 -> ValueError; возвращает int: n с очищенным k-м битом.
        """
        NumberAnalyzer._check_non_negative_int("n", n)
        NumberAnalyzer._check_non_negative_int("k", k)
        return n & ~(1 << k)

    @staticmethod
    def _check_non_negative_int(name: str, value: Any) -> None:
        """
        Внутренняя функция-проверка: name(str), value - должен быть int >= 0.
        TypeError - если не int;
        ValueError - если < 0.
        """
        if type(value) is not int:
            raise TypeError(f"{name} must be int")
        if value < 0:
            raise ValueError(f"{name} must be a non-negative integer")

    @staticmethod
    def get_factorial(n: int) -> int:
        NumberAnalyzer._check_non_negative_int("n", n)
        if n == 0 or n == 1:
            return 1
        return n * NumberAnalyzer.get_factorial(n - 1)
