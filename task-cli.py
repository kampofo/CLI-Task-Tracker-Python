import argparse
import datetime
import json
import os
import sys
from typing import Final


TASKS_JSON_PATH: Final[str] = "./tasks.json"


# read and write file helpers
def read_tasks_file() -> dict:
    # read in json file as python dict
    with open(TASKS_JSON_PATH, "r") as json_file:
        return json.load(json_file)


def write_tasks_file(tasks_dict: dict):
    # write updated dict as content for new file
    with open(TASKS_JSON_PATH, "w") as json_file:
        json.dump(tasks_dict, json_file, indent=4)


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


# list tasks functions
def list_printer(task: dict, status: str | None = None):
    if not status:
        print(task, "\n")
    elif task["status"] == status:
        print(task, "\n")


def list_all_tasks(status: str | None = None):
    tasks_dict = read_tasks_file()

    if not status:
        for task in tasks_dict["tasks"]:
            list_printer(task)
    else:
        for task in tasks_dict["tasks"]:
            list_printer(task, status)


def update_task(id: int, description: str):
    tasks_dict = read_tasks_file()

    for task in tasks_dict["tasks"]:
        if task["id"] == id:
            task["description"] = description
            task["updatedAt"] = datetime.datetime.now().strftime("%c")

    write_tasks_file(tasks_dict)


# mark tasks function
def mark_task(id: int, status: str):
    if status in ["in-progress", "done"]:
        tasks_dict = read_tasks_file()
        for task in tasks_dict["tasks"]:
            if task["id"] == id:
                task["status"] = status
                task["updatedAt"] = datetime.datetime.now().strftime("%c")

        write_tasks_file(tasks_dict)


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

        # handle update action
        if action == "update" and len(args) == 3:
            update_task(int(args[1]), args[2])

        # handle list actions
        elif action == "list":
            if len(args) == 1:
                list_all_tasks()
            elif len(args) == 2:
                if args[1] in ["todo", "in-progress", "done"]:
                    list_all_tasks(args[1])

        elif action == "mark-in-progress" and len(args) == 2:
            # TODO: handle case of trying to cast str int int
            mark_task(int(args[1]), "in-progress")

        elif action == "mark-done" and len(args) == 2:
            # TODO: handle case of trying to cast str int int
            mark_task(int(args[1]), "done")


if __name__ == "__main__":
    main()
