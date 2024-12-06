import copy

file="data/06_data.txt"
mapa_original=[]
posicions_visitades=1
possible_loop = 0

def dimensions_mapa(mapa)->list[int]:
    return [len(mapa), len(mapa[0])-1]
def posicio_inicial_guarda(mapa)->list[int]:
    for i in range(len(mapa)):
        for j in range(len(mapa[0])-1):
            if mapa[i][j]=="^":
                return [i,j,[-1,0]]
    return [-1,-1,-1]
def marca_posicio(posicio,z)->str:
    abs_z = [z[0]+1, z[1]+1]
    dic_marques={
        ".": [[None,["^",0],None],[["<",0],None,[">",0]],[None,["v",0],None]],
        "v": [[None,["|",0],None],[["+",0],None,["+",1]],[None,["v",0],None]],
        "<": [[None,["+",0],None],[["<",0],None,["-",0]],[None,["+",1],None]],
        ">": [[None,["+",1],None],[["-",0],None,[">",0]],[None,["+",0],None]],
        "^": [[None,["^",0],None],[["+",1],None,["+",0]],[None,["|",0],None]],
    }
    if posicio not in dic_marques: nova_marca = [posicio,0]
    else: nova_marca = dic_marques[posicio][abs_z[0]][abs_z[1]] 
    return nova_marca[0]
def visitar_posicio(mapa,posicio)->None:
    [x,y,z] = posicio
    if (mapa[x][y] == "\n"): return
    marca=marca_posicio(mapa[x][y],z)
    mapa[x]=mapa[x][:y]+marca+mapa[x][y+1:]
def gir(posicio)->list[int]:
    return [posicio[1],-posicio[0]]
def seguent_posicio(posicio, mapa)->list[int]:
    [x,y,z] = posicio
    [alçada,llargada] = dimensions_mapa(mapa)
    while x+z[0] in range(alçada) and y+z[1] in range(llargada) and mapa[x+z[0]][y+z[1]] == "#":
        z = gir(z)
    return [x+z[0],y+z[1],z]

### Inici

with open(file, "r") as f:
    mapa_original=f.readlines()

mapa=copy.deepcopy(mapa_original)
[alçada,llargada] = dimensions_mapa(mapa_original)

# Iniciem la ruta i marquem la posició inicial com a visitada
posicio_original = posicio_inicial_guarda(mapa)
posicio = copy.deepcopy(posicio_original)
visitar_posicio(mapa,posicio)

while(posicio[0] in range(alçada) and posicio[1] in range(llargada)):
    if(mapa[posicio[0]][posicio[1]] in [".",":",";","{","}"]):
        posicions_visitades+=1
    visitar_posicio(mapa,posicio)
    posicio=seguent_posicio(posicio, mapa)

print("El guarda ha visitat", posicions_visitades, "posicions diferents") # 5331
with open("data/06_output.txt", "w") as f:
    for line in mapa: f.write(line)

for i in range(alçada):
    for j in range(llargada):
        # Només posem obstacles en llocs que visita en el traçat original
        if(mapa[i][j] not in [".","#"] and [i,j] != posicio_original):
            nou_mapa=copy.deepcopy(mapa_original)
            nou_mapa[i]=nou_mapa[i][:j]+"#"+nou_mapa[i][j+1:]
            comptador_visites = {}

            posicio=copy.deepcopy(posicio_original)
            visitar_posicio(nou_mapa,posicio)
            
            while(posicio[0] in range(alçada) and posicio[1] in range(llargada)):
                [x,y,z] = posicio
                # Guardem la posició i direcció dels llocs visitats. Si torna al mateix lloc en la mateixa direcció, hem creat un loop 
                hash = str(x)+"_"+str(y)+"_"+str(z[0]+1)+"_"+str(z[1]+1)
                if comptador_visites.get(hash) == None: comptador_visites[hash] = True
                else:
                    possible_loop+=1
                    break
                visitar_posicio(nou_mapa,posicio)
                posicio=seguent_posicio(posicio, nou_mapa)

print("Es podrien generar", possible_loop, "possibles loops") # 1812