from __future__ import annotations
from enum import Enum

# === Device / Registers ===
I2C_ADDRESS: int = 0x22

REGISTER_DEVICE_ID: int = 0x04
REGISTER_UV: int = 0x10
REGISTER_LUX: int = 0x12
REGISTER_TEMP: int = 0x14
REGISTER_RH: int = 0x16
REGISTER_PRESS: int = 0x18

# === Physics / Defaults ===
SEA_LEVEL_HPA: float = 1013.25  # Standard sea-level pressure

# Raw scaling (based on original code)
TEMP_OFFSET_C: float = -45.0
TEMP_RANGE: float = 175.0
RAW_SCALE: float = 1024.0
OVERSAMPLE: float = 64.0

class UVSensor(Enum):
    """Supported UV sensor variants on different board revisions."""
    LTR390UV = 0
    S12DS = 1

class Units(Enum):
    """Units for various measurements."""
    HPA = "hPa"
    KPA = "kPa"
    C = "C"
    F = "F"
