file="data/15_data.txt"
file_test="data/15_data_test.txt"
type Mapa = list[list[str]]

def llegeix_input(file: str, doble=False)->tuple[Mapa, str, tuple[int,int]]:
    with open(file, "r") as f:
        mapa=[]
        ordres=""
        file_mapa=True
        for line in f:
            if len(line.strip())==0: file_mapa=False
            elif file_mapa:
                line=line.strip()
                if not doble: mapa.append(list(line))
                else:
                    linia_doble=[]
                    for i in list(line):
                        if i==".": linia_doble.extend([".","."])
                        elif i=="#": linia_doble.extend(["#","#"])
                        elif i=="O": linia_doble.extend(["[","]"])
                        elif i=="@": linia_doble.extend(["@","."])
                    mapa.append(linia_doble)
            else:
                ordres+=line.strip()
    return (mapa, ordres, posicio_robot(mapa))
def dimensions_mapa(mapa:Mapa)->tuple[int,int]:
    return (len(mapa), len(mapa[0]))
def posicio_robot(mapa:Mapa)->tuple[int,int]:
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            if mapa[y][x]=="@":
                return (y,x)
    return (-1,-1)
def empeny(mapa:Mapa,posicio:tuple[int,int],direccio:tuple[int,int])->bool:
    [y,x]=posicio
    [dy,dx]=direccio
    new_stack=set([(y,x)])
    stack=[new_stack]
    while len(new_stack)>0:
        new_stack=set()
        for loc in stack[-1]:
            if mapa[loc[0]][loc[1]]==".": continue
            y_nou=loc[0]+dy
            x_nou=loc[1]+dx
            if mapa[y_nou][x_nou]=="#": return False
            elif mapa[y_nou][x_nou] in [".", "O", "[", "]"]:
                new_stack.add((y_nou,x_nou))
                if mapa[y_nou][x_nou] in ["[", "]"] and dy!=0:
                    if mapa[y_nou][x_nou]=="[": new_stack.add((y_nou,x_nou+1))
                    elif mapa[y_nou][x_nou]=="]": new_stack.add((y_nou,x_nou-1))
        if len(new_stack)>0: stack.append(new_stack)
    for i in range (len(stack)):
        for loc in stack[-i-1]:
            if abs(-i-1) in range(len(stack)) and (loc[0]-dy,loc[1]-dx) not in stack[-i-2]:
                mapa[loc[0]][loc[1]]="."
            else:
                mapa[loc[0]][loc[1]]=mapa[loc[0]-dy][loc[1]-dx]
    return True    
def moviment(mapa:Mapa,posicio:tuple[int,int],direccio:tuple[int,int])->tuple[int,int]:
    [y,x]=posicio
    [dy,dx]=direccio
    [y_nou, x_nou]=[y+dy,x+dx]
    if mapa[y_nou][x_nou]=="#":
        return posicio
    if mapa[y_nou][x_nou] in ["O", "[", "]"] and not empeny(mapa,posicio,direccio):
        return posicio
    mapa[y][x]="."
    mapa[y_nou][x_nou]="@"
    return (y_nou,x_nou)
def executa_ordres(mapa:Mapa,pos_incial:tuple[int,int],ordres:str)->None:
    direccions={ "^": (-1,0), ">": (0,1), "v": (1,0), "<": (0,-1)}
    posicio=pos_incial
    for ordre in ordres:
        posicio=moviment(mapa,posicio,direccions[ordre])
def imprimeix_mapa(mapa:Mapa)->None:
    for line in mapa:
        print("".join(line))
def suma_coordenades(mapa:Mapa)->int:
    suma=0
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            if mapa[y][x] in ["O", "["]: suma+=100*y+x
    return suma

(mapa_og, ordres_og, posicio_inicial) = llegeix_input(file)
executa_ordres(mapa_og,posicio_inicial,ordres_og)
# imprimeix_mapa(mapa_og)
print("La suma de les coordenades de les caixes és de:", suma_coordenades(mapa_og)) # 1413675

(mapa_doble, ordres_doble, pos_inicial_doble) = llegeix_input(file,True)
executa_ordres(mapa_doble,pos_inicial_doble,ordres_doble)
# imprimeix_mapa(mapa_doble)
print("La suma de les coordenades de les caixes en el mapa doble és de:", suma_coordenades(mapa_doble)) # 1399772