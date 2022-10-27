from enum import Enum, auto

TICK_SCALAR = 0.01

class gen_ID(Enum):
    SLIME_GREEN = auto()

class gen_type(Enum):
    PC_GEN = auto()
    GEN_GEN = auto()
    MULTI_GEN = auto()