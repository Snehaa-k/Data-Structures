def Insertion_Sort(arr):
   for i in range(len(arr)):
      key=arr[i]
      pos=i
      while key<arr[pos-1] and pos >0:
         arr[pos]=arr[pos-1]
         pos=pos-1
      arr[pos]=key
lis=[7,4,5,1,2,3,8,6,9]
Insertion_Sort(lis)
print(lis)