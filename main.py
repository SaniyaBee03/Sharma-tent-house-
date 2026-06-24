import inventory
import customers
import bookings
import operations
import payments
import reports


def inventory_menu():
    while True:
        print("\n===== INVENTORY MANAGEMENT =====")
        print("1. Add Item")
        print("2. View Items")
        print("3. Update Quantity")
        print("4. Search Item")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            inventory.add_item()
        elif choice == "2":
            inventory.view_items()
        elif choice == "3":
            inventory.update_item()
        elif choice == "4":
            inventory.search_item()
        elif choice == "5":
            break
        else:
            print("Invalid choice")


def customer_menu():
    while True:
        print("\n===== CUSTOMER MANAGEMENT =====")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            customers.add_customer()
        elif choice == "2":
            customers.view_customers()
        elif choice == "3":
            customers.search_customer()
        elif choice == "4":
            customers.update_customer()
        elif choice == "5":
            break
        else:
            print("Invalid choice")


def booking_menu():
    while True:
        print("\n===== BOOKING MANAGEMENT =====")
        print("1. Create Booking")
        print("2. View Bookings")
        print("3. View Tracked Equipment")
        print("4. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            bookings.create_booking()
        elif choice == "2":
            bookings.view_bookings()
        elif choice == "3":
            bookings.view_tracked_equipment()
        elif choice == "4":
            break
        else:
            print("Invalid choice")


def operations_menu():
    while True:
        print("\n===== OPERATIONS =====")
        print("1. Dispatch Booking")
        print("2. Process Return")
        print("3. Complete Repair")
        print("4. Recover Missing Item")
        print("5. View Return Status")
        print("6. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            operations.dispatch_booking()
        elif choice == "2":
            operations.process_return()
        elif choice == "3":
            operations.complete_repair()
        elif choice == "4":
            operations.recover_missing_item()
        elif choice == "5":
            operations.view_return_status()
        elif choice == "6":
            break
        else:
            print("Invalid choice")


def payments_menu():
    while True:
        print("\n===== PAYMENTS =====")
        print("1. Record Balance Payment")
        print("2. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            payments.record_balance_payment()
        elif choice == "2":
            break
        else:
            print("Invalid choice")


def reports_menu():
    while True:
        print("\n===== REPORTS =====")
        print("1. Active Bookings Report")
        print("2. Inventory Out Report")
        print("3. Damage Report")
        print("4. Missing Items Report")
        print("5. Customer History Report")
        print("6. Today's Deliveries")
        print("7. Today's Pickups")
        print("8. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            reports.active_bookings_report()
        elif choice == "2":
            reports.inventory_out_report()
        elif choice == "3":
            reports.damage_report()
        elif choice == "4":
            reports.missing_items_report()
        elif choice == "5":
            name = input("Enter customer name: ")
            reports.customer_history(name)
        elif choice == "6":
            reports.view_todays_deliveries_report()
        elif choice == "7":
            reports.view_todays_pickups_report()
        elif choice == "8":
            break
        else:
            print("Invalid choice")


while True:
    print("\n===== SHARMA TENT HOUSE =====")
    print("1. Inventory Management")
    print("2. Customer Management")
    print("3. Booking Management")
    print("4. Operations")
    print("5. Payments")
    print("6. Reports")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        inventory_menu()
    elif choice == "2":
        customer_menu()
    elif choice == "3":
        booking_menu()
    elif choice == "4":
        operations_menu()
    elif choice == "5":
        payments_menu()
    elif choice == "6":
        reports_menu()
    elif choice == "7":
        print("Thank You")
        break
    else:
        print("Invalid Choice")