import re
from dataclasses import dataclass, field
from pathlib import Path


COMMAND_PATTERN = re.compile(r"^\$ (?P<command>\w+)( (?P<argument>.+))?$")
FILE_PATTERN = re.compile(r"^(?P<size>\d+) (?P<name>.+)$")
DIR_PATTERN = re.compile(r"^dir (?P<name>.+)$")

DISK_SIZE = 70_000_000
UPDATE_REQUIRED_SIZE = 30_000_000


@dataclass
class File:
    path: Path
    size: int


@dataclass
class Directory:
    path: Path
    parent: "Directory" = None
    files: list[File] = field(default_factory=list)
    directories: list["Directory"] = field(default_factory=list)

    def add_directory(self, name: str):
        directory = Directory(self.path / name, self)
        self.directories.append(directory)

    def add_file(self, name: str, size: int):
        file = File(self.path / name, size)
        self.files.append(file)

    def find_directory(self, name: str):
        for directory in self.directories:
            if directory.path.name == name:
                return directory

    @property
    def size(self):
        total_size = 0

        for file in self.files:
            total_size += file.size

        for directory in self.directories:
            total_size += directory.size

        return total_size

    def find_directories_with_min_size(self, min_size: int):
        directories = []

        for directory in self.directories:
            if directory.size >= min_size:
                directories.append(directory)

            directories += directory.find_directories_with_min_size(min_size)

        return directories


@dataclass
class Shell:
    root = Directory(Path("/"))
    pwd = root

    def cd(self, name: str):
        print

        if name == str(self.root.path):
            self.pwd = self.root
        elif name == "..":
            if self.pwd != self.root:
                self.pwd = self.pwd.parent
        else:
            directory = self.pwd.find_directory(name)

            if not directory:
                raise ValueError(f"Cannot find directory with name {name}")

            self.pwd = directory

    @property
    def disk_size(self):
        return DISK_SIZE

    @property
    def available_size(self):
        return self.disk_size - self.root.size


file_path = Path(__file__).parent / "data.txt"
with file_path.open("r") as file:
    shell = Shell()

    for line in file.read().splitlines():
        if match := COMMAND_PATTERN.match(line):
            command = match.group("command")
            argument = match.group("argument")

            if command == "ls":
                # For now we don't process this in any way, instead we parse the output it produces
                pass
            elif command == "cd":
                shell.cd(argument)
        elif match := FILE_PATTERN.match(line):
            name = match.group("name")
            size = match.group("size")

            shell.pwd.add_file(name, int(size))
        elif match := DIR_PATTERN.match(line):
            name = match.group("name")

            shell.pwd.add_directory(name)
        else:
            raise ValueError(f"Invalid output: {line}")

    size_to_free_up = UPDATE_REQUIRED_SIZE - shell.available_size
    directories = shell.root.find_directories_with_min_size(size_to_free_up)
    total = min(directory.size for directory in directories)

    print(f"Total size is {total}")
