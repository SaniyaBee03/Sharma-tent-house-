from storage import load_data, save_data
from datetime import datetime
from decimal import Decimal

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


def read_date(message):

    while True:

        date_input = input(message).strip()

        try:

            date = datetime.strptime(date_input, "%d/%m/%Y")

            return date

        except ValueError:

            print("Please enter a valid date in DD/MM/YYYY format")


def dates_overlap(start1, end1, start2, end2):

    return start1 <= end2 and start2 <= end1


def check_availability(item_id, requested_quantity, start_date, end_date):

    bookings = load_data(FILE_NAME)

    inventory_items = load_data(INVENTORY_FILE)

    total_quantity = 0

    for item in inventory_items:

        if item["id"] == item_id:

            total_quantity = item["quantity"]

            break

    booked_quantity = 0

    for booking in bookings:

        booking_start = datetime.strptime(
            booking["start_date"],
            "%d/%m/%Y"
        )

        booking_end = datetime.strptime(
            booking["end_date"],
            "%d/%m/%Y"
        )

        if dates_overlap(
            start_date,
            end_date,
            booking_start,
            booking_end
        ):

            for booked_item in booking.get("items", []):

                if booked_item["item_id"] == item_id:

                    booked_quantity += booked_item["quantity"]

    available_quantity = total_quantity - booked_quantity

    return requested_quantity <= available_quantity


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

        start_date = read_date("Enter start date (DD/MM/YYYY): ")

        end_date = read_date("Enter end date (DD/MM/YYYY): ")

        delivery_date = read_date("Enter delivery date (DD/MM/YYYY): ")

        pickup_date = read_date("Enter pickup date (DD/MM/YYYY): ")

        if end_date < start_date:

            print("End date cannot be before start date")

        elif delivery_date > start_date:

            print("Delivery date must be before or on start date")

        elif pickup_date < end_date:

            print("Pickup date must be after or on end date")

        else:

            break

    rental_days = (end_date - start_date).days + 1

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

        while True:

            try:

                quantity = int(input("Enter quantity: "))

                if quantity <= 0:

                    print("Quantity must be greater than 0")

                    continue

                if not check_availability(
                    selected_item["id"],
                    quantity,
                    start_date,
                    end_date
                ):

                    print(
                        "Required quantity is not available "
                        "for the selected dates"
                    )

                    continue

                break

            except ValueError:

                print("Please enter a valid number")

        rent_per_day = Decimal(
            str(selected_item["rent_per_day"])
        )

        item_total = (
            rent_per_day *
            Decimal(str(quantity)) *
            Decimal(str(rental_days))
        )

        booking_items.append({
            "item_id": selected_item["id"],
            "item_name": selected_item["name"],
            "quantity": quantity,
            "rent_per_day": str(rent_per_day),
            "days": rental_days,
            "item_total": str(item_total)
        })

        choice = input("Add another item? (y/n): ").lower()

        if choice != "y":

            break

    if not booking_items:

        print("At least one item must be added")

        return

    total_amount = Decimal("0.00")

    for item in booking_items:

        total_amount += Decimal(item["item_total"])

    while True:

        try:

            deposit_amount = Decimal(
                input("Enter deposit amount: ")
            )

            if deposit_amount < 0:

                print("Deposit cannot be negative")

            elif deposit_amount > total_amount:

                print(
                    "Deposit cannot exceed total amount"
                )

            else:

                break

        except:

            print("Enter a valid amount")

    balance_amount = total_amount - deposit_amount

    booking = {
        "id": generate_booking_id(bookings),
        "customer_id": selected_customer["id"],
        "customer_name": selected_customer["name"],
        "event_name": event_name,
        "event_address": event_address,
        "start_date": start_date.strftime("%d/%m/%Y"),
        "end_date": end_date.strftime("%d/%m/%Y"),
        "delivery_date": delivery_date.strftime("%d/%m/%Y"),
        "pickup_date": pickup_date.strftime("%d/%m/%Y"),
        "rental_days": rental_days,
        "items": booking_items,
        "total_amount": str(total_amount),
        "deposit_amount": str(deposit_amount),
        "balance_amount": str(balance_amount)
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
        print("Rental Days:", booking.get("rental_days", 0))
        print("Total Amount:", booking.get("total_amount", 0))
        print("Deposit Amount:", booking.get("deposit_amount", 0))
        print("Balance Amount:", booking.get("balance_amount", 0))

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
                    item["quantity"],
                    "| Rent/Day:",
                    item.get("rent_per_day", 0),
                    "| Total:",
                    item.get("item_total", 0)
                )
