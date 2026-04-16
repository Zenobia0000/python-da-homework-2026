"""
訪問者 Visitor
==============
意圖：對「結構穩定、操作多變」的物件群，新增操作不必改動原類別。
何時用：AST 走訪、報表 / export 引擎、編譯器各種 pass。

權衡：物件結構若會頻繁加新類，Visitor 就會很痛（每加一個元素類，
      每個 visitor 都要補方法）。所以 Visitor 適用於「結構穩、操作變」。

例子：購物車裡有書、CD、食物三種商品（結構穩）。
      要做「印發票」「算稅金」「算重量」三種操作（操作多變）→ 開三個 Visitor。

跑：python visitor.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


# --- Element 介面 -------------------------------------------------
class Item(ABC):
    @abstractmethod
    def accept(self, v: "Visitor") -> object: ...


@dataclass
class Book(Item):
    title: str
    price: int
    weight_g: int

    def accept(self, v: "Visitor") -> object: return v.visit_book(self)


@dataclass
class CD(Item):
    title: str
    price: int
    weight_g: int

    def accept(self, v: "Visitor") -> object: return v.visit_cd(self)


@dataclass
class Food(Item):
    title: str
    price: int
    weight_g: int

    def accept(self, v: "Visitor") -> object: return v.visit_food(self)


# --- Visitor 介面 -------------------------------------------------
class Visitor(ABC):
    @abstractmethod
    def visit_book(self, b: Book) -> object: ...
    @abstractmethod
    def visit_cd(self, c: CD) -> object: ...
    @abstractmethod
    def visit_food(self, f: Food) -> object: ...


class TaxVisitor(Visitor):
    """書 0%，CD 5%，食物 0%。"""
    def visit_book(self, b: Book) -> int: return 0
    def visit_cd(self, c: CD) -> int: return int(c.price * 0.05)
    def visit_food(self, f: Food) -> int: return 0


class WeightVisitor(Visitor):
    def visit_book(self, b: Book) -> int: return b.weight_g
    def visit_cd(self, c: CD) -> int: return c.weight_g
    def visit_food(self, f: Food) -> int: return f.weight_g


class InvoiceVisitor(Visitor):
    def visit_book(self, b: Book) -> str: return f"[書] {b.title} ${b.price}"
    def visit_cd(self, c: CD) -> str: return f"[CD] {c.title} ${c.price}"
    def visit_food(self, f: Food) -> str: return f"[食] {f.title} ${f.price}"


def main() -> None:
    cart: list[Item] = [
        Book("設計模式", 480, 600),
        CD("Beethoven", 350, 100),
        Food("便當", 120, 800),
    ]

    print("發票：")
    inv = InvoiceVisitor()
    for it in cart:
        print("  " + str(it.accept(inv)))

    tax = TaxVisitor()
    weight = WeightVisitor()
    total_tax = sum(it.accept(tax) for it in cart)        # type: ignore[misc]
    total_weight = sum(it.accept(weight) for it in cart)  # type: ignore[misc]
    print(f"\n總稅金: ${total_tax}")
    print(f"總重量: {total_weight}g")


if __name__ == "__main__":
    main()
