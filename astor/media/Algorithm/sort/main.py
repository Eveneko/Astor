from check import check
import argparse


def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='data_path', type=str, help='the path of data')
    args = parser.parse_args()
    data_path = args.data_path

    if not check(data_path):
        print("The input is invalid,please submit again!")
    else:
        with open(data_path, 'r') as fw:
            result = fw.readline().strip()
            a = result.split(' ')
            a = list(filter(None, a))
            arr = []
            for sub in a:
                arr.append(int(sub))

            insertionSort(arr)
            for i in arr:
                print(i, end=" ")
