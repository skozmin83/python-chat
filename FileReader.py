
def bytesFromFile(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break

def bytesChunkFromFile(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                yield chunk
            else:
                break

# for b in bytesFromFile('C:/tmp/таня.txt '):
#     print(hex(b))
#
# for bc in bytesChunkFromFile('C:/tmp/таня.txt '):
#     print(bc)