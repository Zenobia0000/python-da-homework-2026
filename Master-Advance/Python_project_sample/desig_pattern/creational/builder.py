"""
生成器 Builder
==============
意圖：把「複雜物件的建構過程」與「最終表示」分離，
      讓同樣的步驟組出不同產品。

何時用：
  - 建構子參數爆炸（5 個以上、且很多 optional）
  - 需要「先 A 再 B 再 C」的步驟順序
  - 想要 fluent API：obj.add(...).add(...).build()

例子：手刀組漢堡。麵包、肉、起司、配料、醬料一層層疊上去，
      最後 `.build()` 拿到完成品。

跑：python builder.py
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Burger:
    bun: str = ""
    patty: str = ""
    cheese: bool = False
    veggies: list[str] = field(default_factory=list)
    sauces: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        layers = [self.bun, self.patty]
        if self.cheese:
            layers.append("起司")
        layers.extend(self.veggies)
        layers.extend(self.sauces)
        return "🍔 " + " + ".join(layers)


class BurgerBuilder:
    """fluent builder：每個 step 回傳 self，可以一路 . 下去。"""

    def __init__(self) -> None:
        self._burger = Burger()

    def bun(self, kind: str) -> "BurgerBuilder":
        self._burger.bun = kind; return self

    def patty(self, kind: str) -> "BurgerBuilder":
        self._burger.patty = kind; return self

    def add_cheese(self) -> "BurgerBuilder":
        self._burger.cheese = True; return self

    def add_veggie(self, name: str) -> "BurgerBuilder":
        self._burger.veggies.append(name); return self

    def add_sauce(self, name: str) -> "BurgerBuilder":
        self._burger.sauces.append(name); return self

    def build(self) -> Burger:
        return self._burger


# --- Director：封裝常用組合，讓客戶端連 builder 細節都不用懂 ----------
class BurgerDirector:
    @staticmethod
    def big_mac(builder: BurgerBuilder) -> Burger:
        return (builder
                .bun("芝麻麵包").patty("牛肉")
                .add_cheese()
                .add_veggie("生菜").add_veggie("酸黃瓜").add_veggie("洋蔥")
                .add_sauce("特製醬").build())

    @staticmethod
    def veggie(builder: BurgerBuilder) -> Burger:
        return (builder
                .bun("全麥麵包").patty("豆排")
                .add_veggie("番茄").add_veggie("生菜")
                .add_sauce("美乃滋").build())


def main() -> None:
    print(BurgerDirector.big_mac(BurgerBuilder()))
    print(BurgerDirector.veggie(BurgerBuilder()))

    # 也可以直接用 builder 自由組
    custom = (BurgerBuilder()
              .bun("黑麥").patty("雞胸")
              .add_cheese().add_sauce("辣醬").build())
    print(custom)


if __name__ == "__main__":
    main()
