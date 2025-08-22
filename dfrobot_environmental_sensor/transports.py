from __future__ import annotations
from typing import Protocol

class Transport(Protocol):
    def read_block(self, reg: int, length: int) -> bytes:
        ...

class I2CTransport:
    """I²C transport using smbus3."""
    def __init__(self, bus: int, addr: int):
        import smbus3
        self._bus = smbus3.SMBus(bus)
        self._addr = addr

    def read_block(self, reg: int, length: int) -> bytes:
        try:
            data = self._bus.read_i2c_block_data(self._addr, reg, length)
            return bytes(data)
        except Exception as e:
            raise IOError(f"I2C read failed (reg=0x{reg:02X}, len={length}): {e}") from e

class UARTTransport:
    """UART/Modbus RTU transport. Optional dependency: pyserial & modbus_tk."""
    def __init__(self, port: str, baudrate: int, addr: int):
        try:
            import serial  # type: ignore
            from modbus_tk import modbus_rtu  # type: ignore
        except Exception as e:
            raise ImportError("UARTTransport requires 'pyserial' and 'modbus_tk' to be installed.") from e
        import modbus_tk.defines as cst  # type: ignore

        self._cst = cst
        self._addr = addr
        self._master = modbus_rtu.RtuMaster(
            serial.Serial(port=port, baudrate=baudrate, bytesize=8, parity="N", stopbits=1)
        )
        self._master.set_timeout(1.0)

    def read_block(self, reg: int, length: int) -> bytes:
        # Modbus uses 16-bit registers; compute starting register and count
        count = (length + 1) // 2  # ceil(length/2) to be safe
        start = reg // 2
        try:
            words = self._master.execute(self._addr, self._cst.READ_INPUT_REGISTERS, start, count)
            # Convert 16-bit words (big-endian) to bytes and trim to requested length
            b = bytearray()
            for w in words:
                b.extend([(w >> 8) & 0xFF, w & 0xFF])
            return bytes(b[:length])
        except Exception as e:
            raise IOError(f"UART/Modbus read failed (reg=0x{reg:02X}, len={length}): {e}") from e
