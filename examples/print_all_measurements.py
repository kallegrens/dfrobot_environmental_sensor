# -*- coding: utf-8 -*
"""!
@file  V3_0.py
@brief This example can obtain data from the SEN0501/SEN0500 V3.0 sensor via UART and I2C.
@copyright   Copyright (c) 2021 DFRobot Co.Ltd (http://www.dfrobot.com)
@license     The MIT License (MIT)
@author      TangJie(jie.tang@dfrobot.com)
@version     V1.0
@date        2021-08-31
@url         https://github.com/DFRobot/DFRobot_EnvironmentalSensor
"""

import time

from dfrobot_environmental_sensor import *

"""
Select communication mode
ctype=1：UART
ctype=0：IIC
"""
ctype = 0

ADDRESS = 0x22
I2C_1 = 0x01
BAUD_RATE = 9600

if ctype == 0:
    SEN050X = DFRobot_Environmental_Sensor_I2C(I2C_1, ADDRESS)
else:
    SEN050X = DFRobot_Environmental_Sensor_UART(BAUD_RATE, ADDRESS)

"""
Atmospheric pressure unit select
"""
HPA = 0x01
KPA = 0x02

"""
Temperature unit select
"""
TEMP_C = 0x03
TEMP_F = 0x04


def setup():
    while SEN050X.begin() == False:
        print("Sensor initialization failed!")
        time.sleep(1)
    print("Sensor initialization succeeded!")


def loop():
    ##Obtain sensor data
    print("-----------------------\r\n")
    print("Temp: " + str(SEN050X.get_temperature(TEMP_C)) + " 'C\r\n")
    print("Temp: " + str(SEN050X.get_temperature(TEMP_F)) + " 'F\r\n")
    print("Humidity: " + str(SEN050X.get_humidity()) + " %\r\n")
    print(
        "Ultraviolet intensity: "
        + str(SEN050X.get_ultraviolet_intensity(S12DS))
        + " mw/cm2\r\n"
    )
    print("LuminousIntensity: " + str(SEN050X.get_luminousintensity()) + " lx\r\n")
    print("Atmospheric pressure: " + str(SEN050X.get_atmosphere_pressure(HPA)) + " hpa\r\n")
    print("Elevation: " + str(SEN050X.get_elevation()) + " m\r\n")
    print("-----------------------\r\n")
    time.sleep(1)


if __name__ == "__main__":
    setup()
    while True:
        loop()
