
import random
import agensgraph


def gen_dataset_from_personrelkg(rel_level='basic'):
    data_path = "/home/hz/project/guohx/KGC/kg-reeval/data/Person/"
    ori_file = "personrelkg.data"

    entities = set()
    high_rel = set()
    basic_rel = set()
    triplets1 = set(tuple())
    triplets2 = set(tuple())

    with open(data_path + ori_file, encoding='utf-8', mode='r') as file:
        for line in file.readlines()[1:]:
            h, r1, r2, t = line.strip().replace("'", "").split(',')
            if t == '' or h in high_rel or t in high_rel or h in basic_rel or t in basic_rel:
                continue

            h = agensgraph.gen_entity(h)
            t = agensgraph.gen_entity(t)
            entities.add(h)
            entities.add(t)
            basic_rel.add(r1)
            high_rel.add(r2)
            triplets1.add((h, r1, t))
            triplets2.add((h, r2, t))

    train1 = list(tuple())
    valid1 = list(tuple())
    test1 = list(tuple())
    train2 = list(tuple())
    valid2 = list(tuple())
    test2 = list(tuple())

    ent_visited1 = set()
    ent_visited2 = set()
    rel_visited1 = set()
    rel_visited2 = set()

    all_data = list(zip(triplets1, triplets2))
    random.shuffle(all_data)
    proportion = 0.5
    valid_proportion = 0.2

    for (h1, r1, t1), (h2, r2, t2) in all_data:
        if h1 not in ent_visited1 or t1 not in ent_visited1 or r1 not in rel_visited1:
            ent_visited1.add(h1)
            ent_visited1.add(t1)
            rel_visited1.add(r1)
            train1.append((h1, r1, t1))
        else:
            r = random.random()
            # print(r)
            if r < proportion:
                train1.append((h1, r1, t1))
            elif r < proportion + valid_proportion:
                valid1.append((h1, r1, t1))
            else:
                test1.append((h1, r1, t1))

        if h2 not in ent_visited2 or t2 not in ent_visited2 or r2 not in rel_visited2:
            ent_visited2.add(h2)
            ent_visited2.add(t2)
            rel_visited2.add(r2)
            train2.append((h2, r2, t2))
        else:
            r = random.random()
            if r < proportion:
                train2.append((h2, r2, t2))
            elif r < proportion + valid_proportion:
                valid2.append((h2, r2, t2))
            else:
                test2.append((h2, r2, t2))

    print(f"train1 size:{len(train1)}\nvalid1 size:{len(valid1)}\ntest1 size:{len(test1)}")
    print(f"train2 size:{len(train2)}\nvalid2 size:{len(valid2)}\ntest2 size:{len(test2)}")

    # if rel_level == 'basic':

    write_triplets(data_path + "train2.txt", train1)
    write_triplets(data_path + "valid2.txt", valid1)
    write_triplets(data_path + "test2.txt", test1)
    write_triplets(data_path + "train.txt", train2)
    write_triplets(data_path + "valid.txt", valid2)
    write_triplets(data_path + "test.txt", test2)


def write_triplets(path:str, triplets:list[tuple]):
    with open(path, encoding='utf-8', mode='w') as file:
        file.writelines([f"{h}\t{r}\t{t}\n" for h, r, t in triplets])


if __name__ == '__main__':
    gen_dataset_from_personrelkg()

