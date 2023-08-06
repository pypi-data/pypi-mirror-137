# A Binary Tree Node

class Node:

    # Constructor to create a new node
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST_tree:
    # A utility function to do inorder traversal of BST
    def inorder(self, root):
        if root is not None:
            self.inorder(root.left)
            print(root.key, end=" ")
            self.inorder(root.right)

    def preorder(self, root):
        if root is not None:
            print(root.key, end=" ")
            self.inorder(root.left)
            self.inorder(root.right)

    def postorder(self, root):
        if root is not None:
            self.inorder(root.left)
            self.inorder(root.right)
            print(root.key, end=" ")

    def search(self, root, key):

        # Base Cases: root is null or key is present at root
        if root is None or root.key == key:
            return root

        # Key is greater than root's key
        if root.key < key:
            return self.search(root.right, key)

        # Key is smaller than root's key
        return self.search(root.left, key)

    def findParent(self, node, val, parent) -> None:
        if (node is None):
            return

        # If current node is
        # the required node
        if (node.key == val):

            # Print its parent
            print(parent)
        else:

            # Recursive calls
            # for the children
            # of the current node
            # Current node is now
            # the new parent
            self.findParent(node.left, val, node.key)
            self.findParent(node.right, val, node.key)

    # A utility function to insert a
    # new node with given key in BST

    def insert(self, node, key):

        # If the tree is empty, return a new node
        if node is None:
            return Node(key)

        # Otherwise recur down the tree
        if key < node.key:
            node.left = self.insert(node.left, key)

        else:
            node.right = self.insert(node.right, key)

        # return the (unchanged) node pointer
        return node

    # Given a non-empty binary
    # search tree, return the node
    # with minimum key value
    # found in that tree. Note that the
    # entire tree does not need to be searched

    def minValueNode(self, node):
        current = node

        # loop down to find the leftmost leaf
        while(current.left is not None):
            current = current.left

        return current

    # Given a binary search tree and a key, this function
    # delete the key and returns the new root

    def deleteNode(self, root, key):

        # Base Case
        if root is None:
            return root

        # If the key to be deleted
        # is smaller than the root's
        # key then it lies in  left subtree
        if key < root.key:
            root.left = self.deleteNode(root.left, key)

        # If the kye to be delete
        # is greater than the root's key
        # then it lies in right subtree
        elif(key > root.key):
            root.right = self.deleteNode(root.right, key)

        # If key is same as root's key, then this is the node
        # to be deleted
        else:

            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Node with two children:
            # Get the inorder successor
            # (smallest in the right subtree)
            temp = self.minValueNode(root.right)

            # Copy the inorder successor's
            # content to this node
            root.key = temp.key

            # Delete the inorder successor
            root.right = self.deleteNode(root.right, temp.key)

        return root
