import psycopg2
import re

def read_datasets():
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

            h = gen_entity(h)
            t = gen_entity(t)
            entities.add(h)
            entities.add(t)
            basic_rel.add(r1)
            high_rel.add(r2)
            triplets1.add((h, r1, t))
            triplets2.add((h, r2, t))

    return entities,basic_rel,triplets1


def get_conn():
    return psycopg2.connect("dbname=person host=localhost user=agens password=thinker")


def remove_brackets(s:str, replace:str='') -> str:
    return re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", replace, s)


def gen_entity(s:str) -> str:
    s = remove_brackets(s)
    # s = s.replace(" ", "_")
    # s = s.replace("-", "_")
    # s = s.replace(".", "")

    return s


def create_person_graph():

    entities,relations,triplets = read_datasets()

    conn = get_conn()
    cur=conn.cursor()

    cur.execute("set graph_path=person_graph")

    # insert_triplet_cql = "create (:person {{name: '{}'}})-[:person_relation_person {{relation: '{}'}}]->(:person {{name: '{}'}})"
    # create_triplet = "create (:person {{name: '{}'}})-[:rel {{relation: '{}'}}]->(:person {{name: '{}'}})"
    create_path = "match (h:person {{name:'{}'}}),(t:person {{name:'{}'}}) create (h)-[:rel {{name:'{}'}}]->(t)"
    create_person = "create (:person {{name: '{}'}})"
    # cur.execute("CREATE (:v {name: 'AgensGraph'})")
    ent_visited, rel_visited = set(), set()
    cur.execute("create vlabel person")
    cur.execute("create elabel rel")
    for h,r,t in triplets:
        # hlabel = gen_entity(h)
        # rlabel = gen_entity(r)
        # tlabel = gen_entity(t)
        # if h not in ent_visited and t not in ent_visited and r not in rel_visited:
        #     ent_visited.add(h)
        #     ent_visited.add(t)
        #     rel_visited.add(r)
        #     cur.execute(create_triplet.format(h,r,t))
        # else:
        if h not in ent_visited:
            ent_visited.add(h)
            cur.execute(create_person.format(h))

        if t not in ent_visited:
            ent_visited.add(t)
            cur.execute(create_person.format(t))

        cur.execute(create_path.format(h, t, r))

    conn.commit()

    cur.execute("MATCH (n) RETURN n")
    v = cur.fetchone()
    print(v)




if __name__ == '__main__':

    create_person_graph()
    # entities,relations,triplets = read_datasets()

    # s = "程之[中国]{内地}(已故男)[演员]"
    # print(remove_brackets(s), s)

    # conn = get_conn()
    # cur = conn.cursor()
    # cur.execute("set graph_path=person_graph")
    #
    # cur.execute("MATCH (h:person {name: '王晶'})-[r:person_relation_person]->(t:person) RETURN h.name, r.relation, t.name")



