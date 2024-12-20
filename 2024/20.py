import math

type Mapa=list[list[str]]
type MapaScore=list[list[float]]
type pos=tuple[int,int]

file="data/20_data.txt"
file_test="data/20_data_test.txt"

def importa_mapa(file:str)->Mapa:
  with open(file, "r") as f:
    mapa=[]
    for line in f:
      line=list(line.strip())
      mapa.append(line)
  return mapa
def inicia_mapa_scores(mapa:Mapa)->MapaScore:
  mapa_scores = [[math.inf for _ in range(len(mapa[0]))] for _ in range(len(mapa))]
  return mapa_scores
# def crear_mapa_revers(mapa:Mapa, inici: pos, final: pos)->Mapa:

def posicio_inici_final(mapa:Mapa)->tuple[pos,pos]:
  inici=(-1,-1)
  final=(-1,-1)
  for y in range(len(mapa)):
    for x in range(len(mapa[0])):
      if mapa[y][x] == "S":
        inici=(y,x)
      if mapa[y][x] == "E":
        final=(y,x)
      if inici != (-1,-1) and final != (-1,-1): break
  return (inici,final)
def imprimeix_mapa(mapa:Mapa)->None:
  for line in mapa:
    print("".join(line))
def imprimeix_mapa_scores(mapa_scores:MapaScore, mapa:Mapa)->None:
  for y in range(len(mapa_scores)):
    for x in range(len(mapa_scores[0])):
      if mapa_scores[y][x] == math.inf:
        if mapa[y][x] == "#": print("#", end="")
        else: print(".", end="")
      else: print(int(mapa_scores[y][x])%10, end="")
    print("")
def busca_camins(mapa:Mapa, mapa_scores:MapaScore, posicio:pos)->list[pos]:
  coords_veins=set(((-1,0),(0,1),(1,0),(0,-1)))
  (y,x)=posicio
  veins_no_visitats=[]
  for coord in coords_veins:
    [y_nou,x_nou]=[y+coord[0],x+coord[1]]
    if mapa[y_nou][x_nou] == "#": continue
    else:
      if mapa_scores[y_nou][x_nou] > mapa_scores[y][x]+1:
        mapa_scores[y_nou][x_nou]=mapa_scores[y][x]+1
        veins_no_visitats.append((y_nou,x_nou))
  return veins_no_visitats
def calcula_score_mapa(mapa:Mapa, mapa_scores:MapaScore)->None:
  (inici,_)=posicio_inici_final(mapa)
  mapa_scores[inici[0]][inici[1]]=0
  camins=[inici]
  while camins != []:
    posicio=camins.pop(0)
    camins+=busca_camins(mapa, mapa_scores, posicio)
def afegeix_trampa(trampes:dict, score:int, posicio:pos)->None:
  if score not in trampes.keys():
    trampes[score]=[]
  trampes[score].append(posicio)
def busca_trampes(mapa:Mapa, mapa_scores:MapaScore)->dict:
  trampes={}
  for y in range(1,len(mapa_scores)-1):
    for x in range(1,len(mapa_scores[0])-1):
      if mapa[y][x] == "#":
        for d in range(-1,1):
          dy=-1*(d+1)
          dx=-1*d
          if mapa[y+dy][x+dx] != "#" and mapa[y-dy][x-dx] != "#":
            if mapa_scores[y+dy][x+dx] != math.inf and mapa_scores[y-dy][x-dx] != math.inf:
              score_diff = abs(mapa_scores[y+dy][x+dx]-mapa_scores[y-dy][x-dx])-2
              afegeix_trampa(trampes, score_diff, (y,x))
  return trampes
def quantitat_trampes(trampes:dict, score_min:int)->int:
  quantitat=0
  for score in trampes.keys():
    if score >= score_min:
      quantitat+=len(trampes[score])
  return quantitat
def busca_trampes_llargues(mapa:Mapa, mapa_scores:MapaScore, mida_trampa:int, estalvi_min:int)->int:
  max_y, max_x = [len(mapa), len(mapa[0])]
  for y1 in range(max_y-20):
    for x1 in range(max_x-20):
      for y2 in range(y1+2,y1+20):
        for x2 in range(x1+2,x1+20):
          if mapa[y1][x1]=="#" or mapa[y2][x2]=="#": continue
          if abs(mapa_scores[y1][x1]-mapa_scores[y2][x2])-2 >= estalvi_min:
            # Fer mini mapa on paret és cami i camí paret i calcular-ne l'score
            a=0
  return 0

mapa=importa_mapa(file)
mapa_scores=inicia_mapa_scores(mapa)
calcula_score_mapa(mapa, mapa_scores)
trampes=busca_trampes(mapa, mapa_scores)
print("Hi ha", quantitat_trampes(trampes, 100), "trampes que t'estalvien un mínim de 100 picosegons.") # 1395
# busca_trampes_llargues(mapa,mapa_scores,20,50)