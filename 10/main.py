import re
from dataclasses import dataclass
from pathlib import Path

ADD_OP_PATTERN = re.compile(r"^addx (-?\d+)$")
CRT_ROW_SIZE = 40
SPRITE_SIZE = 3


@dataclass
class CRT:
    current_cycle: int = 1
    current_value: int = 1

    def run_cycle(self):
        if self.position in self.sprite_range:
            print("#", end="")
        else:
            print(".", end="")

        if self.current_cycle % CRT_ROW_SIZE == 0:
            print()

        self.current_cycle += 1

    def increment(self, value: int):
        self.current_value += value

    @property
    def position(self):
        return self.current_cycle % CRT_ROW_SIZE

    @property
    def sprite_range(self):
        return range(self.current_value, self.current_value + SPRITE_SIZE)


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    crt = CRT()

    for op in file.read().splitlines():
        if op == "noop":
            crt.run_cycle()
        elif match := ADD_OP_PATTERN.match(op):
            crt.run_cycle()
            crt.run_cycle()
            crt.increment(int(match.group(1)))
        else:
            raise ValueError(f"Invalid command: {op}")
