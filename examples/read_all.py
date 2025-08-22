# examples/print_all_measurements.py
# -*- coding: utf-8 -*-
"""
Continuously print all measurements from the SEN0500/SEN0501 sensor
using I²C transport.
"""

import time
from dfrobot_environmental_sensor import EnvironmentalSensor, Units, UVSensor

I2C_BUS = 1           # Raspberry Pi I²C is usually bus 1
I2C_ADDRESS = 0x22
UV_VARIANT = UVSensor.LTR390UV  # or UVSensor.S12DS, depending on your board


def setup() -> EnvironmentalSensor:
    """Initialize the sensor and wait until it responds."""
    sensor = EnvironmentalSensor.i2c(I2C_BUS, I2C_ADDRESS, uv_sensor=UV_VARIANT)
    while not sensor.is_present():
        print("❌ Sensor initialization failed! Retrying...")
        time.sleep(1)
    print("✅ Sensor initialization succeeded!")
    return sensor


def loop(sensor: EnvironmentalSensor) -> None:
    """Read and print all available measurements once."""
    print("-------------------------------")
    print(f"🌡️ Temperature: {sensor.read_temperature(Units.C)} °C")
    print(f"🌡️ Temperature: {sensor.read_temperature(Units.F)} °F")
    print(f"💧 Humidity: {sensor.read_humidity()} %")
    print(f"☀️ UV Irradiance: {sensor.read_uv_irradiance()} mW/cm²")
    print(f"💡 Light: {sensor.read_illuminance()} lx")
    print(f"🌪️ Pressure: {sensor.read_pressure(Units.HPA)} hPa")
    print(f"🏔️ Altitude: {sensor.estimate_altitude()} m")
    time.sleep(1)


if __name__ == "__main__":
    sensor = setup()
    while True:
        loop(sensor)
