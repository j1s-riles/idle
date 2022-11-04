from enum import Enum, auto

TICK_SCALAR = 0.01

class gen_type(Enum):
    PC_GEN = auto()
    GEN_GEN = auto()
    MULTI_GEN = auto()
    TICKSPEED_GEN = auto()

class slime_type(Enum):
    GEL = auto()
    GREEN = auto()
    RED = auto()
    BLUE = auto()
    PURPLE = auto()