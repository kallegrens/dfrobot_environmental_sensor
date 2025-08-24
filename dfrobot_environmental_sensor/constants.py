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

# === Conversion factors ===

CELSIUS_TO_FAHRENHEIT_SCALE: float = 1.8
"""Multiplicative factor for Celsius→Fahrenheit conversion."""

CELSIUS_TO_FAHRENHEIT_OFFSET: float = 32.0
"""Additive offset for Celsius→Fahrenheit conversion."""

UV_10BIT_MASK: int = 0x03FF
"""Bit mask for extracting the 10-bit UV ADC value."""

ADC_REFERENCE_VOLTAGE: float = 3.0
"""Reference voltage for ADC conversions (volts)."""

# LTR390UV conversion parameters
LTR390_OUTPUT_MIN_V: float = 0.99
"""Minimum valid output voltage for LTR390UV sensor (volts)."""

LTR390_OUTPUT_MAX_V: float = 2.99
"""Maximum valid output voltage for LTR390UV sensor (volts)."""

LTR390_IRRADIANCE_MIN: float = 0.0
"""Minimum UV irradiance for LTR390UV conversion (mW/cm²)."""

LTR390_IRRADIANCE_MAX: float = 15.0
"""Maximum UV irradiance for LTR390UV conversion (mW/cm²)."""

# S12DS conversion parameters
S12DS_NANOAMP_SCALE: float = 1e12
"""Scale to convert volts to nanoamperes for S12DS sensor."""

S12DS_LOAD_RESISTANCE_OHMS: int = 4_303_300
"""Load resistance in the S12DS circuit (ohms)."""

S12DS_NA_PER_MW_CM2: float = 113.0
"""Nanoamperes corresponding to 1 mW/cm² for S12DS."""

# Illuminance polynomial coefficients
ILLUMINANCE_COEFF_A: float = 1.0023
"""Coefficient A for vendor polynomial of lux conversion."""

ILLUMINANCE_COEFF_B: float = 8.1488e-5
"""Coefficient B for vendor polynomial of lux conversion."""

ILLUMINANCE_COEFF_C: float = -9.3924e-9
"""Coefficient C for vendor polynomial of lux conversion."""

ILLUMINANCE_COEFF_D: float = 6.0135e-13
"""Coefficient D for vendor polynomial of lux conversion."""

PRESSURE_TO_KPA_DIVISOR: float = 10.0
"""Divisor to convert pressure from hPa to kPa."""

ALTITUDE_SCALING_FACTOR: float = 44330.0
"""Scaling factor for barometric altitude estimation (meters)."""

ALTITUDE_EXPONENT: float = 0.1903
"""Exponent used in barometric altitude estimation."""

PERCENTAGE_SCALE: float = 100.0
"""Scale factor to convert fractional values to percentages."""

# UART defaults
UART_DATA_BITS: int = 8
"""UART frame data bits."""

UART_PARITY: str = "N"
"""UART parity mode ("N" = none)."""

UART_STOP_BITS: int = 1
"""UART stop bits."""

UART_TIMEOUT_S: float = 1.0
"""Default UART timeout in seconds."""


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
