import os


def get_datafile(file_name: str = "datafile") -> None:
    with open(file_name, "r", encoding="utf-8") as file:
        info = file.read()
    for line in info.split("\n"):
        if "=" not in line or line[0] == "#":
            continue
        line_info = line.split("=")
        name, value = line_info[0], "=".join(line_info[1:])
        os.environ[name] = value
