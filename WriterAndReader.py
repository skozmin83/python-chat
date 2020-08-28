from Constants import MessageType

HEADER_LENGTH = 5
EXIT_HEADER_LENGHT = 1

class WriterAndReader():
    maxSize = 2 ** 32
    oneByteMask = 2 ** 8 - 1

    def parseMessageType(self, msg: bytearray) -> MessageType:
        firstByte = chr(msg[0])
        firstByte = ord(firstByte)
        pass
        if firstByte == MessageType.CLIENT_NAME.value:
            return MessageType.CLIENT_NAME.value
        elif firstByte == MessageType.IMAGE.value:
            return MessageType.IMAGE.value
        elif firstByte == MessageType.TEXT.value:
            return MessageType.TEXT.value
        elif firstByte == MessageType.TEXT_TO_CLIENT.value:
            return MessageType.TEXT_TO_CLIENT.value
        elif firstByte == MessageType.EXIT.value:
            return MessageType.EXIT.value
        elif firstByte == MessageType.STATUS.value:
            return MessageType.STATUS.value
        elif firstByte ==MessageType.CLIENTS_ONLINE.value:
            return MessageType.CLIENTS_ONLINE.value



    def parseLen(self, msg:bytearray) -> int:
        savedNumber = 0
        lenght = 0
        for i in range(1,5):
            if msg[i] !=0:
                numberWithMask = msg[i] & self.oneByteMask
                if savedNumber !=0:
                    numberWithMask = savedNumber | numberWithMask
                if i !=4:
                    numberWithMask = numberWithMask << 8
                    savedNumber = numberWithMask
                lenght = int(numberWithMask)
        return lenght

    def parseMessage(self,msgType: MessageType, msg: bytearray) -> bytes:
        if msgType == MessageType.CLIENT_NAME.value or msgType == MessageType.IMAGE.value or msgType == MessageType.TEXT.value or msgType ==MessageType.TEXT_TO_CLIENT.value or msgType == MessageType.CLIENTS_ONLINE.value:
            byteArray = msg[HEADER_LENGTH:]
        elif msgType == MessageType.STATUS.value:
            byteArray = msg[HEADER_LENGTH:]
        else:
            byteArray = msg[EXIT_HEADER_LENGHT:]
        bytesMsg = bytes(byteArray)
        return bytesMsg

    def createMessage(self, msgType: MessageType, msg: bytearray) -> bytearray:
        b = bytearray(1 + 4)
        self.writeNumber(b, msgType.value, 0)
        self.writeNumber(b, len(msg), 1)
        # offset = 1 + 4
        # idx = 0
        # while idx < len(msg):
        # newByteArray = b+msg
        retArray = b + msg
            # idx +=1
        return retArray

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
# sol.writeNumber(bytearray(b'\x01\x00\x00\x00\x00\x00'), 1324, 1)
# sol.parseLen(msg=bytearray(b'\x01\x00\x00\x05\x06\x00t\x00a\x00n\x00y\x00a'))
# buf = bytearray(100)
# # sol.writeNumber(buf, 12, 1)
# mes = sol.createMessage(msgType=MessageType.CLIENT_NAME, msg=bytearray('tanya','UTF-8'))
# sol.parseMessage(MessageType.CLIENT_NAME,5,mes)
# print(sol.writeNumber(buf, 16777219, 1)) #bytearray(b'\x00\x01\x00\x00\x01\x00\
# sol.writeNumber(buf, 1234, 1)
# sol.parseMessage(msgType=MessageType.CLIENT_NAME,msg=bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'))
