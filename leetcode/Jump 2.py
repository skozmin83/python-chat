class Solution:
    def jump(self, nums:list) -> int:
        if nums[0] == 0 or len(nums) == 1:
            return 0
        stepsDict ={}
        lenght = len(nums)
        lastIndex =-1
        for i in range(-2, -lenght-1,-1):
            if nums[i]+i>=lastIndex:
                countOfSteps =1
                stepsDict[lenght+i] = countOfSteps
            else:
                if nums[i] !=0:
                    maxIndex = i+nums[i]
                    minCount =999999999999
                    if stepsDict[lenght+maxIndex] !=1:
                        for index in range(maxIndex,i,-1):
                            if stepsDict[index+lenght]!=0 and stepsDict[index+lenght]<minCount:
                                minCount= stepsDict[index+lenght]
                                maxIndex = index
                            else:
                                continue
                    if nums[maxIndex] == 0:
                        stepsDict[lenght+i] =0
                    else:
                        if stepsDict[lenght+maxIndex] !=0:
                            countOfSteps=1+stepsDict[lenght+maxIndex]
                        else:
                            countOfSteps =0
                        stepsDict[lenght+i] =countOfSteps

                else:
                    stepsDict[lenght+i] = 0
        return stepsDict[0]





def test(sol, input, expect):
    ret = sol.jump(input)
    print('input = {}, expect = {}, output ={}, result = {}'.format(input,expect,ret,ret == expect))

sol = Solution()
test(sol,[2,3,1,1,4], 2)
test(sol,[1,2],1)
test(sol,[2,1],1)
test(sol,[1,2,3],2)
test(sol,[2,3,1],1)
test(sol,[1,2,3,4],2)
test(sol,[1,1,1,1],3)
test(sol,[3,4,3,2,5,4,3],3)
test(sol,[1,2,1,1,1],3)
test(sol,[10,9,8,7,6,5,4,3,2,1,1,0],2)
test(sol,[2,3,0,1,4],2)
test(sol,[5,9,3,2,1,0,2,3,3,1,0,0],3)
test(sol,[5,4,0,1,3,6,8,0,9,4,9,1,8,7,4,8],3)
test(sol,[2,3,5,9,0,9,7,2,7,9,1,7,4,6,2,1,0,0,1,4,9,0,6,3],5)