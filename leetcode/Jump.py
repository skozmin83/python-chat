class Solution:
    def canJump(self, nums: list) -> bool:
        lastIndex = len(nums)-1
        curIndex = 0
        loopDictionary = {}
        ret = jumpRecursion(nums,curIndex,lastIndex,loopDictionary)
        return ret

def jumpRecursion(nums: list, curIndex: int, lastIndex:int, loopDictionary: dict):
    if curIndex >lastIndex:
        curIndex = lastIndex-curIndex-1
    if curIndex not in loopDictionary.keys():
        loopDictionary[curIndex] = 1
    else:
        return False
    if curIndex != lastIndex:
        curIndexPositive = curIndex + nums[curIndex]
        if curIndexPositive>lastIndex:
            curIndexPositive = abs(lastIndex-curIndexPositive)-1
        curIndexNegative = curIndex - nums[curIndex]
        if curIndexNegative < 0:
            curIndexNegative = lastIndex - nums[curIndex]+1
        if curIndexPositive != lastIndex:
           retPos = jumpRecursion(nums, curIndexPositive, lastIndex, loopDictionary)
        else:
            return True
        if curIndexNegative != lastIndex:
            retNeg = jumpRecursion(nums,curIndexNegative,lastIndex,loopDictionary)
        else:
            return True
    else:
        return True
    return retPos or retNeg


def test(sol, input, expect):
    ret = sol.canJump(input)
    print('input = {}, expect = {}, output ={}, result = {}'.format(input,expect,ret,ret == expect))


sol = Solution()
test(sol,[2,3,1,1,4], True)
test(sol,[3,2,1,0,4], False)
test(sol,[2,0],True)
test(sol,[1,2,3],True)
