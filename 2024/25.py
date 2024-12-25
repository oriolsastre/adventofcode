type Clau = tuple[int,int,int,int,int]
type Pany = tuple[int,int,int,int,int]

file="data/25_data.txt"
file_test="data/25_data_test.txt"

def importa_claus_panys(file:str)->tuple[list[Clau], list[Pany]]:
    claus,panys=[],[]
    with open(file, "r") as f:
        tot_fitxer = f.readlines()
        for i in range(0,len(tot_fitxer),8):
            clau_pany=[0 for _ in range(5)]
            for j in range(5):
                clau_pany[j]=sum([1 for x in range(7) if tot_fitxer[i+x][j]=="#"])-1
            line=tot_fitxer[i].strip()
            if line==".....":
                # Clau
                claus.append(tuple(clau_pany))
            elif line=="#####":
                # Pany
                panys.append(tuple(clau_pany))
    return (claus,panys)
def parelles_claus_panys(claus:list[Clau], panys:list[Pany])->int:
    parelles=0
    for clau in claus:
        for pany in panys:
            encaix=[clau[i]+pany[i] for i in range(5)]
            if not any([x>5 for x in encaix]): parelles+=1
    return parelles

claus,panys=importa_claus_panys(file)

print("Hi ha",parelles_claus_panys(claus,panys),"parelles de claus i panys que encaixen.") # 3114