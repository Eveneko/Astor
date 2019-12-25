def check():
    with open('data.txt', 'r') as fw:
        result = fw.readline().strip()
        if len(result) != 3:
            # print()
            return False
        temp = result.split(' ')
        if len(temp) != 2:
            return False
        a, b = result.split(' ')
        if (not a.isdigit()) or (not b.isdigit()):
            return False
        return True
