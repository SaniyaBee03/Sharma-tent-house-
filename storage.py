import json
import os

FILE_NAME = "inventory.json"


def load_data():

    if not os.path.exists(FILE_NAME):

        with open(FILE_NAME, "w") as file:
            json.dump([], file)

    with open(FILE_NAME, "r") as file:
        data = json.load(file)

    return data


def save_data(data):

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)