import re
from pathlib import Path
from queue import LifoQueue


item_pattern = re.compile(r"^\[([A-Z])\]$")
command_pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)$")


def parse_stacks_level(level_string):
    items = []

    while len(level_string) >= 3:
        match = item_pattern.match(level_string[:3])
        item = match.groups()[0] if match else None
        items.append(item)
        level_string = level_string[4:]

    return items


def create_initial_queues(stack_string):
    queues = {}
    lines = stack_string.split("\n")[::-1]
    stack_numbers = lines[0].split()

    for number in stack_numbers:
        queues[number] = LifoQueue()

    for line in lines[1:]:
        items = parse_stacks_level(line)

        for index, item in enumerate(items):
            if item:
                queue_index = stack_numbers[index]
                queues[queue_index].put_nowait(item)

    return queues


def execute_command(queues, command):
    match = re.match(command_pattern, command)
    size, source, destination = match.groups()
    source_queue = queues[source]
    destination_queue = queues[destination]
    moving_items = [source_queue.get_nowait() for _ in range(int(size))][::-1]

    for item in moving_items:
        destination_queue.put_nowait(item)


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    stack, commands = file.read().split("\n\n")
    queues = create_initial_queues(stack)

    for command in commands.strip().split("\n"):
        execute_command(queues, command)

    message = "".join(queue.get_nowait() for queue in queues.values())
    print(f"Message: {message}")
