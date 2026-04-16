"""
工廠方法 Factory Method
=======================
意圖：定義一個建立物件的介面，但讓「子類別」決定要實例化哪個類別。
解決：new 關鍵字讓呼叫端綁死具體類別 → 換實作就要改一堆地方。

例子：物流公司，陸運用 Truck，海運用 Ship，未來可能加 Drone。
呼叫端只跟 `Logistics.plan_delivery()` 對話，不在乎裡面 new 出哪個交通工具。

跑：python factory_method.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# --- Product 介面 ----------------------------------------------------
class Transport(ABC):
    @abstractmethod
    def deliver(self, cargo: str) -> str: ...


class Truck(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Truck 由陸路運送 {cargo}"


class Ship(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Ship 由海路運送 {cargo}"


class Drone(Transport):
    def deliver(self, cargo: str) -> str:
        return f"Drone 由空中運送 {cargo}"


# --- Creator 工廠 ----------------------------------------------------
class Logistics(ABC):
    """父類定義骨架，子類決定具體 transport。"""

    @abstractmethod
    def create_transport(self) -> Transport: ...

    def plan_delivery(self, cargo: str) -> str:
        # 注意：plan_delivery 完全不知道是 Truck / Ship / Drone
        transport = self.create_transport()
        return f"[Plan] {transport.deliver(cargo)}"


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport: return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport: return Ship()


class AirLogistics(Logistics):
    def create_transport(self) -> Transport: return Drone()


def main() -> None:
    for company in (RoadLogistics(), SeaLogistics(), AirLogistics()):
        print(company.plan_delivery("100 箱晶片"))


if __name__ == "__main__":
    main()
