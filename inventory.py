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

        if len(parts) != 2:

            print("Warning: Invalid booking ID format: {booking_id}")

            continue

        try:

            current_id = int(parts[1])

        except ValueError:

            print("Warning: Invalid booking ID found: {booking_id}")

            continue

        if current_id > max_id:

            max_id = current_id

    new_id = max_id + 1

    return "ITEM_" + str(new_id).zfill(3)


def add_item():

    items = load_data("inventory.json")

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

    rent_per_day = read_positive_int("Enter rent per day: ")

    tracked = input("Is this tracked equipment? (y/n): ").lower()

    item = {
        "id": generate_id(items),
        "name": item_name,
        "category": category,
        "quantity": quantity,
        "rent_per_day": rent_per_day,
        "tracked": tracked == "y"
    }

    items.append(item)

    save_data("inventory.json", items)

    print("Item added successfully")


def view_items():

    items = load_data("inventory.json")

    if not items:

        print("No items found")

        return

    for item in items:

        print("\nID:", item["id"])
        print("Name:", item["name"])
        print("Category:", item["category"])
        print("Quantity:", item.get("quantity", 0))
        print("Rent Per Day:", item.get("rent_per_day", 0))
        print("Tracked Equipment:","Yes" if item.get("tracked", False)else "No")


def update_item():

    items = load_data("inventory.json")

    item_name = input("Enter item name: ").strip()

    found = False

    normalized_name = " ".join(

    item_name.lower().split()

)

    for item in items:

        existing_name = " ".join(

            item["name"].lower().split()

        )

        if existing_name == normalized_name:

            new_quantity = read_positive_int("Enter new quantity: ")

            item["quantity"] = new_quantity

            found = True

            break

    if found:

        save_data("inventory.json", items)

        print("Quantity updated")

    else:

        print("Item not found")


def search_item():

    items = load_data("inventory.json")

    search_name = input("Enter item name: ").strip()

    found = False

    for item in items:

        if search_name.lower() in item["name"].lower():

            print("\nID:", item["id"])
            print("Name:", item["name"])
            print("Category:", item["category"])
            print("Quantity:", item.get("quantity", 0))
            print("Rent Per Day:", item.get("rent_per_day", 0))

            found = True

    if not found:

        print("Item not found")
