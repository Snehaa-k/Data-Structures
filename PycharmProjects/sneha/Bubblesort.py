#bubble sort..............
list1 = [2,5,6,1,9,4,3,2]
print("unsorted list",list1)
for i in range(len(list1)):
    for j in range(len(list1)-i-1):
        if list1[j] > list1[j+1]:
            list1[j],list1[j+1] = list1[j+1],list1[j]



print("sorted list",list1)
