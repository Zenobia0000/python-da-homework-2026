"""
裝飾 Decorator
==============
意圖：動態地給物件「加責任」，不修改原類別也不靠繼承。
口訣：包一層 → 行為加一個。可以無限疊。

對應原網站例子：Car 加上 autopilot；本檔還示範 Python 原生 @decorator 語法。

何時用：加 logging、加快取、加授權、加重試…又不想動原本的類。

跑：python decorator.py
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable


# ====================================================================
# 第一種：物件導向版（GoF 古典做法）
# ====================================================================
class Car(ABC):
    @abstractmethod
    def description(self) -> str: ...
    @abstractmethod
    def cost(self) -> int: ...


class BasicCar(Car):
    def description(self) -> str: return "基本款轎車"
    def cost(self) -> int: return 500_000


class CarDecorator(Car):
    """Decorator 自己也是 Car，內部包一台 Car。"""

    def __init__(self, car: Car) -> None:
        self._car = car

    def description(self) -> str: return self._car.description()
    def cost(self) -> int: return self._car.cost()


class WithAutopilot(CarDecorator):
    def description(self) -> str: return self._car.description() + " + 自動駕駛"
    def cost(self) -> int: return self._car.cost() + 200_000


class WithSunroof(CarDecorator):
    def description(self) -> str: return self._car.description() + " + 全景天窗"
    def cost(self) -> int: return self._car.cost() + 80_000


class WithSportPackage(CarDecorator):
    def description(self) -> str: return self._car.description() + " + 運動套件"
    def cost(self) -> int: return self._car.cost() + 120_000


# ====================================================================
# 第二種：Python 原生函式裝飾器（最常見、最 Pythonic）
# ====================================================================
def timing(func: Callable[..., Any]) -> Callable[..., Any]:
    """量測函式執行時間。"""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"[timing] {func.__name__} 花了 {elapsed:.2f}ms")
        return result

    return wrapper


def with_log(tag: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """帶參數的裝飾器：印 tag。"""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"[{tag}] enter {func.__name__}")
            ret = func(*args, **kwargs)
            print(f"[{tag}] exit  {func.__name__}")
            return ret

        return wrapper

    return decorator


@timing
@with_log("audit")
def heavy_calc(n: int) -> int:
    return sum(i * i for i in range(n))


def main() -> None:
    print("--- OO 版 Decorator ---")
    car: Car = BasicCar()
    car = WithAutopilot(car)
    car = WithSunroof(car)
    car = WithSportPackage(car)
    print(f"{car.description()}")
    print(f"總價：{car.cost():,} 元")

    print("\n--- 函式裝飾器版 ---")
    heavy_calc(100_000)


if __name__ == "__main__":
    main()
