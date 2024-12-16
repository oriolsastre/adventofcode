type Mapa = list[list[str]]
type MapaScore = list[list[int]]
type pos = tuple[int,int]
type dir = tuple[int,int]

file="data/16_data.txt"
file_test="data/16_data_test.txt"

def importa_mapa(file:str)->tuple[Mapa, MapaScore]:
  with open(file, "r") as f:
    mapa=[]
    mapa_scores = []
    for line in f:
      line=list(line.strip())
      line_zero=[None for _ in range(len(line))]
      mapa.append(list(line))
      mapa_scores.append(line_zero)
  ((y,x),_,score) = posicio_inicial(mapa)
  mapa_scores[y][x]=score
  return (mapa, mapa_scores)
def posicio_inicial(mapa:Mapa, final=False)->tuple[pos,dir,int]:
  for y in range(len(mapa)):
    for x in range(len(mapa[0])):
      if (final and mapa[y][x] == "E") or (not final and mapa[y][x]) == "S":
        return ((y,x),(0,1),0)
  return ((-1,-1),(0,0),0)
def busca_cami_no_visitat(mapa:Mapa, mapa_scores:MapaScore, posicio:tuple[pos,dir,int])->list[tuple[pos,dir,int]]:
  coords_veins=set(((-1,0),(0,1),(1,0),(0,-1)))
  ((y,x),direccio,score)=posicio
  veins_no_visitats=[]
  for coord in coords_veins:
    [y_nou,x_nou]=[y+coord[0],x+coord[1]]
    new_score=score+1+(1000*factor_gir(direccio, coord))
    if mapa[y_nou][x_nou] == "#": continue
    else:
      if mapa_scores[y_nou][x_nou] == None or mapa_scores[y_nou][x_nou] > new_score:
        mapa_scores[y_nou][x_nou]=new_score
        veins_no_visitats.append(((y_nou,x_nou),coord,new_score))
  return sorted(veins_no_visitats, key=lambda x: x[2])
def factor_gir(inicial:dir, final:dir)->int:
  dif_y = abs(inicial[0]-final[0])
  dif_x = abs(inicial[1]-final[1])
  if dif_y==0 and dif_x==0: return 0
  if (dif_y==2 or dif_x==2) and dif_x*dif_y==0: return 2
  if dif_y==1 and dif_x==1: return 1
  else: return 0
def busca_camins(mapa:Mapa, mapa_scores:MapaScore)->int:
  camins = [posicio_inicial(mapa)]
  while len(camins)>0:
    cami=camins.pop(0)
    ((y,x),_,score)=cami
    if mapa[y][x] != "E":
      camins = sorted(camins+busca_cami_no_visitat(mapa, mapa_scores, cami), key=lambda x: x[2])
  (pos_final,_,_) = posicio_inicial(mapa, True)
  return mapa_scores[pos_final[0]][pos_final[1]]
def vei_enrere(mapa_scores, pos)->list[pos]:
  coords_veins=set(((-1,0),(0,1),(1,0),(0,-1)))
  (y,x)=pos
  score=mapa_scores[y][x]
  veins=[]
  for coord in coords_veins:
    [new_y,new_x]=[y+coord[0],x-coord[1]]
    score_vei = mapa_scores[new_y][new_x]
    if (score_vei == score-1 or score_vei == score-1001) and new_x>0 and new_y<len(mapa_scores)-1:
      veins.append((new_y,new_x))
  return veins
def desfes_cami(mapa_scores: MapaScore, pos_final:pos)->int:
  cadires = set()
  veins = [pos_final]
  while len(veins)>0:
    cadira = veins.pop()
    cadires.add(cadira)
    veins.extend(vei_enrere(mapa_scores, cadira))
  print(cadires)
  return len(cadires)


(mapa, mapa_scores)=importa_mapa(file_test)
print(busca_camins(mapa, mapa_scores)) # 85480
(pos_f,dir_f,score_f)=posicio_inicial(mapa, True)
for y in range(len(mapa_scores)):
  print(mapa_scores[y])
print(desfes_cami(mapa_scores, pos_f))

