class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        treeRoot=root
        maxVal = root.val
        countGoodNodes = 0
        count = searchGoodNodeRecursion(treeRoot,maxVal,countGoodNodes)
        print(count)
        return count

def searchGoodNodeRecursion(treeRoot: TreeNode, maxVal: int, countGoodNodes:int):
    if treeRoot.val is not None:
        if treeRoot.val >= maxVal:
            countGoodNodes +=1
        maxVal = max(maxVal,treeRoot.val)
    if treeRoot.left is not None:
        countGoodNodes = searchGoodNodeRecursion(treeRoot.left,maxVal,countGoodNodes)
    if treeRoot.right is not None:
        countGoodNodes = searchGoodNodeRecursion(treeRoot.right,maxVal,countGoodNodes)
    return countGoodNodes

def example(root, node2, node3, node4, node5):
    treeRoot = TreeNode(root)
    treeNode2 = TreeNode(node2)
    treeNode3 = TreeNode(node3)
    treeNode4 = TreeNode(node4)
    treeNode5 = TreeNode(node5)
    treeRoot.left = treeNode2
    treeRoot.right = treeNode3
    treeNode2.left = treeNode4
    treeNode2.right = treeNode5
    return treeRoot


sol = Solution()
sol.goodNodes(example(3,3,None,4,2))

class Sum:
    def __init__(self,s):
        self.s = s

res = Sum(5)

def sum (res: Sum):
    res.s = res.s+2

sum(res)
