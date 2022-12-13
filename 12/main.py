from pathlib import Path

START = "S"
END = "E"
FIRST_HEIGHT = "a"


def get_neighbors(i, j):
    return ((i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j))


def get_height(heightmap, i, j):
    height = heightmap[i][j]

    return FIRST_HEIGHT if height == START else height


def get_route(heightmap, start, end):
    height = len(heightmap)
    width = len(heightmap[0])
    queue = [[start]]
    seen = set([start])

    while queue:
        route = queue.pop(0)
        i, j = route[-1]

        if (i, j) == end:
            return route

        for i2, j2 in get_neighbors(i, j):
            if j2 not in range(width) or i2 not in range(height):
                continue

            if (i2, j2) in seen:
                continue

            current_height = get_height(heightmap, i, j)
            neighbor_height = get_height(heightmap, i2, j2)

            if ord(current_height) + 1 < ord(neighbor_height):
                continue

            queue.append(route + [(i2, j2)])
            seen.add((i2, j2))


def find_position(heightmap, label: str):
    for i, row in enumerate(heightmap):
        for j, square in enumerate(row):
            if square == label:
                return (i, j)


def get_positions(heightmap, labels: list[str]):
    for i, row in enumerate(heightmap):
        for j, square in enumerate(row):
            if square in labels:
                yield (i, j)


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    heightmap = [list(line) for line in file.read().splitlines()]
    end = find_position(heightmap, END)
    routes_lengths = []

    for start in get_positions(heightmap, [START, FIRST_HEIGHT]):
        route = get_route(heightmap, start, end)
        if route:
            route_length = len(route) - 1
            routes_lengths.append(route_length)
            print(f"total steps {route_length}")

    print(f"min: {min(routes_lengths)}")
