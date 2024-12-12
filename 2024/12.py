import copy

file="data/12_data.txt"

def calcula_permietre(mapa:list[str], y:int, x:int)->int:
  coords_veins=((-1,0),(0,1),(1,0),(0,-1))
  perimetre=0
  planta=mapa[y][x]
  for coord in coords_veins:
    new_y=y+coord[0]
    new_x=x+coord[1]
    if new_y in range(len(mapa)) and new_x in range(len(mapa[0])):
      if mapa[new_y][new_x]!=planta: perimetre+=1
    else: perimetre+=1
  return perimetre
def conta_veins(regio:list[tuple[int,int]], planta:tuple[int,int])->int:
  coords_veins=((-1,0),(0,1),(1,0),(0,-1))
  veins=0
  for coord in coords_veins:
    if (planta[0]+coord[0], planta[1]+coord[1]) in regio: veins+=1
  return veins
def completa_costat(planta:tuple[int,int], regio_plantes:list[tuple[int,int]], dict_direccio:dict)->None:
  for signe in range(-1,2,2):
    [y,x] = planta
    [dir_y,dir_x]=dict_direccio["dir"]
    [out_y,out_x]=dict_direccio["out"]
    while((y,x) in regio_plantes and (y+out_y,x+out_x) not in regio_plantes):
      if (y,x) not in dict_direccio["n"]: dict_direccio["n"].add((y,x))
      y+=dir_y*signe
      x+=dir_x*signe
def calcula_costats(regio_plantes:list[tuple[int,int]])->int:
  costats=0
  contat={
    "ha": {"n": set(), "dir":(0,1), "out":(-1,0)},
    "hb": {"n": set(), "dir":(0,1), "out":(1,0)},
    "ve": {"n": set(), "dir":(1,0), "out":(0,-1)},
    "vd": {"n": set(), "dir":(1,0), "out":(0,1)}
    }
  for planta in regio_plantes:
    for direccio in contat.keys():
      dict_direccio=contat[direccio]
      if planta not in dict_direccio["n"]:
        dict_direccio["n"].add(planta)
        if conta_veins(regio_plantes, planta) == 4:
          for dir2 in contat.keys(): contat[dir2]["n"].add(planta)
        else:
          if (planta[0]+dict_direccio["out"][0], planta[1]+dict_direccio["out"][1]) not in regio_plantes:
            costats+=1
          else: continue
          completa_costat(planta, regio_plantes, dict_direccio)
  return costats
def marca_planta_visitada(mapa_visites:list[str], y:int, x:int)->None:
  mapa_visites[y] = mapa_visites[y][:x]+" "+mapa_visites[y][x+1:]
def busca_veins_no_visitats(mapa:list[str], mapa_visites:list[str], y:int, x:int)->list[tuple[int,int]]:
  coords_veins=((-1,0),(0,1),(1,0),(0,-1))
  veins_no_visitats=[]
  planta=mapa[y][x]
  for coord in coords_veins:
    new_y=y+coord[0]
    new_x=x+coord[1]
    if new_y in range(len(mapa)) and new_x in range(len(mapa[0])):
      if mapa[new_y][new_x]==planta and mapa_visites[new_y][new_x] != " ":
        veins_no_visitats.append((new_y,new_x))
        marca_planta_visitada(mapa_visites, new_y, new_x)
  return veins_no_visitats
def calcula_regio_plantes(mapa:list[str], mapa_visites:list[str], y:int, x:int)->dict:
  regio_valors={"area":0, "permietre":0, "costats": 0}
  stack_veins=[(y,x)]
  marca_planta_visitada(mapa_visites, y, x)
  for vei in stack_veins:
    regio_valors["area"]+=1
    regio_valors["permietre"]+=calcula_permietre(mapa, vei[0], vei[1])
    stack_veins+=busca_veins_no_visitats(mapa, mapa_visites, vei[0], vei[1])
  regio_valors["costats"]+=calcula_costats(stack_veins)
  return regio_valors
def get_map_total_price(mapa:list[str])->list[int,int]:
  mapa_visites = copy.deepcopy(mapa)
  total_price=[0,0]
  for y in range(len(mapa)):
    for x in range(len(mapa[0])):
      if mapa_visites[y][x] != " ":
        regio_plantes=calcula_regio_plantes(mapa, mapa_visites, y, x)
        total_price[0]+=regio_plantes["area"]*regio_plantes["permietre"]
        total_price[1]+=regio_plantes["area"]*regio_plantes["costats"]
  return total_price

with open(file, "r") as f:
  mapa=[]
  for line in f:
    mapa.append(line.strip())

[part1,part2] = get_map_total_price(mapa)

print("El preu per tanques individuals és de:", part1) # 1573474
print("El preu per tanques per costat és de:", part2) # 966476