from storage import load_data, save_data

FILE_NAME = "bookings.json"
CUSTOMERS_FILE = "customers.json"
INVENTORY_FILE = "inventory.json"


def generate_booking_id(bookings):

    if not bookings:

        return "BOOK_001"

    max_id = 0

    for booking in bookings:

        booking_id = booking["id"]

        parts = booking_id.split("_")

        current_id = int(parts[1])

        if current_id > max_id:

            max_id = current_id

    new_id = max_id + 1

    return "BOOK_" + str(new_id).zfill(3)


def create_booking():

    bookings = load_data(FILE_NAME)

    customers = load_data(CUSTOMERS_FILE)

    if not customers:

        print("No customers found")

        return

    print("\nAvailable Customers")

    for customer in customers:

        print(customer["id"], "-", customer["name"])

    while True:

        customer_id = input("Enter customer ID: ").strip()

        selected_customer = None

        for customer in customers:

            if customer["id"] == customer_id:

                selected_customer = customer

                break

        if selected_customer:

            break

        print("Customer not found")

    while True:

        event_name = input("Enter event name: ").strip()

        if event_name == "":

            print("Event name cannot be empty")

        else:

            break

    while True:

        event_address = input("Enter event address: ").strip()

        if event_address == "":

            print("Event address cannot be empty")

        else:

            break

    while True:

        start_date = input("Enter start date (DD/MM/YYYY): ").strip()

        if start_date == "":

            print("Start date cannot be empty")

        else:

            break

    while True:

        end_date = input("Enter end date (DD/MM/YYYY): ").strip()

        if end_date == "":

            print("End date cannot be empty")

        else:

            break

    while True:

        delivery_date = input("Enter delivery date (DD/MM/YYYY): ").strip()

        if delivery_date == "":

            print("Delivery date cannot be empty")

        else:

            break

    while True:

        pickup_date = input("Enter pickup date (DD/MM/YYYY): ").strip()

        if pickup_date == "":

            print("Pickup date cannot be empty")

        else:

            break

    inventory_items = load_data(INVENTORY_FILE)

    booking_items = []

    while True:

        print("\nAvailable Inventory")

        for item in inventory_items:

            print(
                item["id"],
                "-",
                item["name"],
                "(Stock:",
                item["quantity"],
                ")"
            )

        item_id = input("Enter item ID: ").strip()

        selected_item = None

        for item in inventory_items:

            if item["id"] == item_id:

                selected_item = item

                break

        if selected_item is None:

            print("Item not found")

            continue

        quantity = int(input("Enter quantity: "))

        booking_items.append({
            "item_id": selected_item["id"],
            "item_name": selected_item["name"],
            "quantity": quantity
        })

        choice = input("Add another item? (y/n): ").lower()

        if choice != "y":

            break

    booking = {
        "id": generate_booking_id(bookings),
        "customer_id": selected_customer["id"],
        "customer_name": selected_customer["name"],
        "event_name": event_name,
        "event_address": event_address,
        "start_date": start_date,
        "end_date": end_date,
        "delivery_date": delivery_date,
        "pickup_date": pickup_date,
        "items": booking_items
    }

    bookings.append(booking)

    save_data(FILE_NAME, bookings)

    print("Booking created successfully")


def view_bookings():

    bookings = load_data(FILE_NAME)

    if not bookings:

        print("No bookings found")

        return

    for booking in bookings:

        print("\nBooking ID:", booking["id"])
        print("Customer ID:", booking["customer_id"])
        print("Customer Name:", booking["customer_name"])
        print("Event Name:", booking["event_name"])
        print("Event Address:", booking.get("event_address", "Not Available"))
        print("Start Date:", booking["start_date"])
        print("End Date:", booking["end_date"])
        print("Delivery Date:", booking.get("delivery_date", "Not Available"))
        print("Pickup Date:", booking.get("pickup_date", "Not Available"))

        print("Items:")

        items = booking.get("items", [])

        if not items:

            print("No items added")

        else:

            for item in items:

                print(
                    "-",
                    item["item_name"],
                    "| Quantity:",
                    item["quantity"]
                )