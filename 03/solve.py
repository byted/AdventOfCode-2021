with open('./input.txt') as f:
    # Sample input
    # 111110110111
    # 100111000111
    # 011101111101
    values = [l.strip() for l in f.readlines()]

def most_and_least_common_bit(values, pos, return_numbers=False):
    counter = 0
    numbers = { '0': [], '1': [] }
    for v in values:
        if v[pos] == '1':
            counter += 1
        else:
            counter -= 1
        
        if return_numbers:
            numbers[v[pos]].append(v)

    return counter, numbers

def calculate_consumption_rate(values):
    length = len(values[0])
    gamma = ''
    delta = ''
    for ix in range(length):
        rating, _ = most_and_least_common_bit(values, ix)
        if rating > 0:
            gamma += '1'
            delta += '0'
        else:
            gamma += '0'
            delta += '1'

    return int(gamma, 2) * int(delta, 2)

def filter(values, pos, keep_if_most_common_1, keep_if_most_common_0, keep_if_same):
    while True:
        rating, numbers = most_and_least_common_bit(values, pos, return_numbers=True)
        if rating > 0:
            remaining_numbers = numbers[keep_if_most_common_1]
        elif rating < 0:
            remaining_numbers = numbers[keep_if_most_common_0]
        else:
            remaining_numbers = numbers[keep_if_same]
        
        if len(remaining_numbers) > 1 and pos < len(remaining_numbers[0])-1:
            return filter(remaining_numbers, pos+1, keep_if_most_common_1, keep_if_most_common_0, keep_if_same)
        else:
            return remaining_numbers[0]

def calc_oxy(values):
    return filter(values, 0, '1', '0', '1')

def calc_co2(values):
    return filter(values, 0, '0', '1', '0')


print(f'Part 1: {calculate_consumption_rate(values)}')
print(f'Part 2: {int(calc_oxy(values),2) * int(calc_co2(values),2)}')
