class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def sumEvenGrandparent(self, root: TreeNode) -> int:
        sum = 0
        even = False
        sum = treeRecursion(root,even,sum)
        return sum

def treeRecursion(TreeRoot: TreeNode, even: bool, sum: int):
    if even == True:
        if TreeRoot.left is not None:
            if TreeRoot.left.val != None:
                sum+= TreeRoot.left.val
        if TreeRoot.right is not None:
            if TreeRoot.right.val != None:
                sum += TreeRoot.right.val
    if TreeRoot.val != None:
        if TreeRoot.val %2 == 0:
            even = True
        else:
            even = False
    if TreeRoot.left is not None:
        sum = treeRecursion(TreeRoot.left,even,sum)
    if TreeRoot.right is not None:
        sum = treeRecursion(TreeRoot.right,even,sum)
    return sum


class Solution1:
    def sumEvenGrandparent(self, root: TreeNode) -> int:
        sum = []
        even = False
        treeRecursion1(root,even,sum)
        allSum =0
        for i in range(0,len(sum)):
            allSum+=sum[i]
        return allSum

def treeRecursion1(TreeRoot: TreeNode, even: bool, sum: list):
    if even == True:
        if TreeRoot.left is not None:
            if TreeRoot.left.val != None:
                sum.append(TreeRoot.left.val)
        if TreeRoot.right is not None:
            if TreeRoot.right.val != None:
                sum.append(TreeRoot.right.val)
    if TreeRoot.val != None:
        if TreeRoot.val %2 == 0:
            even = True
        else:
            even = False
    if TreeRoot.left is not None:
        treeRecursion1(TreeRoot.left,even,sum)
    if TreeRoot.right is not None:
        treeRecursion1(TreeRoot.right,even,sum)




def example (rootNode,node1,node2,node3,node4,node5,node6,node7,node8,node9,node10,node11,node12,node13,node14):
    root = TreeNode(rootNode)
    root.left = TreeNode(node1)
    root.right = TreeNode(node2)
    root.left.left =TreeNode(node3)
    root.left.right = TreeNode(node4)
    root.right.left = TreeNode(node5)
    root.right.right = TreeNode(node6)
    root.left.left.left = TreeNode(node7)
    root.left.left.right = TreeNode(node8)
    root.left.right.left = TreeNode(node9)
    root.left.right.right = TreeNode(node10)
    root.right.left.left = TreeNode(node11)
    root.right.left.right = TreeNode(node12)
    root.right.right.left = TreeNode(node13)
    root.right.right.right = TreeNode(node14)
    return root

def test(sol, inputRoot, expect: int):
    ret = sol.sumEvenGrandparent(inputRoot)
    print('outputSum ={}, root.val = {}, result ={}'.format(ret,inputRoot.val, ret==expect))

sol = Solution()
test(sol,example(6,7,8,2,7,1,3,9,None,1,4,None,None,None,5),18)
