import os


def get_datafile(file_name: str = "datafile") -> None:
    with open(file_name, "r", encoding="utf-8") as file:
        info = file.read()
    for line in info.split("\n"):
        if "=" not in line:
            continue
        line_info = line.split("=")
        os.environ[line_info[0]] = line_info[1]
