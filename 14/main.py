from pathlib import Path

SOURCE = (0, 500)
SAND = "o"
ROCK = "#"
AIR = "."


def create_empty_matrix(paths):
    height = max(max(rng[0] for rng in path) for path in paths) + 2
    width = max(max(rng[1] for rng in path) for path in paths) + 1
    # Won't use Infinity here but adding some extra space horizontaly just in case
    width += 4 * height
    matrix = [[AIR] * width for _ in range(height)]
    # Add floor
    matrix += [[ROCK] * width]

    return matrix


def add_rocks(matrix, paths):
    for path in paths:
        for index in range(len(path) - 1):
            start_i, start_j = path[index]
            end_i, end_j = path[index + 1]

            if start_i == end_i:
                for j in range(min(start_j, end_j), max(start_j, end_j) + 1):
                    matrix[start_i][j] = ROCK
            elif start_j == end_j:
                for i in range(min(start_i, end_i), max(start_i, end_i) + 1):
                    matrix[i][start_j] = ROCK
            else:
                raise ValueError(f"Path should be a vertical or horizontal line")


def sand_unit_fall(matrix):
    i, j = SOURCE

    try:
        while True:
            if matrix[i + 1][j] == AIR:
                i += 1
            elif matrix[i + 1][j - 1] == AIR:
                i += 1
                j -= 1
            elif matrix[i + 1][j + 1] == AIR:
                i += 1
                j += 1
            else:
                if matrix[i][j] == SAND:
                    return False
                else:
                    matrix[i][j] = SAND
                    break

        return True
    except IndexError:
        return False


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    paths = []
    matrix = []

    for line in file.read().splitlines():
        path = []
        for position in line.split(" -> "):
            j, i = map(int, position.split(","))
            path.append((i, j))
        paths.append(path)

    matrix = create_empty_matrix(paths)
    add_rocks(matrix, paths)

    sand_rest_count = 0
    while sand_unit_fall(matrix):
        sand_rest_count += 1

    print(f"Sand rest count: {sand_rest_count}")
