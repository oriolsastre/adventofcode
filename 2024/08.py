file="data/08_data.txt "

def busca_antenes(mapa_antenes)->dict[int]:
    antenes_llocs={}
    for y in range(len(mapa_antenes)):
        for x in range(len(mapa_antenes[0])):
            antena=mapa_antenes[y][x]
            if antena != ".":
                if antena not in antenes_llocs:
                    antenes_llocs[antena]=[]
                antenes_llocs[antena].append([y,x])
    return antenes_llocs
def guarda_antinode(simbol,y,x,antinodes_llocs):
    hash_lloc=str(y)+"_"+str(x)
    if hash_lloc not in antinodes_llocs:
        antinodes_llocs[hash_lloc]=[]
    # TODO: Mirar si el mateix simbol ja hi és o no?
    antinodes_llocs[hash_lloc].append(simbol)
def localitza_antinodes(simbol, antena, antena_post, antinodes_llocs, mapa_antenes):
    [limit_y, limit_x] = [len(mapa_antenes), len(mapa_antenes[0])]
    [antena_y, antena_x] = antena
    [antena_post_y, antena_post_x] = antena_post
    [y_diff, x_diff] = [antena_post_y - antena_y, antena_post_x - antena_x]
    # [new_y, new_x] = [new_y - y_diff, new_x - x_diff] # 1a part
    [new_y, new_x] = [antena_y, antena_x] # 2na part
    # [new_post_y, new_post_x] = [new_post_y + y_diff, new_post_x + x_diff] # 1a part
    [new_post_y, new_post_x] = [antena_post_y, antena_post_x] # 2na part
    # if new_y in range(limit_y) and new_x in range(limit_x): # 1a part
    while new_y in range(limit_y) and new_x in range(limit_x): # 2na part
        guarda_antinode(simbol, new_y, new_x, antinodes_llocs)
        [new_y, new_x] = [new_y - y_diff, new_x - x_diff] # 2na part
    # if new_post_y in range(limit_y) and new_post_x in range(limit_x): # 1a part 
    while new_post_y in range(limit_y) and new_post_x in range(limit_x): # 2na part
        guarda_antinode(simbol, new_post_y, new_post_x, antinodes_llocs)
        [new_post_y, new_post_x] = [new_post_y + y_diff, new_post_x + x_diff] # 2na part

mapa_antenes=[]
with open(file, "r") as f:
    for line in f:
        line=line.strip()
        mapa_antenes.append(line)

antenes_llocs=busca_antenes(mapa_antenes)
antinodes_llocs={}

for y in range(len(mapa_antenes)):
    for x in range(len(mapa_antenes[0])):
        antena=mapa_antenes[y][x]
        if antena != ".":
            # Busquem on més apareix l'antena
            if antena in antenes_llocs:
                antenes_iguals = antenes_llocs[antena]
                # Busquem l'índex ja que compararem amb posteriors
                antena_index = antenes_iguals.index([y,x])
                if antena_index < len(antenes_iguals)-1:
                    for antena_post_yx in antenes_iguals[antena_index+1:]:
                        localitza_antinodes(antena, [y,x], antena_post_yx, antinodes_llocs, mapa_antenes)

print("Hi ha", len(antinodes_llocs.keys()), "llocs que contenen un antinode.") # 336 / 1131