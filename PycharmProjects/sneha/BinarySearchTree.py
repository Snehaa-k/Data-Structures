class BST:
    def __init__(self,key):
        self.key = key
        self.lchild = None
        self.rchild = None

    def insert(self,data):
        if self.key is None:
            self.key = data
            return
        if self.key == data:
            return
        if self.key > data:
            if self.lchild:
                self.lchild.insert(data)
            else:
                self.lchild = BST(data)
        else:
            if self.rchild:
                self.rchild.insert(data)
            else:
                self.rchild = BST(data)
    def search(self,data):
        if self.key == data:
            print("node is found")
            return
        if data < self.key:
            if self.lchild:
                self.lchild.search(data)
            else:
                print("node is not present in the tree")
        else:
            if self.rchild:
                self.rchild.search(data)
            else:
                print("node is not present in the tree")



    def preorder(self):
            print(self.key,end = " ")
            if self.lchild:
                self.lchild.preorder()
            if self.rchild:
                self.rchild.preorder()

    def delete(self, data):
        if self is None:
            return self

        if data < self.key:
            if self.lchild:
                self.lchild = self.lchild.delete(data)
            else:
                print("Given Data not found")
        elif data > self.key:
            if self.rchild:
                self.rchild = self.rchild.delete(data)
            else:
                print("Given data not found")
        else:

            if self.lchild is None:
                return self.rchild
            elif self.rchild is None:
                return self.lchild


            n = self.rchild
            while n.lchild:
                n = n.lchild
            self.key = n.key
            self.rchild = self.rchild.delete(n.key)

        return self

    def inorder(self):
        if self.lchild:
            self.lchild.inorder()
        print(self.key,end=" ")
        if self.rchild:
            self.rchild.inorder()

    def postorder(self):
        if self.lchild:
            self.lchild = self.lchild.postorder()
        if self.rchild:
            self.rchild = self.rchild.postorder()
        print(self.key,end=" ")

    def min_value(self):
        n = self
        while n.lchild:
            n = n.lchild
        print("min value = ", n.key)

    def max_value(self):
        n = self
        while n.rchild:
            n = n.rchild
        print("max value =", n.key)

    def delete_root(self):
        if self.lchild is None:
            return self.rchild
        elif self.rchild is None:
            return self.lchild
        else:

            p = self
            n = self.rchild
            while n.lchild:
                p = n
                n = n.lchild

            self.key = n.key

            if p != self:
                p.lchild = n.rchild
            else:
                p.rchild = n.rchild

        return self

    def height(self,node):
        if node is None:
            return False
        return 1 + max(self.height(node.lchild),self.height(node.rchild))

    def is_check(self,node):
        if node is None:
            return False
        left_height = self.height(node.lchild)
        right_height = self.height(node.rchild)
        if abs(left_height-right_height)<=1:
            return self.is_check(node.lchild) and self.is_check(node.rchild)
        return False

    def closest_value(self,root,target):
        closest = self.key
        while root:
            closest = min(root.key,closest,key = lambda x:abs(target-x))
            root = root.lchild if root.key > target else root.rchild
        return closest


    def is_valid(self,root,low=None,high = None):
        if not root:
            return True
        if (low is not None and root.key <=low) or (high is not None and root.key>=high):
            return self.is_valid(root.lchild,low,root.key) and self.is_valid(root.rchild,root.key,high)




tree = BST(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)
tree.insert(60)
tree.insert(80)


# tree.search(90)
# tree.delete(40)
print(tree.is_check(tree))
print("preorder")
tree.preorder()
print()
print("inoder")
tree.inorder()
print()
print("postorder")
tree.postorder()
print()
# tree.min_value()
# tree.max_value()


