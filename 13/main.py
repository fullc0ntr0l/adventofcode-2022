from functools import cmp_to_key
from math import prod
from pathlib import Path

DIVIDER_PACKETS = [[[2]], [[6]]]


def check_pairs(left, right):
    if type(left) == type(right) == int:
        if left != right:
            return right - left
    elif type(left) == type(right) == list:
        left_len = len(left)
        right_len = len(right)

        for i in range(max(left_len, right_len)):
            if i >= left_len:
                return 1

            if i >= right_len:
                return -1

            left_item = left[i]
            right_item = right[i]

            result = check_pairs(left_item, right_item)

            if result != 0:
                return result
    else:
        if type(left) == int:
            left = [left]

        if type(right) == int:
            right = [right]

        return check_pairs(left, right)

    return 0


def find_packet_index(packets, packet):
    for index, p in enumerate(packets):
        if p == packet:
            return index + 1
    return 1


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    pairs_indexes = []
    packets = []

    for index, packet in enumerate(file.read().split("\n\n")):
        packets += map(eval, packet.split())

    packets += DIVIDER_PACKETS
    packets = sorted(packets, key=cmp_to_key(check_pairs), reverse=True)

    key = prod(find_packet_index(packets, packet) for packet in DIVIDER_PACKETS)
    print(f"Decoder key: {key}")
