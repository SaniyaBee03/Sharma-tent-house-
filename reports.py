from storage import load_data
from datetime import datetime
from decimal import Decimal

BOOKINGS_FILE = "data/bookings.json"
TRACKED_FILE = "data/tracked_equipment.json"
INVENTORY_FILE = "data/inventory.json"
DAMAGE_FILE = "data/damage_reports.json"


def save_report(file_name, report_lines):

    with open(
        file_name,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(report_lines)
        )

    print(
        f"Report saved to {file_name}"
    )


def active_bookings_report():

    bookings = load_data(
        BOOKINGS_FILE
    )

    report_lines = []

    if not bookings:

        print("No bookings found")
        return

    today = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    found = False

    report_lines.append(
        "===== ACTIVE BOOKINGS REPORT ====="
    )

    for booking in bookings:

        pickup_date = datetime.strptime(
            booking["pickup_date"],
            "%d/%m/%Y"
        )

        if pickup_date >= today:

            found = True

            total_amount = booking.get(
                "total_amount",
                "0"
            )

            deposit_amount = booking.get(
                "deposit_amount",
                "0"
            )

            balance_paid = booking.get(
                "balance_paid",
                "0"
            )

            remaining_balance = (
                Decimal(total_amount)
                - Decimal(deposit_amount)
                - Decimal(balance_paid)
            )

            report_lines.append("")
            report_lines.append(
                f"Booking ID: {booking['id']}"
            )
            report_lines.append(
                f"Customer: {booking['customer_name']}"
            )
            report_lines.append(
                f"Event: {booking['event_name']}"
            )
            report_lines.append(
                f"Event Start Date: {booking['start_date']}"
            )
            report_lines.append(
                f"Event End Date: {booking['end_date']}"
            )
            report_lines.append(
                f"Delivery Date: {booking['delivery_date']}"
            )
            report_lines.append(
                f"Pickup Date: {booking['pickup_date']}"
            )
            report_lines.append(
                f"Total Amount: {total_amount}"
            )
            report_lines.append(
                f"Deposit Amount: {deposit_amount}"
            )
            report_lines.append(
                f"Balance Paid: {balance_paid}"
            )
            report_lines.append(
                f"Remaining Balance: {remaining_balance}"
            )

    if not found:

        report_lines.append(
            "No active bookings found"
        )

    save_report(
        "reports/active_bookings_report.txt",
        report_lines
    )


def inventory_out_report():

    tracked_items = load_data(
        TRACKED_FILE
    )

    bookings = load_data(
        BOOKINGS_FILE
    )

    report_lines = []

    report_lines.append(
        "===== INVENTORY OUTSIDE WAREHOUSE ====="
    )

    found = False

    booking_active_statuses = [
        "DISPATCHED"
    ]

    tracked_active_statuses = [
        "OUT_FOR_DELIVERY",
        "RETURNING"
    ]

    for booking in bookings:

        if booking.get(
            "dispatch_status"
        ) not in booking_active_statuses:

            continue

        found = True

        report_lines.append("")
        report_lines.append(
            f"Booking ID: {booking['id']}"
        )

        report_lines.append(
            f"Customer: {booking['customer_name']}"
        )

        report_lines.append(
            f"Status: {booking['dispatch_status']}"
        )

        report_lines.append("")
        report_lines.append(
            "Items Outside Warehouse:"
        )

        for item in booking.get(
            "items",
            []
        ):

            report_lines.append(
                f"- {item['item_name']} "
                f"(Qty: {item['quantity']})"
            )

        tracked_found = False

        for tracked in tracked_items:

            if (
                tracked["booking_id"]
                == booking["id"]
                and tracked.get("status")
                in tracked_active_statuses
            ):

                if not tracked_found:

                    report_lines.append("")
                    report_lines.append(
                        "Tracked Equipment Units:"
                    )

                    tracked_found = True

                report_lines.append(
                    f"- {tracked['unit_id']} "
                    f"(Item ID: {tracked['item_id']}) "
                    f"Status: {tracked['status']}"
                )

    if not found:

        report_lines.append(
            "No inventory is currently outside the warehouse"
        )

    save_report(
        "reports/inventory_out_report.txt",
        report_lines
    )


def damage_report():

    damage_reports = load_data(
        DAMAGE_FILE
    )

    report_lines = []

    report_lines.append(
        "===== DAMAGE REPORT ====="
    )

    found = False

    for damage in damage_reports:

        damaged_quantity = damage.get(
            "damaged_quantity",
            0
        )

        if damaged_quantity <= 0:

            continue

        found = True

        report_lines.append("")
        report_lines.append(
            f"Booking ID: {damage['booking_id']}"
        )
        report_lines.append(
            f"Item: {damage['item_name']}"
        )
        report_lines.append(
            f"Damaged Quantity: {damaged_quantity}"
        )
        report_lines.append(
            f"Status: {damage.get('status', 'UNDER_REPAIR')}"
        )
        report_lines.append(
            f"Reported Date: {damage.get('reported_date', 'N/A')}"
        )

        if damage.get(
            "repaired_date"
        ):

            report_lines.append(
                f"Last Repaired: {damage['repaired_date']}"
            )

    if not found:

        report_lines.append(
            "No damaged items found"
        )

    save_report(
        "reports/damage_report.txt",
        report_lines
    )

