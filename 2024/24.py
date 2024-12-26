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
    return "".join(str(x) for x in cables_z.values()) 
def retorna_cables_xy(cables:Cables)->tuple[str,str]:
    return (retorna_cables_z(cables,"x"), retorna_cables_z(cables,"y"))
def diferencia_xy_z(cables:Cables)->list[str]:
    diffs=[]
    (x_bin,y_bin)=retorna_cables_xy(cables)
    z_bin = retorna_cables_z(cables).zfill(46)
    xy_bin=bin(int(x_bin,2)+int(y_bin,2))[2:].zfill(46)
    for i in range(len(xy_bin)):
        if xy_bin[i] != z_bin[i]: diffs.append("z"+str(len(xy_bin)-i-1).zfill(2))
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
def count_portes_in_diff(portes_in_diff:dict[str, list[str]])->list:
    count_cables={}
    for _, portes in portes_in_diff.items():
        for porta in portes:
            if count_cables.get(porta) == None: count_cables[porta] = 0
            count_cables[porta]+=1
    count_cables = sorted(count_cables.items(), key=lambda x: x[1], reverse=True)
    return count_cables
def input_xor_output(cables_xy:Cables, portes:list[Porta])->list[str]:
    cables_dolents = []
    # En un adder, input i passa a un XOR i el resultat a un XOR que va a output i
    for cable_x in [cables_x for cables_x in cables_xy.keys() if cables_x.startswith("x")]:
        index = cable_x[1:]
        cable_y="y"+index
        cable_z="z"+index
        if index != "00":
            cable_intermedi = next((porta[3] for porta in portes if (porta[1]=="XOR" and ((porta[0]==cable_x and porta[2]==cable_y) or (porta[0]==cable_y and porta[2]==cable_x)))), None)
            if cable_intermedi == None: print("No hauria de passar", cable_x, cable_y)
            else:
                cable_final = next((porta[3] for porta in portes if (porta[1]=="XOR" and ((porta[0]==cable_intermedi or porta[2]==cable_intermedi)))), None)
                if cable_final == None: cables_dolents.append(cable_intermedi)
                else:
                    if cable_final != cable_z: cables_dolents.append(cable_final)
    return cables_dolents
def and_output(portes:list[Porta])->list[str]:
    cables_dolents = []
    # En un adder, l'ouput no surt de cap porta AND
    for porta in portes:
        if porta[1] == "AND" and porta[3].startswith("z"): cables_dolents.append(porta[3])
    return cables_dolents
def xor_output(portes:list[Porta])->list[str]:
    # L'XOR que no prove de input, ha d'acaba a l'ouput
    return [porta[3] for porta in portes if porta[1] == "XOR" and porta[0][0] not in ["x", "y"] and not porta[3].startswith("z")]
def swap_cables(cable_a:str, cable_b:str, portes:list[Porta])->list[Porta]:
    return_portes = portes.copy()
    for i in range(len(return_portes)):
        porta = return_portes[i]
        if porta[3] == cable_a:
            porta_a2 = list(porta)
            porta_a2[3] = cable_b
            return_portes[i] = tuple(porta_a2)
        elif porta[3] == cable_b:
            porta_b2 = list(porta)
            porta_b2[3] = cable_a
            return_portes[i] = tuple(porta_b2)
    return return_portes

(cables_xy,portes)=import_data(file)
cables = executa_cables(cables_xy,portes)
z_bin = retorna_cables_z(cables)
print("El número dels cables que comencen per 'z' és:", int(z_bin,2)) # 51745744348272

portes_in_diff_dict = {}

print("---")
print(set(input_xor_output(cables_xy,portes)+and_output(portes)+xor_output(portes)))
# Miro l'origen de z18 on falla
portes_2 = swap_cables("hmt", "z18", portes)
cables_2 = executa_cables(cables_xy,portes_2)
# portes_in_diff(cables_2,portes_2)

print("---")
print(set(input_xor_output(cables_xy,portes_2)+and_output(portes_2)+xor_output(portes_2)))
# Miro l'origen de z31 on falla
portes_3 = swap_cables("hkh", "z31", portes_2)
cables_3 = executa_cables(cables_xy,portes_3)
# portes_in_diff(cables_3,portes_3)

print("---")
print(set(input_xor_output(cables_xy,portes_3)+and_output(portes_3)+xor_output(portes_3)))
# bfq és el resultat d'un XOR i hauria de ser un z. Mirant origen, ve de x27,y27
portes_4 = swap_cables("bfq", "z27", portes_3)
cables_4 = executa_cables(cables_xy,portes_4)
# portes_in_diff(cables_4,portes_4)

print("---")
print(set(input_xor_output(cables_xy,portes_4)+and_output(portes_4)))
# fjp (malament) està relacionat amb bit 39. Miro l'XOR resultant de z39 i veig que bng no prove d'on toca
portes_5 = swap_cables("fjp", "bng", portes_4)
cables_5 = executa_cables(cables_xy,portes_5)
# portes_in_diff(cables_5,portes_5)

print("Els cables canviats han sigut:", ",".join(sorted(["hmt","z18","hkh","z31","bfq","z27","fjp","bng"])))