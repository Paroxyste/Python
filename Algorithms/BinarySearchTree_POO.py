#------------------------------------------------------------------------------
# Name : Binary Search Tree
# Author: paroxyste
#------------------------------------------------------------------------------

class Node(object) :
    def __init__(self, val) :
        self.l_child = None
        self.r_child = None
        self.val = val

class BinarySearchTree(object) :
    def insert(self, root, node) :
        if root is None :
            return node
        if root.val < node.val :
            root.r_child = self.insert(root.r_child, node)
        else :
            root.l_child = self.insert(root.l_child, node)

        return root

    def in_order_place(self, root) :
        if not root:
            return None
        else :
            self.in_order_place(root.l_child)
            print(root.val)

            self.in_order_place(root.r_child)

    def pre_order_place(self, root) :
        if not root :
            return None
        else :
            print(root.val)
            self.pre_order_place(root.l_child)
            self.pre_order_place(root.r_child)

    def post_order_place(self, root) :
        if not root :
            return None
        else :
            self.post_order_place(root.l_child)
            self.post_order_place(root.r_child)
        print(root.val)
