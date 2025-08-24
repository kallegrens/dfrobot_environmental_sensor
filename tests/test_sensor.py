import pytest

from dfrobot_environmental_sensor.constants import Units
from tests.conftest import build_sensor


@pytest.fixture
def sensor():
    return build_sensor()


def test_is_present(sensor) -> None:
    assert sensor.is_present()


def test_read_temperature(sensor) -> None:
    assert sensor.read_temperature(Units.C) == pytest.approx(25.0, abs=0.01)
    assert sensor.read_temperature(Units.F) == pytest.approx(77.0, abs=0.01)


def test_read_humidity(sensor) -> None:
    assert sensor.read_humidity() == pytest.approx(55.0, abs=0.01)


def test_read_uv_irradiance(sensor) -> None:
    assert sensor.read_uv_irradiance() == pytest.approx(10.17, abs=0.01)


def test_read_illuminance(sensor) -> None:
    assert sensor.read_illuminance() == pytest.approx(533.32, abs=0.01)


def test_read_pressure(sensor) -> None:
    assert sensor.read_pressure() == pytest.approx(1013.0, abs=0.01)
    assert sensor.read_pressure(Units.KPA) == pytest.approx(101.3, abs=0.01)


def test_estimate_altitude(sensor) -> None:
    assert sensor.estimate_altitude() == pytest.approx(2.08, abs=0.01)
