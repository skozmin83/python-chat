class Solution:
    def canJump(self, nums: list) -> bool:
        lastIndex = len(nums)-1
        curIndex = 0
        if len(nums) == 1:
            return True
        if nums[curIndex] ==0:
            return False
        loopDictionary = {}
        ret = jumpRecursion(nums,curIndex,lastIndex,loopDictionary,curIndex)
        return ret

def jumpRecursion(nums: list, curIndex: int, lastIndex:int, loopDictionary: dict, beforeCurIndex:int):
   step =0
   maxValInJump =0
   savedIndex =0
   nowIndex = curIndex
   if curIndex not in loopDictionary.keys():
       loopDictionary[curIndex] = 1
       if curIndex != lastIndex:
           while step<nums[nowIndex]:
               step+=1
               curIndex+=1
               if maxValInJump<=nums[curIndex]:
                   savedIndex = curIndex
                   maxValInJump = nums[curIndex]
               if curIndex == lastIndex:
                   return True
           if nowIndex != lastIndex-1:
                if maxValInJump ==0:
                    if nums[beforeCurIndex]>nums[curIndex]:
                        nums[savedIndex] = nums[beforeCurIndex]-savedIndex
                        ret = jumpRecursion(nums,beforeCurIndex,lastIndex,loopDictionary,0)
                    else:
                        return False
                else:
                    ret = jumpRecursion(nums,savedIndex,lastIndex,loopDictionary,curIndex)
           else:
               ret = False
       else:
           return True
   else:
       return False
   return ret

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