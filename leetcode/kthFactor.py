class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        arrayOfFactors =[]
        i = 0
        while i<=n:
            i+=1
            if n%i == 0:
                arrayOfFactors.append(i)
        if k-1>len(arrayOfFactors)-1:
            return -1
        else:
            return arrayOfFactors[k-1]

def test(sol, n:int, k:int, expect:int):
    ret = sol.kthFactor(n,k)
    print('n ={}, k = {}, expect ={}, return = {}, result = {}'.format(n,k,expect,ret,ret==expect))

sol = Solution()
test(sol,12,3,3)
test(sol,7,2,7)
test(sol,4,4,-1)