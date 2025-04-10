import argparse
import datetime
import json
import os
import sys
from typing import Final


TASKS_JSON_PATH: Final[str] = "./tasks.json"


def read_tasks_file() -> dict:
    # read in json file as python dict
    with open(TASKS_JSON_PATH, "r") as json_file:
        return json.load(json_file)


def write_tasks_file(tasks_dict: dict):
    # write updated dict as content for new file
    with open(TASKS_JSON_PATH, "w") as json_file:
        json.dump(tasks_dict, json_file, indent=4)


def list_printer(task: dict, status: str | None = None):
    if not status:
        print(task)
    elif task["status"] == status:
        print(task)


def add_task(description: str):
    # file DNE? create it and write to it
    if not os.path.isfile(TASKS_JSON_PATH):
        with open(TASKS_JSON_PATH, "w") as json_file:
            json.dump({"counter": 0, "tasks": []}, json_file)

    tasks_dict = read_tasks_file()
    tasks_dict["counter"] += 1

    # append task to python dict
    tasks_dict["tasks"].append(
        {
            "id": tasks_dict["counter"],
            "description": description,
            "status": "todo",
            "createdAt": datetime.datetime.now().strftime("%c"),
            "updatedAt": "",
        }
    )

    write_tasks_file(tasks_dict)

    message = f"Task added successfully (ID: {tasks_dict['counter']})"
    print(message)


def list_all_tasks():
    tasks_dict = read_tasks_file()

    for task in tasks_dict["tasks"]:
        list_printer(task)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("args", nargs="+", help="1 to 3 positional arguments")

    parsed = parser.parse_args()
    args: list = parsed.args

    # check that correct number of args are passed
    if not (1 <= len(args) <= 3):
        print("Error: Expected between 1 and 3 arguments.")
        parser.print_usage()
        sys.exit(1)
    else:
        action = args[0]
        # handle add action
        if action == "add" and len(args) == 2:
            add_task(args[1])
        elif action == "list" and len(args) == 1:
            list_all_tasks()


if __name__ == "__main__":
    main()
