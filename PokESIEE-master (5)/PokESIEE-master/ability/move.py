# from ..pokemon import Pokemon
import sys
sys.path.append('.')
from element import TYPES, Type
from typing import List


SPECIAL = "SPECIAL"
STATUS = "STATUS"
PHYSICAL = "PHYSICAL"

CATEGORYS: List[str] = [SPECIAL, STATUS, PHYSICAL]


class MoveError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return f"MoveError : {self.message}"
        else:
            return "Error in class Move has been raised"


class Move:

    def __init__(self, name: str, move_type: str, category: str, description: str, pp: int, power: int, accuracy: float,
                 self_dmg: float) -> None:
        self.name: str = name
        self.move_type: Type = TYPES[move_type]
        if category not in CATEGORYS:
            raise MoveError(f"Invalid category {category}, not in CATEGORYS list")
        self.category: str = category
        self.description = description
        self.pp: int = pp
        self.pp_max: int = pp
        self.power: int = power
        self.accuracy: float = accuracy
        self.self_dmg: float = self_dmg

    def use(self, battle_mech, user, target):
        hp_before_move = target.health
        damage = battle_mech.calculate_damage(self, user, target)
        target.apply_damage(damage)

    def get_accuracy(self):
        return self.accuracy
