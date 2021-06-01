from typing import Dict
import os


def get_datafile() -> Dict[str, str]:
    assert "datafile" in os.listdir(), "Файл не обнаружен."
    res: Dict[str, str] = {}
    with open("datafile", "r", encoding="utf-8") as f:
        info = f.read()
    for line in info.split("\n"):
        if "=" not in line:
            continue
        line_info = line.split("=")
        new_dict = {line_info[0]: line_info[1]}
        res = {**res, **new_dict}
    return res


def save_datafile(datafile: dict) -> None:
    res = ""
    for line in datafile:
        res += "{}={}\n".format(line, str(datafile[line]))
    with open("datafile", "w", encoding="utf-8") as f:
        f.write(res)
