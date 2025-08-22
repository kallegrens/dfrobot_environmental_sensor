from __future__ import annotations
from .constants import (
    I2C_ADDRESS,
    REGISTER_DEVICE_ID,
    REGISTER_TEMP,
    REGISTER_RH,
    REGISTER_LUX,
    REGISTER_UV,
    REGISTER_PRESS,
    SEA_LEVEL_HPA,
    Units,
    UVSensor,
    TEMP_OFFSET_C,
    TEMP_RANGE,
    RAW_SCALE,
    OVERSAMPLE,
)
from .transports import Transport, I2CTransport, UARTTransport


def clamp(x: float, lower: float, upper: float) -> float:
    """Clamp value x to the inclusive range [lower, upper]."""
    return max(lower, min(upper, x))


def mapfloat(x: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """Linearly map a float x from one range [in_min, in_max] to another [out_min, out_max]."""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def _u16_be(b: bytes) -> int:
    return (b[0] << 8) | b[1]


def _uv_ltr390(raw: int) -> float:
    output_v = 3.0 * raw / RAW_SCALE
    # Clamp to [0.99, 2.99]
    output_v = clamp(output_v, lower=0.99, upper=2.99)
    # Map to [0.0, 15.0]
    uv = mapfloat(output_v, in_min=0.99, in_max=2.9, out_min=0.0, out_max=15.0)
    return round(uv, 3)


def _uv_s12ds(raw: int) -> float:
    output_mV = 3000.0 * raw / RAW_SCALE
    na = output_mV * 1e9 / 4_303_300
    return round(na / 113.0, 3)


_UV_COMPUTE = {
    UVSensor.LTR390UV: _uv_ltr390,
    UVSensor.S12DS: _uv_s12ds,
}


class EnvironmentalSensor:
    """High-level driver for DFRobot SEN0500/SEN0501.

    Parameters
    ----------
    transport : Transport
        I²C or UART transport implementation.
    uv_sensor : UVSensor, optional
        Which UV sensor variant is mounted. Defaults to UVSensor.LTR390UV.
    """

    def __init__(self, transport: Transport, uv_sensor: UVSensor = UVSensor.LTR390UV) -> None:
        self._t = transport
        self.uv_sensor = uv_sensor

    # ---- Construction helpers ----
    @classmethod
    def i2c(
        cls, bus: int, addr: int = I2C_ADDRESS, uv_sensor: UVSensor = UVSensor.LTR390UV
    ) -> "EnvironmentalSensor":
        return cls(I2CTransport(bus, addr), uv_sensor)

    @classmethod
    def uart(
        cls,
        port: str = "/dev/ttyAMA0",
        baudrate: int = 9600,
        addr: int = I2C_ADDRESS,
        uv_sensor: UVSensor = UVSensor.LTR390UV,
    ) -> "EnvironmentalSensor":
        return cls(UARTTransport(port, baudrate, addr), uv_sensor)

    # ---- Low-level helpers ----
    def _read_u16(self, reg: int) -> int:
        b = self._t.read_block(reg, 2)
        if len(b) < 2:
            raise IOError(f"Short read: expected 2 bytes, got {len(b)} at reg 0x{reg:02X}")
        return _u16_be(b)

    # ---- API ----
    def begin(self) -> bool:
        """Probe the device ID/register.

        Returns
        -------
        bool
            True if device responds with expected address/ID, False otherwise.
        """
        try:
            dev = self._read_u16(REGISTER_DEVICE_ID)
        except IOError:
            return False
        # The upstream code compared to 0x22; if you have a distinct device ID, adjust here.
        return (dev & 0xFFFF) in (I2C_ADDRESS,)

    def temperature(self, units: Units = Units.C) -> float:
        """Get ambient temperature.

        Parameters
        ----------
        units : Units
            Units.C (default) or Units.F.

        Returns
        -------
        float
            Temperature in selected units.
        """
        raw = self._read_u16(REGISTER_TEMP)
        temp_c = TEMP_OFFSET_C + (raw * TEMP_RANGE) / (RAW_SCALE * OVERSAMPLE)
        return round(temp_c * 1.8 + 32.0, 2) if units == Units.F else round(temp_c, 2)

    def humidity(self) -> float:
        """Get relative humidity (percent)."""
        raw = self._read_u16(REGISTER_RH)
        rh = (raw / RAW_SCALE) * 100.0 / OVERSAMPLE
        return round(rh, 2)

    def uv_index(self) -> float:
        """Get UV index."""
        raw = self._read_u16(REGISTER_UV)
        return _UV_COMPUTE[self.uv_sensor](raw)

    def illuminance(self) -> float:
        """Get illuminance (lux)."""
        raw = self._read_u16(REGISTER_LUX)
        lux = raw * (1.0023 + raw * (8.1488e-5 + raw * (-9.3924e-9 + raw * 6.0135e-13)))
        return round(lux, 2)

    def pressure(self, units: Units = Units.HPA) -> float:
        """Get pressure.

        Parameters
        ----------
        units : Units
            Units.HPA (default) or Units.KPA.

        Returns
        -------
        float
            Pressure in hPa or kPa.
        """
        raw = self._read_u16(REGISTER_PRESS)
        hpa = float(raw)
        return round(hpa / 10.0, 2) if units == Units.KPA else round(hpa, 2)

    def altitude(self, sea_level_hpa: float = SEA_LEVEL_HPA) -> float:
        """Estimate altitude (meters) from pressure and sea-level pressure."""
        p = self.pressure(Units.HPA)
        alt = 44330.0 * (1.0 - (p / sea_level_hpa) ** 0.1903)
        return round(alt, 2)
