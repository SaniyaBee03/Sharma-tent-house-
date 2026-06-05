import json

FILE_NAME = "inventory.json"


def load_data(file_name):

    try:

        with open(FILE_NAME, "r") as file:

            data = json.load(file)

            return data

    except FileNotFoundError:

        return []

    except json.JSONDecodeError:

        print("Invalid JSON data found")

        return []


def save_data(data):

    with open(FILE_NAME, "w") as file:

        json.dump(data, file, indent=4)
