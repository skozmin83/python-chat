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
        forSend = writer.createPicture(MessageType.IMAGE_TO_CLIENT,bytesPicture, bytearray(clientName,'UTF-8'))
        return forSend

    def nameOfReceiver(self, msg: str):
        list = msg.split(':')
        if len(list)>2:
            return list[0]
        else:
            return False

    def sendPicture(self, filePath:str):
        writer = WriterAndReader()
        bytesPicture = b''
        for bc in FileReader.bytesChunkFromFile(filePath):
            bytesPicture += bc
        forSend = writer.createMessage(MessageType.IMAGE, bytesPicture)
        return forSend


# sol =CreatePicture()
# sol.nameOfReceiver('rada: picture:')
# sol.nameOfReceiver(':picture')
# sol.nameOfReceiver('picture:')

