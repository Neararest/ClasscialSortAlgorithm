import random as rd
import time
import pandas as pd
import gc

rd.seed(42)
N1 = [rd.randint(0,100) for _ in range(10)]
N10 = [rd.randint(0,100) for _ in range(100)]
N100 = [rd.randint(0,100) for _ in range(1000)]
N1000 = [rd.randint(0,100) for _ in range(10000)]
N10000 = [rd.randint(0,100) for _ in range(100000)]
N100000 = [rd.randint(0,100) for _ in range(1000000)]

dataset = [("N=10", N1), ("N=100", N10), ("N=1000", N100), ("N=10000", N1000), ("N=100000", N10000), ("N=1000000", N100000)]

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l
    
    if r < n and arr[r] > arr[largest]:
        largest = r
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0] 
        heapify(arr, i, 0)

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + mid + quick_sort(right) 

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        mergeSort(L)
        mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i - gap
            while j >= 0 and arr[j] > temp:
                arr[j + gap] = arr[j]
                j -= gap
            arr[j + gap] = temp
        gap //= 2
    return arr

def tim_sort(arr):
    return sorted(arr)

algoritma = {
    "Heap Sort": heap_sort,
    "Merge Sort": mergeSort,
    "Quick Sort": quick_sort,
    "Shell Sort": shell_sort,
    "Tim Sort": tim_sort,
}

if __name__ == "__main__":
    hasil = []
    for nama, func in algoritma.items():
        row = {"Algoritma": nama}
        for nama_data, data in dataset:
            arr = data.copy()
            gc.collect()
            start = time.perf_counter()
            func(arr)   
            end = time.perf_counter()

            row[nama_data] = f"{end - start:.6f}"
            del arr
        hasil.append(row)

    df = pd.DataFrame(hasil)
    print(df.to_string(index=False, col_space=15, justify='left'))
