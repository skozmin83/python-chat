from Constants import MessageType


class WriterAndReader():
    maxSize = 2 ** 32
    oneByteMask = 2 ** 8 - 1

    def parseMessageType(self, msg: bytearray) -> MessageType:
        pass
    def parseMessage(self, msg: bytearray) -> bytearray:
        pass

    def createMessage(self, msgType: MessageType, msg: bytearray) -> bytearray:
        b = bytearray(1 + 4 + len(msg))
        self.writeNumber(b, msgType.value, 0)
        self.writeNumber(b, len(msg), 1)
        offset = 1 + 4
        idx = 0
        while idx < len(msg):
            b[idx + offset] = msg[idx]
            idx += 1
        return b

    def writeNumber(self, buf: bytearray, toWrite: int, position: int) -> bytearray:
        if toWrite > self.maxSize:
            raise RuntimeError("Size of {} is too big. Max size {}".format(toWrite, position))
        curNum = toWrite
        step = 3
        while curNum > 0:
            curByte = curNum & self.oneByteMask
            buf[position + step] = curByte
            curNum = curNum >> 8
            step -= 1
        return buf

    def readNumber(self, buf: bytearray, position: int, numberOfBytes:int) -> int:
        pass

# sol = WriterAndReader()
# buf = bytearray(100)
# sol.writeNumber(buf, 12, 1)
# print(sol.writeNumber(buf, 16777219, 1)) #bytearray(b'\x00\x01\x00\x00\x01\x00\
# sol.writeNumber(buf, 2**33, 1)
