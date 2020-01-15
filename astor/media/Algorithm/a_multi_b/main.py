from check import check
import argparse

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
            a, b = result.split(' ')
            print(int(a) * int(b))

