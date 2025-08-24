import pytest

from dfrobot_environmental_sensor.core import (
    _bytes_to_u16_big_endian,
    clamp_value,
    convert_celsius_to_fahrenheit,
    map_linear,
)


def test_convert_celsius_to_fahrenheit() -> None:
    assert convert_celsius_to_fahrenheit(0.0) == 32.0
    assert convert_celsius_to_fahrenheit(100.0) == 212.0


def test_clamp_value() -> None:
    assert clamp_value(5, 0, 10) == 5
    assert clamp_value(-1, 0, 10) == 0
    assert clamp_value(15, 0, 10) == 10


def test_map_linear() -> None:
    assert map_linear(5, 0, 10, 0, 100) == 50
    with pytest.raises(ValueError):
        map_linear(1, 0, 0, 0, 1)


def test_bytes_to_u16_big_endian() -> None:
    assert _bytes_to_u16_big_endian(b"\x12\x34") == 0x1234
    with pytest.raises(ValueError):
        _bytes_to_u16_big_endian(b"\x00")
