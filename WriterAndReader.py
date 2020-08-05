from Constants import MessageType


class WriterAndReader():
    maxSize = 2 ** 32
    oneByteMask = 2 ** 8 - 1

    def parseMessageType(self, msg: bytearray) -> MessageType:
        firstByte = msg[0]
        if firstByte == 1:
            return MessageType.CLIENT_NAME
        elif firstByte == 2:
            return MessageType.IMAGE
        elif firstByte == 3:
            return MessageType.TEXT
        elif firstByte == 4:
            return MessageType.TEXT_TO_CLIENT
        elif firstByte == 5:
            return MessageType.EXIT
        elif firstByte == 6:
            return MessageType.STATUS
        elif firstByte ==7:
            return MessageType.CLIENTS_ONLINE

    def parseLen(self, msg:bytearray) -> int:
        lenght = 0
        if msg[4] !=0:
            lenght+=msg[4]
        if msg[3] !=0:
            lenght+=msg[3]
        if msg[2] !=0:
            lenght+=msg[2]
        if msg[1] !=0:
            lenght+=msg[1]
        return lenght


    def parseMessage(self,msgType: MessageType, msg: bytearray) -> bytes:
        if msgType.value == 1 or msgType.value == 2 or msgType.value == 3 or msgType.value == 4:
            ByteArray = msg[5:]
        else:
            ByteArray = msg[1:]
        bytesMsg = bytes(ByteArray)
        return bytesMsg


    def createMessage(self, msgType: MessageType, msg: bytearray) -> bytearray:
        b = bytearray(1 + 4 + len(msg))
        self.writeNumber(b, msgType.value, 0)
        self.writeNumber(b, len(msg), 1)
        offset = 1 + 4
        idx = 0
        correctIdx = 1
        while idx < len(msg):
            b.append(0)
            b[offset + correctIdx+ idx] = msg[idx]
            idx += 1
            correctIdx+=1
        return b

    def writeNumber(self, buf: bytearray, toWrite: int, position: int) -> bytearray:
        if toWrite > self.maxSize:
            raise RuntimeError("Size of {} is too big. Max size {}".format(toWrite, position))
        curNum = toWrite
        step = 3
        if buf[0] != 0:
            while curNum > 0:
                curByte = curNum & self.oneByteMask
                buf[position + step] = curByte
                curNum = curNum >> 8
                step -= 1
        else:
            buf[0] = toWrite
            return buf

    # def readNumber(self, buf: bytearray, position: int, numberOfBytes:int) -> int:
    #     pass

# sol = WriterAndReader()
# sol.parseMessage(msgType=MessageType.CLIENT_NAME,msg=bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'))
# sol.parseMessageType(msg=bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'))
# # buf = bytearray(100)
# # sol.writeNumber(buf, 12, 1)
# mes = sol.createMessage(msgType=MessageType.CLIENT_NAME, msg=bytearray('tanya','UTF-8'))
# sol.parseMessage(MessageType.CLIENT_NAME,5,mes)
# # print(sol.writeNumber(buf, 16777219, 1)) #bytearray(b'\x00\x01\x00\x00\x01\x00\
# # sol.writeNumber(buf, 2**33, 1)
