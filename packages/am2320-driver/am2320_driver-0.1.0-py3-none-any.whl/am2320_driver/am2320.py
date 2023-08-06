import time
from typing import Tuple

from smbus2.smbus2 import SMBus


class AM2320:
    def __init__(self, bus: int = 1, address: int = 0x5C):
        self.i2c = SMBus(bus)
        self.address = address
        while True:
            try:
                self.i2c.write_i2c_block_data(self.address, 0x00, [])
                break
            except IOError:
                pass
        time.sleep(0.003)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        pass

    def get_humi(self) -> float:
        while True:
            try:
                self.i2c.write_i2c_block_data(self.address, 0x03, [0x00, 0x02])
                break
            except IOError:
                pass
        time.sleep(0.015)
        block = self.i2c.read_i2c_block_data(self.address, 0, 4)
        return float(block[2] << 8 | block[3]) / 10

    def get_temp(self) -> float:
        while True:
            try:
                self.i2c.write_i2c_block_data(self.address, 0x03, [0x02, 0x04])
                break
            except IOError:
                pass
        time.sleep(0.015)
        block = self.i2c.read_i2c_block_data(self.address, 0, 4)
        return float(block[2] << 8 | block[3]) / 10

    def get_humi_temp(self) -> Tuple[float, float]:
        while True:
            try:
                self.i2c.write_i2c_block_data(self.address, 0x03, [0x00, 0x04])
                break
            except IOError:
                pass
        time.sleep(0.015)
        block = self.i2c.read_i2c_block_data(self.address, 0, 6)
        humi = float(block[2] << 8 | block[3]) / 10
        temp = float(block[4] << 8 | block[5]) / 10
        return humi, temp
