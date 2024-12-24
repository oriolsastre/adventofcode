type Cables = dict[str,int]
type Porta = tuple[str,str,str,str]

file="data/24_data.txt"
file_test="data/24_data_test.txt"

def import_data(file:str)->tuple[Cables, list[Porta]]:
    cables = {}
    portes = []
    son_cables=True
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line == "": son_cables = False; continue
            if son_cables:
                cable=line.split(": ")
                cables[cable[0]] = int(cable[1])
            else:
                porta=line.split(" ")
                portes.append((porta[0],porta[1],porta[2],porta[4]))
    return (cables, portes)
def executa_porta(porta:Porta, cables:Cables)->int:
    match porta[1]:
        case "AND":
            return cables[porta[0]] & cables[porta[2]] 
        case "OR":
            return cables[porta[0]] | cables[porta[2]]
        case "XOR":
            return cables[porta[0]] ^ cables[porta[2]]       
def executa_cables(cables: Cables, portes:list[Porta])->None:
    while any((porta[3].startswith("z") and porta[3] not in cables) for porta in portes):
        for porta in portes:
            if porta[0] in cables and porta[2] in cables:
                cables[porta[3]] = executa_porta(porta,cables)
def retorna_cables(cables:Cables)->int:
    cables_z={k: v for k,v in sorted(cables.items(), reverse=True) if k.startswith("z")}
    cables_z_bin = "".join(str(x) for x in cables_z.values())
    return int(cables_z_bin,2)

(cables,portes)=import_data(file)
executa_cables(cables,portes)
bin_1 = retorna_cables(cables)
print("El número dels cables que comencen per 'z' és:", bin_1) # 51745744348272