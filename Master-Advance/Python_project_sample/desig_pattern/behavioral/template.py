"""
模板方法 Template Method
========================
意圖：在父類別定義演算法的「骨架」，把可變步驟留給子類別 override。
口訣：「Hollywood Principle - Don't call us, we'll call you」。
       父類別呼叫子類別的鉤子，反過來則不行。

何時用：框架的 lifecycle hook、Web framework 的 middleware、報表流程、ETL。

例子：資料匯出流程：抓資料 → 轉格式 → 寫檔。
      JSON / CSV 匯出器只需 override 「轉格式」這步。

跑：python template.py
"""
from __future__ import annotations

import json
from abc import ABC, abstractmethod


class DataExporter(ABC):
    """演算法骨架由父類別固定。"""

    def export(self, path: str) -> None:
        # ---- 模板方法：步驟順序固定 ----
        rows = self.fetch()
        text = self.format(rows)
        self.write(text, path)
        self.on_done(path)        # 可選的 hook，預設什麼都不做

    # 必須由子類別實作的步驟
    @abstractmethod
    def fetch(self) -> list[dict[str, object]]: ...
    @abstractmethod
    def format(self, rows: list[dict[str, object]]) -> str: ...

    # 共用步驟，子類別通常不用動
    def write(self, text: str, path: str) -> None:
        print(f"  [Write] → {path}\n{text}")

    # Hook：預設空實作，子類別想要可以 override
    def on_done(self, path: str) -> None:
        return None


class JsonExporter(DataExporter):
    def fetch(self) -> list[dict[str, object]]:
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def format(self, rows: list[dict[str, object]]) -> str:
        return json.dumps(rows, ensure_ascii=False, indent=2)


class CsvExporter(DataExporter):
    def fetch(self) -> list[dict[str, object]]:
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

    def format(self, rows: list[dict[str, object]]) -> str:
        if not rows:
            return ""
        headers = list(rows[0].keys())
        lines = [",".join(headers)]
        lines.extend(",".join(str(r[h]) for h in headers) for r in rows)
        return "\n".join(lines)

    def on_done(self, path: str) -> None:
        # 用一下 hook
        print(f"  [Hook] CSV 匯出完成，通知資料分析組去拉 {path}")


def main() -> None:
    print("--- JSON ---")
    JsonExporter().export("/tmp/users.json")
    print("\n--- CSV ---")
    CsvExporter().export("/tmp/users.csv")


if __name__ == "__main__":
    main()
