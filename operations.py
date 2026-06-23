from storage import load_data, save_data
from datetime import datetime

RETURNS_FILE = "data/returns.json"
DAMAGE_FILE = "data/damage_reports.json"
MISSING_FILE = "data/missing_items.json"
TRACKED_FILE = "data/tracked_equipment.json"
BOOKINGS_FILE = "data/bookings.json"

def dispatch_booking():

    while True:

        bookings = load_data(BOOKINGS_FILE)

        tracked_items = load_data(
            TRACKED_FILE
        )

        today = datetime.now().strftime(
            "%d/%m/%Y"
        )

        todays_bookings = []

        print(
            "\n===== BOOKINGS FOR DELIVERY TODAY ====="
        )

        for booking in bookings:

            if (
                booking.get("delivery_date")
                == today
            ):

                todays_bookings.append(
                    booking
                )

                print(
                    booking["id"],
                    "-",
                    booking["customer_name"],
                    "-",
                    booking["event_name"]
                )

        if not todays_bookings:

            print(
                "No bookings scheduled for delivery today"
            )

            return

        booking_id = input(
            "\nEnter booking ID to dispatch: "
        ).strip()

        selected_booking = None

        for booking in todays_bookings:

            if booking["id"] == booking_id:

                selected_booking = booking

                break

        if selected_booking is None:

            print("Booking not found")

            continue

        selected_booking["dispatch_status"] = "DISPATCHED"

        save_data(
            BOOKINGS_FILE,
            bookings
        )

        tracked_found = False

        for item in tracked_items:

            if item["booking_id"] == booking_id:

                item["status"] = (
                    "OUT_FOR_DELIVERY"
                )

                tracked_found = True

        if tracked_found:

            save_data(
                TRACKED_FILE,
                tracked_items
            )

        print(
            "Booking dispatched successfully"
        )

        while True:

            choice = input(
                "Dispatch another booking? (y/n): "
            ).strip().lower()

            if choice == "y":

                break

            elif choice == "n":

                return

            else:

                print(
                    "Please enter only y or n"
                )

