from storage import load_data, save_data
from datetime import datetime
from decimal import Decimal, InvalidOperation

FILE_NAME = "data/bookings.json"
CUSTOMERS_FILE = "data/customers.json"
INVENTORY_FILE = "data/inventory.json"
TRACKED_FILE = "data/tracked_equipment.json"

ITEM_WEIGHT = 10
OVERLAP_WEIGHT = 20

LOW_PRESSURE_LIMIT = 50
MEDIUM_PRESSURE_LIMIT = 100

def generate_booking_id(bookings):

    if not bookings:
        return "BOOK_001"

    max_id = 0

    for booking in bookings:

        booking_id = booking["id"]

        parts = booking_id.split("_")

        if len(parts) != 2:

            print(f"Warning: Invalid booking ID format: {booking_id}")

            continue

        try:

            current_id = int(parts[1])

        except ValueError:

            print(f"Warning: Invalid booking ID found: {booking_id}")

            continue

        if current_id > max_id:
            max_id = current_id

    new_id = max_id + 1

    return "BOOK_" + str(new_id).zfill(3)

def validate_booking_data(bookings):

    required_fields = [
        "id",
        "customer_id",
        "customer_name",
        "event_name",
        "event_address",
        "start_date",
        "end_date",
        "delivery_date",
        "pickup_date",
        "items"
    ]

    for booking in bookings:

        for field in required_fields:

            if field not in booking:

                print(
                    f"Missing field '{field}' "
                    f"in booking {booking.get('id', 'Unknown')}"
                )

                return False

    return True

def read_date(message):

    while True:

        date_input = input(message).strip()

        try:

            date = datetime.strptime(date_input, "%d/%m/%Y")

            return date

        except ValueError:

            print("Please enter a valid date in DD/MM/YYYY format")

def read_booking_dates():

    today = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    while True:

        start_date = read_date(
            "Enter start date (DD/MM/YYYY): "
        )

        if start_date < today:

            print(
                "Start date cannot be in the past"
            )

        else:

            break

    while True:

        end_date = read_date(
            "Enter end date (DD/MM/YYYY): "
        )

        if end_date < today:

            print(
                "End date cannot be in the past"
            )

        elif end_date < start_date:

            print(
                "End date cannot be before start date"
            )

        else:

            break

    while True:

        delivery_date = read_date(
            "Enter delivery date (DD/MM/YYYY): "
        )

        if delivery_date < today:

            print(
                "Delivery date cannot be in the past"
            )

        elif delivery_date > start_date:

            print(
                "Delivery date must be before or on start date"
            )

        else:

            break

    while True:

        pickup_date = read_date(
            "Enter pickup date (DD/MM/YYYY): "
        )

        if pickup_date < today:

            print(
                "Pickup date cannot be in the past"
            )

        elif pickup_date < end_date:

            print(
                "Pickup date must be after or on end date"
            )

        else:

            break

    return (
        start_date,
        end_date,
        delivery_date,
        pickup_date
    )

def dates_overlap(
    start1,
    end1,
    start2,
    end2
):

    return (
        start1 <= end2
        and start2 <= end1
    )

