from Enemy.AI.BaseAI import BaseAI
from Enemy.AI.Chase import Chase
from Enemy.AI.Passive import Passive
from Enemy.Body.Cleft import Cleft
from Enemy.Body.EnemyType import EnemyType
from Enemy.Body.Snail import Snail


class EnemyFactory:
    @staticmethod
    def create(_id: int, enemy_type: EnemyType) -> BaseAI | None:
        match enemy_type:
            case EnemyType.NONE:
                return None
            case EnemyType.SNAIL:
                return Passive.new(_id, Snail.new())
            case EnemyType.CLEFT:
                return Chase.new(_id, Cleft.new())
            case _id:
                print(f"Enemy type not implemented: {enemy_type}")
