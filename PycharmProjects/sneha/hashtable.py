
class Node:
    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.ref = None

class Hashtable:
    def __init__(self,size):
        self.size = size
        self.table = [None]*size

    def hash_function(self,key):
        return hash(key)%self.size

    def insert(self,key,value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = Node(key,value)
        else:
            n = self.table[index]
            while n is not None:
                n = n.ref
            n.ref = Node(key,value)

    def search(self,key):
        index = self.hash_function(key)
        if self.table[index] is None:
            print("table is empty..!")
        else:
            n = self.table[index]
            while n:
                if n.key == key:
                    print(n.value)
                n= n.ref
            return None

    def delete(self,key):
        index = self.hash_function(key)
        n = self.table[index]
        previous = None
        while n:
            if n.key == key:
                if previous:
                    previous.ref = n.ref
                else:
                    self.table[index] = n.ref
            previous = n
            n = n.ref

    def display(self):
        for i in range(self.size):
            n = self.table[i]
            while n:
                print(f"[{n.key}:{n.value}]",end="-->")
                n = n.ref

    def count_letters(self):
        lettercount = {}
        for i in range(self.size):
            n = self.table[i]
            while n:
                key = n.key
                lettercount[key] = sum([key.count(i) for i in key])
                n = n.ref
        print(lettercount)



hastable = Hashtable(10)
hastable.insert("apple",1)
hastable.insert("orange",8)
hastable.insert("mango",9)
# hastable.delete("mango")
hastable.search("orange")
hastable.count_letters()

hastable.display()



