class Solution:
    def canReach(self, arr: list, start: int) -> bool:
        zeroDict = {}
        lenght = len(arr)
        jumpedIndexes = []
        lastIndex = lenght - 1
        for i in range (0, lenght):
            if arr[i] ==0:
                zeroDict[i] = False
        if start+arr[start]> lastIndex:
            curIndexMax = lastIndex
        else:
            curIndexMax = start+arr[start]
        if start-arr[start]<0:
            curIndexMin = 0
        else:
            curIndexMin = start-arr[start]
        jumRecursion(arr,zeroDict,jumpedIndexes,lastIndex,start, curIndexMax,curIndexMin)
        if False in zeroDict.values():
            return False
        else:
            return True
def jumRecursion (arr: list, zeroDict: dict, jumpedIndexes: list, lastIndex: int, curIndex: int, curIndexMax: int,curIndexMin: int):
    if curIndex not in jumpedIndexes:
        jumpedIndexes.append(curIndex)
        if curIndex in zeroDict.keys():
            del zeroDict[curIndex]
        if curIndex < curIndexMax:
            curIndex = curIndex+1
        else:
            if curIndex+arr[curIndex]<=lastIndex:
                curIndexMax = curIndex+arr[curIndex]
            else:
                curIndexMax = lastIndex
        jumRecursion(arr, zeroDict, jumpedIndexes, lastIndex, curIndex, curIndexMax, curIndexMin)
        if curIndex > curIndexMin:
            curIndex =curIndex-1
        else:
            if curIndex - arr[curIndex]>=0:
                curIndexMin = curIndex - arr[curIndex]
            else:
                curIndexMin = 0
        jumRecursion(arr,zeroDict,jumpedIndexes,lastIndex,curIndex,curIndexMax,curIndexMin)


def test(sol, inputArr, start, expect):
    ret = sol.canReach(inputArr, start)
    print('inputArr = {}, startIndex = {}, expect = {}, output ={}, result = {}'.format(inputArr, start,  expect, ret, ret == expect))

sol = Solution()
# test(sol, [4,2,3,0,3,1,2], 5, True)
# test(sol, [3,0,2,1,2],2, False)
test(sol,[0,3,0,6,3,3,4],6, True)
