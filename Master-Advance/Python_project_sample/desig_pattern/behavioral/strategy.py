"""
策略 Strategy
=============
意圖：把「演算法」抽出來變成可抽換的物件，
      讓客戶端在執行期決定用哪一個。
口訣：又一個消滅 if/elif 巨型分支的招式。

何時用：排序、付款方式、壓縮、運費計算、折扣方案。

例子：電商結帳，支援信用卡 / Apple Pay / 街口支付。

Python tip: 因為函式是一等公民，策略其實常常直接傳函式就好，
            不一定要包成類。本檔示範兩種寫法。

跑：python strategy.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


# ====================================================================
# 寫法 1：OO 版
# ====================================================================
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: int) -> None: ...


class CreditCard(PaymentStrategy):
    def __init__(self, number: str) -> None: self.number = number
    def pay(self, amount: int) -> None:
        print(f"  💳 信用卡 {self.number[-4:]} 扣款 {amount}")


class ApplePay(PaymentStrategy):
    def pay(self, amount: int) -> None:
        print(f"  🍎 Apple Pay 扣款 {amount}")


class JKoPay(PaymentStrategy):
    def pay(self, amount: int) -> None:
        print(f"  🟢 街口支付 扣款 {amount}")


class Cart:
    def __init__(self) -> None:
        self._items: list[tuple[str, int]] = []

    def add(self, name: str, price: int) -> "Cart":
        self._items.append((name, price)); return self

    def total(self) -> int:
        return sum(p for _, p in self._items)

    def checkout(self, strategy: PaymentStrategy) -> None:
        amount = self.total()
        print(f"[Cart] 應付 {amount}")
        strategy.pay(amount)


# ====================================================================
# 寫法 2：Pythonic 版（直接傳函式）
# ====================================================================
ShippingFee = Callable[[int], int]

flat_fee: ShippingFee = lambda weight: 80
weight_based: ShippingFee = lambda weight: max(60, weight * 5)
free_over_1kg: ShippingFee = lambda weight: 0 if weight >= 1000 else 100


def calc_shipping(weight_grams: int, strategy: ShippingFee) -> int:
    return strategy(weight_grams)


def main() -> None:
    cart = Cart().add("AirPods", 5990).add("線材", 290)
    cart.checkout(CreditCard("1234567812341234"))
    cart.checkout(ApplePay())
    cart.checkout(JKoPay())

    print("\n--- 函式版策略 ---")
    for w in (300, 800, 1500):
        print(f"  {w}g  flat={calc_shipping(w, flat_fee)} "
              f"weight_based={calc_shipping(w, weight_based)} "
              f"free_over_1kg={calc_shipping(w, free_over_1kg)}")


if __name__ == "__main__":
    main()
