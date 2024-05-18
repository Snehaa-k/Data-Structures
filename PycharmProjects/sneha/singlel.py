# single Linked List


class Node:
    def __init__(self, data):
        self.data = data
        self.ref = None

class LinkedList:
    def __init__(self):
        self.head = None

    def p_ll(self):
        if not self.head:
            print("LinkedList is empty!")
        else:
            n = self.head
            while n is not None:
                print(n.data, "--->", end=" ")
                n = n.ref
    def add_begin(self, data):
        new_node = Node(data)
        new_node.ref = self.head
        self.head = new_node

    def add_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            n = self.head
            while n.ref is not None:
                n = n.ref
            n.ref = new_node

    def add_after(self, data, x):
        n = self.head
        while n is not None:
            if x == n.data:
                break
            n = n.ref
        if n is None:
            print(" not present in the linkedlist ")
        else:
            new_node = Node(data)
            new_node.ref = n.ref
            n.ref = new_node

    def add_before(self, data, x):
        if self.head is None:
            print(" linkedlist is empty")
            return
        if self.head.data == x:
            new_node = Node(data)
            new_node.ref = self.head
            self.head = new_node
            return
        n = self.head
        while n.ref is not None:
            if n.ref.data == x:
                break
            n = n.ref
        if n.ref is None:
            print("Node is not found")

        else:
            new_node = Node(data)
            new_node.ref = n.ref
            n.ref = new_node

    def insert_empty(self, data):
        if self.head is None:
            new_node = Node(data)
            self.head = new_node
        else:
            print("linkedlist is not empty")

    def delete_begin(self):
        if self.head is None:
            print("the linkedlist is empty")
        else:
            self.head = self.head.ref

    def delete_last(self):
        if self.head is None:
            print("linked list empty")
        elif self.head.ref is None:
            self.head = None
        else:
            n = self.head
            while n.ref.ref is not None:
                n = n.ref
            n.ref = None

    def delete_by_value(self, x):
        if self.head is None:
            print("linked list is none")
        if x == self.head:
            self.head = self.head.ref
            return
        n = self.head
        while n.ref is not None:
            if x == n.ref.data:
                break
            n = n.ref
        if n.ref is None:
            print("node is not present")
        else:
            n.ref = n.ref.ref


ll1 = LinkedList()
ll1.add_begin(40)
ll1.add_begin(30)
# ll1.add_begin(20)
ll1.add_end(100)
ll1.add_end(80)
# ll1.delete_begin()
# ll1.delete_last()
# ll1.delete_by_value(21)

ll1.insert_empty(30)

ll1.p_ll()
