file = "data/19_data.txt"
file_test = "data/19_data_test.txt"

def import_towels(file:str)->tuple[list[str], list[str]]:
  with open(file, "r") as f:
    lines = f.read().strip().split("\n")
    tovalloles = lines.pop(0).split(", ")
    lines.pop(0)
    return (tovalloles, lines)

def patrons_possibles(patrons: str, tovalloles: list[str])->tuple[int,int]:
  acumulat=0
  quantitat=0
  manual_patrons = {}
  def patro_manual(patro:str)->int:
    if patro in manual_patrons: return manual_patrons[patro]
    possible=0
    for tovallola in tovalloles:
      if patro==tovallola: possible+=1
      if patro.startswith(tovallola):
        possible+=patro_manual(patro[len(tovallola):])
    manual_patrons[patro]=possible
    return possible
  
  for patro in patrons:
    possibles=patro_manual(patro)
    acumulat+=possibles
    if possibles>0: quantitat+=1
  return (quantitat, acumulat)
  
(tovalloles, patrons) = import_towels(file)
(quantitat, possibles) = patrons_possibles(patrons, tovalloles)
print("Hi ha", quantitat, "patrons possibles") # 333
print("Es poden aconseguir de", possibles, "maneres diferents") # 678536865274732 