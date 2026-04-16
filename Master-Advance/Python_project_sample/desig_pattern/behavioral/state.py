"""
狀態 State
==========
意圖：讓物件在內部狀態改變時，看起來像「換了類別」。
口訣：消滅 if state == 'A' / elif state == 'B' / … 的長條件鏈。

何時用：訂單狀態機、TCP 連線、文件審核流程、遊戲角色狀態。

例子：訂單。建立 → 已付款 → 已出貨 → 已完成。
不同狀態下，pay() / ship() / cancel() 行為都不同。

跑：python state.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class OrderState(ABC):
    name: str

    @abstractmethod
    def pay(self, order: "Order") -> None: ...
    @abstractmethod
    def ship(self, order: "Order") -> None: ...
    @abstractmethod
    def cancel(self, order: "Order") -> None: ...


class Created(OrderState):
    name = "Created"
    def pay(self, order: "Order") -> None:
        print("  付款成功"); order.set_state(Paid())
    def ship(self, order: "Order") -> None: print("  尚未付款，不能出貨")
    def cancel(self, order: "Order") -> None:
        print("  取消訂單"); order.set_state(Cancelled())


class Paid(OrderState):
    name = "Paid"
    def pay(self, order: "Order") -> None: print("  已付款，請勿重複")
    def ship(self, order: "Order") -> None:
        print("  出貨"); order.set_state(Shipped())
    def cancel(self, order: "Order") -> None:
        print("  退款並取消"); order.set_state(Cancelled())


class Shipped(OrderState):
    name = "Shipped"
    def pay(self, order: "Order") -> None: print("  已付款")
    def ship(self, order: "Order") -> None: print("  已出貨")
    def cancel(self, order: "Order") -> None: print("  已出貨無法取消，請走退貨流程")


class Cancelled(OrderState):
    name = "Cancelled"
    def pay(self, order: "Order") -> None: print("  訂單已取消")
    def ship(self, order: "Order") -> None: print("  訂單已取消")
    def cancel(self, order: "Order") -> None: print("  訂單已取消")


class Order:
    def __init__(self) -> None:
        self._state: OrderState = Created()

    def set_state(self, s: OrderState) -> None:
        print(f"  [狀態] {self._state.name} → {s.name}")
        self._state = s

    # 客戶端只看到單純三個動作，看不到 if/elif
    def pay(self) -> None: self._state.pay(self)
    def ship(self) -> None: self._state.ship(self)
    def cancel(self) -> None: self._state.cancel(self)


def main() -> None:
    o = Order()
    o.ship()    # 失敗：還沒付款
    o.pay()
    o.pay()     # 失敗：重複付款
    o.ship()
    o.cancel()  # 失敗：已出貨

    print("\n--- 另一條路徑 ---")
    o2 = Order()
    o2.pay()
    o2.cancel()


if __name__ == "__main__":
    main()
