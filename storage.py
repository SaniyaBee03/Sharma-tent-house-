import json


def load_data(file_name):

    try:

        with open(file_name, "r") as file:

            data = json.load(file)

            return data

    except FileNotFoundError:

        return []

    except json.JSONDecodeError:

        print("Invalid JSON data found")

        return []


def save_data(file_name, data):

    with open(file_name, "w") as file:

        json.dump(data, file, indent=4)
