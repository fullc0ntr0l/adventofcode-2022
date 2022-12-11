from pathlib import Path


def parse_line(tree_list):
    ntrees = len(tree_list)
    visibility = [True, *[False] * (ntrees - 2), True]

    tallest = tree_list[0]
    for i in range(1, ntrees):
        if tallest == 9:
            break

        if tree_list[i] > tallest:
            tallest = tree_list[i]
            visibility[i] = True

    tallest = tree_list[ntrees - 1]
    for i in range(ntrees - 2, -1, -1):
        if tallest == 9:
            break

        if tree_list[i] > tallest:
            tallest = tree_list[i]
            visibility[i] = True

    return visibility


def get_scenic_score(height_list):
    current_tree_height = height_list[0]
    score = 0

    for height in height_list[1:]:
        score += 1

        if height >= current_tree_height:
            break

    return score


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    height_matrix = [list(map(int, line)) for line in file.read().splitlines()]
    nrows = len(height_matrix)
    ncols = len(height_matrix[0])
    visibility_matrix = []

    for i in range(nrows):
        line = height_matrix[i]
        visibility_line = parse_line(line)
        visibility_matrix.append(visibility_line)

    for i in range(ncols):
        line = [row[i] for row in height_matrix]
        visibility_line = parse_line(line)

        for j in range(nrows):
            visibility_matrix[j][i] |= visibility_line[j]

    total_visible = sum(map(sum, visibility_matrix))

    print(f"Total visible trees from outside: {total_visible}")

    # Part 2

    scenic_scores = []

    for i in range(nrows):
        for j in range(ncols):
            up = get_scenic_score([height_matrix[x][j] for x in range(i, -1, -1)])
            down = get_scenic_score([height_matrix[x][j] for x in range(i, nrows)])
            left = get_scenic_score([height_matrix[i][x] for x in range(j, -1, -1)])
            right = get_scenic_score([height_matrix[i][x] for x in range(j, nrows)])
            score = up * down * left * right

            scenic_scores.append(score)

    print(f"Max scenic score: {max(scenic_scores)}")
