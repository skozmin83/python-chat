class Solution:
    def toBin (self, number: int):
        lastbit = howMuchbits(number)
        retBinNumber =''
        for shiftOfMask in range (0,lastbit):
            binMask = 0b1 << shiftOfMask
            addMask = binMask&number
            if addMask >0:

                retBinNumber +='1'
            else:
                retBinNumber+='0'
        return retBinNumber[::-1]

def howMuchbits (number: int):
    bit = 1
    countOfBit =0
    if number ==0 or number ==1:
        return 1
    while number>bit:
        bit = bit*2
        countOfBit+=1
    return countOfBit


sol = Solution()
sol.toBin(16000000)
sol.toBin(3)
sol.toBin(1)