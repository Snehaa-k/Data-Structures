# doubly Linked List


class Node:
    def __init__(self, data):
        self.data = data
        self.nref = None
        self.pref = None


class DLinkedList:
    def __init__(self):
        self.head = None

    def print_dL(self):
        if self.head is None:
            print("linkedlist empty")

        else:
            n = self.head
            while n is not None:
                print(n.data, "--->", end=" ")
                n = n.nref

    def print_rev(self):
        print()
        if not self.head:
            print("linkedlist empty")
        else:
            n = self.head
            while n.nref is not None:
                n = n.nref
            while n is not None:
                print(n.data, "--->", end="")
                n = n.pref

    def add_empty(self, data):
        if self.head is None:
            new_node = Node(data)
            self.head = new_node
        else:
            print("the linked list is not empty")

    def add_begin(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            new_node.nref = self.head
            self.head.pref = new_node
            self.head = new_node

    def add_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node

        else:
            n = self.head
            while n.nref is not None:
                n = n.nref
            n.nref = new_node
            new_node.pref = n

    def add_after(self, data, x):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            n = self.head
            while n is not None:
                if x == n.data:
                    break
                n = n.nref
            if n is None:
                print("not found")
            else:
                new_node.nref = n.nref
                new_node.pref = n
                if n.nref is not None:
                    n.nref.pref = new_node
                n.nref = new_node

    def add_before(self, data, x):
        new_node = Node(data)
        if self.head is None:
            print("empty")
        else:
            n = self.head
            while n is not None:
                if x == n.data:
                    break
                n = n.nref
            if n is None:
                print("not found")
            else:
                new_node.nref = n
                new_node.pref = n.pref
                if n.pref is not None:
                    n.pref.nref = new_node
                else:
                    self.head = new_node
                n.pref = new_node

    def delete_begin(self):
        if self.head is None:
            print("the linked list is empty")
            return
        if self.head.nref is None:
            self.head = None

        else:
            self.head = self.head.nref
            self.head.pref = None

    def delete_end(self):
        if self.head is None:
            print("the linkedlist is empty")
            return
        if self.head.nref is None:
            self.head = None
        else:
            n = self.head
            while n.nref is not None:
                n = n.nref
            n.pref.nref = None

    def delete_by_value(self, x):
        if self.head is None:
            print("the linkedlist is empty")
            return
        if self.head.nref is None:
            self.head = None
        else:
            n = self.head
            while n.nref is not None:
                if x == n.data:
                    break
                n = n.nref
            if n is not None:
                n.nref.pref = n.pref
                n.pref.nref = n.nref
            else:
                if n.data == x:
                    n.pref.nref = None
                else:
                    print("x is not present")


dl = DLinkedList()
dl.add_empty(30)
dl.add_begin(40)
dl.add_begin(50)
dl.add_end(70)
dl.add_end(80)
dl.add_end(90)
dl.add_after(770, 40)
dl.add_before(550, 40)
dl.delete_begin()
dl.delete_end()
dl.delete_by_value(770)
dl.print_dL()
dl.print_rev()
