from storage import load_data, save_data


def read_positive_int(message):

    while True:

        try:

            value = int(input(message))

            if value <= 0:

                print("Value must be greater than 0")

            else:

                return value

        except ValueError:

            print("Please enter a valid number")


def generate_id(items):

    if not items:

        return "ITEM_001"

    max_id = 0

    for item in items:

        item_id = item["id"]

        parts = item_id.split("_")

        current_id = int(parts[1])

        if current_id > max_id:

            max_id = current_id

    new_id = max_id + 1

    return "ITEM_" + str(new_id).zfill(3)


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

    rental_price = read_positive_int("Enter rental price per day: ")

    item = {
        "id": generate_id(items),
        "name": item_name,
        "category": category,
        "quantity": quantity,
        "rental_price": rental_price
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
        print("Rental Price:", item["rental_price"])


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

    search_name = input("Enter item name: ").strip()

    found = False

    for item in items:

        if search_name.lower() in item["name"].lower():

            print("\nID:", item["id"])
            print("Name:", item["name"])
            print("Category:", item["category"])
            print("Quantity:", item["quantity"])
            print("Rental Price:", item.get("rental_price", 0))

            found = True

    if found == False:

        print("Item not found")
