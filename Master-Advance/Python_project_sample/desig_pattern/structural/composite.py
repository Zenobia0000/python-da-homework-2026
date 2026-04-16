"""
組合 Composite
==============
意圖：把物件組成「樹狀結構」，讓客戶端對「單一物件」與「組合物件」一視同仁。
何時用：檔案系統、UI 元件樹、選單、組織架構、AST。

關鍵：Leaf 與 Composite 實作同一個介面，遞迴就會自己跑通。

例子：檔案系統。File 是葉節點，Folder 是組合節點，兩者都實作 size()。

跑：python composite.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class FsNode(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def show(self, indent: int = 0) -> None: ...


# --- Leaf 葉節點 ---------------------------------------------------
class File(FsNode):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    def size(self) -> int:
        return self._size

    def show(self, indent: int = 0) -> None:
        print(f"{' ' * indent}- {self.name} ({self._size}B)")


# --- Composite 組合節點 --------------------------------------------
class Folder(FsNode):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.children: list[FsNode] = []

    def add(self, node: FsNode) -> "Folder":
        self.children.append(node); return self

    def size(self) -> int:
        # 遞迴：對 leaf 與 composite 同樣呼叫 .size()，根本不用 isinstance 判斷
        return sum(c.size() for c in self.children)

    def show(self, indent: int = 0) -> None:
        print(f"{' ' * indent}+ {self.name}/  ({self.size()}B)")
        for c in self.children:
            c.show(indent + 2)


def main() -> None:
    root = Folder("root")
    docs = Folder("docs")
    src = Folder("src")

    docs.add(File("readme.md", 200)).add(File("license", 100))
    src.add(File("main.py", 1500)).add(File("utils.py", 800))

    root.add(docs).add(src).add(File(".gitignore", 50))

    root.show()
    print(f"\n總大小：{root.size()} bytes")


if __name__ == "__main__":
    main()
