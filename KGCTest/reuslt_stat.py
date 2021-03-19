

def filtered_results(results:set, head:str=None,rel:str=None,tail:str=None,score:float=0.5):
    if head is None and rel is None and tail is None:
        return []

    filtered_res = []

    for h,r,t,v in results:
        v = float(v)
        if (h == head or head is None) and (r == rel or rel is None) and (t == tail or tail is None) and v > score:
            filtered_res.append((h,r,t,v))

    return filtered_res


if __name__ == '__main__':
    result_path = "/home/hz/project/guohx/KGC/kg-reeval/ConvE/results/person_11_03_2021_17:26:55"

    results = set[tuple]()

    with open(result_path, encoding='utf-8', mode='r') as file:
        for line in file.readlines():
            h,r,t,v = line.strip().split("\t")
            results.add((h,r,t,float(v)))

    res = filtered_results(results, head = "王晶", tail = "周星驰", score=0.9)