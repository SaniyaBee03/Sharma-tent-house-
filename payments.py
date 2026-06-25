from storage import load_data, save_data
from decimal import Decimal, InvalidOperation

BOOKINGS_FILE = "data/bookings.json"

def calculate_remaining_balance(total_amount, deposit_amount, balance_paid):
    return (
        Decimal(total_amount)
        - Decimal(deposit_amount)
        - Decimal(balance_paid)
    )


def record_balance_payment():

    while True:

        bookings = load_data(BOOKINGS_FILE)

        print("\n===== ACTIVE BOOKINGS =====")

        active_found = False

        for booking in bookings:

            remaining_balance = calculate_remaining_balance(
                booking["total_amount"],
                booking["deposit_amount"],
                booking.get("balance_paid", "0")
            )

            if remaining_balance > 0:

                active_found = True

                print(
                    booking["id"],
                    "-",
                    booking["customer_name"],
                    "- Remaining:",
                    remaining_balance
                )

        if not active_found:

            print("No bookings with pending balance found")
            return

        booking_id = input("\nEnter booking ID: ").strip()

        selected_booking = None

        for booking in bookings:

            if booking["id"] == booking_id:

                selected_booking = booking
                break

        if selected_booking is None:

            print("Booking not found")
            continue

        total_amount = Decimal(selected_booking["total_amount"])
        deposit_amount = Decimal(selected_booking["deposit_amount"])
        balance_paid = Decimal(selected_booking.get("balance_paid", "0"))

        remaining_balance = calculate_remaining_balance(
            total_amount,
            deposit_amount,
            balance_paid
        )

        print("\nCustomer:", selected_booking["customer_name"])
        print("Total Amount:", total_amount)
        print("Deposit Amount:", deposit_amount)
        print("Already Paid:", balance_paid)
        print("Remaining Balance:", remaining_balance)

        while True:

            try:

                payment_amount = Decimal(
                    input("Enter payment amount: ")
                )

                if payment_amount <= 0:
                    print("Payment amount must be greater than 0")

                elif payment_amount > remaining_balance:
                    print("Payment cannot exceed remaining balance")

                else:
                    break

            except InvalidOperation:
                print("Enter a valid amount")

        selected_booking["balance_paid"] = str(
            balance_paid + payment_amount
        )

        new_remaining = calculate_remaining_balance(
            total_amount,
            deposit_amount,
            selected_booking["balance_paid"]
        )

        if new_remaining == 0:
            selected_booking["payment_status"] = "PAID"

        save_data(BOOKINGS_FILE, bookings)

        print("\nPayment recorded successfully")
        print("Updated Remaining Balance:", new_remaining)

        while True:

            choice = input(
                "\nRecord another balance payment? (y/n): "
            ).strip().lower()

            if choice == "y":
                break

            elif choice == "n":
                print("Payment process completed")
                return

            else:
                print("Please enter only y or n")
