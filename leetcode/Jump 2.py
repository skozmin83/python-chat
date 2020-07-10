class Solution:
    def jump(self, nums:list) -> int:
        curIndex =0
        lastIndex = len(nums)-1
        remainder = nums[curIndex]
        minCountOfJump = 0
        return (jumpRecursion(nums,curIndex,remainder,lastIndex,minCountOfJump))

def jumpRecursion(nums:list, curIndex: int, remainder: int, lastIndex: int, minCountOfJump:int):
    minCountOfJump+=1
    if remainder>0:
        remainder-=1
        if curIndex < lastIndex:
            curIndex+=1
            remainder = nums[curIndex]
            if remainder+curIndex<lastIndex:
                minCountOfJump = jumpRecursion(nums,curIndex,remainder,lastIndex,minCountOfJump)
            else:
                minCountOfJump+=1
    return minCountOfJump

def test(sol, input, expect):
    ret = sol.jump(input)
    print('input = {}, expect = {}, output ={}, result = {}'.format(input,expect,ret,ret == expect))

sol = Solution()
test(sol,[2,3,1,1,4], 2)
