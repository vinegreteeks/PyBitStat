import pytest
from PyBitStat import NumberAnalyzer


# --- Тесты для инициализации и get_even_numbers ---
def test_analyzer_basic():
    analyzer = NumberAnalyzer([1, 2, 3, 4])
    assert analyzer.data == [1, 2, 3, 4]
    assert analyzer.get_even_numbers() == [2, 4]


def test_analyzer_mixed_types():
    data = [1.0, 2.0, 3.5, True, "7", 10]
    analyzer = NumberAnalyzer(data)
    assert analyzer.get_even_numbers() == [2, 10]


def test_analyzer_empty():
    analyzer = NumberAnalyzer([])
    assert analyzer.get_even_numbers() == []

    analyzer_odds = NumberAnalyzer([1, 3, 5])
    assert analyzer_odds.get_even_numbers() == []


# --- Тесты для get_even_stats ---
def test_stats_normal():
    analyzer = NumberAnalyzer([1, 2, 3, 4])
    stats = analyzer.get_even_stats()
    assert stats["sum"] == 6
    assert stats["min"] == 2
    assert stats["max"] == 4
    assert stats["avg"] == 3.0


def test_stats_none():
    analyzer = NumberAnalyzer([1, 3, 5])
    assert analyzer.get_even_stats() is None


# --- Тесты для get_sign_counts ---
def test_sign_counts():
    analyzer = NumberAnalyzer([10, -5, 0, 2])
    counts = analyzer.get_sign_counts()
    assert counts["pos"] == 2  # 10, 2
    assert counts["neg"] == 1  # -5
    assert counts["zero"] == 1  # 0


def test_sign_counts_empty():
    analyzer = NumberAnalyzer([])
    assert analyzer.get_sign_counts() is None
