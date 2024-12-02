# Llegeix el fitxer 01_data.txt i guarda les dades
left = []
right = []
with open('01_data.txt', 'r') as f:
    # Guarda els valors del primer numero a l'array left i l'altre número a l'array right
    # Iterant en data, separa el contingut de cada línia per " " i guarda el primer valor a left i el segon a right
    for line in f:
        leftValue, rightValue = line.split(',')
        left.append(leftValue)
        right.append(rightValue)
# Ordena de menor a major els arrays left i right
left.sort()
right.sort()

distance = 0
# Fes un loop per cada element de left o right
for i in range(len(left)):
    # Fes el valor absolut del valor de left[i] - right[i]
    distance += abs(int(left[i]) - int(right[i]))

print("La distància es de:", distance)

similarity = 0
cache = {}
for leftValue in left:
    if leftValue not in cache:
        occurrence = 0
        for rightValue in right:
            if int(leftValue) == int(rightValue):
                occurrence += 1
            elif int(rightValue) > int(leftValue):
                # Els arrays estan ordenats, per això no cal fer més comparacions
                break
        cache[leftValue] = occurrence*int(leftValue)
    similarity += cache[leftValue]

print("La similaritat es de:", similarity)