def missing_items_report():

    missing_items = load_data(
        "data/missing_items.json"
    )

    active_missing = []

    for item in missing_items:

        if item.get(
            "missing_quantity",
            0
        ) > 0:

            active_missing.append(item)

    report_file = (
        "reports/missing_items_report.txt"
    )

    with open(
        report_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "===== MISSING ITEMS REPORT =====\n"
        )

        if not active_missing:

            file.write(
                "\nNo missing items found\n"
            )

        else:

            for item in active_missing:

                file.write(
                    "\nBooking ID: "
                    + item["booking_id"]
                    + "\n"
                )

                file.write(
                    "Item: "
                    + item["item_name"]
                    + "\n"
                )

                file.write(
                    "Missing Quantity: "
                    + str(
                        item["missing_quantity"]
                    )
                    + "\n"
                )

                file.write(
                    "Reported Date: "
                    + item["reported_date"]
                    + "\n"
                )

    print(
        "Report generated successfully:"
    )

    print(report_file)

def customer_history(customer_name):

    bookings = load_data(
        BOOKINGS_FILE
    )

    report_lines = []

    report_lines.append(
        "===== CUSTOMER HISTORY ====="
    )

    found = False

    total_business = Decimal("0")

    for booking in bookings:

        if (
            customer_name.strip().lower() == booking["customer_name"].strip().lower()
        ):

            found = True

            total_amount = Decimal(
                booking.get(
                    "total_amount",
                    "0"
                )
            )

            total_business += total_amount

            deposit_amount = booking.get(
                "deposit_amount",
                "0"
            )

            balance_paid = booking.get(
                "balance_paid",
                "0"
            )

            remaining_balance = (
                total_amount
                - Decimal(deposit_amount)
                - Decimal(balance_paid)
            )

            report_lines.append("")
            report_lines.append(
                f"Booking ID: {booking['id']}"
            )
            report_lines.append(
                f"Customer: {booking['customer_name']}"
            )
            report_lines.append(
                f"Event: {booking['event_name']}"
            )
            report_lines.append(
                f"Event Address: {booking['event_address']}"
            )
            report_lines.append(
                f"Start Date: {booking['start_date']}"
            )
            report_lines.append(
                f"End Date: {booking['end_date']}"
            )
            report_lines.append(
                f"Delivery Date: {booking['delivery_date']}"
            )
            report_lines.append(
                f"Pickup Date: {booking['pickup_date']}"
            )
            report_lines.append(
                f"Total Amount: {total_amount}"
            )
            report_lines.append(
                f"Deposit Amount: {deposit_amount}"
            )
            report_lines.append(
                f"Balance Paid: {balance_paid}"
            )
            report_lines.append(
                f"Remaining Balance: {remaining_balance}"
            )

            report_lines.append("Items:")

            for item in booking.get(
                "items",
                []
            ):

                report_lines.append(
                    f"- {item['item_name']} | Quantity: {item['quantity']}"
                )

    if not found:

        report_lines.append(
            "No booking history found for this customer"
        )

    else:

        report_lines.append("")
        report_lines.append(
            f"Total Business From Customer: {total_business}"
        )

    save_report(
        "reports/customer_history_report.txt",
        report_lines
    )

def view_todays_deliveries_report():

    bookings = load_data(BOOKINGS_FILE)

    today = datetime.now().strftime("%d/%m/%Y")

    found = False

    report_lines = []
    report_lines.append("===== DELIVERIES FOR TODAY =====")

    print("\n===== DELIVERIES FOR TODAY =====")

    for booking in bookings:

        if booking.get("delivery_date") == today:

            found = True

            print("\n" + booking["id"])
            print("Customer:", booking["customer_name"])
            print("Event:", booking["event_name"])
            print("Delivery Date:", booking["delivery_date"])

            report_lines.append("\nBooking ID: " + booking["id"])
            report_lines.append("Customer: " + booking["customer_name"])
            report_lines.append("Event: " + booking["event_name"])
            report_lines.append("Delivery Date: " + booking["delivery_date"])
            report_lines.append("Items:")

            for item in booking.get("items", []):

                report_lines.append(
                    "- " + item["item_name"] +
                    " | Quantity: " + str(item["quantity"])
                )

    if not found:

        print("No deliveries scheduled for today")
        report_lines.append("\nNo deliveries scheduled for today")

    save_report(
        "reports/todays_deliveries_report.txt",
        report_lines
    )

def view_todays_pickups_report():

    bookings = load_data(BOOKINGS_FILE)

    today = datetime.now().strftime("%d/%m/%Y")

    found = False

    report_lines = []
    report_lines.append("===== PICKUPS FOR TODAY =====")

    print("\n===== PICKUPS FOR TODAY =====")

    for booking in bookings:

        if booking.get("pickup_date") == today:

            found = True

            print("\n" + booking["id"])
            print("Customer:", booking["customer_name"])
            print("Event:", booking["event_name"])
            print("Pickup Date:", booking["pickup_date"])

            report_lines.append("\nBooking ID: " + booking["id"])
            report_lines.append("Customer: " + booking["customer_name"])
            report_lines.append("Event: " + booking["event_name"])
            report_lines.append("Pickup Date: " + booking["pickup_date"])
            report_lines.append("Items:")

            for item in booking.get("items", []):

                report_lines.append(
                    "- " + item["item_name"] +
                    " | Quantity: " + str(item["quantity"])
                )

    if not found:

        print("No pickups scheduled for today")
        report_lines.append("\nNo pickups scheduled for today")

    save_report(
        "reports/todays_pickups_report.txt",
        report_lines
    )
