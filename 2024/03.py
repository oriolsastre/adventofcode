import re

file="data/03_data.txt"

def sum_muls(memory_string:str)->int:
  suma_muls=0
  mulregex = re.compile(r"mul\(\d{1,3},\d{1,3}\)")
  muls = mulregex.finditer(memory_string)
  for mul in muls:
    nums = mul.group()[4:-1].split(",")
    suma_muls += int(nums[0]) * int(nums[1])
  return suma_muls


with open(file, "r") as f:
  mul_memory = f.read()
  resultat = sum_muls(mul_memory)
  # Mirem els límits entre un don't() i un do() i n'eliminem aquesta part de la memòria
  dodonotregex = re.compile(r"don't\(\)(.|\n)*?do\(\)")
  dolimits = dodonotregex.finditer(mul_memory)
  offset = 0
  for limit in dolimits:
    mul_memory = mul_memory[:limit.start()-offset] + mul_memory[limit.end()-offset:]
    offset += limit.end() - limit.start()
  # Eliminem des de l'últim don't() fins al final, en cas d'existir. Tots els don't han sigut eliminats. Només pot quedar un don't() que no tingués un do() a continuació.
  last_dont = list(re.finditer(r"don't\(\)", mul_memory))
  if len(last_dont) > 0:
    mul_memory = mul_memory[:last_dont[-1].start()]
    print(last_dont[-1])
  resultat2 = sum_muls(mul_memory)

print("La suma dels muls és:", resultat)           # 180233229
print("La suma dels muls permesos és:", resultat2) # 95411583