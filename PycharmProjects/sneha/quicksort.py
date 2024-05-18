def quicksort(list1, left, right):
    if left < right:
        p = pivot_place(list1, left, right)
        quicksort(list1, left, p - 1)
        quicksort(list1, p + 1, right)

def pivot_place(list1, left, right):
    i = left
    j = right - 1
    pivot = list1[right]
    while True:
        while i <= j and list1[i] < pivot:
            i += 1
        while i <= j and list1[j] >= pivot:
            j -= 1
        if i < j:
            list1[i], list1[j] = list1[j], list1[i]
        else:
            break
    if list1[i] > pivot:
        list1[i], list1[right] = list1[right], list1[i]
    return i

list1 = [2, 4, 5, 3, 1, 89, 9]
n = len(list1)

print("Original List:", list1)
quicksort(list1, 0, n - 1)
print("Sorted List:", list1)














# insertion







