# selection sort....................

list1 = [2,4,5,1,8,9]
print("unsorted list",list1)
for i in range(len(list1)-1):
    for j in range(i+1,len(list1)):
        if list1[i] > list1[j]:
            list1[i],list1[j] = list1[j] ,list1[i]

print("sorted list",list1)
