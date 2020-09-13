from Constants import MessageType

HEADER_LENGTH = 5
EXIT_HEADER_LENGHT = 1

class WriterAndReader():

    maxSize = 2 ** 32
    maxSizeForReceiver = 2**8
    maxSizeForPicture = 2**24
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
        elif firstByte ==MessageType.IMAGE_TO_CLIENT.value:
            return MessageType.IMAGE_TO_CLIENT.value


    def parseLenReceiver(self, msg:bytearray) -> int:
        numberWithMask = msg[1] & self.oneByteMask
        lenght = int(numberWithMask)
        return lenght


    def parseLenPicrture(self, msg:bytearray) -> int:
        savedNumber = 0
        lenght = 0
        for i in range(2,5):
            if msg[i] !=0:
                numberWithMask = msg[i] & self.oneByteMask
                if savedNumber !=0:
                    numberWithMask = savedNumber | numberWithMask
                if i !=4:
                    numberWithMask = numberWithMask << 8
                    savedNumber = numberWithMask
                lenght = int(numberWithMask)
        return lenght

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
        if msgType != MessageType.EXIT.value:
            byteArray = msg[HEADER_LENGTH:]
        else:
            byteArray = msg[EXIT_HEADER_LENGHT:]
        bytesMsg = bytes(byteArray)
        return bytesMsg

    def parsePictureReceiver(self, msg: bytearray, lenOfName: int) -> bytes:
        delHeader = msg[HEADER_LENGTH:]
        name = delHeader[:lenOfName]
        ret = bytes(name)
        return ret

    def parsePicture(self, msg: bytearray, lenOfName: int) -> bytes:
        delHeader = msg[HEADER_LENGTH:]
        pic = delHeader[lenOfName:]
        ret = bytes(pic)
        return ret

    def createMessage(self, msgType: MessageType, msg: bytearray) -> bytearray:
        b = bytearray(1 + 4 + len(msg))
        self.writeNumber(b, msgType.value, 0)
        self.writeNumber(b, len(msg), 1)
        offset = 1 + 4
        idx = 0
        while idx < len(msg):
            b[offset+idx] = msg[idx]
            idx +=1
        return b

    def createPicture(self, msgType: MessageType, msg: bytearray, clientName:bytearray) -> bytearray:
        b = bytearray(1 + 1 + 3 + len(msg) + len(clientName))
        self.writeNumberPicture(b, msgType.value, 0)
        if len(clientName)> self.maxSizeForReceiver:
            raise RuntimeError("Size of {} is too big".format(len(clientName)))
        if len(msg)> self.maxSizeForPicture:
            raise RuntimeError("Size of {} is too big".format(len(msg)))
        self.writeNumberPicture(b, len(clientName), 1)
        self.writeNumberPicture(b,len(msg),1)
        offset = 1 + 1 + 3
        idx = 0
        while idx < len(clientName):
            b[offset+idx] = clientName[idx]
            idx +=1
        index = 0
        idx +=5
        while index < len(msg):
            b[idx] = msg[index]
            idx +=1
            index+=1
        return b

    def writeNumberPicture(self, buf: bytearray, toWrite: int, position: int) -> bytearray:
        if toWrite > self.maxSize:
            raise RuntimeError("Size of {} is too big. Max size {}".format(toWrite, position))
        curNum = toWrite
        step = 3
        if buf[0] != 0 and buf[1] !=0:
            while curNum > 0:
                curByte = curNum & self.oneByteMask
                buf[position + step] = curByte
                curNum = curNum >> 8
                step -= 1
        else:
            if buf[0] ==0:
                buf[0] = toWrite
            elif buf[1] ==0:
                buf[1] = toWrite
        return buf


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


# sol = WriterAndReader()
# sol.createMessage(MessageType.IMAGE,msg=bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'))
# sol.createPicture(MessageType.IMAGE_TO_CLIENT,bytearray(b'\x00p\x00i\x00c\x00t\x00u\x00r\x00e'),bytearray(b'\x00t\x00a\x00n\x00y\x00a'))
# sol.writeNumberPicture(bytearray(b'\x01\x00\x00\x00\x00\x00'), 1324, 1)
# sol.parseLen(msg=bytearray(b'\x01\x00\x00\x05\x06\x00t\x00a\x00n\x00y\x00a'))
# buf = bytearray(100)
# # sol.writeNumber(buf, 12, 1)
# mes = sol.createMessage(msgType=MessageType.CLIENT_NAME, msg=bytearray('tanya','UTF-8'))
# sol.parsePicture(bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'),1)
# sol.parsePictureReceiver(bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'),1)
# print(sol.writeNumber(buf, 16777219, 1)) #bytearray(b'\x00\x01\x00\x00\x01\x00\
# sol.writeNumber(buf, 1234, 1)
# sol.parseMessage(msgType=MessageType.CLIENT_NAME,msg=bytearray(b'\x01\x00\x00\x00\x05\x00t\x00a\x00n\x00y\x00a'))
