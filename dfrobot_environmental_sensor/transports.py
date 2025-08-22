from __future__ import annotations
from typing import Protocol


class Transport(Protocol):
    """Abstract communication transport for SEN050X sensors.

    A transport is responsible for reading raw bytes from the device,
    regardless of whether the physical connection is I²C, UART/Modbus,
    or another medium.

    All concrete transports must implement :meth:`read_block`.
    """
    def read_block(self, reg: int, length: int) -> bytes:
        """Read a contiguous block of bytes starting at a device register.

        Parameters
        ----------
        reg : int
            Starting register address (byte address).
        length : int
            Number of bytes to read.

        Returns
        -------
        bytes
            Raw data read from the device.

        Raises
        ------
        IOError
            If the transport layer encounters a communication error.
        """
        ...


class I2CTransport:
    """I²C transport using the `smbus3` library.

    This transport communicates with the sensor over the I²C bus using
    standard SMBus block reads.

    Parameters
    ----------
    bus : int
        I²C bus index (e.g., 1 on Raspberry Pi).
    addr : int
        I²C device address.

    Notes
    -----
    Requires the ``smbus3`` package to be installed.
    """

    def __init__(self, bus: int, addr: int):
        import smbus3

        self._bus = smbus3.SMBus(bus)
        self._addr = addr

    def read_block(self, reg: int, length: int) -> bytes:
        """Read a block of data from the device over I²C.

        Parameters
        ----------
        reg : int
            Register address to read from.
        length : int
            Number of bytes to read.

        Returns
        -------
        bytes
            Raw data read from the device.

        Raises
        ------
        IOError
            If the underlying I²C read fails.
        """
        try:
            data = self._bus.read_i2c_block_data(self._addr, reg, length)
            return bytes(data)
        except Exception as e:
            raise IOError(f"I2C read failed (reg=0x{reg:02X}, len={length}): {e}") from e


class UARTTransport:
    """UART/Modbus RTU transport for SEN050X sensors.

    Communicates with the device over Modbus RTU via a serial port.

    Parameters
    ----------
    port : str
        Serial port path (e.g., ``/dev/ttyAMA0`` or ``COM3``).
    baudrate : int
        Baud rate for UART communication.
    addr : int
        Modbus slave address of the device.

    Notes
    -----
    Requires both ``pyserial`` and ``modbus_tk`` to be installed.
    """

    def __init__(self, port: str, baudrate: int, addr: int):
        try:
            import serial  # type: ignore
            from modbus_tk import modbus_rtu  # type: ignore
        except Exception as e:
            raise ImportError(
                "UARTTransport requires 'pyserial' and 'modbus_tk' to be installed."
            ) from e
        import modbus_tk.defines as cst  # type: ignore

        self._cst = cst
        self._addr = addr
        self._master = modbus_rtu.RtuMaster(
            serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity="N", stopbits=1)
        )
        self._master.set_timeout(1.0)

    def read_block(self, reg: int, length: int) -> bytes:
        """Read a block of data from the device over Modbus RTU.

        Parameters
        ----------
        reg : int
            Starting register address in bytes. Will be converted into a
            Modbus 16-bit register index.
        length : int
            Number of bytes to read.

        Returns
        -------
        bytes
            Raw data read from the device.

        Raises
        ------
        IOError
            If the underlying Modbus read fails.
        """
        # Modbus uses 16-bit registers; compute starting register and count
        count = (length + 1) // 2  # ceil(length/2) to be safe
        start = reg // 2
        try:
            words = self._master.execute(
                self._addr, self._cst.READ_INPUT_REGISTERS, start, count
            )
            # Convert 16-bit words (big-endian) to bytes and trim to requested length
            b = bytearray()
            for w in words:
                b.extend([(w >> 8) & 0xFF, w & 0xFF])
            return bytes(b[:length])
        except Exception as e:
            raise IOError(
                f"UART/Modbus read failed (reg=0x{reg:02X}, len={length}): {e}"
            ) from e
