from typing import Dict, Union
import os


def get_datafile() -> Dict[str, str]:
    assert "datafile" in os.listdir(), "Файл не обнаружен."
    res_data: Dict[str, str] = {}
    with open("datafile", "r", encoding="utf-8") as file:
        info = file.read()
    for line in info.split("\n"):
        if "=" not in line:
            continue
        line_info = line.split("=")
        new_dict = {line_info[0]: line_info[1]}
        res_data.update(new_dict)
    return res_data


def save_datafile(datafile: Dict[str, Union[str, int]]) -> None:
    res_to_save = ""
    for name, value in datafile.items():
        res_to_save += "{}={}\n".format(name, str(value))
    with open("datafile", "w", encoding="utf-8") as file:
        file.write(res_to_save)
