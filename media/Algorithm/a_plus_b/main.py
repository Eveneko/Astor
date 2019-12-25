from check import check

if not check():
    print("The input is invalid,please submit again!")
else:
    with open('data.txt', 'r') as fw:
        result = fw.readline().strip()
        a, b = result.split(' ')
        print(int(a) + int(b))
