"""
享元 Flyweight
==============
意圖：用「共享」減少海量同質物件的記憶體佔用。
關鍵分離：
  - intrinsic（內在）狀態：可共享、不變的部分 → 抽出來當 flyweight
  - extrinsic（外在）狀態：每個實例不同的部分 → 由客戶端傳入

例子：森林裡 100 萬棵樹。每棵樹 (x, y) 不同，但「松樹」「楓樹」這種樹種
      （含貼圖、模型、顏色）只有 5 種。把樹種抽成 flyweight 共享，省記憶體。

跑：python flyweight.py
"""
from __future__ import annotations

from dataclasses import dataclass


# --- Flyweight：可共享的「內在狀態」-------------------------------
@dataclass(frozen=True)
class TreeType:
    name: str
    color: str
    texture: str    # 假設這個東西很大（貼圖 bytes）

    def render(self, x: int, y: int) -> str:
        # 渲染時把外在狀態 (x, y) 傳進來
        return f"  draw {self.name}({self.color}) at ({x},{y})"


# --- Factory：負責共享 flyweight，已存在就回收用 -------------------
class TreeTypeFactory:
    _cache: dict[tuple[str, str, str], TreeType] = {}

    @classmethod
    def get(cls, name: str, color: str, texture: str) -> TreeType:
        key = (name, color, texture)
        if key not in cls._cache:
            cls._cache[key] = TreeType(name, color, texture)
            print(f"[Factory] 新建 TreeType {key}")
        return cls._cache[key]


# --- 真正的物件：只存外在狀態 + 一個 flyweight 指標 ----------------
@dataclass
class Tree:
    x: int
    y: int
    type_: TreeType

    def render(self) -> str:
        return self.type_.render(self.x, self.y)


# --- 森林 ----------------------------------------------------------
class Forest:
    def __init__(self) -> None:
        self.trees: list[Tree] = []

    def plant(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        t = TreeTypeFactory.get(name, color, texture)
        self.trees.append(Tree(x, y, t))

    def render(self) -> None:
        for t in self.trees:
            print(t.render())


def main() -> None:
    forest = Forest()
    # 種 6 棵樹，但只用到 2 種 TreeType
    for i, (name, color) in enumerate([
        ("松", "深綠"), ("松", "深綠"), ("松", "深綠"),
        ("楓", "紅"),   ("楓", "紅"),   ("松", "深綠"),
    ]):
        forest.plant(i * 10, i * 10, name, color, texture=f"{name}_BIG_TEXTURE_BYTES")

    print("\n--- 渲染 ---")
    forest.render()
    print(f"\n樹的實例數：{len(forest.trees)}, 共享的 TreeType 數：{len(TreeTypeFactory._cache)}")


if __name__ == "__main__":
    main()
