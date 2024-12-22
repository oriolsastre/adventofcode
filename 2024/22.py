import operator

file="data/22_data.txt"
file_test="data/22_data_test.txt"

def import_secret_numbers(file:str)->list[int]:
    with open(file, "r") as f:
        return [int(x) for x in f.read().strip().split("\n")]
def mix_value(value:int, secret_number:int)->int:
    return operator.xor(value, secret_number)
def prune_secret_number(secret_number:int)->int:
    return secret_number%16777216
def next_secret_number(secret_number:int)->int:
    # First step
    first_step=secret_number*64
    first_mix = mix_value(first_step, secret_number)
    first_prune = prune_secret_number(first_mix)
    # Second step
    second_step = first_prune//32
    second_mix = mix_value(second_step, first_prune)
    second_prune = prune_secret_number(second_mix)
    # Third step
    third_step = second_prune*2048
    third_mix = mix_value(third_step, second_prune)
    third_prune = prune_secret_number(third_mix)
    
    return third_prune
def n_secret_number(secret_number:int, n:int)->int:
    for _ in range(n): secret_number=next_secret_number(secret_number)
    return secret_number
def best_buy_n_secret_number(secret_number:int, n:int)->dict:
    millors_preus={}
    preu=secret_number%10
    preu_prev=None
    dpreu=None
    d_preus=[]
    for i in range(n):
        if i > 0: dpreu=preu-preu_prev
        d_preus.append(dpreu)
        if len(d_preus)>4: d_preus.pop(0)
        if tuple(d_preus) not in millors_preus: millors_preus[tuple(d_preus)]=preu
        preu_prev=preu
        secret_number=next_secret_number(secret_number)
        preu=secret_number%10
    return millors_preus
def troba_millor_ordre(millors_preus:list[dict[tuple: int]])->tuple[tuple, int]:
    gran_total={}
    for millor_preu in millors_preus:
        for ordre in millor_preu.keys():
            if None in ordre: continue
            if ordre not in gran_total: gran_total[ordre]=millor_preu[ordre]
            else: gran_total[ordre]+=millor_preu[ordre]
    return max(gran_total.items(), key=operator.itemgetter(1))

### Inici
secret_numbers = import_secret_numbers(file)

result1=sum([n_secret_number(secret_number, 2000) for secret_number in secret_numbers])
print("La suma del 2000è número secret és:", result1) # 13022553808

result2=troba_millor_ordre([best_buy_n_secret_number(secret_number, 2000) for secret_number in secret_numbers])
print("Amb una ordre de", result2[0], "podem vendre", result2[1], "plàtans.") # 1555