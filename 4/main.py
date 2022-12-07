from pathlib import Path


def section_range(range_string):
    start, end = map(int, range_string.split("-"))
    return set(range(start, end + 1))


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    total = 0

    for line in file.read().splitlines():
        first, second = map(section_range, line.split(","))

        if first.intersection(second):
            total += 1

    print(f"Total overlaps: {total}")
