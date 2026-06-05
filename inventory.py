from storage import load_data, save_data


def read_positive_int(message):

    while True:

        try:

            value = int(input(message))

            if value < 0:

                print("Quantity cannot be negative")

            else:

                return value

        except ValueError:

            print("Please enter a valid number")


def generate_id(items):

    if not items:

        return 1

    max_id = max(item["id"] for item in items)

    return max_id + 1


def add_item():

    items = load_data()

    while True:

        item_name = input("Enter item name: ").strip()

        if item_name == "":

            print("Item name cannot be empty")

        else:

            break

    for item in items:

        if item["name"].lower() == item_name.lower():

            print("Item already exists")

            return

    while True:

        category = input("Enter category: ").strip()

        if category == "":

            print("Category cannot be empty")

        else:

            break

    quantity = read_positive_int("Enter quantity: ")

    item = {
        "id": generate_id(items),
        "name": item_name,
        "category": category,
        "quantity": quantity
    }

    items.append(item)

    save_data(items)

    print("Item added successfully")


def view_items():

    items = load_data()

    if not items:

        print("No items found")

        return

    for item in items:

        print("\nID:", item["id"])
        print("Name:", item["name"])
        print("Category:", item["category"])
        print("Quantity:", item["quantity"])


def update_item():

    items = load_data()

    item_name = input("Enter item name: ")

    found = False

    for item in items:

        if item["name"].lower() == item_name.lower():

            new_quantity = read_positive_int("Enter new quantity: ")

            item["quantity"] = new_quantity

            found = True

            break

    if found:

        save_data(items)

        print("Quantity updated")

    else:

        print("Item not found")


def search_item():

    items = load_data()

    search_name = input("Enter item name: ")

    found = False

    for item in items:

        if search_name.lower() in item["name"].lower():

            print("\nID:", item["id"])
            print("Name:", item["name"])
            print("Category:", item["category"])
            print("Quantity:", item["quantity"])

            found = True

    if found == False:

        print("Item not found")