def process_return():

    while True:

        bookings = load_data(BOOKINGS_FILE)

        returns = load_data(RETURNS_FILE)

        damage_reports = load_data(DAMAGE_FILE)

        missing_items = load_data(MISSING_FILE)

        print(
            "\n===== BOOKINGS AVAILABLE FOR RETURN ====="
        )

        available_bookings = []

        for booking in bookings:

            if booking.get(
                "dispatch_status"
            ) != "DISPATCHED":

                continue

            pending_return = False

            for item in booking["items"]:

                booked_quantity = item["quantity"]

                returned_quantity = item.get(
                    "returned_quantity",
                    0
                )

                damaged_quantity = item.get(
                    "damaged_quantity",
                    0
                )

                missing_quantity = item.get(
                    "missing_quantity",
                    0
                )

                if (
                    returned_quantity
                    + damaged_quantity
                    + missing_quantity
                    < booked_quantity
                ):

                    pending_return = True
                    break

            if pending_return:

                available_bookings.append(
                    booking
                )

                print(
                    booking["id"],
                    "-",
                    booking["customer_name"],
                    "-",
                    booking["event_name"]
                )

        if not available_bookings:

            print(
                "No dispatched bookings pending return"
            )

            return

        booking_id = input(
            "\nEnter booking ID: "
        ).strip()

        selected_booking = None

        for booking in available_bookings:

            if booking["id"] == booking_id:

                selected_booking = booking
                break

        if selected_booking is None:

            print("Booking not found")
            continue

        items_processed = False

        for item in selected_booking["items"]:

            booked_quantity = item["quantity"]

            returned_quantity = item.get(
                "returned_quantity",
                0
            )

            damaged_quantity = item.get(
                "damaged_quantity",
                0
            )

            missing_quantity = item.get(
                "missing_quantity",
                0
            )

            if (
                returned_quantity
                + damaged_quantity
                + missing_quantity
                >= booked_quantity
            ):

                continue

            items_processed = True

            print(
                "\nItem:",
                item["item_name"]
            )

            print(
                "Booked Quantity:",
                booked_quantity
            )

            while True:

                try:

                    new_returned = int(
                        input(
                            "Returned Quantity: "
                        )
                    )

                    new_damaged = int(
                        input(
                            "Damaged Quantity: "
                        )
                    )

                    new_missing = int(
                        input(
                            "Missing Quantity: "
                        )
                    )

                    if (
                        new_returned < 0
                        or new_damaged < 0
                        or new_missing < 0
                    ):

                        print(
                            "Quantities cannot be negative"
                        )

                        continue

                    total_quantity = (
                        new_returned
                        + new_damaged
                        + new_missing
                    )

                    if (
                        total_quantity
                        != booked_quantity
                    ):

                        print(
                            "Returned + Damaged + Missing must equal booked quantity"
                        )

                        continue

                    break

                except ValueError:

                    print(
                        "Please enter valid quantities"
                    )

            item["returned_quantity"] = (
                new_returned
            )

            item["damaged_quantity"] = (
                new_damaged
            )

            item["missing_quantity"] = (
                new_missing
            )

            if new_returned > 0:

                returns.append({

                    "booking_id":
                    booking_id,

                    "item_id":
                    item["item_id"],

                    "item_name":
                    item["item_name"],

                    "returned_quantity":
                    new_returned,

                    "return_date":
                    datetime.now().strftime(
                        "%d/%m/%Y"
                    )
                })

            if new_damaged > 0:

                damage_reports.append({

                    "booking_id":
                    booking_id,

                    "item_id":
                    item["item_id"],

                    "item_name":
                    item["item_name"],

                    "damaged_quantity":
                    new_damaged,

                    "status":
                    "UNDER_REPAIR",

                    "reported_date":
                    datetime.now().strftime(
                        "%d/%m/%Y"
                    )
                })

            if new_missing > 0:

                missing_items.append({

                    "booking_id":
                    booking_id,

                    "item_id":
                    item["item_id"],

                    "item_name":
                    item["item_name"],

                    "missing_quantity":
                    new_missing,

                    "reported_date":
                    datetime.now().strftime(
                        "%d/%m/%Y"
                    )
                })

        if not items_processed:

            print(
                "All items for this booking have already been processed"
            )

            continue

        all_returned = True

        for item in selected_booking["items"]:

            if (
                item.get(
                    "returned_quantity",
                    0
                )
                + item.get(
                    "damaged_quantity",
                    0
                )
                + item.get(
                    "missing_quantity",
                    0
                )
                < item["quantity"]
            ):

                all_returned = False
                break

        if all_returned:

            selected_booking[
                "dispatch_status"
            ] = "RETURNED"

        save_data(
            BOOKINGS_FILE,
            bookings
        )

        save_data(
            RETURNS_FILE,
            returns
        )

        save_data(
            DAMAGE_FILE,
            damage_reports
        )

        save_data(
            MISSING_FILE,
            missing_items
        )

        print(
            "\nReturn processing completed"
        )

        while True:

            another = input(
                "\nProcess another return? (y/n): "
            ).strip().lower()

            if another == "y":

                break

            elif another == "n":

                return

            else:

                print(
                    "Please enter only y or n"
                )

