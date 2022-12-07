import string
from pathlib import Path

MAPPINGS_LOWER = {char: ord(char) - 96 for char in string.ascii_lowercase}
MAPPINGS_UPPER = {char: ord(char) - 38 for char in string.ascii_uppercase}
MAPPINGS = {**MAPPINGS_LOWER, **MAPPINGS_UPPER}

priority = lambda char: MAPPINGS[char]


def batch(items, size):
    for i in range(0, len(items), size):
        yield items[i : i + size]


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    total = 0
    rucksacks = file.read().splitlines()

    for group in batch(rucksacks, 3):
        first, second, third = map(set, group)
        priority_items = first.intersection(second, third)

        total += sum(map(priority, priority_items))

    print(f"Sum of priority items is {total}")
