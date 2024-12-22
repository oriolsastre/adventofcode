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

secret_numbers = import_secret_numbers(file)

result1=sum([n_secret_number(secret_number, 2000) for secret_number in secret_numbers])
print("La suma del 2000è número secret és:", result1) # 13022553808