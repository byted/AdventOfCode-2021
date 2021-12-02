with open('./input.txt') as f:
    values = [int(l.strip()) for l in f.readlines()]

def increase_counter(values, windows_size = 1):
    #1393
    #1359
    length = len(values)
    last_sum = None
    increases = 0

    for ix in range(windows_size, length+1):
        # Careful with the list slice offsets; syntax is my_list[start(inclusive):end(exclusive)]
        # x=[1,2]; x[0:1] => 1
        current_sum = sum(values[ix-windows_size:ix])
        if last_sum is not None and current_sum > last_sum:
            increases += 1
        last_sum = current_sum

    return increases

print(f'Part 1: {increase_counter(values, windows_size=1)}')
print(f'Part 2: {increase_counter(values, windows_size=3)}')