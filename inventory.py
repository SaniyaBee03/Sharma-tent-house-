from storage import load_data, save_data


def add_item():

    items = load_data()

    item_name = input("Enter item name: ")
    category = input("Enter category: ")
    quantity = int(input("Enter quantity: "))

    item = {
        "id": len(items) + 1,
        "name": item_name,
        "category": category,
        "quantity": quantity
    }

    items.append(item)

    save_data(items)

    print("Item added successfully")


def view_items():

    items = load_data()

    if len(items) == 0:
        print("No items found")
        return

    for item in items:

        print("\nID:", item["id"])
        print("Name:", item["name"])
        print("Category:", item["category"])
        print("Quantity:", item["quantity"])


def update_item():

    items = load_data()

    item_id = int(input("Enter item id: "))

    found = False

    for item in items:

        if item["id"] == item_id:

            new_quantity = int(input("Enter new quantity: "))

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