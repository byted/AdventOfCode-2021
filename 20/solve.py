import sys
import math

mapping = {'.': '0', '#': '1'}
mapping_rev = {'0': '.', '1': '#'}

def get_pixels(map, rx, cx, default_pixel):
    pixels = [
        # top row
        map[rx-1][cx-1] if rx-1  >= 0 and cx-1 >= 0 else default_pixel,
        map[rx-1][cx] if rx-1 >= 0 else default_pixel,
        map[rx-1][cx+1] if rx-1 >= 0 and cx+1 < len(map[rx]) else default_pixel,
        # middle row
        map[rx][cx-1] if cx-1 >= 0 < len(map) else default_pixel,
        map[rx][cx],
        map[rx][cx+1] if cx+1 < len(map[rx]) else default_pixel,
        # bottom row
        map[rx+1][cx-1] if rx+1 < len(map) and cx-1 >= 0 else default_pixel,
        map[rx+1][cx] if rx+1 < len(map) else default_pixel,
        map[rx+1][cx+1] if rx+1 < len(map) and cx+1 < len(map[rx]) else default_pixel,
    ]
    return int(''.join(pixels), base=2)

def extend(image, default_pixel):
    empty_row = [default_pixel]*(len(image[0])+2)
    bigger_img = [empty_row]
    for row in image:
        bigger_img.append([default_pixel] + row + [default_pixel])
    bigger_img.append(empty_row)
    return bigger_img

def enhance_once(image, default_pixel):
    image = extend(image, default_pixel)
    out_img = [[default_pixel]*len(image[0]) for _ in range(len(image))]
    for rx, r in enumerate(out_img):
            for cx, c in enumerate(r):
                out_img[rx][cx] = mapping[image_filter[get_pixels(image, rx, cx, default_pixel)]]
    return out_img

def enhance(image, image_filter, iterations):
    for i in range(iterations):
        image = enhance_once(image, str(i%2) if image_filter[0] == '#' else '0')

    return sum(int(c) for r in image for c in r)

all_lines = [s.strip() for s in sys.stdin.readlines()]
image_filter = all_lines[0].strip()
image = [[mapping[c] for c in line.strip()] for line in all_lines[2:]]

print(f'Part 1: {enhance(image, image_filter, 2)}')
print(f'Part 2: {enhance(image, image_filter, 50)}')