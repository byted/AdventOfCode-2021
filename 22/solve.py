import sys
import math
import re

cuboids = []
for line in sys.stdin.readlines():
    mode, x1, x2, y1, y2, z1, z2 = re.match(r'^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$', line.strip()).groups()
    cuboids.append((mode, int(x1), int(x2), int(y1), int(y2), int(z1), int(z2)))

# Part 1: just do it!
def boot_seq(cuboids):
    core = set()
    for mode, x1, x2, y1, y2, z1, z2 in cuboids:
        for x in range(max(-50, x1), min(50, x2)+1):
            for y in range(max(-50, y1), min(50, y2)+1):
                for z in range(max(-50, z1), min(50, z2)+1):
                    if mode == 'on':
                        core.add((x,y,z))
                    else:
                        core.discard((x,y,z))
    return core

# Part 2:
def substract_cube(cube1, cube2):
    '''
        Produces a list of regions of cube 1 that do not overlap with cube 2.
        Repeatedly cuts of non-overlapping cubes from cube 1.
    '''
    def split_overlap(cube1, cube2):
        '''Split cube 1 along the overlap with cube 2. Returns the overlapping part and the non-overlapping one'''
        no_overlap, overlap = None, None
        for i in range(0, len(cube1), 2):
            # left-side overlap
            if cube2[i+1] >= cube1[i] and cube2[i+1] < cube1[i+1]:
                no_overlap = [c for c in cube1]
                no_overlap[i] = cube2[i+1]+1

                overlap = [c for c in cube1]
                overlap[i+1] = cube2[i+1]

            # and the other side
            elif cube2[i] > cube1[i] and cube2[i] <= cube1[i+1]:
                no_overlap = [c for c in cube1]
                no_overlap[i+1] = cube2[i]-1

                overlap = [c for c in cube1]
                overlap[i] = cube2[i]

            if overlap is not None:
                return [tuple(no_overlap), tuple(overlap)]

        return None, None

    def is_fully_contained(cube1, cube2):
        '''Return True if cube 1 is fully within the bounds of cube 2'''
        return cube2[0] <= cube1[0] and cube2[1] >= cube1[1] and cube2[2] <= cube1[2] and cube2[3] >= cube1[3] and cube2[4] <= cube1[4] and cube2[5] >= cube1[5]

    def has_overlap(cube1, cube2):
        '''Return True if cube 1 does not overlap with cube 2 at all'''
        return cube2[0] > cube1[1] or cube2[1] < cube1[0] or cube2[2] > cube1[3] or cube2[3] < cube1[2] or cube2[4] > cube1[5] or cube2[5] < cube1[4]

    new_cubes = []
    curr_cube = cube1
    while True:
        if has_overlap(curr_cube, cube2):
            new_cubes.append(curr_cube)
            return new_cubes
        if is_fully_contained(curr_cube, cube2):
            return new_cubes

        no_overlap_cube, curr_cube = split_overlap(curr_cube, cube2)
        if curr_cube is not None:
            new_cubes.append(no_overlap_cube)

def smart_boot_seq(cuboids):
    core = [cuboids[0][1:]]
    for mode, *cube in cuboids[1:]:
        # Check overlap of new cuboid with all existing ones in the core
        core = [split_cube for c1 in core for split_cube in (substract_cube(c1, cube))]
        # now that the new one is "cut out" from all others...
        if mode =='on':
            # ...add it back in to turn it on; this prevents double-counting of overlapping 'on' cuboids
            core.append(cube)
    return core

def count_ons_in_core(core):
    return sum((x2-x1+1) * (y2-y1+1) * (z2-z1+1) for x1, x2, y1, y2, z1, z2 in core)

print(f'Part 1: {len(boot_seq(cuboids))}')
print(f'Part 2: {count_ons_in_core(smart_boot_seq(cuboids))}')