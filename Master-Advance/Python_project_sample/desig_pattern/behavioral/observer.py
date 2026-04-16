"""
觀察者 Observer
===============
意圖：定義一對多的依賴關係，當主題狀態改變，所有訂閱者自動收到通知。
何時用：事件系統、MVC、reactive、訊息廣播。

例子：股價推送。多個 client 訂閱同一支股票，價格一變動就通知。

跑：python observer.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, symbol: str, price: float) -> None: ...


class Subject:
    def __init__(self) -> None:
        self._subs: list[Observer] = []

    def attach(self, o: Observer) -> None: self._subs.append(o)
    def detach(self, o: Observer) -> None: self._subs.remove(o)

    def notify(self, *args: object, **kwargs: object) -> None:
        for o in self._subs:
            o.update(*args, **kwargs)   # type: ignore[arg-type]


class Stock(Subject):
    def __init__(self, symbol: str, price: float) -> None:
        super().__init__()
        self.symbol = symbol
        self._price = price

    @property
    def price(self) -> float: return self._price

    @price.setter
    def price(self, p: float) -> None:
        # 價格沒變就不通知 → 避免 spam
        if p != self._price:
            self._price = p
            self.notify(self.symbol, p)


# --- 各種訂閱者 -----------------------------------------------------
class PhoneApp(Observer):
    def __init__(self, user: str) -> None: self.user = user

    def update(self, symbol: str, price: float) -> None:
        print(f"  📱 {self.user} APP 推播：{symbol} 現價 {price}")


class TradingBot(Observer):
    def update(self, symbol: str, price: float) -> None:
        action = "BUY" if price < 100 else "HOLD"
        print(f"  🤖 Bot 看到 {symbol}={price} → {action}")


def main() -> None:
    aapl = Stock("AAPL", 150.0)
    aapl.attach(PhoneApp("Alice"))
    aapl.attach(PhoneApp("Bob"))
    aapl.attach(TradingBot())

    aapl.price = 152.5
    aapl.price = 152.5     # 同價不通知
    aapl.price = 95.0


if __name__ == "__main__":
    main()
