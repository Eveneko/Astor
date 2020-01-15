def check(data_path):
    with open(data_path, 'r') as fw:
        result = fw.readline().strip()
        temp = result.split(' ')
        if len(temp) != 2:
            return False
        a, b = result.split(' ')
        if (not a.isdigit()) or (not b.isdigit()):
            return False
        return True
