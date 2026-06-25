from storage import load_data, save_data

def read_yes_no(message):

    while True:

        choice = input(
            message
        ).strip().lower()

        if choice in ["y", "n"]:

            return choice

        print(
            "Please enter only y or n"
        )

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

            print(f"Warning: Invalid item ID format: {item_id}")

            continue

        try:

            current_id = int(parts[1])

        except ValueError:

            print(f"Warning: Invalid item ID found: {item_id}")

            continue

        if current_id > max_id:

            max_id = current_id

    new_id = max_id + 1

    return "ITEM_" + str(new_id).zfill(3)


def validate_inventory_data(items):

    for item in items:

        required_fields = [
            "id",
            "name",
            "category",
            "quantity",
            "rent_per_day",
            "tracked"
        ]

        for field in required_fields:

            if field not in item:

                print(
                    f"Warning: Missing field "
                    f"'{field}' in item {item}"
                )

                return False

        try:

            quantity = int(item["quantity"])

            rent_per_day = int(item["rent_per_day"])

            if quantity <= 0:

                print(
                    f"Warning: Invalid quantity "
                    f"in item {item['id']}"
                )

                return False

            if rent_per_day <= 0:

                print(
                    f"Warning: Invalid rent per day "
                    f"in item {item['id']}"
                )

                return False

        except (ValueError, TypeError):

            print(
                f"Warning: Invalid numeric values "
                f"in item {item['id']}"
            )

            return False

    return True


def add_item():

    while True:

        items = load_data("data/inventory.json")

        while True:

            item_name = input(
                "Enter item name: "
            ).strip()

            if item_name == "":

                print(
                    "Item name cannot be empty"
                )

            else:

                break

        normalized_name = " ".join(
            item_name.lower().split()
        )

        duplicate_found = False

        for item in items:

            existing_name = " ".join(
                item["name"].lower().split()
            )

            if existing_name == normalized_name:

                print("Item already exists")

                duplicate_found = True

                break

        if duplicate_found:

            continue

        while True:

            category = input(
                "Enter category: "
            ).strip()

            if category == "":

                print(
                    "Category cannot be empty"
                )

            else:

                break

        quantity = read_positive_int(
            "Enter quantity: "
        )

        rent_per_day = read_positive_int(
            "Enter rent per day: "
        )

        while True:

            tracked = input(
                "Is this tracked equipment? (y/n): "
            ).strip().lower()

            if tracked not in ["y", "n"]:

                print(
                    "Please enter only y or n"
                )

                continue

            break

        item = {

            "id": generate_id(items),

            "name": item_name,

            "category": category,

            "quantity": quantity,

            "rent_per_day": rent_per_day,

            "tracked": tracked == "y"
        }

        if tracked == "y":

            units = []

            prefix = item["id"].replace("_", "")

            for number in range(
                1,
                quantity + 1
            ):

                units.append(
                    prefix
                    + str(number).zfill(3)
                )

            item["units"] = units

        items.append(item)

        save_data(
            "data/inventory.json",
            items
        )

        print(
            "Item added successfully"
        )

        another = read_yes_no(
            "\nAdd another item? (y/n): "
        )
        if another == "n":
            return

def view_items():

    items = load_data("data/inventory.json")

    if not validate_inventory_data(items):

        print("Inventory data validation failed")

        return

    if not items:

        print("No items found")

        return

    for item in items:

        print("\nID:", item["id"])
        print("Name:", item["name"])
        print("Category:", item["category"])
        print("Quantity:", item.get("quantity", 0))
        print("Rent Per Day:", item.get("rent_per_day", 0))
        print(
            "Tracked Equipment:",
            "Yes" if item.get("tracked", False) else "No"
        )

        if item.get("tracked", False):

            tracked_items = load_data(
                "data/tracked_equipment.json"
            )

            assigned = False

            for tracked in tracked_items:

                if (
                    tracked["item_id"] == item["id"]
                    and tracked.get("status") == "ACTIVE"
                ):

                    assigned = True
                    break

            print(
                "Assignment Status:",
                "Assigned" if assigned else "Available"
            )

def update_item():

    while True:

        items = load_data("data/inventory.json")

        if not validate_inventory_data(items):

            print("Inventory data validation failed")

            return

        item_name = input(
            "Enter item name: "
        ).strip()

        found = False

        normalized_name = " ".join(
            item_name.lower().split()
        )

        for item in items:

            existing_name = " ".join(
                item["name"].lower().split()
            )

            if existing_name == normalized_name:

                new_quantity = read_positive_int(
                    "Enter new quantity: "
                )

                if item.get(
                    "tracked",
                    False
                ):

                    tracked_items = load_data(
                        "data/tracked_equipment.json"
                    )

                    assigned_units = 0

                    for tracked in tracked_items:

                        if (
                            tracked["item_id"]
                            == item["id"]
                            and tracked.get("status") in [
                                "RESERVED",
                                "OUT_FOR_DELIVERY",
                                "RETURNING"
                            ]
                        ):

                            assigned_units += 1

                    if (
                        new_quantity
                        < assigned_units
                    ):

                        print(
                            f"Quantity cannot be less than "
                            f"assigned units ({assigned_units})"
                        )

                        return

                item["quantity"] = (
                    new_quantity
                )

                found = True

                break

        if found:

            save_data(
                "data/inventory.json",
                items
            )

            print(
                "Quantity updated"
            )

        else:

            print("Item not found")

        another = read_yes_no(
            "\nUpdate another item? (y/n): "
        )
        if another == "n":
            return

def search_item():

    while True:

        items = load_data(
            "data/inventory.json"
        )

        if not validate_inventory_data(items):

            print(
                "Inventory data validation failed"
            )

            return

        search_name = input(
            "Enter item name: "
        ).strip()

        found = False

        for item in items:

            if (
                search_name.lower()
                in item["name"].lower()
            ):

                print(
                    "\nID:",
                    item["id"]
                )

                print(
                    "Name:",
                    item["name"]
                )

                print(
                    "Category:",
                    item["category"]
                )

                print(
                    "Quantity:",
                    item.get(
                        "quantity",
                        0
                    )
                )

                print(
                    "Rent Per Day:",
                    item.get(
                        "rent_per_day",
                        0
                    )
                )

                print(
                    "Tracked Equipment:",
                    "Yes"
                    if item.get(
                        "tracked",
                        False
                    )
                    else "No"
                )

                found = True

        if not found:

            print("Item not found")

        another = read_yes_no(
            "\nSearch another item? (y/n): "
        )
        if another == "n":
            return