def complete_repair():

    while True:

        damage_reports = load_data(
            DAMAGE_FILE
        )

        inventory_items = load_data(
            "data/inventory.json"
        )

        bookings = load_data(
            BOOKINGS_FILE
        )

        item_summary = {}

        for damage in damage_reports:

            damaged_quantity = damage.get(
                "damaged_quantity",
                0
            )

            if damaged_quantity <= 0:

                continue

            item_id = damage["item_id"]

            if item_id not in item_summary:

                item_summary[item_id] = {

                    "item_name":
                    damage["item_name"],

                    "total_damaged": 0

                }

            item_summary[item_id][
                "total_damaged"
            ] += damaged_quantity

        if not item_summary:

            print(
                "No items are currently under repair"
            )

            return

        item_list = list(
            item_summary.items()
        )

        print(
            "\n===== ITEMS UNDER REPAIR ====="
        )

        for index, (
            item_id,
            details
        ) in enumerate(
            item_list,
            start=1
        ):

            print(
                "\n" + str(index) + ".",
                details["item_name"]
            )

            print(
                "Damaged Quantity:",
                details["total_damaged"]
            )

        while True:

            try:

                choice = int(
                    input(
                        "\nSelect item number: "
                    )
                )

                if (
                    choice < 1
                    or choice > len(item_list)
                ):

                    print(
                        "Invalid selection"
                    )

                    continue

                break

            except ValueError:

                print(
                    "Enter valid number"
                )

        selected_item_id = (
            item_list[
                choice - 1
            ][0]
        )

        selected_item = (
            item_list[
                choice - 1
            ][1]
        )

        total_damaged = (
            selected_item[
                "total_damaged"
            ]
        )

        while True:

            try:

                repaired_quantity = int(
                    input(
                        "Enter repaired quantity: "
                    )
                )

                if repaired_quantity <= 0:

                    print(
                        "Quantity must be greater than 0"
                    )

                    continue

                if repaired_quantity > total_damaged:

                    print(
                        "Cannot repair more than damaged quantity"
                    )

                    continue

                break

            except ValueError:

                print(
                    "Enter valid quantity"
                )

        remaining_to_repair = (
            repaired_quantity
        )

        for damage in damage_reports:

            if (
                damage["item_id"]
                != selected_item_id
            ):

                continue

            damaged_quantity = (
                damage.get(
                    "damaged_quantity",
                    0
                )
            )

            if damaged_quantity <= 0:

                continue

            if (
                remaining_to_repair
                >= damaged_quantity
            ):

                remaining_to_repair -= (
                    damaged_quantity
                )

                damage[
                    "damaged_quantity"
                ] = 0

                damage[
                    "status"
                ] = "AVAILABLE"

            else:

                damage[
                    "damaged_quantity"
                ] = (
                    damaged_quantity
                    - remaining_to_repair
                )

                damage[
                    "status"
                ] = "UNDER_REPAIR"

                remaining_to_repair = 0

            damage[
                "repaired_date"
            ] = datetime.now().strftime(
                "%d/%m/%Y"
            )

            if remaining_to_repair == 0:

                break

        for inventory_item in inventory_items:

            if (
                inventory_item["id"]
                == selected_item_id
            ):

                inventory_item[
                    "quantity"
                ] += repaired_quantity

                break

        remaining_repaired = repaired_quantity

        for booking in bookings:

            for item in booking["items"]:

                if (
                    item["item_id"]
                    == selected_item_id
                    and item.get(
                        "damaged_quantity",
                        0
                    ) > 0
                ):

                    repair_amount = min(
                        remaining_repaired,
                        item[
                            "damaged_quantity"
                        ]
                    )

                    item[
                        "damaged_quantity"
                    ] -= repair_amount

                    item[
                        "returned_quantity"
                    ] += repair_amount

                    remaining_repaired -= (
                        repair_amount
                    )

                    if (
                        remaining_repaired
                        == 0
                    ):

                        break

            if (
                remaining_repaired
                == 0
            ):

                break

        save_data(
            DAMAGE_FILE,
            damage_reports
        )

        save_data(
            BOOKINGS_FILE,
            bookings
        )

        save_data(
            "data/inventory.json",
            inventory_items
        )

        print(
            "\nRepair updated successfully"
        )

        print(
            "Repaired Quantity:",
            repaired_quantity
        )

        while True:

            choice = input(
                "\nRepair another item? (y/n): "
            ).strip().lower()

            if choice == "y":

                break

            elif choice == "n":

                return

            else:

                print(
                    "Please enter only y or n"
                )

