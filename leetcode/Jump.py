class Solution:
    def canJump(self, nums: list) -> bool:
        lastIndex = len(nums)-1
        curIndex = 0
        loopDictionary = {}
        step = 0
        ret = jumpRecursion(nums,curIndex,lastIndex,loopDictionary)
        return ret

def jumpRecursion(nums: list, curIndex: int, lastIndex:int, loopDictionary: dict):
   step =0
   nowIndex = curIndex
   if curIndex not in loopDictionary.keys():
       loopDictionary[curIndex] = 1
       if curIndex != lastIndex:
           while step<nums[nowIndex]:
               step+=1
               curIndex+=1
               if curIndex == lastIndex:
                   return True
           if nowIndex != lastIndex-1 and nums[nowIndex] !=0:
              ret = jumpRecursion(nums,nowIndex+1,lastIndex,loopDictionary)
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
