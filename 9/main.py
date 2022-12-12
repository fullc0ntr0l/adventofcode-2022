from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, point) -> bool:
        return self.x == point.x and self.y == point.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def clone(self):
        return Point(self.x, self.y)

    def is_touching(self, point):
        return abs(self.x - point.x) <= 1 and abs(self.y - point.y) <= 1


@dataclass
class Knot:
    position: Point = Point(0, 0)
    child_knot: Optional["Knot"] = None

    def add_tail(self):
        current_tail = self.tail
        current_tail.child_knot = Knot(self.position.clone())

    @property
    def tail(self):
        return self.child_knot.tail if self.child_knot else self

    def change_position(self, x: int, y: int):
        if abs(x - self.position.x) > 1 or abs(y - self.position.y) > 1:
            raise ValueError("Cannot move knot more than one step at a time")

        self.position.x = x
        self.position.y = y

        if self.child_knot and not self.position.is_touching(self.child_knot.position):
            increment_x = 0
            increment_y = 0

            if self.position.x != self.child_knot.position.x:
                increment_x = 1 if self.position.x > self.child_knot.position.x else -1

            if self.position.y != self.child_knot.position.y:
                increment_y = 1 if self.position.y > self.child_knot.position.y else -1

            self.child_knot.change_position(
                self.child_knot.position.x + increment_x,
                self.child_knot.position.y + increment_y,
            )


ROPE_SIZE = 10  # number of knots, including head and tail

file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    tail_points_entered = set()
    head = Knot()
    for _ in range(1, ROPE_SIZE):
        head.add_tail()

    for line in file.read().splitlines():
        direction, moves = line.split()

        for _ in range(int(moves)):
            if direction == "U":
                head.change_position(head.position.x, head.position.y + 1)
            elif direction == "D":
                head.change_position(head.position.x, head.position.y - 1)
            elif direction == "L":
                head.change_position(head.position.x - 1, head.position.y)
            elif direction == "R":
                head.change_position(head.position.x + 1, head.position.y)
            else:
                raise ValueError(f"Invalid direction {direction}")

            tail_points_entered.add(head.tail.position.clone())

    print(f"Entered positions: {len(tail_points_entered)}")
