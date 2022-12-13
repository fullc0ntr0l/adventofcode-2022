import re
from dataclasses import dataclass, field
from math import prod
from pathlib import Path


@dataclass
class Monkey:
    items: list[int]
    raw_operation: str = field(repr=False)
    test_divisible: int = field(repr=False)
    operation_success_monkey: int = field(repr=False)
    operation_fail_monkey: int = field(repr=False)
    inspected_count: int = field(default=0, repr=False)

    def throw_item(self):
        old = self.items.pop(0)
        new = eval(self.raw_operation)
        new = new // WORRY_LEVEL_DIVISOR
        to_monkey = (
            self.operation_fail_monkey
            if new % self.test_divisible
            else self.operation_success_monkey
        )
        self.inspected_count += 1

        return new, to_monkey

    def add_item(self, item):
        self.items.append(item)


ROUNDS_COUNT = 10000
WORRY_LEVEL_DIVISOR = 1
MONKEY_INDEX_PATTERN = re.compile(r"Monkey (\d+):")
WORRY_LEVELS_PATTERN = re.compile(r"Starting items: (.+)")
OPERATION_PATTERN = re.compile(r"Operation: new = (.+)")
DIVISIBLE_PATTERN = re.compile(r"Test: divisible by (\d+)")
TRUE_EVAL_PATTERN = re.compile(r"If true: throw to monkey (\d+)")
FALSE_EVAL_PATTERN = re.compile(r"If false: throw to monkey (\d+)")

file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    content = file.read()
    monkeys = {}

    for monkey_definition in content.split("\n\n"):
        index = MONKEY_INDEX_PATTERN.search(monkey_definition).group(1)
        raw_items = WORRY_LEVELS_PATTERN.search(monkey_definition).group(1)
        items = list(map(int, raw_items.split(", ")))
        raw_operation = OPERATION_PATTERN.search(monkey_definition).group(1)
        divisible = DIVISIBLE_PATTERN.search(monkey_definition).group(1)
        success_outcome_monkey = TRUE_EVAL_PATTERN.search(monkey_definition).group(1)
        fail_outcome_monkey = FALSE_EVAL_PATTERN.search(monkey_definition).group(1)
        monkeys[int(index)] = Monkey(
            items,
            raw_operation,
            int(divisible),
            int(success_outcome_monkey),
            int(fail_outcome_monkey),
        )

    worry_level_threshold = prod(monkey.test_divisible for monkey in monkeys.values())

    for _ in range(ROUNDS_COUNT):
        for monkey_index in sorted(monkeys.keys()):
            monkey = monkeys[monkey_index]

            while monkey.items:
                worry_level, to_monkey = monkey.throw_item()
                worry_level = worry_level % worry_level_threshold
                to_monkey = monkeys[to_monkey]
                to_monkey.add_item(worry_level)

    for monkey_index, monkey in monkeys.items():
        print(f"Monkey {monkey_index} inspected items {monkey.inspected_count} times.")

    inspected_times = [monkeys[index].inspected_count for index in monkeys.keys()]
    inspected_times = sorted(inspected_times, reverse=True)
    monkey_business = inspected_times[0] * inspected_times[1]
    print(f"Monkey business: {monkey_business}")
