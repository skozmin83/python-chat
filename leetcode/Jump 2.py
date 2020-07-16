class Solution:
#     def jump2(self, nums:list) -> int:
#         if nums[0] ==0 or len(nums) ==1:
#             return 0
#         lastIndex = len(nums)-1
#         stepsArray =[]
#         retArray = jumpRecursion(nums,0,lastIndex,0,stepsArray)
#         return min(retArray)
# def jumpRecursion(nums:list,curIndex:int,lastIndex:int, countOfSteps:int, stepsArray:list):
#     countOfSteps+=1
#     if curIndex+nums[curIndex]<lastIndex:
#         saved = nums[curIndex]
#         while saved>0:
#             curIndex+=1
#             saved-=1
#             jumpRecursion(nums,curIndex,lastIndex,countOfSteps,stepsArray)
#     else:
#         stepsArray.append(countOfSteps)
#     return stepsArray

    def jump(self, nums: list) -> int:
        if nums[0] == 0 or len(nums) == 1:
            return 0
        lastIndex = len(nums)-1
        curIndex = 0
        indexOfMax = 0
        maxNum =0
        countOfSteps =0
        saved = nums[curIndex]
        if curIndex<lastIndex:
            while True:
                if curIndex+saved<lastIndex:
                    countOfSteps +=1
                    while saved>0:
                        saved-=1
                        curIndex+=1
                        if maxNum<=nums[curIndex]:
                            maxNum = nums[curIndex]
                            indexOfMax =curIndex
                    else:
                        saved = maxNum
                        maxNum =0
                        curIndex =indexOfMax

                else:
                    countOfSteps+=1
                    return countOfSteps






def test(sol, input, expect):
    ret = sol.jump(input)
    print('input = {}, expect = {}, output ={}, result = {}'.format(input,expect,ret,ret == expect))

sol = Solution()
# test(sol,[2,3,1,1,4], 2)
# test(sol,[1,2],1)
# test(sol,[2,1],1)
# test(sol,[1,2,3],2)
# test(sol,[2,3,1],1)
# test(sol,[1,2,3,4],2)
# test(sol,[1,1,1,1],3)
# test(sol,[3,4,3,2,5,4,3],3)
# test(sol,[1,2,1,1,1],3)
test(sol,[10,9,8,7,6,5,4,3,2,1,1,0],2)
