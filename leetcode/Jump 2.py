class Solution:
    def jump(self, nums:list) -> int:
        countOfsteps = 0
        saved = 0
        lastIndex = len(nums)-1

        if len(nums) ==1 or nums[0] ==0:
            return 0
        for i in range(0,len(nums)):
            saved-=1
            if saved <= 0:
                saved = nums[i]
                countOfsteps+=1
            if saved ==0 and i != lastIndex:
                return 0
            if i == lastIndex:
                return countOfsteps
        return countOfsteps




def test(sol, input, expect):
    ret = sol.jump(input)
    print('input = {}, expect = {}, output ={}, result = {}'.format(input,expect,ret,ret == expect))

sol = Solution()
test(sol,[2,3,1,1,4], 2)
# test(sol,[1,2],1)
# test(sol,[2,1],1)
# test(sol,[1,2,3],2)
# test(sol,[2,3,1],1)
# test(sol,[1,2,3,4],2)
