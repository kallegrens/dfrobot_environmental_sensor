from __future__ import annotations
from enum import Enum, auto

# === Device / Registers ===

EXPECTED_DEVICE_ID: int = 0x22
"""Expected device ID value returned by the sensor (from :data:`REG_DEVICE_ID`)."""

DEFAULT_I2C_ADDRESS: int = 0x22
"""Default I²C bus address of the sensor device."""

REG_DEVICE_ID: int = 0x04
"""Register address for device ID (16-bit)."""

REG_UV_IRRADIANCE: int = 0x10
"""Register address for UV irradiance measurement (16-bit)."""

REG_ILLUMINANCE: int = 0x12
"""Register address for ambient illuminance measurement (16-bit)."""

REG_TEMPERATURE: int = 0x14
"""Register address for ambient temperature measurement (16-bit)."""

REG_HUMIDITY: int = 0x16
"""Register address for relative humidity measurement (16-bit)."""

REG_PRESSURE: int = 0x18
"""Register address for barometric pressure measurement (16-bit)."""

DEFAULT_BAUDRATE: int = 9600
"""Default UART baud rate (bits per second) for Modbus RTU communication."""

# === Physics / Defaults ===

STANDARD_SEA_LEVEL_PRESSURE_HPA: float = 1013.25
"""Standard sea-level pressure in hPa (International Standard Atmosphere)."""

TEMPERATURE_OFFSET_C: float = -45.0
"""Temperature sensor offset in degrees Celsius applied to raw readings."""

TEMPERATURE_RANGE_C: float = 175.0
"""Effective measurable temperature range in degrees Celsius."""

RAW_SCALE_FACTOR: int = 1023
"""Raw ADC full-scale value (10-bit ADC → 0–1023)."""

OVERSAMPLING_FACTOR: int = 64
"""Default oversampling factor used for temperature and humidity conversions."""


class UVSensor(Enum):
    """Enumerates supported UV sensor variants.

    Some board revisions use different UV detectors.
    """

    LTR390UV = auto()
    """LTR390UV sensor variant."""

    S12DS = auto()
    """S12DS sensor variant."""


class Units(Enum):
    """Measurement units supported by the sensor API."""

    HPA = "hPa"
    """Pressure in hectopascals."""

    KPA = "kPa"
    """Pressure in kilopascals."""

    C = "C"
    """Temperature in degrees Celsius."""

    F = "F"
    """Temperature in degrees Fahrenheit."""
