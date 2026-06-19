from storage import load_data, save_data

FILE_NAME = "data/customers.json"


def generate_customer_id(customers):

    if not customers:

        return "CUST_001"

    max_id = 0

    for customer in customers:

        customer_id = customer["id"]

        parts = customer_id.split("_")

        current_id = int(parts[1])

        if current_id > max_id:

            max_id = current_id

    new_id = max_id + 1

    return "CUST_" + str(new_id).zfill(3)


def add_customer():

    customers = load_data(FILE_NAME)

    while True:

        customer_name = input("Enter customer name: ").strip()

        if customer_name == "":

            print("Customer name cannot be empty")

        else:

            break

    while True:

        phone = input("Enter phone number: ").strip()

        if phone == "":

            print("Phone number cannot be empty")

        elif len(phone) != 10:

            print("Mobile number must be exactly 10 digits")

        elif not phone.isdigit():

            print("Mobile number should contain only numbers")

        else:

            break

    for customer in customers:

        if customer["phone"] == phone:

            print("Customer with this phone number already exists")

            return

    customer = {
        "id": generate_customer_id(customers),
        "name": customer_name,
        "phone": phone
    }

    customers.append(customer)

    save_data(FILE_NAME, customers)

    print("Customer added successfully")


def view_customers():

    customers = load_data(FILE_NAME)

    if not customers:

        print("No customers found")

        return

    for customer in customers:

        print("\nID:", customer["id"])
        print("Name:", customer["name"])
        print("Phone:", customer["phone"])


def search_customer():

    customers = load_data(FILE_NAME)

    search_name = input("Enter customer name: ").strip()

    found = False

    for customer in customers:

        if search_name.lower() in customer["name"].lower():

            print("\nID:", customer["id"])
            print("Name:", customer["name"])
            print("Phone:", customer["phone"])

            found = True

    if found == False:

        print("Customer not found")


def update_customer():

    customers = load_data(FILE_NAME)

    search_name = input("Enter customer name: ").strip()

    found = False

    for customer in customers:

        if search_name.lower() in customer["name"].lower():

            print("\nCurrent Details")
            print("ID:", customer["id"])
            print("Name:", customer["name"])
            print("Phone:", customer["phone"])

            while True:

                new_name = input("Enter new customer name: ").strip()

                if new_name == "":

                    print("Customer name cannot be empty")

                else:

                    break

            while True:

                new_phone = input("Enter new phone number: ").strip()

                if new_phone == "":

                    print("Phone number cannot be empty")

                elif len(new_phone) != 10:

                    print("Mobile number must be exactly 10 digits")

                elif not new_phone.isdigit():

                    print("Mobile number should contain only numbers")

                else:

                    break

            for other_customer in customers:

                if other_customer["phone"] == new_phone and other_customer["id"] != customer["id"]:

                    print("Customer with this phone number already exists")

                    return

            customer["name"] = new_name
            customer["phone"] = new_phone

            save_data(FILE_NAME, customers)

            print("Customer updated successfully")

            found = True

            break

    if found == False:

        print("Customer not found")