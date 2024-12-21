import math

file="data/21_data.txt"
file_test="data/21_data_test.txt"

arrow_keypad={"^":(0,1), "A": (0,2), "<": (1,0), "v": (1,1), ">": (1,2)}
numeric_keypad={"7": (0,0), "8":(0,1), "9":(0,2), "4":(1,0), "5":(1,1), "6":(1,2), "1":(2,0), "2":(2,1), "3":(2,2), "0": (3,1), "A": (3,2)}
direccio_arrow={(0,1): ">", (1,0): "v", (0,-1): "<", (-1,0): "^"}

def importa_dades(file:str)->list[str]:
    with open(file, "r") as f:
        return f.read().strip().split("\n")
def ordena_sequencia(sequencia:str, inici:tuple[int,int], final: tuple[int,int], numeric:bool)->str:
    ordenament={'<': 0, 'v': 1, '^': 2, '>': 3}
    if not numeric:
        if inici==(1,0): ordenament={'>': 0, '^': 1,}
        elif final==(1,0): ordenament={'v': 0, '<': 1}
    else:
        if inici in [(3,1), (3,2)] and final[1]==0: ordenament={'^': 0, '<': 1, '>': 2}
        elif inici[1]==0 and final in [(3,1), (3,2)]: ordenament={'<': 0, '>': 1, 'v': 2}
    return "".join(sorted(sequencia, key=lambda x: ordenament.get(x,4)))
def moviment_teclat(inici: str, final: str, numeric:bool=False)->str:
    (y1,x1) = numeric_keypad[inici] if numeric else arrow_keypad[inici]
    (y2,x2) = numeric_keypad[final] if numeric else arrow_keypad[final]
    (y,x) = (y1,x1)
    dy = 0 if y1==y2 else math.copysign(1,y2-y1)
    dx = 0 if x1==x2 else math.copysign(1,x2-x1)
    output=""
    while x!=x2:
        x+=dx
        output+=direccio_arrow[(0,dx)]
    while y!=y2:
        y+=dy
        output+=direccio_arrow[(dy,0)]
    output_ordenat=ordena_sequencia(output, (y1,x1), (y2,x2), numeric)
    return output_ordenat
def ordre_to_arrow(ordre:str, numeric:bool=False)->str:
    start="A"
    output=""
    for char in ordre:
        output+=moviment_teclat(start, char, numeric)
        output+="A"
        start=char
    return output
def jo_maquina_maquina_numeric(ordre:str)->str:
    # Cal posar l'ordre al teclat numeric, amb radiació
    output1 = ordre_to_arrow(ordre, True)
    # Cal controlar el robot que s'ha posat al teclat numeric; té fred
    output2 = ordre_to_arrow(output1, False)
    # Cal controlar el robot que controla el robot amb fred; sóc jo
    return ordre_to_arrow(output2, False)
def complexitat_ordre(ordre:str)->int:
    sequencia=jo_maquina_maquina_numeric(ordre)
    num_ordre=int(ordre[:-1])
    return num_ordre*len(sequencia)

ordres=importa_dades(file)
resultat1=sum([complexitat_ordre(ordre) for ordre in ordres]) ## 184716
print(resultat1)