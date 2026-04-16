"""
責任鏈 Chain of Responsibility
==============================
意圖：把請求沿著一條 handler 鏈傳，誰能處理誰處理。
何時用：middleware（HTTP / log）、審批流程、事件冒泡、表單驗證。

例子：請假審批。3 天以下組長批；3-7 天經理批；超過 7 天 CEO 批。

跑：python chain_of_responsibility.py
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LeaveRequest:
    employee: str
    days: int
    reason: str


class Approver(ABC):
    def __init__(self) -> None:
        self._next: Approver | None = None

    def set_next(self, nxt: "Approver") -> "Approver":
        self._next = nxt
        return nxt        # 回傳 nxt 以便 chain：a.set_next(b).set_next(c)

    def handle(self, req: LeaveRequest) -> None:
        if self._can_approve(req):
            self._approve(req)
        elif self._next is not None:
            self._next.handle(req)
        else:
            print(f"[Reject] 無人能批 {req.employee} 請 {req.days} 天")

    @abstractmethod
    def _can_approve(self, req: LeaveRequest) -> bool: ...
    @abstractmethod
    def _approve(self, req: LeaveRequest) -> None: ...


class TeamLead(Approver):
    def _can_approve(self, req: LeaveRequest) -> bool: return req.days <= 3
    def _approve(self, req: LeaveRequest) -> None:
        print(f"[組長] 批准 {req.employee} 請 {req.days} 天 ({req.reason})")


class Manager(Approver):
    def _can_approve(self, req: LeaveRequest) -> bool: return req.days <= 7
    def _approve(self, req: LeaveRequest) -> None:
        print(f"[經理] 批准 {req.employee} 請 {req.days} 天 ({req.reason})")


class CEO(Approver):
    def _can_approve(self, req: LeaveRequest) -> bool: return req.days <= 30
    def _approve(self, req: LeaveRequest) -> None:
        print(f"[CEO] 批准 {req.employee} 請 {req.days} 天 ({req.reason})")


def main() -> None:
    chain = TeamLead()
    chain.set_next(Manager()).set_next(CEO())

    for req in [
        LeaveRequest("Alice", 1, "感冒"),
        LeaveRequest("Bob", 5, "家庭旅遊"),
        LeaveRequest("Carol", 14, "婚假"),
        LeaveRequest("Dave", 60, "環遊世界"),
    ]:
        chain.handle(req)


if __name__ == "__main__":
    main()
