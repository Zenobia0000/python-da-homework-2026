# 設計模式 Python 實作集

本目錄收錄 GoF 23 個經典設計模式的 Python 實作，內容對應網站
<https://zhaocchen.github.io/docs/design-pattern/decorator>（簡中 JS 版）的章節清單，
以 Python 慣用法重新撰寫，每支檔案皆可獨立執行 (`python <file>.py`)。

## 設計哲學（Linus 風格）

> "Bad programmers worry about the code. Good programmers worry about data structures."

模式不是聖經，是**詞彙表**。當你能用一句「這是 Observer」描述一段架構，
team 的溝通成本立刻下降一個數量級。但別為了用模式而用模式 —— 三行 if 永遠
比一個過度抽象的工廠方法清楚。

## 目錄結構

```
desig_pattern/
├── design_principles.py        SOLID 等基本原則速覽
├── creational/                 創建型：管理「如何生出物件」
│   ├── factory_method.py
│   ├── abstract_factory.py
│   ├── singleton.py
│   ├── builder.py
│   └── prototype.py
├── structural/                 結構型：管理「物件如何組合」
│   ├── adapter.py
│   ├── bridge.py
│   ├── composite.py
│   ├── decorator.py
│   ├── facade.py
│   ├── flyweight.py
│   └── proxy.py
└── behavioral/                 行為型：管理「物件如何互動」
    ├── chain_of_responsibility.py
    ├── command.py
    ├── iterator.py
    ├── mediator.py
    ├── memento.py
    ├── observer.py
    ├── state.py
    ├── strategy.py
    ├── template.py
    └── visitor.py
```

## 模式速查表

### 創建型 Creational（5）

| 模式 | 一句話 | 何時用 |
|---|---|---|
| Factory Method | 子類別決定要 new 哪個物件 | 同一介面、多家實作、執行期才知挑哪家 |
| Abstract Factory | 一組相關物件的家族工廠 | UI 主題、跨平台元件這類「成套」需求 |
| Singleton | 全程式只一個實例 | 設定、日誌、連線池（小心：常被濫用） |
| Builder | 一步步組裝複雜物件 | 建構子參數爆炸、需要 fluent API |
| Prototype | 用 clone 取代 new | 物件初始化貴，或需動態複製 |

### 結構型 Structural（7）

| 模式 | 一句話 | 何時用 |
|---|---|---|
| Adapter | 把舊介面包成新介面 | 整合第三方、legacy code |
| Bridge | 抽象與實作分離，各自獨立演化 | 「N 種形狀 × M 種顏色」想避免 N×M 爆炸 |
| Composite | 樹狀結構，葉子與容器同介面 | 檔案系統、選單、組織架構 |
| Decorator | 動態套上額外責任，不改原類 | 加 logging、加快取、加授權 |
| Facade | 一個門面屏蔽子系統複雜度 | API gateway、SDK 簡化層 |
| Flyweight | 共享相同狀態節省記憶體 | 棋盤格子、字型 glyph、海量同質物件 |
| Proxy | 占位物件，控制存取真實物件 | 延遲載入、權限檢查、遠端代理 |

### 行為型 Behavioral（10）

| 模式 | 一句話 | 何時用 |
|---|---|---|
| Chain of Responsibility | 請求沿著鏈傳，誰能處理誰處理 | middleware、log handler、審批流程 |
| Command | 把「動作」包成物件 | undo/redo、佇列、巨集 |
| Iterator | 統一走訪集合的方式 | Python 內建 `__iter__`、generator |
| Mediator | 中介者集中管多對多互動 | 聊天室、UI 元件協調 |
| Memento | 快照物件狀態，可回復 | undo、checkpoint、存檔 |
| Observer | 一對多訂閱 / 通知 | 事件系統、MVC、reactive |
| State | 狀態切換對應行為切換 | 訂單狀態機、TCP 連線 |
| Strategy | 演算法可抽換 | 排序、付款方式、壓縮演算法 |
| Template Method | 骨架在父類，細節留子類 | 框架 lifecycle hook |
| Visitor | 對固定結構新增操作 | AST 走訪、報表產生 |

## 快速使用

```bash
# 跑某個模式的 demo
python creational/singleton.py
python structural/decorator.py
python behavioral/observer.py
```

每支檔案結尾都有 `if __name__ == "__main__":` 區塊，
直接執行即可看到示範輸出。

## 學習路徑建議

1. 先讀 `design_principles.py`（SOLID）建立判斷標準
2. 從**最常用的 5 個**開始：Strategy → Observer → Decorator → Factory Method → Singleton
3. 行有餘力再補完整 23 個

> "If you need more than 3 levels of indentation, you're screwed anyway, and should fix your program."
> — Linus
