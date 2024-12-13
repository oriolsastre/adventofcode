import numpy as np

file="data/13_data.txt"
file_test="data/13_data_test.txt"

def llegeix_boto(linia:str, premi=0)->dict:
  boto_linia = linia.strip().split(" ")
  boto = {
    "x": int(boto_linia[2-premi][2:-1])+10000000000000*premi,
    "y": int(boto_linia[3-premi][2:])+10000000000000*premi,
  }
  return boto
def maquina_100(maquina:dict)->bool:
  if maquina["a"]["x"]*100+maquina["b"]["x"]*100<maquina["premi"]["x"]: return True
  if maquina["a"]["y"]*100+maquina["b"]["y"]*100<maquina["premi"]["y"]: return True
  return False
def maquina_parell(maquina:dict)->bool:
  boto_a=maquina["a"]
  boto_b=maquina["b"]
  premi=maquina["premi"]
  x_parell = boto_a["x"]+boto_b["x"]%2 == 0
  y_parell = boto_a["y"]+boto_b["y"]%2 == 0
  premi_x_parell = premi["x"]%2 == 0
  premi_y_parell = premi["y"]%2 == 0
  if x_parell==True and premi_x_parell==False: return True
  if y_parell==True and premi_y_parell==False: return True
  return False
def juga_maquina(maquina:dict)->None:
  botons=np.array([[maquina["a"]["x"],maquina["b"]["x"]],[maquina["a"]["y"],maquina["b"]["y"]]])
  premis=np.array([maquina["premi"]["x"],maquina["premi"]["y"]])
  resultat=np.linalg.solve(botons,premis)
  resultat_int = np.round(resultat).astype(int)
  if np.isclose(resultat[0],resultat_int[0]) and np.isclose(resultat[1],resultat_int[1]):
    if resultat_int[0]>=0 and resultat_int[1]>=0:
      if resultat_int[0]*maquina["a"]["x"]+resultat_int[1]*maquina["b"]["x"]==maquina["premi"]["x"]:
        if resultat_int[0]*maquina["a"]["y"]+resultat_int[1]*maquina["b"]["y"]==maquina["premi"]["y"]:
          maquina["resultat"]=[resultat_int[0],resultat_int[1]]
          maquina["resolt"] = True

with open(file, "r") as f:
  maquines=[]
  i=0
  for line in f:
    if i%4==0:
      maquines.append({"resolt":False, "resultat":[0,0]})
      boto_a=llegeix_boto(line)
      maquines[-1]["a"] = boto_a
    elif i%4==1:
      boto_b=llegeix_boto(line)
      maquines[-1]["b"] = boto_b
    elif i%4==2:
      premi=llegeix_boto(line, 1)
      maquines[-1]["premi"] = premi
    elif i%4==3:
      maquines[-1]["resolt"] = maquina_parell(maquines[-1])
    i+=1

  for maquina in maquines:
    if maquina["resolt"]: continue
    juga_maquina(maquina)
    print(maquina)

tokens=0
for maquina in maquines:
  tokens+=maquina["resultat"][0]*3+maquina["resultat"][1]
# print(maquines)
print(tokens) # 37901
# 77407675412647