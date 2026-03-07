import os, time, logging
from dataclasses import dataclass
from functools import wraps
from typing import Callable, Any, Tuple


def time_it(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        its_time = end_time - start_time
        logging.info(f"Функция {func.__name__} выполнилась за {its_time:.6f} секунд.")
        return result

    return wrapper


def normalize_path(path: str, fmt: str) -> Tuple[str, str]:
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
