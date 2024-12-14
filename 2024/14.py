import copy

file="data/14_data.txt"
file_test="data/14_data_test.txt"

def moviment_robots(robots:list[list[int]], passos:int, mapa:list[int]=[103,101])->list:
    [mapa_y,mapa_x]=mapa
    robots_nous=[]
    for robot in robots:
        [[x_0,y_0],[v_x,v_y]]=robot
        y=((y_0+(v_y*passos) % mapa_y) + mapa_y) % mapa_y
        x=((x_0+(v_x*passos) % mapa_x) + mapa_x) % mapa_x
        robots_nous.append([[x,y],[v_x,v_y]])
    return robots_nous
def pinta_robots(robots:list[int], mapa:list[int]=[103,101])->list:
    [mapa_y,mapa_x]=mapa
    linia_blanc=' '*mapa_x
    mapa_blanc=[linia_blanc]*mapa_y
    for robot in robots:
        [x,y]=robot[0]
        mapa_blanc[y]=mapa_blanc[y][:x]+"X"+mapa_blanc[y][x+1:]
    for linia in mapa_blanc:
        print(linia)
# M'ha servit per veure que els robots tenen un cicle de 10402 passos diferents
def compara_robots(nous_robots:list[int], robots:list[list[int]])->bool:
    for i in range(len(nous_robots)):
        if nous_robots[i][0] != robots[i][0]: return False
        if nous_robots[i][1] != robots[i][1]: return False
    return True
# M'ha servit per veure quines iteracions podien tenir un dibuix.
def mostra_robot(robots:list[list[int]], mapa:list[int]=[103,101])->None:
    nous_robots=copy.deepcopy(robots)
    for i in range(10403):
        nous_robots = moviment_robots(nous_robots,1,mapa)
        tercos=tercos_mapa(nous_robots,mapa)
        mig_vertical = tercos[0][1]+tercos[1][1]+tercos[2][1] > (tercos[0][0]+tercos[0][2]+tercos[1][0]+tercos[1][2]+tercos[2][0]+tercos[2][2])
        mig_horizontal = tercos[1][0]+tercos[1][1]+tercos[1][2] > (tercos[0][0]+tercos[0][1]+tercos[0][2]+tercos[2][0]+tercos[2][1]+tercos[2][2])
        if mig_vertical or mig_horizontal:
            print("Passos:",i)
            pinta_robots(nous_robots,mapa)
            input()
def quadrant_mapa(robots:list[list[int]], mapa:list[int]=[103,101])->list[int]:
    mapa_quadrant=[0,0,0,0]
    [mapa_y,mapa_x]=mapa
    for robot in robots:
        [x,y]=robot[0]
        if y < (mapa_y//2) and x < (mapa_x//2): mapa_quadrant[0]+=1
        elif y < (mapa_y//2) and x > (mapa_x//2): mapa_quadrant[1]+=1
        elif y > (mapa_y//2) and x < (mapa_x//2): mapa_quadrant[2]+=1
        elif y > (mapa_y//2) and x > (mapa_x//2): mapa_quadrant[3]+=1
    return mapa_quadrant
# M'ha servit per veure aquelles iteracions on més robots eren al centre
def tercos_mapa(robots:list[list[int]], mapa:list[int]=[103,101])->list[int]:
    mapa_tercos=[[0,0,0],[0,0,0],[0,0,0]]
    [mapa_y,mapa_x]=mapa
    for robot in robots:
        [x,y]=robot[0]
        if y < (mapa_y//3) and x < (mapa_x//3): mapa_tercos[0][0]+=1
        elif y < (mapa_y//3) and x > (mapa_x//3*2): mapa_tercos[0][2]+=1
        elif y < (mapa_y//3) and x > (mapa_x//3): mapa_tercos[0][1]+=1
        elif y > (mapa_y//3*2) and x < (mapa_x//3): mapa_tercos[2][0]+=1
        elif y > (mapa_y//3*2) and x > (mapa_x//3*2): mapa_tercos[2][2]+=1
        elif y > (mapa_y//3*2) and x > (mapa_x//3): mapa_tercos[2][1]+=1
        elif y > (mapa_y//3) and x < (mapa_x//3): mapa_tercos[1][0]+=1
        elif y > (mapa_y//3) and x > (mapa_x//3*2): mapa_tercos[1][2]+=1
        elif y > (mapa_y//3) and x > (mapa_x//3): mapa_tercos[1][1]+=1
    return mapa_tercos
def seguretat_mapa(robots:list[list[int]], mapa:list[int]=[103,101])->int:
    seguretat=1
    quadrants=quadrant_mapa(robots,mapa)
    for x in quadrants:
        seguretat*=x
    return seguretat
with open(file, "r") as f:
    robots=[]
    for line in f:
        [posicio,velocitat]=line.strip().split(" ")
        posicio=[int(x) for x in posicio.split("=")[1].split(",")]
        velocitat=[int(x) for x in velocitat.split("=")[1].split(",")]
        robots.append([posicio,velocitat])

robots_100=moviment_robots(robots,100)
seguretat=seguretat_mapa(robots_100)
print("La seguretat del mapa es:", seguretat) # 228410028
easteregg=8258
print("L'easteregg es troba a la iteració:", easteregg) # 8258
pinta_robots(moviment_robots(robots,easteregg))