def recover_missing_item():

    while True:

        missing_items = load_data(MISSING_FILE)

        bookings = load_data(BOOKINGS_FILE)

        inventory_items = load_data(
            "data/inventory.json"
        )

        active_missing = []

        for record in missing_items:

            if record.get(
                "missing_quantity",
                0
            ) > 0:

                active_missing.append(
                    record
                )

        if not active_missing:

            print(
                "No missing items found"
            )

            return

        print(
            "\n===== MISSING ITEMS ====="
        )

        for index, record in enumerate(
            active_missing,
            start=1
        ):

            customer_name = "Unknown"

            for booking in bookings:

                if (
                    booking["id"]
                    == record["booking_id"]
                ):

                    customer_name = booking[
                        "customer_name"
                    ]

                    break

            print(
                "\n" + str(index) + ".",
                record["item_name"]
            )

            print(
                "Booking:",
                record["booking_id"]
            )

            print(
                "Customer:",
                customer_name
            )

            print(
                "Missing Quantity:",
                record["missing_quantity"]
            )

        while True:

            try:

                choice = int(
                    input(
                        "\nSelect item number: "
                    )
                )

                if (
                    choice < 1
                    or choice > len(
                        active_missing
                    )
                ):

                    print(
                        "Invalid selection"
                    )

                    continue

                break

            except ValueError:

                print(
                    "Enter a valid number"
                )

        selected_record = (
            active_missing[
                choice - 1
            ]
        )

        while True:

            try:

                recovered_quantity = int(
                    input(
                        "Recovered Quantity: "
                    )
                )

                if recovered_quantity <= 0:

                    print(
                        "Quantity must be greater than 0"
                    )

                    continue

                if (
                    recovered_quantity
                    > selected_record[
                        "missing_quantity"
                    ]
                ):

                    print(
                        "Recovered quantity cannot exceed missing quantity"
                    )

                    continue

                break

            except ValueError:

                print(
                    "Enter a valid quantity"
                )

        selected_record[
            "missing_quantity"
        ] -= recovered_quantity

        for booking in bookings:

            if (
                booking["id"]
                == selected_record[
                    "booking_id"
                ]
            ):

                for item in booking["items"]:

                    if (
                        item["item_id"]
                        == selected_record[
                            "item_id"
                        ]
                    ):

                        current_missing = item.get(
                            "missing_quantity",
                            0
                        )

                        item[
                            "missing_quantity"
                        ] = max(
                            0,
                            current_missing
                            - recovered_quantity
                        )

                        item[
                            "returned_quantity"
                        ] = (
                            item.get(
                                "returned_quantity",
                                0
                            )
                            + recovered_quantity
                        )

                        break

                break

        for inventory_item in inventory_items:

            if (
                inventory_item["id"]
                == selected_record[
                    "item_id"
                ]
            ):

                inventory_item[
                    "quantity"
                ] += recovered_quantity

                break

        save_data(
            MISSING_FILE,
            missing_items
        )

        save_data(
            BOOKINGS_FILE,
            bookings
        )

        save_data(
            "data/inventory.json",
            inventory_items
        )

        print(
            "\nMissing item recovered successfully"
        )

        print(
            "Recovered Quantity:",
            recovered_quantity
        )

        while True:

            another = input(
                "\nRecover another item? (y/n): "
            ).strip().lower()

            if another == "y":

                break

            elif another == "n":

                print(
                    "Recovery process completed"
                )

                return

            else:

                print(
                    "Please enter only y or n"
                )

def view_return_status():

    bookings = load_data(
        BOOKINGS_FILE
    )

    print(
        "\n===== RETURN STATUS ====="
    )

    found_pending = False

    for booking in bookings:

        booking_has_pending = False

        for item in booking["items"]:

            if (
                item.get(
                    "damaged_quantity",
                    0
                )
                +
                item.get(
                    "missing_quantity",
                    0
                )
            ) > 0:

                booking_has_pending = True

                break

        if not booking_has_pending:

            continue

        found_pending = True

        print(
            "\nBooking:",
            booking["id"]
        )

        print(
            "Customer:",
            booking["customer_name"]
        )

        for item in booking.get(
            "items",
            []
        ):

            item_id = item["item_id"]

            booked_qty = item["quantity"]

            returned_qty = item.get(
                "returned_quantity",
                0
            )

            damaged_qty = item.get(
                "damaged_quantity",
                0
            )

            missing_qty = item.get(
                "missing_quantity",
                0
            )

            pending_qty = (
                damaged_qty
                + missing_qty
            )

            if pending_qty <= 0:

                continue

            print(
                "\nItem:",
                item["item_name"]
            )

            print(
                "Booked:",
                booked_qty
            )

            print(
                "Returned:",
                returned_qty
            )

            print(
                "Damaged:",
                damaged_qty
            )

            print(
                "Missing:",
                missing_qty
            )

            print(
                "Pending:",
                pending_qty
            )

    if not found_pending:

        print(
            "No pending damaged or missing items"
        )