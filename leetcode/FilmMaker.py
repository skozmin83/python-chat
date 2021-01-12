import os
import time
import Logging

logger = Logging.getConsoleLogger()
SIZE_128MB = 2**17
SIZE_1MB = 2 ** 20
class Film():
    def getTime(self):
        return time.time()

    def filmCode(self, fileInPath, fileOutPath, chunksize=64):
        counter = 0
        p1 = 0
        fileIn = open(fileInPath, "rb")
        fileInSize = os.path.getsize(fileInPath)
        fileOut = open(fileOutPath, 'wb+')
        p1T = self.getTime()
        while True:
            counter += 1
            if counter % SIZE_128MB == 0:
                logger.info('{} mb of {}'.format(counter * chunksize / SIZE_1MB, fileInSize / SIZE_1MB))
            chunkIn = fileIn.read(chunksize*2)
            chunkOne = chunkIn[0:chunksize]
            chunkTwo = chunkIn[chunksize:chunksize*2]
            if chunkOne:
                if chunkTwo:
                    fileOut.write(chunkTwo)
                    fileOut.write(chunkOne)
                else:
                    fileOut.write(chunkOne)
            else:
                break

        p2T = self.getTime()
        fileOut.close()
        fileIn.close()
        p1 += (p2T - p1T)



    def filmDecode(self, fileInPath, fileOutPath, chunksize=64):
        fileInSize = os.path.getsize(fileInPath)
        remainder = fileInSize%chunksize
        counter = 0
        p1 = 0
        fileIn = open(fileInPath, "rb")
        fileOut = open(fileOutPath, 'wb+')
        p1T = self.getTime()
        while True:
            counter += 1
            if counter % SIZE_128MB == 0:
                logger.info('{} mb of {}'.format(counter * chunksize / SIZE_1MB, fileInSize / SIZE_1MB))
            chunkIn = fileIn.read(chunksize*2)
            if len(chunkIn)<chunksize*2:
                chunkOne = chunkIn[0:remainder]
                chunkTwo = chunkIn[remainder:chunksize*2]
                if chunkOne:
                    if chunkTwo:
                        fileOut.write(chunkTwo)
                        fileOut.write(chunkOne)
                    else:
                        fileOut.write(chunkOne)
                else:
                    break
            else:
                chunkOne = chunkIn[0:chunksize]
                chunkTwo = chunkIn[chunksize:chunksize*2]
                if chunkOne:
                    if chunkTwo:
                        fileOut.write(chunkTwo)
                        fileOut.write(chunkOne)
                    else:
                        fileOut.write(chunkOne)
                else:
                    break

        p2T = self.getTime()
        fileOut.close()
        fileIn.close()
        p1 += (p2T - p1T)

        logger.info('time = {} seconds'.format(p1))
        logger.info('{} mb per second'.format(((fileInSize/SIZE_1MB)/ (p1))))

logger.info('start')

fi = Film()
fileInPath = 'C:/Users/tanya/Downloads/A Sound of Thunder.avi'
print(fi.filmCode(fileInPath, fileInPath + '.new.avi', 16))
print(fi.filmDecode(fileInPath + '.new.avi', fileInPath + '.changed.avi', 16))

# fileInPath = 'C:/Users/tanya/Downloads/a.txt'
# fi.filmCode(fileInPath, fileInPath + '.new.txt')
# fi.filmCode(fileInPath + '.new.txt', fileInPath + '.changed.txt')

# fileInPath = 'C:/Users/tanya/Downloads/b.txt'
# fi.filmCode(fileInPath, fileInPath + '.new.txt')
# fi.filmDecode(fileInPath + '.new.txt', fileInPath + '.changed.txt')

# fileInPath = 'C:/Users/tanya/Downloads/Tourist.mkv'
# fi.filmCode(fileInPath, fileInPath + '.new.mkv', 16)
# fi.filmDecode(fileInPath + '.new.mkv', fileInPath + '.changed.mkv', 16)


# fileInPath = 'C:/Users/tanya/Downloads/c.txt'
# fi.filmCode(fileInPath, fileInPath + '.new.txt')
# fi.filmDecode(fileInPath + '.new.txt', fileInPath + '.changed.txt')

# fileInPath = 'C:/Users/tanya/Downloads/d.txt'
# fi.filmCode(fileInPath, fileInPath + '.new.txt')
# fi.filmDecode(fileInPath + '.new.txt', fileInPath + '.changed.txt')


# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',32))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',64))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',128))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',256))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',512))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',1024))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',2048))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',4096))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',8192))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',16384))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',32768))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',65536))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',131072))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',262144))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',524288))
# print(fi.bytesFromFile(fileInPath, fileInPath + '.new.avi',1048576))
logger.info('done')