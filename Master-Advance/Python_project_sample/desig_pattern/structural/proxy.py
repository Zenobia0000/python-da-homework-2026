"""
代理 Proxy
==========
意圖：用一個替身控制對真實物件的存取。常見三種變體：
  1. Virtual Proxy   - 延遲建立貴的物件
  2. Protection Proxy- 權限控管
  3. Remote Proxy    - 遠端物件的本地代理 (gRPC stub 就是)

與 Decorator 的差別：
  Decorator 是「加功能」；Proxy 是「控制存取」。
  結構幾乎一樣，意圖不同。

例子：高解析圖片延遲載入（Virtual） + 文件權限檢查（Protection）。

跑：python proxy.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# ====================================================================
# Virtual Proxy：載入很慢的圖片
# ====================================================================
class Image(ABC):
    @abstractmethod
    def display(self) -> None: ...


class RealImage(Image):
    def __init__(self, path: str) -> None:
        self.path = path
        self._load_from_disk()      # 假裝這步要 2 秒

    def _load_from_disk(self) -> None:
        print(f"  [RealImage] 從硬碟讀 {self.path} … (慢)")

    def display(self) -> None:
        print(f"  [RealImage] display {self.path}")


class ImageProxy(Image):
    def __init__(self, path: str) -> None:
        self.path = path
        self._real: RealImage | None = None    # 還沒讀

    def display(self) -> None:
        if self._real is None:                 # 真的需要才讀
            self._real = RealImage(self.path)
        self._real.display()


# ====================================================================
# Protection Proxy：權限控管
# ====================================================================
class Document(ABC):
    @abstractmethod
    def read(self) -> str: ...
    @abstractmethod
    def write(self, content: str) -> None: ...


class RealDocument(Document):
    def __init__(self, content: str) -> None:
        self._content = content

    def read(self) -> str: return self._content
    def write(self, content: str) -> None: self._content = content


class DocumentProxy(Document):
    def __init__(self, doc: RealDocument, user_role: str) -> None:
        self._doc = doc
        self.role = user_role

    def read(self) -> str:
        # 讀允許所有人
        return self._doc.read()

    def write(self, content: str) -> None:
        if self.role != "admin":
            raise PermissionError(f"role={self.role} 沒有寫入權限")
        self._doc.write(content)


def main() -> None:
    print("--- Virtual Proxy ---")
    img = ImageProxy("photo.png")     # 此刻不讀檔
    print("  proxy 已建立，但檔案還沒載入")
    img.display()                     # 第一次才載入
    img.display()                     # 第二次直接用快取

    print("\n--- Protection Proxy ---")
    doc = RealDocument("hello world")
    admin = DocumentProxy(doc, "admin")
    guest = DocumentProxy(doc, "guest")

    print(f"  guest read: {guest.read()}")
    admin.write("changed by admin")
    print(f"  guest read again: {guest.read()}")
    try:
        guest.write("hack!")
    except PermissionError as e:
        print(f"  攔截 → {e}")


if __name__ == "__main__":
    main()
