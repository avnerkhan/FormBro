import json


def read_and_load(file_name: str) -> list:
    try:
        return json.loads(open(file_name).read())
    except:
        print("Error occured at read_and_load when trying to read " + file_name)


def write_to_file(file_name: str, info: list) -> None:
    if not info:
        raise ValueError("Info we are trying to write is empty")
    try:
        with open(file_name, "w") as f:
            json.dump(info, f)
    except:
        print("Error occeuer at write_to_file when trying to write to " + file_name)
