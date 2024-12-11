file="data/11_data.txt"

pedra_roseta={}

def blink_stone(stone:int)->list[int]:
  new_stones=[]
  if stone == 0: new_stones.append(1)
  elif len(str(stone)) % 2 == 0:
    digit_len=len(str(stone))
    new_stones.append(int(str(stone)[:digit_len//2]))
    new_stones.append(int(str(stone)[digit_len//2:]))
  else:
    new_stones.append(stone*2024)
  return new_stones

def blink_stones(stones:list[int], blinks:int)->int:
  global pedra_roseta
  def roseta_stones(stone:int, blink:int)->int:
    if (stone, blink) in pedra_roseta: return pedra_roseta[(stone, blink)]
    elif blink == 0: return 1
    else:
      new_stones=blink_stone(stone)
      stone_count=sum([roseta_stones(stone, blink-1) for stone in new_stones])
      pedra_roseta[(stone, blink)]=stone_count
      return stone_count
  
  result=0
  for stone in stones:
    result+=roseta_stones(stone, blinks)
  return result

with open(file, "r") as f:
  stones=[int(x) for x in f.readline().strip().split(" ")]

print("Hi haurà", blink_stones(stones, 25), "pedres després de 25 pestanyejos.") # 218079
print("Hi haurà", blink_stones(stones, 75), "pedres després de 75 pestanyejos.") # 259755538429618