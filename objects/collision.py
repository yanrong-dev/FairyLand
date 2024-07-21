from enum import auto, IntEnum


class Collision(IntEnum):
    DIE = auto()
    REWARD = auto()
    NONE = auto()