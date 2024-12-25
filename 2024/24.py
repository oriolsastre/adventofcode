from random import randint

type Cables = dict[str,int]
type Porta = tuple[str,str,str,str]

file="data/24_data.txt"
file_test="data/24_data_test.txt"

def import_data(file:str)->tuple[Cables, list[Porta]]:
    cables_xy = {}
    portes = []
    son_cables=True
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line == "": son_cables = False; continue
            if son_cables:
                cable=line.split(": ")
                cables_xy[cable[0]] = int(cable[1])
            else:
                porta=line.split(" ")
                portes.append((porta[0],porta[1],porta[2],porta[4]))
    return (cables_xy, portes)
def executa_porta(porta:Porta, cables:Cables)->int:
    match porta[1]:
        case "AND":
            return cables[porta[0]] & cables[porta[2]] 
        case "OR":
            return cables[porta[0]] | cables[porta[2]]
        case "XOR":
            return cables[porta[0]] ^ cables[porta[2]]       
def executa_cables(cables_xy: Cables, portes:list[Porta])->Cables:
    cables = cables_xy.copy()
    while any((porta[3].startswith("z") and porta[3] not in cables) for porta in portes):
        for porta in portes:
            if porta[0] in cables and porta[2] in cables:
                cables[porta[3]] = executa_porta(porta,cables)
    return cables
def genera_input_xy(x:int, y:int)->Cables:
    cables_xy = {}
    x_bin = bin(x)[2:].zfill(45)
    y_bin = bin(y)[2:].zfill(45)
    for i in range(45):
        cables_xy["x"+str(i).zfill(2)] = int(x_bin[-i-1])
        cables_xy["y"+str(i).zfill(2)] = int(y_bin[-i-1])
    return cables_xy
def retorna_cables_z(cables:Cables, lletra:str="z")->str:
    cables_z={k: v for k,v in sorted(cables.items(), reverse=True) if lletra and k.startswith(lletra)}
    # print(cables_z)
    return "".join(str(x) for x in cables_z.values()) 
def retorna_cables_xy(cables:Cables)->tuple[str,str]:
    return (retorna_cables_z(cables,"x"), retorna_cables_z(cables,"y"))
def diferencia_xy_z(cables:Cables)->list[str]:
    diffs=[]
    (x_bin,y_bin)=retorna_cables_xy(cables)
    z_bin = retorna_cables_z(cables).zfill(46)
    xy_bin=bin(int(x_bin,2)+int(y_bin,2))[2:].zfill(46)
    # print(x_bin.zfill(46))
    # print(y_bin.zfill(46))
    # print(z_bin)
    # print(xy_bin)
    for i in range(len(xy_bin)):
        if xy_bin[i] != z_bin[i]: diffs.append("z"+str(len(xy_bin)-i-1).zfill(2))
    # print(diffs)
    return diffs
def get_porta_parent(cable: str, portes:list[Porta])->Porta:
    return next((porta for porta in portes if porta[3] == cable), None)
def portes_in_diff(cables:Cables, portes:list[Porta]):
    diffs = diferencia_xy_z(cables)
    global portes_in_diff_dict
    while len(diffs)>0:
        cable = diffs.pop(0)
        porta = get_porta_parent(cable, portes)
        if cable not in portes_in_diff_dict: portes_in_diff_dict[cable] = []
        if porta != None:
            portes_in_diff_dict[cable].append(porta)
            diffs += [porta[0], porta[2]]
    return count_portes_in_diff(portes_in_diff_dict)
def get_cables_children(cable: str, portes:list[Porta])->list[str]:
    return [porta[3] for porta in portes if porta[0] == cable or porta[2] == cable]
def count_portes_in_diff(portes_in_diff:dict[str, list[str]])->list:
    count_cables={}
    for _, portes in portes_in_diff.items():
        for porta in portes:
            if count_cables.get(porta) == None: count_cables[porta] = 0
            count_cables[porta]+=1
    count_cables = sorted(count_cables.items(), key=lambda x: x[1], reverse=True)
    return count_cables
def swap_portes(porta_a:Porta, porta_b:Porta, portes:list[Porta])->list[Porta]:
    return_portes = portes.copy()
    res_a = porta_a[3]
    res_b = porta_b[3]
    for porta in portes:
        if porta == porta_a:
            porta_a2 = list(porta_a)
            porta_a2[3] = res_b
            porta = tuple(porta_a2)
        elif porta == porta_b:
            porta_b2 = list(porta_b)
            porta_b2[3] = res_a
            porta = tuple(porta_b2)
    return return_portes

(cables_xy,portes)=import_data(file)
cables = executa_cables(cables_xy,portes)
z_bin = retorna_cables_z(cables)
print("El número dels cables que comencen per 'z' és:", int(z_bin,2)) # 51745744348272

print("------")
portes_in_diff_dict = {}

cables_zero_u = executa_cables(genera_input_xy(1,2**45-1),portes)
z_bin_zero_u = retorna_cables_z(cables_zero_u)
portes_in_diff(cables_zero_u,portes)

print("------")

cables_u_zero = executa_cables(genera_input_xy(2**43+2**42+2**41+2**40+2**39,0),portes)
z_bin_u_zero = retorna_cables_z(cables_u_zero)
portes_in_diff(cables_u_zero,portes)

print("------")

for _ in range(150):
    cables_rand = executa_cables(genera_input_xy(randint(0,2**45-1),randint(0,2**45-1)),portes)
    z_bin_rand = retorna_cables_z(cables_rand)
    count_rand=portes_in_diff(cables_rand,portes)
print(count_rand)

for a in range(len(count_rand)):
    for b in range(a+1,len(count_rand)):
        for c in range(b+1,len(count_rand)):
            for d in range(c+1,len(count_rand)):
                for e in range(d+1,len(count_rand)):
                    for f in range(e+1,len(count_rand)):
                        for g in range(f+1,len(count_rand)):
                            for h in range(g+1,len(count_rand)):
                                portes_rand = swap_portes(count_rand[a][0],count_rand[b][0],portes)
                                portes_rand = swap_portes(count_rand[c][0],count_rand[d][0],portes_rand)
                                portes_rand = swap_portes(count_rand[e][0],count_rand[f][0],portes_rand)
                                portes_rand = swap_portes(count_rand[g][0],count_rand[h][0],portes_rand)
                                rand_x,rand_y = [randint(0,2**45-1) for _ in range(2)]
                                cables_swap = executa_cables(genera_input_xy(rand_x,rand_y),portes_rand)
                                z_bin_rand = retorna_cables_z(cables_rand)
                                if bin((rand_x+rand_y))[2:].zfill(46) == z_bin_rand: print(a,b,c,d,e,f,g,h)

for porta in portes:
    if porta not in [porta_diff[0] for porta_diff in count_rand]:
        print(porta)