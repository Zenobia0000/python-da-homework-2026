"""
設計原則 Design Principles
==========================
SOLID + 其他常被引用的原則。設計模式是這些原則的「具體招式」，
原則才是內功。先理解原則，再決定要不要套模式。

跑：python design_principles.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol


# ----------------------------------------------------------------------
# S - Single Responsibility Principle 單一職責
# ----------------------------------------------------------------------
# 一個類別只該有一個改變的理由。
# 反例：User 同時管「資料」+「資料庫存取」+「Email 通知」→ 三件事改任何一件都要動它。
class UserBad:
    def __init__(self, name: str, email: str) -> None:
        self.name, self.email = name, email

    def save_to_db(self) -> None: ...        # 違反 SRP
    def send_welcome_email(self) -> None: ...  # 違反 SRP


# 正解：拆成 model / repository / mailer 三件事
class User:
    def __init__(self, name: str, email: str) -> None:
        self.name, self.email = name, email


class UserRepository:
    def save(self, user: User) -> None:
        print(f"[DB] saved {user.name}")


class WelcomeMailer:
    def send(self, user: User) -> None:
        print(f"[Mail] welcome {user.email}")


# ----------------------------------------------------------------------
# O - Open/Closed Principle 開放擴充、封閉修改
# ----------------------------------------------------------------------
# 加新功能應該「加新類」，而不是「改舊類」。
class Discount(ABC):
    @abstractmethod
    def apply(self, price: float) -> float: ...


class NoDiscount(Discount):
    def apply(self, price: float) -> float: return price


class PercentOff(Discount):
    def __init__(self, pct: float) -> None: self.pct = pct
    def apply(self, price: float) -> float: return price * (1 - self.pct)


# 想加 BlackFridayDiscount？新增子類即可，無需動既有程式碼。


# ----------------------------------------------------------------------
# L - Liskov Substitution Principle 里氏替換
# ----------------------------------------------------------------------
# 子類別必須能無痛取代父類別。經典反例：Square 繼承 Rectangle 卻把 setWidth 偷改 height。
class Bird:
    def fly(self) -> str: return "flying"


# 反例：Penguin 繼承 Bird 卻不能 fly → 違反 LSP
# 正解：把「會飛」抽成獨立能力（Interface Segregation 也適用）
class FlyingBird(Bird): ...
class Penguin:
    def swim(self) -> str: return "swimming"


# ----------------------------------------------------------------------
# I - Interface Segregation Principle 介面隔離
# ----------------------------------------------------------------------
# 用戶不該被強迫依賴它用不到的方法。寧可多個小介面，不要一個肥介面。
class Printer(Protocol):
    def print_doc(self, doc: str) -> None: ...


class Scanner(Protocol):
    def scan(self) -> str: ...


class SimplePrinter:
    def print_doc(self, doc: str) -> None: print(f"print: {doc}")
    # 不需要實作 scan，因為它根本不該被強迫實作


# ----------------------------------------------------------------------
# D - Dependency Inversion Principle 依賴反轉
# ----------------------------------------------------------------------
# 高階模組不該依賴低階模組，兩者都該依賴抽象。
class Logger(Protocol):
    def log(self, msg: str) -> None: ...


class ConsoleLogger:
    def log(self, msg: str) -> None: print(f"[console] {msg}")


class FileLogger:
    def log(self, msg: str) -> None: print(f"[file] {msg}")


class OrderService:
    # 依賴抽象（Protocol），不依賴具體實作 → 換 logger 不需動 OrderService
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def place(self, item: str) -> None:
        self.logger.log(f"order placed: {item}")


# ----------------------------------------------------------------------
# 其他常被引用的原則
# ----------------------------------------------------------------------
# DRY  - Don't Repeat Yourself     重複是萬惡之源
# KISS - Keep It Simple, Stupid    簡單到笨也能懂
# YAGNI- You Aren't Gonna Need It  別為假想需求寫程式
# LoD  - Law of Demeter            只跟直接朋友說話 (a.b.c.d.e 是壞味道)
# Composition over Inheritance     優先用組合而非繼承


def main() -> None:
    user = User("Alice", "alice@example.com")
    UserRepository().save(user)
    WelcomeMailer().send(user)

    print(f"原價 100, 8 折後: {PercentOff(0.2).apply(100)}")

    OrderService(ConsoleLogger()).place("MacBook")
    OrderService(FileLogger()).place("iPad")


if __name__ == "__main__":
    main()