def check_availability(
    item_id,
    requested_quantity,
    start_date,
    end_date
):

    bookings = load_data(FILE_NAME)

    inventory_items = load_data(INVENTORY_FILE)

    selected_item = None

    for item in inventory_items:

        if item["id"] == item_id:

            selected_item = item
            break

    if selected_item is None:

        return False

    try:

        total_quantity = int(

            selected_item.get("quantity", 0)

        )

    except (ValueError, TypeError):

        print("Invalid quantity found in inventory data")

        return False

    if total_quantity <= 0:

        return False

    booked_quantity = 0

    for booking in bookings:

        booking_start = datetime.strptime(
            booking["delivery_date"],
            "%d/%m/%Y"
        )

        booking_end = datetime.strptime(
            booking["pickup_date"],
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

def get_available_quantity(
    item_id,
    start_date,
    end_date
):

    bookings = load_data(FILE_NAME)

    inventory_items = load_data(
        INVENTORY_FILE
    )

    total_quantity = 0

    for item in inventory_items:

        if item["id"] == item_id:

            total_quantity = item["quantity"]

            break

    booked_quantity = 0

    for booking in bookings:

        booking_start = datetime.strptime(
            booking["delivery_date"],
            "%d/%m/%Y"
        )

        booking_end = datetime.strptime(
            booking["pickup_date"],
            "%d/%m/%Y"
        )

        if dates_overlap(
            start_date,
            end_date,
            booking_start,
            booking_end
        ):

            for booked_item in booking["items"]:

                if booked_item["item_id"] == item_id:

                    booked_quantity += (
                        booked_item["quantity"]
                    )

    return (
        total_quantity -
        booked_quantity
    )

def validate_booking_items(items):

    required_fields = [
        "item_id",
        "quantity",
        "rent_per_day",
        "item_total"
    ]

    for item in items:

        for field in required_fields:

            if field not in item:

                print(
                    f"Invalid booking item. "
                    f"Missing field: {field}"
                )

                return False

    return True

def calculate_pressure_score(
    booking_items,
    delivery_date,
    pickup_date
):

    bookings = load_data(FILE_NAME)

    total_quantity = 0

    for item in booking_items:

        total_quantity += item["quantity"]

    item_count = len(booking_items)

    overlap_count = 0

    for booking in bookings:

        booking_delivery = datetime.strptime(
            booking["delivery_date"],
            "%d/%m/%Y"
        )

        booking_pickup = datetime.strptime(
            booking["pickup_date"],
            "%d/%m/%Y"
        )

        if dates_overlap(
            delivery_date,
            pickup_date,
            booking_delivery,
            booking_pickup
        ):

            overlap_count += 1

    pressure_score = (
        total_quantity +
        (item_count * ITEM_WEIGHT) +
        (overlap_count * OVERLAP_WEIGHT)
    )

    if pressure_score < LOW_PRESSURE_LIMIT:

        pressure_level = "LOW"

    elif pressure_score < MEDIUM_PRESSURE_LIMIT:

        pressure_level = "MEDIUM"

    else:

        pressure_level = "HIGH"

    return pressure_score, pressure_level

def assign_tracked_equipment(
    item_id,
    booking_id,
    assigned_unit
):

    tracked_items = load_data(TRACKED_FILE)

    tracked_items.append({
        "item_id": item_id,
        "booking_id": booking_id,
        "unit_id": assigned_unit,
        "assigned_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "released_at": None,
        "status": "RESERVED"
    })

    save_data(
        TRACKED_FILE,
        tracked_items
    )

def unassign_tracked_equipment(booking_id):

    tracked_items = load_data(TRACKED_FILE)

    found = False

    for item in tracked_items:

        if item["booking_id"] == booking_id:

            item["released_at"] = (
                datetime.now().strftime("%d/%m/%Y %H:%M")
            )

            item["status"] = "AVAILABLE"

            found = True

    if found:

        save_data(
            TRACKED_FILE,
            tracked_items
        )

        print("Tracked equipment released successfully")

    else:

        print("No tracked equipment found for this booking")

def get_available_unit(
    item_id,
    delivery_date,
    pickup_date
):

    inventory_items = load_data(INVENTORY_FILE)

    tracked_items = load_data(TRACKED_FILE)

    for item in inventory_items:

        if item["id"] == item_id:

            units = item.get("units", [])

            break

    else:

        return None

    used_units = []

    bookings = load_data(FILE_NAME)

    for tracked in tracked_items:

        if tracked.get("status") in ["RESERVED",
                                     "OUT_FOR_DELIVERY",
                                     "AT_EVENT",
                                     "RETURNING"]:
            
            used_units.append(
                tracked["unit_id"]
            )

        for booking in bookings:

            if booking["id"] == tracked["booking_id"]:

                booking_delivery = datetime.strptime(
                    booking["delivery_date"],
                    "%d/%m/%Y"
                )

                booking_pickup = datetime.strptime(
                    booking["pickup_date"],
                    "%d/%m/%Y"
                )

                if dates_overlap(
                    delivery_date,
                    pickup_date,
                    booking_delivery,
                    booking_pickup
                ):

                    used_units.append(
                        tracked["unit_id"]
                    )

    for unit in units:

        if unit not in used_units:

            return unit

    return None

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

        event_address = input(

            "Enter event address: "

            ).strip()
        
        if event_address == "":

            print(

                "Event address cannot be empty"

            )

        elif not any(

                char.isalpha()

                for char in event_address

                ):
            
            print(

                "Address must contain at least one letter"

            )

        else:
            
            break
        
    (
        start_date,
        end_date,
        delivery_date,
        pickup_date
    ) = read_booking_dates()

    rental_days = (end_date - start_date).days + 1

    inventory_items = load_data(INVENTORY_FILE)

    booking_items = []

    while True:

        print("\nAvailable Inventory")

        for item in inventory_items:

            available_quantity = (
                get_available_quantity(
                    item["id"],
                    delivery_date,
                    pickup_date
                )
            )

            print(
                item["id"],
                "-",
                item["name"],
                "(Available:",
                available_quantity,
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

        assigned_unit = None

        if selected_item.get("tracked", False):

            assigned_unit = get_available_unit(
                selected_item["id"],
                delivery_date,
                pickup_date
            )

            if assigned_unit is None:

                print("No tracked equipment unit available")

                continue

        while True:

            try:

                quantity = int(input("Enter quantity: "))

                if quantity <= 0:

                    print("Quantity must be greater than 0")

                    continue

                available_quantity = (
                    get_available_quantity(
                        selected_item["id"],
                        delivery_date,
                        pickup_date
                    )
                )

                if quantity > available_quantity:

                    print(
                        "Only",
                        available_quantity,
                        "items available for selected dates"
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
            "returned_quantity": 0,
            "damaged_quantity": 0,
            "missing_quantity": 0,
            "assigned_unit": assigned_unit,
            "rent_per_day": str(rent_per_day),
            "days": rental_days,
            "item_total": str(item_total)
        })

        while True:

            choice = input(
                "Add another item? (y/n): "
            ).strip().lower()

            if choice in ["y", "n"]:

                break

            print("Please enter only y or n")

        if choice == "n":

            break

    if not booking_items:

        print("At least one item must be added")

        return

    if not validate_booking_items(
        booking_items
    ):

        return

    total_amount = Decimal("0.00")

    for item in booking_items:

        total_amount += Decimal(
            item["item_total"]
        )

    while True:

        try:

            deposit_amount = Decimal(
                input("Enter deposit amount: ")
            )

            if deposit_amount < 0:

                print(
                    "Deposit cannot be negative"
                )

            elif deposit_amount > total_amount:

                print(
                    "Deposit cannot exceed total amount"
                )

            else:

                break

        except InvalidOperation:

            print("Enter a valid amount")

    balance_amount = (
        total_amount - deposit_amount
    )

    pressure_score, pressure_level = (
        calculate_pressure_score(
            booking_items,
            delivery_date,
            pickup_date
        )
    )

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
        "balance_paid": "0",
        "pressure_score": pressure_score,
        "dispatch_status": "PENDING"
    }

    bookings.append(booking)

    for item in booking_items:

        for inventory_item in inventory_items:

            if (
                inventory_item["id"] == item["item_id"]
                and inventory_item.get(
                    "tracked",
                    False
                )
            ):

                assign_tracked_equipment(
                    item["item_id"],
                    booking["id"],
                    item.get("assigned_unit")
                )

    save_data(FILE_NAME, bookings)

    print("Booking created successfully")
    
    while True:
        choice = input(
            "Create another booking? (y/n): "
            ).strip().lower()
        
        if choice == "y":
            create_booking()
            return
        
        elif choice == "n":
            return
        else:
            print("Please enter only y or n")


