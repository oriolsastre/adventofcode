file="data/04_data.txt"

xmas_count=0
masmas_count=0

def eXmas(line, j)->bool:
  if (j > len(line)-1-3):
    return False
  xmas=line[j]=="X" and line[j+1]=="M" and line[j+2]=="A" and line[j+3]=="S"
  samx=line[j]=="S" and line[j+1]=="A" and line[j+2]=="M" and line[j+3]=="X"
  return xmas or samx
def sXmas(puzzle, i, j)->bool:
  if (i > len(puzzle)-1-3):
    return False
  xmas=puzzle[i][j]=="X" and puzzle[i+1][j]=="M" and puzzle[i+2][j]=="A" and puzzle[i+3][j]=="S"
  samx=puzzle[i][j]=="S" and puzzle[i+1][j]=="A" and puzzle[i+2][j]=="M" and puzzle[i+3][j]=="X"
  return xmas or samx
def neXmas(puzzle, i, j)->bool:
  if (i<3 or j>len(puzzle[0])-1-3):
    return False
  xmas=puzzle[i][j]=="X" and puzzle[i-1][j+1]=="M" and puzzle[i-2][j+2]=="A" and puzzle[i-3][j+3]=="S"
  samx=puzzle[i][j]=="S" and puzzle[i-1][j+1]=="A" and puzzle[i-2][j+2]=="M" and puzzle[i-3][j+3]=="X"
  return xmas or samx
def seXmas(puzzle, i, j)->bool:
  if (i>len(puzzle)-1-3 or j>len(puzzle[0])-1-3):
    return False
  xmas=puzzle[i][j]=="X" and puzzle[i+1][j+1]=="M" and puzzle[i+2][j+2]=="A" and puzzle[i+3][j+3]=="S"
  samx=puzzle[i][j]=="S" and puzzle[i+1][j+1]=="A" and puzzle[i+2][j+2]=="M" and puzzle[i+3][j+3]=="X"
  return xmas or samx
def x_mas(puzzle, i, j)->bool:
  if (i>len(puzzle)-3 or j>len(puzzle[0])-1-3):
    return False
  if (puzzle[i+1][j+1] != "A"):
    return False
  mas1=(puzzle[i][j]=="M" and puzzle[i+1][j+1]=="A" and puzzle[i+2][j+2]=="S") or (puzzle[i][j]=="S" and puzzle[i+1][j+1]=="A" and puzzle[i+2][j+2]=="M")
  mas2=(puzzle[i][j+2]=="M" and puzzle[i+1][j+1]=="A" and puzzle[i+2][j]=="S") or (puzzle[i][j+2]=="S" and puzzle[i+1][j+1]=="A" and puzzle[i+2][j]=="M")
  return mas1 and mas2

with open(file, "r") as f:
  puzzle=f.readlines()
  puzzle_size=len(puzzle)
  line_length=len(puzzle[0])

  for i in range(puzzle_size):
    for j in range(line_length):
      if eXmas(puzzle[i], j):
        xmas_count+=1
      if sXmas(puzzle, i, j):
        xmas_count+=1
      if neXmas(puzzle, i, j):
        xmas_count+=1
      if seXmas(puzzle, i, j):
        xmas_count+=1
      if x_mas(puzzle, i, j):
        masmas_count+=1

print("He trobat la paraula XMAS:", xmas_count) #2633
print("He trobat la paraula MASMAS:", masmas_count) #1905 too low