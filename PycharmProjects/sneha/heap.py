class Minheap:
    def __init__(self):
        self.heap = []

    def build_heap(self, array):
        self.heap = array
        n = len(array)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify_down(i)

    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap)-1)

    def remove(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return root

    def heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2
            if self.heap[index] < self.heap[parent]:
                self.heap[index],self.heap[parent] = self.heap[parent], self.heap[index]
                index = parent
            else:
                break

    def heapify_down(self, index):
        n = len(self.heap)
        while 2 * index + 1 < n:
            child = 2 * index + 1
            if child + 1 < n and self.heap[child + 1] < self.heap[child]:
                child += 1
            if self.heap[index] > self.heap[child]:
                self.heap[child], self.heap[index] = self.heap[index], self.heap[child]
                index = child
            else:
                break

    def print_heap(self):
        print("Min Heap:", self.heap)





heap = Minheap()
heap.insert(30)
heap.insert(40)
heap.insert(55)
heap.insert(89)
heap.insert(77)



# heap.remove()


heap.print_heap()
