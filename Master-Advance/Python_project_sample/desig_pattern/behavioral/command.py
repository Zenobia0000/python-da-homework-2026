"""
命令 Command
============
意圖：把「動作」包成物件，讓動作可被儲存、傳遞、排隊、undo / redo。
何時用：undo / redo、巨集錄製、任務佇列、GUI 按鈕綁動作、回放。

例子：簡易文字編輯器。每個編輯動作都是一個 Command，存在 undo stack 裡。

跑：python command.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


# --- Receiver：真正幹活的物件 -------------------------------------
class TextEditor:
    def __init__(self) -> None:
        self.text = ""

    def insert(self, s: str) -> None: self.text += s
    def delete(self, n: int) -> str:
        cut, self.text = self.text[-n:], self.text[:-n]
        return cut


# --- Command 介面 -------------------------------------------------
class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...
    @abstractmethod
    def undo(self) -> None: ...


class InsertCmd(Command):
    def __init__(self, editor: TextEditor, s: str) -> None:
        self.editor, self.s = editor, s

    def execute(self) -> None: self.editor.insert(self.s)
    def undo(self) -> None: self.editor.delete(len(self.s))


class DeleteCmd(Command):
    def __init__(self, editor: TextEditor, n: int) -> None:
        self.editor, self.n = editor, n
        self._removed = ""

    def execute(self) -> None: self._removed = self.editor.delete(self.n)
    def undo(self) -> None: self.editor.insert(self._removed)


# --- Invoker：負責呼叫、記錄歷史 ----------------------------------
class History:
    def __init__(self) -> None:
        self._stack: list[Command] = []
        self._redo: list[Command] = []

    def run(self, cmd: Command) -> None:
        cmd.execute()
        self._stack.append(cmd)
        self._redo.clear()         # 新動作清掉 redo 軌跡

    def undo(self) -> None:
        if self._stack:
            cmd = self._stack.pop()
            cmd.undo()
            self._redo.append(cmd)

    def redo(self) -> None:
        if self._redo:
            cmd = self._redo.pop()
            cmd.execute()
            self._stack.append(cmd)


def main() -> None:
    editor = TextEditor()
    history = History()

    history.run(InsertCmd(editor, "Hello"))
    history.run(InsertCmd(editor, ", World"))
    history.run(InsertCmd(editor, "!"))
    print(f"step1: {editor.text!r}")

    history.undo()
    print(f"undo : {editor.text!r}")

    history.run(DeleteCmd(editor, 5))
    print(f"del5 : {editor.text!r}")

    history.undo()
    print(f"undo : {editor.text!r}")
    history.redo()
    print(f"redo : {editor.text!r}")


if __name__ == "__main__":
    main()
