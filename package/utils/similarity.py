from difflib import SequenceMatcher


def _similar(a, b):
    return SequenceMatcher(None, a, b).ratio() * 100


def process_list(dic, sim):
    result = {}
    for string in dic.keys():
        data = []
        for other in dic.keys():
            similarity = _similar(string, other)
            if other != string and similarity >= sim:
                data.append("{}: {}% similar".format(dic[other], str(int(similarity))))
        result[dic[string]] = data
    return result
