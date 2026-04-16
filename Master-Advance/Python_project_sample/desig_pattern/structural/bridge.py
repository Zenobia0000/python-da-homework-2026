"""
橋接 Bridge
===========
意圖：把「抽象」與「實作」分開，兩邊各自獨立演化，避免 N×M 子類爆炸。
口訣：「優先用組合，不要繼承」的具體招式。

例子：N 種形狀（圓 / 方）× M 種繪圖 API（向量 / 點陣）。
若用繼承做：VectorCircle / RasterCircle / VectorSquare / RasterSquare … 4 個。
加一種形狀就 +M 個，加一種 API 就 +N 個 → 爆炸。
Bridge 的解法：形狀 hold 一個 DrawingAPI 物件，組合而非繼承。

跑：python bridge.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# --- Implementor：實作端介面 ---------------------------------------
class DrawingAPI(ABC):
    @abstractmethod
    def draw_circle(self, x: float, y: float, r: float) -> None: ...
    @abstractmethod
    def draw_square(self, x: float, y: float, side: float) -> None: ...


class VectorAPI(DrawingAPI):
    def draw_circle(self, x: float, y: float, r: float) -> None:
        print(f"[Vector] <circle cx={x} cy={y} r={r}/>")

    def draw_square(self, x: float, y: float, side: float) -> None:
        print(f"[Vector] <rect x={x} y={y} w={side} h={side}/>")


class RasterAPI(DrawingAPI):
    def draw_circle(self, x: float, y: float, r: float) -> None:
        print(f"[Raster] 點陣畫 {int(3.14 * r * r)} 像素圓於 ({x},{y})")

    def draw_square(self, x: float, y: float, side: float) -> None:
        print(f"[Raster] 點陣畫 {int(side*side)} 像素方塊於 ({x},{y})")


# --- Abstraction：抽象端，hold 著 implementor -----------------------
class Shape(ABC):
    def __init__(self, api: DrawingAPI) -> None:
        self.api = api          # ← 橋接點

    @abstractmethod
    def draw(self) -> None: ...


class Circle(Shape):
    def __init__(self, x: float, y: float, r: float, api: DrawingAPI) -> None:
        super().__init__(api)
        self.x, self.y, self.r = x, y, r

    def draw(self) -> None:
        self.api.draw_circle(self.x, self.y, self.r)


class Square(Shape):
    def __init__(self, x: float, y: float, side: float, api: DrawingAPI) -> None:
        super().__init__(api)
        self.x, self.y, self.side = x, y, side

    def draw(self) -> None:
        self.api.draw_square(self.x, self.y, self.side)


def main() -> None:
    for api in (VectorAPI(), RasterAPI()):
        Circle(10, 20, 5, api).draw()
        Square(0, 0, 8, api).draw()


if __name__ == "__main__":
    main()
