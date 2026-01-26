import pytest
from PyBitStat import even_only, even_stats, to_binary_divmod, _is_valid_number


# --- тесты для even_only ---
def test_even_only_basic():
    # простой кейс
    assert even_only([1, 2, 3, 4]) == [2, 4]


def test_even_only_mixed_types():
    # проверка фильтрации мусора
    data = [1.0, 2.0, 3.5, True, "7", 10]
    # ожидаем: 2.0 (это int 2) и 10.
    # 3.5 не целое, True - бул, "7" - строка.
    assert even_only(data) == [2, 10]


def test_even_only_empty():
    assert even_only([]) == []
    assert even_only([1, 3, 5]) == []


# --- тесты для even_stats ---
def test_even_stats_normal():
    data = [1, 2, 3, 4]
    stats = even_stats(data)
    # проверяем ключи и значения
    assert stats["sum"] == 6
    assert stats["min"] == 2
    assert stats["max"] == 4
    assert stats["avg"] == 3.0


def test_even_stats_none():
    # если четных нет, должно быть None
    assert even_stats([1, 3, 5]) is None


# --- тесты для вспомогательной функции ---
def test_is_valid_number():
    assert _is_valid_number(5) is True
    assert _is_valid_number(5.0) is True
    assert _is_valid_number(5.1) is False
    assert _is_valid_number(True) is False  # bool ломает математику
    assert _is_valid_number("5") is False
