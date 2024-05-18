# ............by using array.............



stack = []
def push():
    element = int(input("enter the element:"))
    stack.append(element)
    print(stack)
def pop():
    stack_pop = stack.pop()
    print("removed elemnet:",stack_pop)
    print(stack)
def peek():

    stack_peek = stack[-1]
    print("peek element:",stack_peek)
while True:
    print("1.push,2.pop,3.q")
    choice = int(input())
    if choice == 1:
        push()
    elif choice == 2:
        pop()
    elif choice == 3:
        peek()
    else:
        print("enter valid choice")




..........................by using linked list..........................


class Node:
    def __init__(self,data):
        self.data = data
        self.ref = None

class Stack:
    def __init__(self):
        self.top = None

    def is_empty(self):
        return self.top is None

    def push(self,data):
        new_node = Node(data)
        new_node.ref = self.top
        self.top = new_node
    def pop(self):
        if self.is_empty():
            print("stack is empty")
        else:
            popped = self.top.data
            self.top = self.top.ref
            print("popped data:",popped)
            return popped

    def peek(self):
        if self.is_empty():
            print("stack is empty")
        else:
            print(self.top.data)

    def display(self):
        n = self.top
        while n:
            print(n.data,"-->",end=" ")
            n = n.ref

stack = Stack()
stack.push(3)
stack.push(6)
stack.push(9)
stack.push(7)
stack.push(3)
stack.push(6)
stack.push(5)
stack.pop()
stack.pop()

stack.display()



















