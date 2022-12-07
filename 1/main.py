from pathlib import Path

file_path = Path(__file__).parent / "data.txt"

with file_path.open("r") as file:
    content = file.read()

    arr = content.split("\n\n")
    arr = [sum(int(c) for c in item.split("\n") if c) for item in arr]
    arr = sorted(arr, reverse=True)

    print(f"Calories for top 3 elfs {sum(arr[:3])}")
