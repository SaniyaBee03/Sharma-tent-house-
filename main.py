import inventory

while True:

    print("\n===== SHARMA TENT HOUSE =====")
    print("1. Add Item")
    print("2. View Items")
    print("3. Update Quantity")
    print("4. Search Item")
    print("5. Exit")

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
        print("Thank You")
        break

    else:
        print("Invalid Choice")
        
