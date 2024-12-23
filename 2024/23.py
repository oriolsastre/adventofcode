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


graph = import_graph(file)
grup_tres_test = get_three_group(graph,"t")
print("Hi ha", len(grup_tres_test), "groups de 3 ordinadors en què almenys un comença per 't'.") # 1062