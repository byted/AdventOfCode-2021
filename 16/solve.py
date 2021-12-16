import sys
import math
import bitstring

ops = {
    0: sum,
    1: math.prod,
    2: min,
    3: max,
    5: lambda ops: 1 if ops[0] > ops[1] else 0,
    6: lambda ops: 1 if ops[0] < ops[1] else 0,
    7: lambda ops: 1 if ops[0] == ops[1] else 0
}

def parse_type4(stream):
    literal_value = bitstring.BitArray()
    while(True):
        last_part = stream.read('bool') is False
        literal_value.append(stream.read('bits:4'))
        if last_part:
            break
    return literal_value.uint

def parse_packet(stream):
    versions = [stream.read('uint:3')]
    type = stream.read('uint:3')
        
    if type == 4:
        return versions, parse_type4(stream)

    # operator packet
    values = []
    if stream.read('bool'):
        # next 11bits tell us how many sub-packets are following
        num_of_packets = stream.read('uint:11')
        for _ in range(num_of_packets):
            subpacket_versions, value = parse_packet(stream)
            versions.extend(subpacket_versions)
            values.append(value)
    else:
        # next 15bits tell us total length all sub-packets
        len_of_packets = stream.read('uint:15')
        start_pos = stream.pos
        while True:
            subpacket_versions, value = parse_packet(stream)
            versions.extend(subpacket_versions)
            values.append(value)
            if stream.pos - start_pos == len_of_packets:
                break
    return versions, ops[type](values)

versions, value = parse_packet(bitstring.BitStream(hex=sys.stdin.readline()))
print(f'Part 1: {sum(versions)}')
print(f'Part 2: {value}')