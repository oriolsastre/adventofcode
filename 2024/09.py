import copy
file="data/09_data.txt"

def prepare_file(line)->list:
  block_list=[]
  file_id=0
  for i in range(len(line)):
    file_size=int(line[i])
    if i % 2 == 0:
      for _ in range(file_size):
        block_list.append(file_id)
      file_id+=1
    else:
      for _ in range(file_size):
        block_list.append(".")
  return block_list
def prepare_file_2(line)->list:
  block_list=[]
  file_id=0
  for i in range(len(line)):
    file_size=int(line[i])
    if i % 2 == 0:
      file_block=[file_id,file_size]
      block_list.append(file_block)
      file_id+=1
    elif file_size > 0:
      space_block=[".", file_size]
      block_list.append(space_block)
  return block_list
  
def compress_block(block_list)->list[int]:
  compressed_block_list=[]
  j=len(block_list)-1
  for i in range(len(block_list)):
    if i > j: break
    block=block_list[i]
    if block != ".": compressed_block_list.append(block)
    else:
      if j > i:
        while(block_list[j] == "."): j-=1
        compressed_block_list.append(block_list[j])
        j-=1
  return compressed_block_list
def compress_block_2(block_list)->list[int]:
  compressed_block_list=copy.deepcopy(block_list)
  for block in reversed(block_list):
    if block[0] == "." or block[0] == "-": continue
    add_file_to_free_space(compressed_block_list, block)
  return compressed_block_list
def search_first_free_space(block_list, space_size)->int:
  for i in range(len(block_list)):
    if block_list[i][0] == "." and block_list[i][1] >= space_size: return i
  return -1
def add_file_to_free_space(block_list, file)->bool:
  space_index=search_first_free_space(block_list, file[1])
  file_index = block_list.index(file)
  if space_index < 0: print(file_index, space_index)
  if space_index == -1 or space_index > file_index:
    return False
  block_list[space_index][1]-=file[1]  
  insert_file=copy.deepcopy(file)
  block_list[file_index] = ["-", file[1]]
  block_list.insert(space_index, insert_file)
  return True

def get_checksum(compressed_block_list)->int:
  checksum=0
  for i in range(len(compressed_block_list)):
    checksum+=i * compressed_block_list[i]
  return checksum
def get_checksum2(compressed_block_list)->int:
  checksum=0
  i=0
  for block in compressed_block_list:
    if block[1] == 0: continue
    for _ in range(block[1]):
      if block[0] != "." and block[0] != "-": checksum+=i*block[0]
      i+=1
  return checksum

with open(file, "r") as f:
  line=f.readline().strip()

line1=prepare_file(line)
compressed_line=compress_block(line1)
checksum1=get_checksum(compressed_line)
print("La suma de control dels blocks comprimits amb el primer mètode és:", checksum1) # 6346871685398

line2=prepare_file_2(line)
compressed_line2=compress_block_2(line2)
checksum2=get_checksum2(compressed_line2)
print("La suma de control dels blocks comprimits amb el segon mètode es:", checksum2) # 6373055193464