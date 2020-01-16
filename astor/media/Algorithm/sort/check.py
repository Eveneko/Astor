def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def check(data_path):
    with open(data_path, 'r') as fw:
        result = fw.readline().strip()
        a = result.split(' ')
        a = list(filter(None, a))
        for te in a:
            if not is_number(te):
                return False
        return True
# print(check())
