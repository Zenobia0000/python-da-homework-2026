"""
備忘錄 Memento
==============
意圖：在「不破壞封裝」的前提下，捕捉物件內部狀態並可日後回復。
何時用：undo / 存檔點 / 編輯器歷史 / 遊戲存檔。

三個角色：
  - Originator 真正的物件（會產生 memento）
  - Memento    狀態快照（不可變、外界不該偷看內容）
  - Caretaker  保管 memento，但不解析它

例子：簡易繪圖板，可以隨時 save / undo / load。

跑：python memento.py
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CanvasMemento:
    # 對外是黑盒；只有 Canvas 自己會去讀 _state
    _state: tuple[tuple[int, int, str], ...]


class Canvas:
    def __init__(self) -> None:
        self._strokes: list[tuple[int, int, str]] = []

    def draw(self, x: int, y: int, color: str) -> None:
        self._strokes.append((x, y, color))

    def show(self) -> None:
        print(f"  畫布: {self._strokes}")

    # --- memento 介面 ---
    def save(self) -> CanvasMemento:
        return CanvasMemento(tuple(self._strokes))

    def restore(self, m: CanvasMemento) -> None:
        self._strokes = list(m._state)


class History:
    def __init__(self) -> None:
        self._stack: list[CanvasMemento] = []

    def push(self, m: CanvasMemento) -> None:
        self._stack.append(m)

    def pop(self) -> CanvasMemento | None:
        return self._stack.pop() if self._stack else None


def main() -> None:
    canvas = Canvas()
    history = History()

    canvas.draw(1, 1, "red"); history.push(canvas.save())
    canvas.draw(2, 2, "blue"); history.push(canvas.save())
    canvas.draw(3, 3, "green")
    canvas.show()

    print("undo")
    snap = history.pop()
    if snap: canvas.restore(snap)
    canvas.show()

    print("undo again")
    snap = history.pop()
    if snap: canvas.restore(snap)
    canvas.show()


if __name__ == "__main__":
    main()
