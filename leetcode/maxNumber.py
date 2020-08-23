class Solution:
    def maxNumber(self, nums1: list, nums2: list, k: int) -> list:
        nums1Dict ={}
        nums2Dict ={}
        ret = list()
        for i in range(0,len(nums1)):
            nums1Dict[nums1[i]] = i
        for j in range(0,len(nums2)):
            nums2Dict[nums2[j]] = j
        allNumbers = len(nums1Dict)+len(nums2Dict)
        lastTakenIndexNums1 = 0
        lastTakenIndexNums2 = 0
        while len(ret)<k:
            if allNumbers>=k:
                if nums1Dict !={}:
                    maxInNums1 = max(nums1Dict)
                else:
                    maxInNums1 = 0
                if nums2Dict != {}:
                    maxInNums2 = max(nums2Dict)
                else:
                    maxInNums2 = 0
                if maxInNums1>maxInNums2:
                    if nums1Dict[maxInNums1]<lastTakenIndexNums1:
                        allNumbers-=1
                        del nums1Dict[maxInNums1]
                        continue
                    lastTakenIndexNums1 =nums1Dict[maxInNums1]
                    ret.append(maxInNums1)
                    allNumbers-=1
                    del nums1Dict[maxInNums1]
                elif maxInNums1==maxInNums2:
                    if min(nums1Dict.keys())< min(nums2Dict.keys()):
                        if nums1Dict[maxInNums1] < lastTakenIndexNums1:
                            allNumbers -= 1
                            del nums1Dict[maxInNums1]
                            continue
                        lastTakenIndexNums1 = nums1Dict[maxInNums1]
                        ret.append(maxInNums1)
                        allNumbers -= 1
                        del nums1Dict[maxInNums1]
                    else:
                        if nums2Dict[maxInNums2] < lastTakenIndexNums2:
                            allNumbers -= 1
                            del nums2Dict[maxInNums2]
                            continue
                        lastTakenIndexNums2 = nums2Dict[maxInNums2]
                        ret.append(maxInNums2)
                        allNumbers -= 1
                        del nums2Dict[maxInNums2]
                else:
                    if nums2Dict[maxInNums2]<lastTakenIndexNums2:
                        allNumbers-=1
                        del nums2Dict[maxInNums2]
                        continue
                    lastTakenIndexNums2 = nums2Dict[maxInNums2]
                    ret.append(maxInNums2)
                    allNumbers-=1
                    del nums2Dict[maxInNums2]
            else:
                for key1 in nums1Dict.keys():
                    if nums1Dict[key1]>=lastTakenIndexNums1:
                        if len(ret)<k:
                            ret.append(key1)
                for key2 in nums2Dict.keys():
                    if nums2Dict[key2]>=lastTakenIndexNums2:
                        if len(ret)<k:
                            ret.append(key2)
        return ret


def test(sol, nums1, nums2, k, expect):
    ret = sol.maxNumber(nums1,nums2, k)
    print('nums1 = {}, nums2 = {}, k = {}, expect = {}, output ={}, result = {}'.format(nums1, nums2, k, expect, ret, ret == expect))

sol = Solution()
# test(sol, [3, 4, 6, 5], [9, 1, 2, 5, 8, 3], 5, [9, 8, 6, 5, 3])
# test(sol,[3, 9],[8, 9],3,[9, 8, 9])
test(sol,[6, 7],[6, 0, 4],5,[6, 7, 6, 0, 4])
# test(sol,[8,9],[3,9],3,[9,8,9])
# test(sol,[6,7,5],[4,8,1],3, [8,7,5])
# test(sol,[5,2,2],[6,4,1],3, [6,5,4])