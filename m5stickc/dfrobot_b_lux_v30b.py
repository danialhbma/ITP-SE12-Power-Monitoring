# Credits to DFRobot for the original Arduino library
# Credits to ChatGPT for converting it to MicroPython

from machine import Pin, I2C
import time

class DFRobot_B_LUX_V30B:
    def __init__(self, cEN, scl, sda):
        self._deviceAddr = 0x94
        self._SCL = scl
        self._SDA = sda
        self._cEN = cEN
        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)

    def begin(self):
        pin_sda = Pin(self._SDA, Pin.OUT)
        pin_scl = Pin(self._SCL, Pin.OUT)
        pin_sda.value(1)
        pin_scl.value(1)
        pin_cEN = Pin(self._cEN, Pin.OUT)
        pin_cEN.value(0)
        time.sleep_ms(1000)
        pin_cEN.value(1)
        while self.lightStrengthLux() <= 0:
            pass

    def readMode(self):
        self.iicStartBit()
        if self.iicSend(self._deviceAddr + 0):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        if self.iicSend(0x04):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        self.iicStartBit()
        if self.iicSend(self._deviceAddr + 1):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        time.sleep_ms(10)
        mode = self.iicReadByte()
        self.iicSendAck(1)
        self.iicStopBit()
        while self.lightStrengthLux() <= 0:
            pass
        return mode

    def setMode(self, isManualMode, isCDR, isTime):
        mode = isManualMode + isCDR + isTime
        self.iicStartBit()
        if self.iicSend(self._deviceAddr + 0):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        if self.iicSend(0x04):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        if self.iicSend(mode):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        pin_sda = Pin(self._SDA, Pin.OUT)
        pin_sda.value(0)
        self.iicStopBit()
        time.sleep_ms(10)
        return 1

    def iicStartBit(self):
        pin_scl = Pin(self._SCL, Pin.OUT)
        pin_sda = Pin(self._SDA, Pin.OUT)
        pin_scl.value(1)
        pin_sda.value(1)
        time.sleep_us(5)
        pin_sda.value(0)
        time.sleep_us(5)
        pin_scl.value(0)
        time.sleep_us(5)

    def iicStopBit(self):
        pin_scl = Pin(self._SCL, Pin.OUT)
        pin_sda = Pin(self._SDA, Pin.OUT)
        pin_scl.value(1)
        pin_sda.value(0)
        time.sleep_us(5)
        pin_sda.value(1)
        time.sleep_us(5)
        pin_scl.value(0)
        time.sleep_us(5)

    def iicSendAck(self, ack):
        pin_sda = Pin(self._SDA, Pin.OUT)
        if ack & 0x01:
            pin_sda.value(1)
        else:
            pin_sda.value(0)
        pin_scl = Pin(self._SCL, Pin.OUT)
        pin_scl.value(1)
        time.sleep_us(5)
        pin_scl.value(0)
        time.sleep_us(5)

    def iicRecvAck(self):
        pin_sda = Pin(self._SDA, Pin.IN)
        pin_scl = Pin(self._SCL, Pin.OUT)
        pin_scl.value(1)
        time.sleep_us(5)
        cy = pin_sda.value()
        pin_scl.value(0)
        pin_sda = Pin(self._SDA, Pin.OUT)
        pin_sda.value(1)
        time.sleep_us(5)
        return cy

    def iicSend(self, data):
        pin_sda = Pin(self._SDA, Pin.OUT)
        for i in range(8):
            if data & 0x80:
                pin_sda.value(1)
            else:
                pin_sda.value(0)
            time.sleep_us(5)
            pin_scl = Pin(self._SCL, Pin.OUT)
            pin_scl.value(1)
            time.sleep_us(5)
            pin_scl.value(0)
            time.sleep_us(5)
            data = data << 1
        return self.iicRecvAck()

    def iicReadByte(self):
        data = 0
        pin_sda = Pin(self._SDA, Pin.IN)
        pin_scl = Pin(self._SCL, Pin.OUT)
        for i in range(8):
            pin_scl.value(1)
            time.sleep_us(5)
            data |= pin_sda.value()
            pin_scl.value(0)
            time.sleep_us(5)
            if i < 7:
                data <<= 1
        pin_sda = Pin(self._SDA, Pin.OUT)
        return data

    def iicRead(self, num, data):
        self.iicStartBit()
        if self.iicSend(self._deviceAddr + 0):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        if self.iicSend(0x00):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        self.iicStartBit()
        if self.iicSend(self._deviceAddr + 1):
            pin_sda = Pin(self._SDA, Pin.OUT)
            pin_sda.value(0)
            self.iicStopBit()
            return 0
        time.sleep_ms(10)
        for i in range(num):
            data[i] = self.iicReadByte()
            if i == num - 1:
                self.iicSendAck(0x01)  # send NACK
            else:
                self.iicSendAck(0x00)  # send ACK
        pin_sda = Pin(self._SDA, Pin.OUT)
        pin_sda.value(0)
        self.iicStopBit()
        return 1

    def lightStrengthLux(self):
        value = 0
        data = bytearray(6)
        if self.iicRead(4, data):
            value = data[3]
            value = (value << 8) | data[2]
            value = (value << 8) | data[1]
            value = (value << 8) | data[0]
            return float(value * 1.4) / 1000
        return -1
