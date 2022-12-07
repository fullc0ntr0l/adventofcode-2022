from pathlib import Path

SHAPE_SCORES = {
    # Rock
    "A": 1,
    "X": 1,
    # Paper
    "B": 2,
    "Y": 2,
    # Scissors
    "C": 3,
    "Z": 3,
}

OUTCOME_SCORES = {
    "AZ": 0,
    "BX": 0,
    "CY": 0,
    "AX": 3,
    "BY": 3,
    "CZ": 3,
    "AY": 6,
    "BZ": 6,
    "CX": 6,
}

SHAPE_OUTCOME = {
    "X": 0,  # lose
    "Y": 3,  # draw
    "Z": 6,  # win
}

file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    score = 0

    for line in file.readlines():
        you, me = line.split()

        my_outcome_score = SHAPE_OUTCOME[me]
        me = [
            outcome
            for outcome, score in OUTCOME_SCORES.items()
            if score == my_outcome_score and outcome.startswith(you)
        ][0][1]

        score += SHAPE_SCORES[me]
        score += OUTCOME_SCORES[you + me]

    print(f"Total score is {score}")
