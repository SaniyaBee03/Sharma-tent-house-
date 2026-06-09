import inventory
import customers
import bookings

while True:

    print("\n===== SHARMA TENT HOUSE =====")
    print("1. Add Item")
    print("2. View Items")
    print("3. Update Quantity")
    print("4. Search Item")
    print("5. Add Customer")
    print("6. View Customers")
    print("7. Search Customer By Name")
    print("8. Update Customer")
    print("9. Create Booking")
    print("10. View Bookings")
    print("11. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        inventory.add_item()

    elif choice == "2":

        inventory.view_items()

    elif choice == "3":

        inventory.update_item()

    elif choice == "4":

        inventory.search_item()

    elif choice == "5":

        customers.add_customer()

    elif choice == "6":

        customers.view_customers()

    elif choice == "7":

        customers.search_customer()

    elif choice == "8":

        customers.update_customer()

    elif choice == "9":

        bookings.create_booking()

    elif choice == "10":

        bookings.view_bookings()

    elif choice == "11":

        print("Thank You")
        break

    else:

        print("Invalid Choice")