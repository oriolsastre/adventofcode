import math, operator
file="data/17_data.txt"
file_test="data/17_data_test.txt"

def importa_dades(file:str)->tuple[dict[int,int,int], list[int]]:
  with open(file, "r") as f:
    lines=f.readlines()
    registers_abc=[int(x.split(":")[1].strip()) for x in lines[:3]]
    program= [int(x) for x in lines[4].split(":")[1].strip().split(",")]
  return (registers_abc, program)
def get_combo_operand(operand:int, registers:list[int])->int:
  combo_operand=(0,1,2,3,registers[0],registers[1],registers[2])
  return combo_operand[operand]

def run_program(program:list[int], registers_abc:list[int,int,int])->str:
  i=0
  output=[]
  while i < len(program)-1:
    salt=2
    match program[i]:
      case 0:
        registers_abc[0]=math.trunc(registers_abc[0]/math.pow(2,get_combo_operand(program[i+1],registers_abc)))
      case 1:
        registers_abc[1]=operator.xor(registers_abc[1],program[i+1])
      case 2:
        registers_abc[1]=get_combo_operand(program[i+1], registers_abc) % 8
      case 3:
        if registers_abc[0]!=0:
          i=program[i+1]
          salt=0
      case 4:
        registers_abc[1]=operator.xor(registers_abc[1],registers_abc[2])
      case 5:
        output.append(get_combo_operand(program[i+1], registers_abc)%8)
      case 6:
        registers_abc[1]=math.trunc(registers_abc[0]/math.pow(2,get_combo_operand(program[i+1],registers_abc)))
      case 7:
        registers_abc[2]=math.trunc(registers_abc[0]/math.pow(2,get_combo_operand(program[i+1],registers_abc)))
    i+=salt
  return ",".join([str(x) for x in output])

(registres, programa) = importa_dades(file)
print("L'output del programa és:", run_program(programa, registres)) # 6,2,7,2,3,1,6,0,5

a=(((((((((((((((6*8)+5)*8+6)*8+2)*8+1)*8+6)*8+6)*8+0)*8+5)*8+2)*8+2)*8+4)*8+7)*8+1)*8+5)*8+5
print("Amb un registre A de:", a, "el programa es produeix a ell mateix") # 36548287712877