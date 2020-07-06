class Solution:
    def canJump2(self, nums: list) -> bool:
        rememberedNumber = nums[0]
        curIndex = 0
        lastIndex = len(nums)-1
        if len(nums) == 1:
            return True
        if rememberedNumber == 0:
            return False
        else:
            while rememberedNumber>=0:
                if curIndex == lastIndex:
                    return True
                else:
                    rememberedNumber-=1
                    curIndex+=1
                    if nums[curIndex] >rememberedNumber:
                        rememberedNumber = nums[curIndex]
                    if rememberedNumber == 0 and curIndex !=lastIndex:
                        return False
            return False

    def canJump(self, nums: list) -> bool:
        saved =0
        lastIndex = len(nums)-1
        if len(nums) ==1:
            return True
        if nums[0] == 0:
            return False
        for i in range(0,len(nums)):
            if saved <= nums[i]:
                saved = nums[i]+1
            saved-=1
            if saved ==0 and i != lastIndex:
                return False
            if i == lastIndex:
                return True




def test(sol, input, expect):
    ret = sol.canJump(input)
    print('input = {}, expect = {}, output ={}, result = {}'.format(input,expect,ret,ret == expect))


sol = Solution()
test(sol,[2,3,1,1,4], True)
test(sol,[3,2,1,0,4], False)
test(sol,[2,0],True)
test(sol,[1,2,3],True)
test(sol,[1,0,2],False)
test(sol,[2,0,0],True)
test(sol,[0,2,3],False)
test(sol,[3,0,8,2,0,0,1],True)
test(sol,[0],True)
test(sol,[1,0,1,0], False)
test(sol,[5,9,3,2,1,0,2,3,3,1,0,0],True)
test(sol,[4,2,0,0,1,1,4,4,4,0,4,0], True)