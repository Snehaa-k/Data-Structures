# queue = []
# def enqueue():
#     element = int(input("enter the element"))
#     queue.append(element)
#     print(queue)
# def dequeue():
#     if not queue:
#         print("queue is empty..!")
#     else:
#         e = queue.pop(0)
#         print("removed element:",e)
# def peek():
#     print(queue[0])
#
# def display():
#
#     return queue
#
#
#
#
# enqueue()
# enqueue()
# dequeue()
# peek()
# print(display())



#..........queue_using linkedlist.........

# class Node:
#     def __init__(self, data):
#         self.data = data
#         self.ref = None
#
# class Queue:
#     def __init__(self):
#         self.front = None
#         self.rear = None
#
#     def is_empty(self):
#         return self.front is None
#
#     def enqueue(self, data):
#         new_node = Node(data)
#         if self.is_empty():
#             self.front = self.rear = new_node
#         else:
#             self.rear.ref = new_node
#             self.rear = new_node
#
#     def dequeue(self):
#         if self.is_empty():
#             print("Queue is empty..!")
#         else:
#             popped = self.front.data
#             if self.front == self.rear:
#                 self.front = self.rear = None
#             else:
#                 self.front = self.front.ref
#             return popped
#
#     def display(self):
#         n = self.front
#         while n is not None:
#             print(n.data, "-->", end=" ")
#             n = n.ref
#
#
# queue = Queue()
# queue.enqueue(3)
# queue.enqueue(4)
# queue.enqueue(5)
# queue.dequeue()
# queue.display()















