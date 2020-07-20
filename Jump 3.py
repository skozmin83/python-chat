class Solution:
    def canReach(self, arr: list, start: int) -> bool:
        zeroDict = {}
        lenght = len(arr)
        jumpedIndexes = []
        lastIndex = lenght - 1
        for i in range (0, lenght):
            if arr[i] ==0:
                zeroDict[i] = False
        nextPosIndex = start
        nextNegIndex = start
        while True:
            if arr[nextPosIndex] == 0:
                zeroDict[nextPosIndex] = True
            if arr[nextNegIndex] == 0:
                zeroDict[nextNegIndex] = True
            if nextPosIndex + arr[nextPosIndex] <=lastIndex:
                nextPosIndex = nextPosIndex+arr[nextPosIndex]
            if nextNegIndex - arr[nextNegIndex]>=0:
                



def test(sol, inputArr, start, expect):
    ret = sol.canReach(inputArr, start)
    print('inputArr = {}, startIndex = {}, expect = {}, output ={}, result = {}'.format(inputArr, start,  expect, ret, ret == expect))

sol = Solution()
test(sol, [4,2,3,0,3,1,2], 5, True)
test(sol, [3,0,2,1,2],2, False)
