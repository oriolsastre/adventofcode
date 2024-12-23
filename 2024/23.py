type Graph = dict[str, set[str]]

file="data/23_data.txt"
file_test="data/23_data_test.txt"

def import_graph(file:str)->Graph:
    with open(file, "r") as f:
        graph = {}
        for line in f:
            line = line.strip().split("-")
            if line[0] not in graph: graph[line[0]] = set()
            if line[1] not in graph: graph[line[1]] = set()
            graph[line[0]].add(line[1])
            graph[line[1]].add(line[0])
    return graph
def get_three_group(graph:Graph, first_letter:str="")->set[frozenset[str]]:
    group = set()
    for node_a in graph:
        if len(first_letter)>0 and not node_a.startswith(first_letter): continue
        veins_a=graph[node_a]
        for node_b in veins_a:
            veins_b=graph[node_b]
            for node_c in veins_b:
                if node_c==node_a: continue
                if node_c in veins_a: group.add(frozenset([node_a,node_b,node_c]))
    return group
# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def find_maximal_cliques(graph:Graph):
    max_clique=set()
    def bron_kerbosch(r:set, p:set, x:set)->None:
        if len(p)==0 and len(x)==0: max_clique.add(frozenset(r))
        else:
            for vertex in p:
                bron_kerbosch(r.union({vertex}), p.intersection(graph[vertex]), x.intersection(graph[vertex]))
                p=p.difference({vertex})
                x=x.union({vertex})
    bron_kerbosch(set(), set(graph.keys()), set())
    return max_clique
def find_biggest_clique(max_cliques:set[frozenset])->frozenset[str]:
    return max(max_cliques, key=len)
def get_clique_password(clique:frozenset[str])->str:
    return ",".join(sorted(clique))

graph = import_graph(file)
grup_tres_test = get_three_group(graph,"t")
print("Hi ha", len(grup_tres_test), "groups de 3 ordinadors en què almenys un comença per 't'.") # 1062

maximal_cliques = find_maximal_cliques(graph)
biggest_clique = find_biggest_clique(maximal_cliques)
print("El password de la LAN party més grossa és:", get_clique_password(biggest_clique)) # bz,cs,fx,ms,oz,po,sy,uh,uv,vw,xu,zj,zm