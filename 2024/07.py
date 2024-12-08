import numpy

file="data/07_data.txt"
data=[]

def print_true(test_value,values,bin)->None:
    operands=["+","*","||"]
    string=str(test_value)+"="+str(values[0])
    for i in range(len(values)-1):
        string+=str(operands[int(bin[i])])+str(values[i+1])
    print(string+"->"+bin)

def test2operand(test_value,values,operands=2)->bool: 
    options=operands**(len(values)-1)
    for i in range(options):
        total_sum=values[0]
        base_i = numpy.base_repr(i, base=operands).zfill(len(values)-1)
        for j in range(len(values)-1):
            if base_i[j] == "0": total_sum+=values[j+1]
            elif base_i[j] == "1": total_sum=total_sum*values[j+1]
            else: total_sum = int(str(total_sum)+str(values[j+1]))
        if total_sum == test_value:
            # print_true(test_value,values,base_i)
            return True
    return False

with open(file, "r") as f:
    for line in f:
        test_value=int(line.split(":")[0])
        values=[int(x) for x in line.split(":")[1].strip().split(" ")]
        data.append([test_value,values])

result1=0
result2=0
for data_line in data:
    if test2operand(data_line[0],data_line[1]): result1+=data_line[0]
    if test2operand(data_line[0],data_line[1],3): result2+=data_line[0]
print("La suma de tots els valors valids es:", result1) # 7885693428401
print("La suma de tots els valors valids amb 3 operands es:", result2) # 348360680516005