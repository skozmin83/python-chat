class Solution:
    def groupAnagrams(self, strs: list) -> list:
        numbersDict ={}
        for n in range (0, len(strs)):
            if strs[n] in numbersDict:
                numbersDict[strs[n]] +=1
            else:
                numbersDict[strs[n]] = 1
        retArray =[]
        searchArray =[]
        for i in range(0, len(strs)):
            if i != 0:
                tempArray =[]
                for s in range (0, len(searchArray)):
                    if searchArray[s] != 'None':
                        tempArray.append(searchArray[s])
                        numbersDict[searchArray[s]] = 0
                if tempArray != []:
                    retArray.append(tempArray)
                searchArray = []
            for j in range(0, len(strs[i])):
                remembered = strs[i][j]
                if len(searchArray)<1:
                    for k in range(0, len(strs)):
                        if remembered in strs[k] and numbersDict[strs[k]] !=0:
                            searchArray.append(strs[k])
                else:
                    for v in range(0,len(searchArray)):
                        if remembered not in searchArray[v]:
                            searchArray[v] = 'None'
            if i == len(strs)-1 and strs[i] !='':
                numbersDict[strs[i]] = 0
        if len(searchArray)>0:
            tempArray = []
            for s in range(0, len(searchArray)):
                if searchArray[s] != 'None':
                    tempArray.append(searchArray[s])
            retArray.append(tempArray)
        dictArray = []
        for d in numbersDict.keys():
            while numbersDict[d] >0:
                dictArray.append(d)
                numbersDict[d] -=1
        if len(dictArray)>0:
            retArray.append(dictArray)
        return retArray







sol = Solution()
# print(sol.groupAnagrams(["eat","tea","tan","ate","nat","bat"]))
# print(sol.groupAnagrams([""]))
# print(sol.groupAnagrams(["a"]))
# print(sol.groupAnagrams(["",""]))
print(sol.groupAnagrams(["ddddddddddg","dgggggggggg"]))