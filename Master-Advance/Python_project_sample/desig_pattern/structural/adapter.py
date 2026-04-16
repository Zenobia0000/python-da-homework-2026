"""
適配器 Adapter
==============
意圖：把一個類別的介面轉成客戶端期望的另一個介面，
      讓原本「介面不相容」的東西能合作。
何時用：整合第三方 SDK、包 legacy code、轉換資料格式。

例子：app 統一吃 JSON，但供應商 B 只給 XML，做個 Adapter 把 XML 轉 JSON。

跑：python adapter.py
"""
from __future__ import annotations

import json
from typing import Protocol


# --- 客戶端期望的介面 ----------------------------------------------
class JsonProvider(Protocol):
    def get_json(self) -> str: ...


# --- 既有可直接用的實作 --------------------------------------------
class ModernApi:
    def get_json(self) -> str:
        return json.dumps({"src": "modern", "users": ["a", "b"]})


# --- 不相容的 legacy 元件 ------------------------------------------
class LegacyXmlApi:
    """只會吐 XML 字串，動不了。"""

    def get_xml(self) -> str:
        return "<root><src>legacy</src><users><u>x</u><u>y</u></users></root>"


# --- Adapter：把 XML API 包成符合 JsonProvider 介面 ------------------
class XmlToJsonAdapter:
    def __init__(self, legacy: LegacyXmlApi) -> None:
        self._legacy = legacy

    def get_json(self) -> str:
        # 真實情境會用 xml.etree 解析，這裡簡化示範
        xml = self._legacy.get_xml()
        return json.dumps({"src": "legacy", "raw_xml_len": len(xml)})


# --- 客戶端：只認 JsonProvider 介面，不在乎背後是 modern 還是 legacy ---
def report(provider: JsonProvider) -> None:
    print(provider.get_json())


def main() -> None:
    report(ModernApi())
    report(XmlToJsonAdapter(LegacyXmlApi()))


if __name__ == "__main__":
    main()