def view_bookings():

    bookings = load_data(FILE_NAME)

    if not validate_booking_data(bookings):

        return

    inventory_items = load_data(INVENTORY_FILE)

    valid_item_ids = []

    for inventory_item in inventory_items:

        valid_item_ids.append(inventory_item["id"])

    if not bookings:

        print("No bookings found")

        return

    for booking in bookings:

        booking_id = booking["id"]

        parts = booking_id.split("_")

        if len(parts) != 2:

            print(f"Warning: Invalid booking ID format: {booking_id}")

        elif not parts[1].isdigit():

            print(f"Warning: Invalid booking ID found: {booking_id}")
        
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
        
        balance_paid = Decimal(
            booking.get(
                "balance_paid",
                "0"
            )
        )

        balance_amount = (
            Decimal(booking["total_amount"]) -
            Decimal(booking["deposit_amount"]) -
            balance_paid
        )

        print("Balance Paid:", balance_paid)
        print("Remaining Balance:", balance_amount)
        print("Items:")
        pressure_score = booking.get("pressure_score", 0)
        if pressure_score < 50:
            pressure_level = "LOW"
        elif pressure_score < 100:
            pressure_level = "MEDIUM"
        else:
            pressure_level = "HIGH"
        print("Pressure Score:", pressure_score)
        print("Pressure Level:", pressure_level)

        items = booking.get("items", [])

        if not items:

            print("No items added")

        else:

            for item in items:

                if item["item_id"] not in valid_item_ids:

                    print("- Invalid Item Reference:",item["item_id"])

                    continue

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

                for inventory_item in inventory_items:

                    if (inventory_item["id"] == item["item_id"]and inventory_item.get("tracked", False)):

                        print("  Tracked Equipment: Yes")

                        if item.get("assigned_unit"):

                            print(
                                "  Assigned Unit:",
                                item["assigned_unit"]
                            )

                        break

def view_tracked_equipment():

    tracked_items = load_data(TRACKED_FILE)

    bookings = load_data(FILE_NAME)

    inventory_items = load_data(INVENTORY_FILE)

    if not tracked_items:

        print("No tracked equipment assignments found")

        return

    for tracked in tracked_items:

        item_name = "Unknown"

        for item in inventory_items:

            if item["id"] == tracked["item_id"]:

                item_name = item["name"]

                break

        for booking in bookings:

            if booking["id"] == tracked["booking_id"]:

                print(
                    "\nEquipment:",
                    item_name,
                    "(" + tracked["item_id"] + ")"
                )

                print(
                    "Booking ID:",
                    booking["id"]
                )

                print(
                    "Customer:",
                    booking["customer_name"]
                )

                print(
                    "Delivery:",
                    booking["delivery_date"]
                )

                print(
                    "Pickup:",
                    booking["pickup_date"]
                )

                print(
                    "Status:",
                    tracked.get("status", "RESERVED")
                )

                print(
                    "Assigned At:",
                    tracked.get("assigned_at", "N/A")
                )

                print(
                    "Released At:",
                    tracked.get("released_at", "N/A")
                )

                break