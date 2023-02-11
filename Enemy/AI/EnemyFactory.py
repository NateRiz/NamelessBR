from Enemy.AI.BaseAI import BaseAI
from Enemy.AI.Passive import Passive
from Enemy.Body.EnemyType import EnemyType
from Enemy.Body.Snail import Snail


class EnemyFactory:
    @staticmethod
    def create(enemy_type: EnemyType) -> BaseAI | None:
        match enemy_type:
            case EnemyType.NONE:
                return None
            case EnemyType.SNAIL:
                return Passive.new(Snail.new())
