from enum import Enum

class TOTPOptions(str, Enum):
    ascii = "ascii"
    hex = "hex"