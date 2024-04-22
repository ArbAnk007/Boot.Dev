# Some common sorting Algorithms

# Bubble Sort

def bubble_sort(nums):
    swapping = True
    end = len(nums)
    while swapping:
        swapping = False
        for i in range(1, end):
            if nums[i-1] > nums[i]:
                temp = nums[i-1]
                nums[i-1] = nums[i]
                nums[i] = temp
                swapping = True
        end -= 1
    return nums

# Merge Sort

def merge_sort(nums):
    if len(nums) < 2:
        return nums

    middle_index = len(nums)//2
    left = nums[:middle_index]
    right = nums[middle_index:]
    left_sorted = merge_sort(left)
    right_sorted = merge_sort(right)
    return merge(left_sorted, right_sorted)

def merge(first, second):
    i = 0
    j = 0

    final = []

    while i < len(first) and j < len(second):
        if first[i] <= second[j]:
            final.append(first[i])
            i += 1
        else:
            final.append(second[j])
            j += 1
    
    while i < len(first):
        final.append(first[i])
        i += 1
    
    while j < len(second):
        final.append(second[j])
        j += 1

    return final

# Insertion Sort

def insertion_sort(nums):
    for i in range(len(nums)):
        j = i
        while j>0 and nums[j-1] > nums[j]:
            temp = nums[j-1]
            nums[j-1] = nums[j]
            nums[j] = temp
            j -= 1
    
    return nums

# Quick Sort

def quick_sort(nums, low, high):
    if low < high:
        pivot_index = partition(nums, low, high)
        quick_sort(nums, low, pivot_index-1)
        quick_sort(nums, pivot_index+1, high)
    return nums

def partition(nums, low, high):
    pivot = nums[high]
    i = low
    for j in range(low, high+1):
        if nums[j] < pivot:
            temp = nums[j]
            nums[j] = nums[i]
            nums[i] = temp
            i += 1
    temp = nums[i]
    nums[i] = pivot
    nums[high] = temp
    return i

# Selection Sort

def selection_sort(nums):
    for i in range(len(nums)):
        smallest_index = i
        for j in range(smallest_index+1, len(nums)):
            if nums[smallest_index] > nums[j]:
                smallest_index = j
        temp = nums[smallest_index]
        nums[smallest_index] = nums[i]
        nums[i] = temp
    return nums