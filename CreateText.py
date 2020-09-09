from WriterAndReader import WriterAndReader
from Constants import MessageType

class CreateText():
    def determineNameOfClient(self,msg: str):
        firstValue = msg[0]
        secondValue = msg[1]
        try:
            int(firstValue)
            itIsName = False
        except:
            try:
                int(secondValue)
                itIsName = False
            except:
                itIsName = True
        forSend = self.sendTextToClient(itIsName,firstValue,msg)
        return forSend

    def sendTextToClient(self, itIsName: bool, firstValue: str, msg: str):
        writer = WriterAndReader()
        if firstValue == ':' or itIsName == False:
            forSend = writer.createMessage(MessageType.TEXT, bytearray(msg,'UTF-8'))
        else:
            forSend = writer.createMessage(MessageType.TEXT_TO_CLIENT, bytearray(msg,'UTF-8'))
        return forSend
