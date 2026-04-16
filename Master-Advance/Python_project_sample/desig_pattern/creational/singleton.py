"""
單例 Singleton
==============
意圖：保證一個類別「只有一個實例」，並提供全域存取點。
警告：Singleton 是被濫用最嚴重的模式。本質上是 OOP 包裝過的全域變數，
      會傷害可測性。只在「真的只該有一個」時才用：設定中心、連線池、log。

Python 提供至少四種寫法，這裡列三個常見的：metaclass / __new__ / module-level。

跑：python singleton.py
"""
from __future__ import annotations

import threading
from typing import Any


# --- 寫法 1：metaclass（最乾淨，也最容易被反射打破） ------------------
class _SingletonMeta(type):
    _instances: dict[type, Any] = {}
    _lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:                      # 雙重檢查鎖，多執行緒安全
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AppConfig(metaclass=_SingletonMeta):
    def __init__(self) -> None:
        self.db_url = "postgres://localhost/app"
        self.debug = False


# --- 寫法 2：override __new__（最白話） -------------------------------
class Logger:
    _instance: "Logger | None" = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.lines = []         # type: ignore[attr-defined]
        return cls._instance

    def log(self, msg: str) -> None:
        self.lines.append(msg)               # type: ignore[attr-defined]
        print(f"[LOG] {msg}")


# --- 寫法 3：module-level（最 Pythonic） ------------------------------
# 直接 `import config` 拿到的 module 本身就是天然單例。
# 這裡用一個簡單物件示範：
class _Settings:
    def __init__(self) -> None:
        self.theme = "dark"


settings = _Settings()                       # 全 module 共用


def main() -> None:
    a, b = AppConfig(), AppConfig()
    print(f"AppConfig 同一實例? {a is b}    db_url={a.db_url}")

    log1, log2 = Logger(), Logger()
    log1.log("hello"); log2.log("world")
    print(f"Logger 同一實例? {log1 is log2}    lines={log1.lines}")

    print(f"settings.theme = {settings.theme}")


if __name__ == "__main__":
    main()
