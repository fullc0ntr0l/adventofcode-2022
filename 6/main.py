from pathlib import Path

MARKER_LENGTH = 14

file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    data_stream = file.readline().strip()

    for index in range(MARKER_LENGTH, len(data_stream)):
        mask = data_stream[index - MARKER_LENGTH : index]

        if len(mask) == len(set(mask)):
            print(f"Mask is {mask} with index {index}")
            break
