"""
迭代器 Iterator
===============
意圖：提供統一的方式走訪集合，不暴露內部結構。
Python 已內建：__iter__ / __next__ / generator，本檔示範三種寫法。

例子：自訂一個「樹的深度優先走訪器」。

跑：python iterator.py
"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field


@dataclass
class TreeNode:
    value: int
    children: list["TreeNode"] = field(default_factory=list)


# --- 寫法 1：實作 __iter__ + __next__（古典 GoF） ------------------
class DfsIterator:
    def __init__(self, root: TreeNode) -> None:
        self._stack: list[TreeNode] = [root]

    def __iter__(self) -> "DfsIterator": return self

    def __next__(self) -> int:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        # 反向放，才能維持「左到右」的 DFS 順序
        self._stack.extend(reversed(node.children))
        return node.value


# --- 寫法 2：用 generator（最 Pythonic）---------------------------
def dfs(node: TreeNode) -> Iterator[int]:
    yield node.value
    for c in node.children:
        yield from dfs(c)


# --- 寫法 3：把 __iter__ 直接寫成 generator -----------------------
class Tree:
    def __init__(self, root: TreeNode) -> None:
        self.root = root

    def __iter__(self) -> Iterator[int]:
        yield from dfs(self.root)


def main() -> None:
    root = TreeNode(1, [
        TreeNode(2, [TreeNode(4), TreeNode(5)]),
        TreeNode(3, [TreeNode(6)]),
    ])

    print("古典迭代器:", list(DfsIterator(root)))
    print("generator: ", list(dfs(root)))
    print("Tree.__iter__:", list(Tree(root)))


if __name__ == "__main__":
    main()
