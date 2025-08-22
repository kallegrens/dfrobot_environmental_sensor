"""Top-level package exports for the SEN050X sensor library.

This module exposes the primary high-level API components:

- :class:`~.core.EnvironmentalSensor`: main driver class
- :class:`~.constants.Units`: measurement units
- :class:`~.constants.UVSensor`: supported UV sensor variants

Importing these symbols directly from the package is the recommended usage:

>>> from dfrobot_environmental_sensor import EnvironmentalSensor, Units
>>> sensor = EnvironmentalSensor.i2c(bus=1)
>>> print(sensor.read_temperature(Units.C))
"""


from .constants import Units, UVSensor
from .core import EnvironmentalSensor

__all__ = ["EnvironmentalSensor", "Units", "UVSensor"]
