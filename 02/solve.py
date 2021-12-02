with open('./input.txt') as f:
    # Sample input
    # forward 8
    # forward 3
    # down 8
    # down 2
    # up 1
    values = []
    for l in f.readlines():
        direction, value = l.strip().split(' ')
        values.append((direction, int(value)))

def navigate(values, apply_aim=False):
    horizontal = 0
    depth = 0
    aim = 0

    # Part 1
    # forward X increases the horizontal position by X units.
    # down X increases the depth by X units.
    # up X decreases the depth by X units.

    # Part 2
    # down X increases your aim by X units.
    # up X decreases your aim by X units.
    # forward X does two things:
    #   It increases your horizontal position by X units.
    #   It increases your depth by your aim multiplied by X.

    for dir, val in values:
        if apply_aim:
            if dir == 'forward':
                horizontal += val
                depth += aim * val
            elif dir == 'up':
                aim -= val
            elif dir == 'down':
                aim += val
        else:
            if dir == 'forward':
                horizontal += val
            elif dir == 'up':
                depth -= val
            elif dir == 'down':
                depth += val

    return horizontal, depth, aim

horizontal_end, depth_end, _ = navigate(values)
print(f'Part 1: {horizontal_end * depth_end}')

horizontal_end, depth_end, _ = navigate(values, apply_aim=True)
print(f'Part 2: {horizontal_end * depth_end}')
