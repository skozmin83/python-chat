class Solution():
    def maskOf8bit (self, binNumber: str) -> bytes:
        # byt = bytes.fromhex(binNumber)
        # print(byt)
        # return byt
        intBinNumber = int
        for shiftOfMask in range (0,len(binNumber)):
            binMask = 0b00000000 << shiftOfMask
            binInt = int(binNumber)
            addMask = binMask|binInt
            print(bin(addMask))



sol = Solution()
sol.maskOf8bit('111101000010010000000000')