from enum import auto, IntEnum


class Layer(IntEnum):
    BACKGROUND = auto()
    FINISH = auto()
    OBSTACLE = auto()
    FLOOR = auto()
    PLAYER = auto()
    REWARD = auto()
    UI = auto()