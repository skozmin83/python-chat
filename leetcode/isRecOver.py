class Solution:
    def isRectangleOverlap(self, rec1: list, rec2: list) -> bool:
        flag = False
        if rec1[0] == rec1[2] or rec2[0] == rec2[2]:
           return False
        if rec1[1] == rec1[3] or rec2[1] == rec2[3]:
           return False
        if rec2[0]>rec1[0] and rec2[0]  < rec1[2]:
            flag = True
        if rec2[2] > rec1[0] and rec2[2] < rec1[2]:
            flag =True
        if rec2[0] < rec1[0] and rec2[0] > rec1[2]:
            flag = True
        if rec2[2] < rec1[0] and rec2[2] > rec1[2]:
            flag = True
        if rec2[2] >= rec1[0] and rec2[2] >= rec1[2] and rec2[0] < rec1[0] and rec2[0] < rec1[2]:
            flag = True
        if rec2[0] >= rec1[0] and rec2[0] >= rec1[2] and rec2[2] < rec1[0] and rec2[2] < rec1[2]:
            flag = True
        if flag == True:
            if rec2[1] >= rec1[1] and rec2[1] <= rec1[3]:
                return True
            if rec2[3] >= rec1[1] and rec2[3] <= rec1[3]:
                return True
            if rec2[1] <= rec1[1] and rec2[1] >= rec1[3]:
                return True
            if rec2[3] <= rec1[1] and rec2[3] >= rec1[3]:
                return True
            if rec2[3]>=rec1[1] and rec2[3]>=rec1[3] and rec2[1] < rec1[1] and rec2[1] < rec1[3]:
                return True
            if rec2[1] >= rec1[1] and rec2[1] >= rec1[3] and rec2[3] < rec1[1] and rec2[3] < rec1[3]:
                return True
            return False
        return False




#         dict ={'x1': [], 'y1':[], 'x2':[], 'y2':[]}
#         for number in range (rec1[0]+1, rec1[2]):
#             dict['x1'].append(number)
#         for number in range(rec1[1] + 1, rec1[3]):
#             dict['y1'].append(number)
#         for number in range (rec2[0]+1, rec2[2]):
#             dict['x2'].append(number)
#         for number in range (rec2[1]+1, rec1[3]):
#             dict['y2'].append(number)
#         print(dict)
#         if dict['x1'] and dict['y1']:
#             for i in dict['x1']:
#                 for j in dict['y1']:
#                     if i == j:
#                         return True
#             return False
#         if dict['x2'] and dict['y2']:
#             for i in dict['x2']:
#                 for j in dict['y2']:
#                     if i == j:
#                         return True
#             return False
#         return False
        # if dict['x1'] and dict['y1'] or dict['x2'] and dict['y2']:
        #     return True
        # else:
        #     return False
sol = Solution()
print(sol.isRectangleOverlap(rec1 = [0,0,2,2], rec2 = [1,1,3,3]))
print(sol.isRectangleOverlap(rec1 = [0,0,1,1], rec2 = [1,0,2,1]))
print(sol.isRectangleOverlap(rec1 = [0,0,1,1], rec2 = [2,2,3,3]))
print(sol.isRectangleOverlap([8,20,12,20],[14,2,19,11]))
print(sol.isRectangleOverlap([7,8,13,15],[10,8,12,20]))
print(sol.isRectangleOverlap([2,17,6,20], [3,8,6,20]))
print(sol.isRectangleOverlap([4,4,14,7],[4,3,8,8])) #true
print(sol.isRectangleOverlap([-6,-10,9,2],[0,5,4,8])) #false
print(sol.isRectangleOverlap([229,-132,833,333],[-244,-577,837,804])) #true
print(sol.isRectangleOverlap([-1,0,1,1],[0,-1,0,1])) #false
print(sol.isRectangleOverlap([-1,0,1,0],[0,-1,1,1])) #false
