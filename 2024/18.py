import math

type Mapa = list[list[str]]
type MapaScores = list[list[float]]
type pos = tuple[int,int,int]

file="data/18_data.txt"
file_test="data/18_data_test.txt"

def importa_mapa(file:str, max_bytes:int)->tuple[Mapa, MapaScores, list[int]]:
  mapa = [["." for _ in range(71)] for _ in range(71)]
  mapa_scores = [[math.inf for _ in range(71)] for _ in range(71)]
  falling_bytes=[]
  with open(file, "r") as f:
    byte=0
    for line in f:
      byte_coord=[int(x) for x in line.strip().split(",")]
      if byte < max_bytes:
        mapa[byte_coord[1]][byte_coord[0]] = "#"
      falling_bytes.append(byte_coord)
      byte+=1
  return (mapa, mapa_scores, falling_bytes)
def imprimeix_mapa(mapa:list[list])->None:
  if isinstance(mapa[0][0], str):  
    for line in mapa:
      print("".join(line))
  else:
    for line in mapa:
      output=[]
      for x in line:
        if x == math.inf: output.append(".")
        else: output.append(str(x%10))
      print("".join(output))
def busca_veins(mapa:Mapa, mapa_scores:MapaScores, posicio:pos, reverse=False)->list[pos]:
  coords_veins = ((-1,0),(0,1),(1,0),(0,-1))
  (y,x,score) = posicio
  veins_no_visitats = []
  for coord in coords_veins:
    [y_nou,x_nou] = [y+coord[0],x+coord[1]]
    if y_nou in range(len(mapa)) and x_nou in range(len(mapa[0])):
      if mapa[y_nou][x_nou] == "#": continue
      else:
        if not reverse and mapa_scores[y_nou][x_nou] > score+1:
          mapa_scores[y_nou][x_nou] = score+1
          veins_no_visitats.append((y_nou,x_nou,score+1))
        elif reverse and mapa_scores[y_nou][x_nou] == score-1:
          veins_no_visitats.append((y_nou,x_nou,mapa_scores[y_nou][x_nou]))
  return sorted(veins_no_visitats, key=lambda x: x[2])
def mapa_score(mapa:Mapa, mapa_scores:MapaScores)->int:
  mapa_scores[0][0] = 0
  camins=[(0,0,0)]
  while len(camins)>0:
    cami=camins.pop(0)
    if cami[0] == len(mapa)-1 and cami[1] == len(mapa[0])-1: break
    camins = sorted(camins+busca_veins(mapa, mapa_scores, cami), key=lambda x: x[2])
  return mapa_scores[len(mapa)-1][len(mapa[0])-1]
def pinta_camins(mapa:Mapa, mapa_scores:MapaScores)->set[pos]:
  [max_y,max_x] = [len(mapa)-1, len(mapa[0])-1] 
  posicions=set()
  camins=[(max_y,max_x,mapa_scores[max_y][max_x])]
  while len(camins)>0:
    cami=camins.pop(0)
    posicions.add((cami[0], cami[1]))
    for vei in busca_veins(mapa, mapa_scores, cami, True):
      if (vei[0],vei[1]) not in posicions:
        posicions.add((vei[0],vei[1]))
        camins.append(vei)
  return posicions
def pinta_mapa(mapa:Mapa, posicions:set[pos])->None:
  for posicio in posicions:
    print(posicio)
    mapa[posicio[0]][posicio[1]] = "O"
  imprimeix_mapa(mapa)

def ultim_byte(mapa:Mapa, mapa_scores:MapaScores, falling_bytes:list[int])->tuple[int,list[int]]:
  posicions=pinta_camins(mapa, mapa_scores)
  for i in range(len(falling_bytes[1024:])):
    fall_byte = (falling_bytes[1024+i][1], falling_bytes[1024+i][0])
    mapa[fall_byte[0]][fall_byte[1]] = "#"
    # Si cau algun byte per allà on passa un camí òptim, recalculem el mapa
    if fall_byte in posicions:
      mapa_scores = [[math.inf for _ in range(71)] for _ in range(71)]
      score=mapa_score(mapa, mapa_scores)
      if score == math.inf: break
      posicions=pinta_camins(mapa, mapa_scores)
  return (i, falling_bytes[1024+i])
  

(mapa_kb, mapa_scores_kb, falling_bytes) = importa_mapa(file, 1024)
score=mapa_score(mapa_kb, mapa_scores_kb)
print("Amb el primer kilobyte, el camí més curt és de", score, "passes") #246

(i, byte) = ultim_byte(mapa_kb, mapa_scores_kb, falling_bytes)
print("El", i+1024,"è byte", falling_bytes[1024+i], "bloquejarà la sortida des de l'inici.") # 22,50