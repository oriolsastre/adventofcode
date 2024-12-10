file="data/10_data.txt"
total_score=0
total_score_distinct=0

def search_veins(mapa:list[list[int]],y:int,x:int)->list[list[int]]:
  altura=mapa[y][x]
  veins=[]
  coords_veins=((-1,0),(0,1),(1,0),(0,-1))
  for coord in coords_veins:
    new_y=y+coord[0]
    new_x=x+coord[1]
    if new_y in range(len(mapa)) and new_x in range(len(mapa[0])):
      if mapa[new_y][new_x]==altura+1: veins.append([new_y,new_x])
  return veins
    
def search_path(mapa:list[list[int]], y:int, x:int, end_path:set)->None:
  global total_score, total_score_distinct
  altura_actual = mapa[y][x]
  if(altura_actual == 9):
    alt_hash=str(y)+"_"+str(x)
    if alt_hash not in end_path:
      total_score+=1
      end_path.add(alt_hash)
    total_score_distinct+=1
    return
  veins = search_veins(mapa,y,x)
  for vei in veins:
    search_path(mapa,vei[0],vei[1],end_path)


mapa=[]
with open(file, "r") as f:
  for line in f:
    line=[int(x) for x in list(line.strip())]
    mapa.append(line)

for y in range(len(mapa)):
  for x in range(len(mapa[0])):
    if mapa[y][x] == 0:
      search_path(mapa,y,x,set())

print("Hi ha", total_score, "camins que comparteixen inici/destí.") # 538
print("Hi ha", total_score_distinct, "camins únics.") # 1110