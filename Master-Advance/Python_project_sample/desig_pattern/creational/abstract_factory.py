"""
抽象工廠 Abstract Factory
=========================
意圖：提供一個介面來建立「一族相關物件」，無需指定具體類別。
與 Factory Method 差異：FM 生「一個」產品；AF 生「一整套」相容產品。

例子：跨平台 UI。Windows 風格的 Button 必須配 Windows 風格的 Checkbox，
不能 Windows Button 配 macOS Checkbox（風格錯亂）。

跑：python abstract_factory.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# --- 抽象產品 --------------------------------------------------------
class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...


class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...


# --- Windows 系列 ----------------------------------------------------
class WinButton(Button):
    def render(self) -> str: return "[Win Button]  方角、灰底"


class WinCheckbox(Checkbox):
    def render(self) -> str: return "[Win Checkbox] ☑ 方框"


# --- macOS 系列 ------------------------------------------------------
class MacButton(Button):
    def render(self) -> str: return "[Mac Button]  圓角、毛玻璃"


class MacCheckbox(Checkbox):
    def render(self) -> str: return "[Mac Checkbox] ✓ 圓框"


# --- 抽象工廠 --------------------------------------------------------
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...
    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...


class WinFactory(GUIFactory):
    def create_button(self) -> Button: return WinButton()
    def create_checkbox(self) -> Checkbox: return WinCheckbox()


class MacFactory(GUIFactory):
    def create_button(self) -> Button: return MacButton()
    def create_checkbox(self) -> Checkbox: return MacCheckbox()


# --- 客戶端 ----------------------------------------------------------
class Application:
    def __init__(self, factory: GUIFactory) -> None:
        self.button = factory.create_button()
        self.checkbox = factory.create_checkbox()

    def paint(self) -> None:
        print(self.button.render())
        print(self.checkbox.render())


def detect_factory(os_name: str) -> GUIFactory:
    return WinFactory() if os_name.lower() == "windows" else MacFactory()


def main() -> None:
    for os_name in ("Windows", "macOS"):
        print(f"--- {os_name} ---")
        Application(detect_factory(os_name)).paint()


if __name__ == "__main__":
    main()
