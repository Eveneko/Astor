def check(data_path):
    with open(data_path, 'r') as fw:
        result = fw.readline().strip()
        temp = result.split(' ')
        print(temp)
        if len(temp) != 2:
            return False
        a, b = result.split(' ')
        if (not isinstance(a, str)) or (not isinstance(b, str)):
            return False
        return True


# if __name__ == "__main__":
#     a = check("./data.txt")
#     print(a )


