"""Test helpers for simulating SEN050X hardware.

The ``EnvironmentalSensor`` class accepts any object implementing the
``Transport`` protocol.  ``FakeTransport`` provides a minimal in-memory
implementation returning preset register values.  Tests can therefore
exercise sensor logic without requiring real hardware or the ``smbus3`` or
``modbus-tk`` dependencies.
"""

from dataclasses import dataclass
from typing import Dict

from dfrobot_environmental_sensor.core import EnvironmentalSensor
from dfrobot_environmental_sensor.constants import (
    EXPECTED_DEVICE_ID,
    REG_DEVICE_ID,
    REG_HUMIDITY,
    REG_ILLUMINANCE,
    REG_PRESSURE,
    REG_TEMPERATURE,
    REG_UV_IRRADIANCE,
)
from dfrobot_environmental_sensor.transports import Transport


@dataclass
class FakeTransport(Transport):
    """Simple transport that serves register values from a dictionary."""

    registers: Dict[int, int]

    def read_block(self, reg: int, length: int) -> bytes:  # pragma: no cover - trivial
        value = self.registers.get(reg, 0)
        return value.to_bytes(length, "big")


def build_sensor() -> EnvironmentalSensor:
    """Construct an :class:`EnvironmentalSensor` backed by ``FakeTransport``."""
    # Raw register values chosen to produce human-friendly measurements
    registers = {
        REG_DEVICE_ID: EXPECTED_DEVICE_ID,
        REG_TEMPERATURE: 26189,  # ≈25 °C
        REG_HUMIDITY: 36010,  # ≈55 %RH
        REG_UV_IRRADIANCE: 800,  # ≈10.17 mW/cm²
        REG_ILLUMINANCE: 512,  # ≈533.32 lux
        REG_PRESSURE: 1013,  # ≈1013 hPa
    }
    return EnvironmentalSensor(FakeTransport(registers))
