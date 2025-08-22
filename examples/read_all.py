# examples/print_all_measurements.py
# -*- coding: utf-8 -*-
import time

from dfrobot_environmental_sensor import EnvironmentalSensor, Units, UVSensor

I2C_BUS = 1          # Raspberry Pi I²C is usually bus 1
I2C_ADDR = 0x22
UV_VARIANT = UVSensor.S12DS   # or UVSensor.LTR390UV, depending on your board

def setup():
    global sensor
    sensor = EnvironmentalSensor.i2c(I2C_BUS, I2C_ADDR, uv_sensor=UV_VARIANT)
    while not sensor.begin():
        print("Sensor initialization failed!")
        time.sleep(1)
    print("Sensor initialization succeeded!")

def loop():
    print("-----------------------")
    print(f"Temp: {sensor.temperature(Units.C)} °C")
    print(f"Temp: {sensor.temperature(Units.F)} °F")
    print(f"Humidity: {sensor.humidity()} %")
    print(f"Ultraviolet intensity: {sensor.uv_index()} mW/cm²")   # unit depends on compute method
    print(f"LuminousIntensity: {sensor.illuminance()} lx")
    print(f"Atmospheric pressure: {sensor.pressure(Units.HPA)} hPa")
    print(f"Elevation: {sensor.altitude()} m")
    print("-----------------------")
    time.sleep(1)

if __name__ == "__main__":
    setup()
    while True:
        loop()
