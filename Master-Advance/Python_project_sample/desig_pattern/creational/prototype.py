"""
原型 Prototype
==============
意圖：用「複製現有物件」的方式取代「new 一個新的」。
何時用：
  - 物件初始化很貴（讀檔、查 DB、跑運算）
  - 執行期才知道要 new 哪個類，但你手上有現成的 sample
  - 想避免子類別爆炸

Python 內建 copy.copy / copy.deepcopy，已經實作好原型模式核心，
我們只要在類別上加個 clone() 方法包一下即可。

例子：遊戲怪物 spawn。先設一隻 sample 怪，後續批次 clone 出來改參數。

跑：python prototype.py
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field


@dataclass
class Monster:
    name: str
    hp: int
    skills: list[str] = field(default_factory=list)
    drops: dict[str, int] = field(default_factory=dict)

    def clone(self) -> "Monster":
        # deepcopy 保證 nested list/dict 不會被多隻怪共用 → 改 A 不會動到 B
        return copy.deepcopy(self)

    def __str__(self) -> str:
        return f"<{self.name} HP={self.hp} skills={self.skills} drops={self.drops}>"


def main() -> None:
    sample = Monster(
        name="哥布林",
        hp=30,
        skills=["亂揮"],
        drops={"金幣": 5, "破布": 1},
    )

    # 從 sample clone 出兩隻變種，不重新跑初始化邏輯
    elite = sample.clone()
    elite.name = "哥布林菁英"
    elite.hp = 80
    elite.skills.append("狂暴")

    boss = sample.clone()
    boss.name = "哥布林王"
    boss.hp = 500
    boss.drops["王者印記"] = 1

    print(sample)   # 不受 clone 後修改影響
    print(elite)
    print(boss)


if __name__ == "__main__":
    main()
