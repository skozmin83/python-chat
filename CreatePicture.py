from tkinter import filedialog
import FileReader
from WriterAndReader import WriterAndReader
from Constants import MessageType

class CreatePicture():
    def openPicture (self):
        filePath = filedialog.askopenfilename()
        if not filePath:
            return False
        return filePath

    def sendPicToClient (self, clientName: str, filePath:str):
        writer = WriterAndReader()
        bytesPicture = b''
        for bc in FileReader.bytesChunkFromFile(filePath):
            bytesPicture+=bc
        if clientName == '':
            forSend = writer.createMessage(MessageType.IMAGE, bytesPicture)
        else:
            forSend = writer.createMessage(MessageType.IMAGE_TO_CLIENT,bytesPicture)
        return forSend

    def sendNameOfReceiver(self, clientName: str):
        writer = WriterAndReader()
        clientName = bytes(clientName, 'UTF-8')
        nameForSend = writer.createMessage(MessageType.RECEIVER, bytearray(clientName))
        return nameForSend

