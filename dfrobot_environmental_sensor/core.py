from __future__ import annotations
import struct
from .constants import (
    DEFAULT_BAUDRATE,
    DEFAULT_I2C_ADDRESS,
    EXPECTED_DEVICE_ID,
    REG_DEVICE_ID,
    REG_TEMPERATURE,
    REG_HUMIDITY,
    REG_ILLUMINANCE,
    REG_UV_IRRADIANCE,
    REG_PRESSURE,
    STANDARD_SEA_LEVEL_PRESSURE_HPA,
    Units,
    UVSensor,
    TEMPERATURE_OFFSET_C,
    TEMPERATURE_RANGE_C,
    RAW_SCALE_FACTOR,
    OVERSAMPLING_FACTOR,
    CELSIUS_TO_FAHRENHEIT_SCALE,
    CELSIUS_TO_FAHRENHEIT_OFFSET,
    UV_10BIT_MASK,
    ADC_REFERENCE_VOLTAGE,
    LTR390_OUTPUT_MIN_V,
    LTR390_OUTPUT_MAX_V,
    LTR390_IRRADIANCE_MIN,
    LTR390_IRRADIANCE_MAX,
    S12DS_NANOAMP_SCALE,
    S12DS_LOAD_RESISTANCE_OHMS,
    S12DS_NA_PER_MW_CM2,
    ILLUMINANCE_COEFF_A,
    ILLUMINANCE_COEFF_B,
    ILLUMINANCE_COEFF_C,
    ILLUMINANCE_COEFF_D,
    PRESSURE_TO_KPA_DIVISOR,
    ALTITUDE_SCALING_FACTOR,
    ALTITUDE_EXPONENT,
    PERCENTAGE_SCALE,
)
from .transports import Transport, I2CTransport, UARTTransport


