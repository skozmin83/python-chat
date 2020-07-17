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
                    maxStep = i+nums[i]
                    if stepsDict[lenght+maxStep] !=0:
                        countOfSteps =1+stepsDict[lenght+maxStep]
                        stepsDict[lenght+i] =countOfSteps
                    else:
                        stepsDict[lenght+i] =0
                else:
                    stepsDict[lenght+i] = 0
            print(stepsDict)
        minStep = 999999999999
        if len(stepsDict)>1 and stepsDict[0] !=1:
            for j in range (1,nums[0]+1):
                if stepsDict[j]<minStep and stepsDict[j] !=0:
                    minStep = stepsDict[j]
            return minStep+1
        else:
            return stepsDict[0]







# class Solution:
#     def jump(self, nums:list) -> int:
#         if nums[0] ==0 or len(nums) ==1:
#             return 0
#         lastIndex = len(nums)-1
#         stepsArray =[9999999999999999]
#         retArray = jumpRecursion(nums,0,lastIndex,0,stepsArray)
#         return retArray[0]
# def jumpRecursion(nums:list,curIndex:int,lastIndex:int, countOfSteps:int, stepsArray:list):
#     countOfSteps+=1
#     if curIndex+nums[curIndex]<lastIndex:
#         saved = nums[curIndex]
#         while saved>0:
#             curIndex+=1
#             saved-=1
#             jumpRecursion(nums,curIndex,lastIndex,countOfSteps,stepsArray)
#     else:
#         if countOfSteps<stepsArray[0]:
#             stepsArray[0] = countOfSteps
#     return stepsArray
#
#

    # def jump(self, nums: list) -> int:

        # if nums[0] == 0 or len(nums) == 1:
        #     return 0
        # lastIndex = len(nums)-1
        # curIndex = 0
        # indexOfMax = 0
        # maxNum =0
        # countOfSteps =0
        # saved = nums[curIndex]
        # if curIndex<lastIndex:
        #     while True:
        #         if curIndex+saved<lastIndex:
        #             countOfSteps +=1
        #             while saved>0:
        #                 saved-=1
        #                 curIndex+=1
        #                 if maxNum<=nums[curIndex]:
        #                     maxNum = nums[curIndex]
        #                     indexOfMax =curIndex
        #             else:
        #                 saved = maxNum
        #                 maxNum =0
        #                 curIndex =indexOfMax
        #
        #         else:
        #             countOfSteps+=1
        #             return countOfSteps
        #





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
