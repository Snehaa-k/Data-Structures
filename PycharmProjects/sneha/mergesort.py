def mergesort(list1):
    if len(list1)>1:
        mid = len(list1)//2
        left = list1[mid:]
        right = list1[:mid]
        mergesort(left)
        mergesort(right)
        i = j = k = 0
        while i < len(left) and j <len(right):
            if left[i] < right[j]:
                list1[k] = left[i]
                i = i+1
            else:
                list1[k]=right[j]
                j = j+1
            k = k+1

        while i < len(left):
            list1[k] = left[i]
            i = i+1
            k = k+1
        while j < len(right):
            list1[k] = right[j]
            j = j+1
            k = k+1

list1 = [4,5,6,3,2,1]
print("before sorting:",list1)
mergesort(list1)
print("after sorting:" ,list1)
