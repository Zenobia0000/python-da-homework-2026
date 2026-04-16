"""
中介者 Mediator
===============
意圖：用一個中介者集中處理「多對多」的元件互動，
      讓元件間從「網狀依賴」變成「星狀依賴」。
何時用：聊天室、UI 元件聯動、空管塔台、Event Bus。

例子：聊天室。每個 User 不直接 call 對方，而是丟到 ChatRoom 廣播。

跑：python mediator.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Mediator(ABC):
    @abstractmethod
    def broadcast(self, sender: "User", msg: str) -> None: ...
    @abstractmethod
    def direct(self, sender: "User", to: str, msg: str) -> None: ...


class User:
    def __init__(self, name: str, room: Mediator) -> None:
        self.name = name
        self.room = room

    def send(self, msg: str) -> None:
        self.room.broadcast(self, msg)

    def whisper(self, to: str, msg: str) -> None:
        self.room.direct(self, to, msg)

    def receive(self, sender: "User", msg: str, private: bool = False) -> None:
        tag = "(私)" if private else ""
        print(f"  → {self.name} 收到{tag} <{sender.name}>: {msg}")


class ChatRoom(Mediator):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def join(self, user: User) -> None:
        self._users[user.name] = user
        print(f"[Room] {user.name} 加入聊天室")

    def broadcast(self, sender: User, msg: str) -> None:
        print(f"[Room] {sender.name} 廣播：{msg}")
        for u in self._users.values():
            if u is not sender:
                u.receive(sender, msg)

    def direct(self, sender: User, to: str, msg: str) -> None:
        target = self._users.get(to)
        if target is not None and target is not sender:
            target.receive(sender, msg, private=True)


def main() -> None:
    room = ChatRoom()
    alice = User("Alice", room)
    bob = User("Bob", room)
    carol = User("Carol", room)
    for u in (alice, bob, carol):
        room.join(u)

    alice.send("大家好")
    bob.whisper("Carol", "Alice 看起來很忙耶")
    carol.send("我聽到了 Bob")


if __name__ == "__main__":
    main()