def convert_celsius_to_fahrenheit(temperature_c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit.

    Parameters
    ----------
    temperature_c : float
        Temperature in degrees Celsius.

    Returns
    -------
    float
        Equivalent temperature in degrees Fahrenheit.
    """
    return (
        temperature_c * CELSIUS_TO_FAHRENHEIT_SCALE
        + CELSIUS_TO_FAHRENHEIT_OFFSET
    )


def clamp_value(x: float, lower: float, upper: float) -> float:
    """Clamp a numeric value to a closed interval.

    Parameters
    ----------
    x : float
        Value to clamp.
    lower : float
        Minimum allowed value.
    upper : float
        Maximum allowed value.

    Returns
    -------
    float
        ``x`` constrained to the interval [lower, upper].
    """
    return max(lower, min(upper, x))


def map_linear(
    x: float, in_min: float, in_max: float, out_min: float, out_max: float
) -> float:
    """Map a value linearly from one range to another.

    Parameters
    ----------
    x : float
        Input value to transform.
    in_min : float
        Minimum of input range.
    in_max : float
        Maximum of input range.
    out_min : float
        Minimum of output range.
    out_max : float
        Maximum of output range.

    Returns
    -------
    float
        Value scaled into the output range.

    Raises
    ------
    ValueError
        If ``in_min == in_max``.
    """
    if in_min == in_max:
        raise ValueError("in_min and in_max must be different")

    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def _bytes_to_u16_big_endian(byte_buffer: bytes) -> int:
    """Interpret exactly 2 bytes as an unsigned 16-bit big-endian integer.

    Parameters
    ----------
    byte_buffer : bytes
        A 2-byte buffer.

    Returns
    -------
    int
        Unsigned 16-bit integer value.

    Raises
    ------
    ValueError
        If ``byte_buffer`` does not contain exactly 2 bytes.
    """
    if len(byte_buffer) != 2:
        raise ValueError(f"Expected 2 bytes, but got {len(byte_buffer)}")
    return struct.unpack(">H", byte_buffer)[0]


def _compute_uv_ltr390(raw: int) -> float:
    """Compute UV irradiance from LTR390UV raw ADC value.

    Parameters
    ----------
    raw : int
        Raw 16-bit ADC reading.

    Returns
    -------
    float
        UV irradiance in mW/cm² (rounded to 2 decimals).
    """
    raw10 = raw & UV_10BIT_MASK
    output_voltage = ADC_REFERENCE_VOLTAGE * raw10 / RAW_SCALE_FACTOR  # volts
    clamped_output_voltage = clamp_value(
        output_voltage, lower=LTR390_OUTPUT_MIN_V, upper=LTR390_OUTPUT_MAX_V
    )
    uv_irradiance = map_linear(
        clamped_output_voltage,
        in_min=LTR390_OUTPUT_MIN_V,
        in_max=LTR390_OUTPUT_MAX_V,
        out_min=LTR390_IRRADIANCE_MIN,
        out_max=LTR390_IRRADIANCE_MAX,
    )  # mW/cm²
    return round(uv_irradiance, 2)


def _compute_uv_s12ds(raw: int) -> float:
    """Compute UV irradiance from S12DS raw ADC value.

    Parameters
    ----------
    raw : int
        Raw 16-bit ADC reading.

    Returns
    -------
    float
        UV irradiance in mW/cm² (rounded to 2 decimals).
    """
    output_voltage = ADC_REFERENCE_VOLTAGE * raw / RAW_SCALE_FACTOR  # volts
    photocurrent = (
        output_voltage * S12DS_NANOAMP_SCALE / S12DS_LOAD_RESISTANCE_OHMS
    )  # nanoamperes
    return round(photocurrent / S12DS_NA_PER_MW_CM2, 2)


_UV_COMPUTE_MAP = {
    UVSensor.LTR390UV: _compute_uv_ltr390,
    UVSensor.S12DS: _compute_uv_s12ds,
}


class EnvironmentalSensor:
    """High-level driver for DFRobot SEN0500/SEN0501 environmental sensors.

    Provides access to temperature, humidity, UV irradiance, illuminance,
    and pressure measurements via either I²C or UART/Modbus transports.

    Parameters
    ----------
    transport : Transport
        Concrete transport implementation (I²C or UART).
    uv_sensor : UVSensor, optional
        Which UV sensor variant is mounted. Defaults to ``UVSensor.LTR390UV``.
    """

    def __init__(
        self, transport: Transport, uv_sensor: UVSensor = UVSensor.LTR390UV
    ) -> None:
        self._transport = transport
        self.uv_sensor = uv_sensor

    # ---- Construction helpers ----
    @classmethod
    def i2c(
        cls,
        bus: int,
        address: int = DEFAULT_I2C_ADDRESS,
        uv_sensor: UVSensor = UVSensor.LTR390UV,
    ) -> EnvironmentalSensor:
        """Construct a sensor instance using I²C transport.

        Parameters
        ----------
        bus : int
            I²C bus index.
        address : int, optional
            I²C device address. Defaults to :data:`DEFAULT_I2C_ADDRESS`.
        uv_sensor : UVSensor, optional
            UV sensor variant. Defaults to ``UVSensor.LTR390UV``.

        Returns
        -------
        EnvironmentalSensor
            Configured sensor instance.
        """
        return cls(I2CTransport(bus, address), uv_sensor)

    @classmethod
    def uart(
        cls,
        port: str = "/dev/ttyAMA0",
        baudrate: int = DEFAULT_BAUDRATE,
        address: int = EXPECTED_DEVICE_ID,
        uv_sensor: UVSensor = UVSensor.LTR390UV,
    ) -> EnvironmentalSensor:
        """Construct a sensor instance using UART/Modbus RTU transport.

        Parameters
        ----------
        port : str, optional
            Serial port path (e.g. ``/dev/ttyAMA0`` or ``COM3``).
        baudrate : int, optional
            Baud rate for UART communication. Defaults to :data:`DEFAULT_BAUDRATE`.
        address : int, optional
            Modbus slave address. Defaults to :data:`EXPECTED_DEVICE_ID`.
        uv_sensor : UVSensor, optional
            UV sensor variant. Defaults to ``UVSensor.LTR390UV``.

        Returns
        -------
        EnvironmentalSensor
            Configured sensor instance.
        """
        return cls(UARTTransport(port, baudrate, address), uv_sensor)

    # ---- Low-level helpers ----
    def _read_u16(self, reg_address: int) -> int:
        """Read a 16-bit unsigned value from the given register.

        Parameters
        ----------
        reg_address : int
            Register address to read from.

        Returns
        -------
        int
            Unsigned 16-bit integer value.

        Raises
        ------
        IOError
            If the transport layer fails to return two bytes.
        """
        try:
            word_bytes = self._transport.read_block(reg_address, 2)
        except Exception as e:
            raise IOError(
                f"Failed to read 2 bytes at register 0x{reg_address:02X}"
            ) from e
        return _bytes_to_u16_big_endian(word_bytes)

    # ---- API ----
    def is_present(self) -> bool:
        """Check if the sensor is responding at the expected address.

        Returns
        -------
        bool
            True if the device ID matches :data:`EXPECTED_DEVICE_ID`,
            False otherwise.
        """
        try:
            device = self._read_u16(REG_DEVICE_ID)
        except IOError:
            return False
        # The upstream code compared to 0x22; if you have a distinct device ID, adjust here.
        return (device & 0xFFFF) in (EXPECTED_DEVICE_ID,)

    def read_temperature(self, units: Units = Units.C) -> float:
        """Read the ambient temperature.

        Parameters
        ----------
        units : Units, optional
            Temperature units, ``Units.C`` (default) or ``Units.F``.

        Returns
        -------
        float
            Temperature in the requested units, rounded to 2 decimals.
        """
        raw = self._read_u16(REG_TEMPERATURE)
        temperature_c = TEMPERATURE_OFFSET_C + (raw * TEMPERATURE_RANGE_C) / (
            RAW_SCALE_FACTOR * OVERSAMPLING_FACTOR
        )
        return (
            round(convert_celsius_to_fahrenheit(temperature_c), 2)
            if units == Units.F
            else round(temperature_c, 2)
        )

    def read_humidity(self) -> float:
        """Read the relative humidity.

        Returns
        -------
        float
            Relative humidity in percent (%RH), rounded to 2 decimals.
        """
        raw = self._read_u16(REG_HUMIDITY)
        relative_humidity = (
            raw / RAW_SCALE_FACTOR * PERCENTAGE_SCALE / OVERSAMPLING_FACTOR
        )
        return round(relative_humidity, 2)

    def read_uv_irradiance(self) -> float:
        """Read the UV irradiance.

        Returns
        -------
        float
            UV irradiance in mW/cm², rounded to 2 decimals.
        """
        raw = self._read_u16(REG_UV_IRRADIANCE)
        return _UV_COMPUTE_MAP[self.uv_sensor](raw)

    def read_illuminance(self) -> float:
        """Read the ambient illuminance.

        Returns
        -------
        float
            Illuminance in lux, rounded to 2 decimals.

        Notes
        -----
        Uses the vendor-provided polynomial fit for ADC → lux conversion.
        """
        raw = self._read_u16(REG_ILLUMINANCE)
        lux = raw * (
            ILLUMINANCE_COEFF_A
            + raw
            * (
                ILLUMINANCE_COEFF_B
                + raw * (ILLUMINANCE_COEFF_C + raw * ILLUMINANCE_COEFF_D)
            )
        )
        return round(lux, 2)

    def read_pressure(self, units: Units = Units.HPA) -> float:
        """Read the ambient pressure.

        Parameters
        ----------
        units : Units, optional
            Pressure units, ``Units.HPA`` (default) or ``Units.KPA``.

        Returns
        -------
        float
            Pressure in the requested units, rounded to 2 decimals.
        """
        raw = self._read_u16(REG_PRESSURE)
        pressure_hpa = float(raw)
        return (
            round(pressure_hpa / PRESSURE_TO_KPA_DIVISOR, 2)
            if units == Units.KPA
            else round(pressure_hpa, 2)
        )

    def estimate_altitude(
        self, sea_level_hpa: float = STANDARD_SEA_LEVEL_PRESSURE_HPA
    ) -> float:
        """Estimate altitude from measured pressure.

        Parameters
        ----------
        sea_level_hpa : float, optional
            Reference sea-level pressure in hPa. Defaults to the
            international standard atmosphere (1013.25 hPa).

        Returns
        -------
        float
            Estimated altitude above sea level in meters, rounded to 2 decimals.
        """
        pressure_hpa = self.read_pressure(Units.HPA)
        altitude = ALTITUDE_SCALING_FACTOR * (
            1.0 - (pressure_hpa / sea_level_hpa) ** ALTITUDE_EXPONENT
        )
        return round(altitude, 2)
