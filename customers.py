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

    while True:

        customers = load_data(FILE_NAME)

        while True:

            customer_name = input(
                "Enter customer name: "
            ).strip()

            if customer_name == "":

                print(
                    "Customer name cannot be empty"
                )

            else:

                break

        while True:

            phone = input(
                "Enter phone number: "
            ).strip()

            if phone == "":

                print(
                    "Phone number cannot be empty"
                )

            elif len(phone) != 10:

                print(
                    "Mobile number must be exactly 10 digits"
                )

            elif not phone.isdigit():

                print(
                    "Mobile number should contain only numbers"
                )

            else:

                break

        duplicate_found = False

        for customer in customers:

            if customer["phone"] == phone:

                print(
                    "Customer with this phone number already exists"
                )

                duplicate_found = True

                break

        if duplicate_found:

            continue

        while True:

            address = input(
                "Enter address: "
            ).strip()

            if address == "":

                print(
                    "Address cannot be empty"
                )

            elif not any(
                character.isalpha()
                for character in address
            ):

                print(
                    "Address must contain location details"
                )

            else:

                break

        customer = {

            "id": generate_customer_id(
                customers
            ),

            "name": customer_name,

            "phone": phone,

            "address": address
        }

        customers.append(customer)

        save_data(
            FILE_NAME,
            customers
        )

        print(
            "Customer added successfully"
        )

        while True:

            another = input(
                "\nAdd another customer? (y/n): "
            ).strip().lower()

            if another == "y":

                break

            elif another == "n":

                return

            else:

                print(
                    "Please enter only y or n"
                )


def view_customers():

    customers = load_data(FILE_NAME)

    if not customers:

        print("No customers found")

        return

    for customer in customers:

        print("\nID:", customer["id"])
        print("Name:", customer["name"])
        print("Phone:", customer["phone"])
        print("Address:", customer.get("address", "Not Available"))


def search_customer():

    while True:

        customers = load_data(FILE_NAME)

        search_name = input(
            "Enter customer name: "
        ).strip()

        found = False

        for customer in customers:

            if (
                search_name.lower()
                in customer["name"].lower()
            ):

                print(
                    "\nID:",
                    customer["id"]
                )

                print(
                    "Name:",
                    customer["name"]
                )

                print(
                    "Phone:",
                    customer["phone"]
                )

                print(
                    "Address:",
                    customer.get(
                        "address",
                        "Not Available"
                    )
                )

                found = True

        if not found:

            print(
                "Customer not found"
            )

        while True:

            another = input(
                "\nSearch another customer? (y/n): "
            ).strip().lower()

            if another == "y":

                break

            elif another == "n":

                return

            else:

                print(
                    "Please enter only y or n"
                )


def update_customer():

    while True:

        customers = load_data(FILE_NAME)

        search_name = input(
            "Enter customer name: "
        ).strip()

        found = False

        for customer in customers:

            if (
                search_name.lower()
                in customer["name"].lower()
            ):

                print(
                    "\nCurrent Details"
                )

                print(
                    "ID:",
                    customer["id"]
                )

                print(
                    "Name:",
                    customer["name"]
                )

                print(
                    "Phone:",
                    customer["phone"]
                )

                print(
                    "Address:",
                    customer.get(
                        "address",
                        "Not Available"
                    )
                )

                while True:

                    new_name = input(
                        "Enter new customer name: "
                    ).strip()

                    if new_name == "":

                        print(
                            "Customer name cannot be empty"
                        )

                    else:

                        break

                while True:

                    new_phone = input(
                        "Enter new phone number: "
                    ).strip()

                    if new_phone == "":

                        print(
                            "Phone number cannot be empty"
                        )

                    elif len(new_phone) != 10:

                        print(
                            "Mobile number must be exactly 10 digits"
                        )

                    elif not new_phone.isdigit():

                        print(
                            "Mobile number should contain only numbers"
                        )

                    else:

                        break

                duplicate_found = False

                for other_customer in customers:

                    if (
                        other_customer["phone"]
                        == new_phone
                        and other_customer["id"]
                        != customer["id"]
                    ):

                        print(
                            "Customer with this phone number already exists"
                        )

                        duplicate_found = True

                        break

                if duplicate_found:

                    return

                while True:

                    new_address = input(
                        "Enter new address: "
                    ).strip()

                    if new_address == "":

                        print(
                            "Address cannot be empty"
                        )

                    elif not any(
                        character.isalpha()
                        for character in new_address
                    ):

                        print(
                            "Address must contain location details"
                        )

                    else:

                        break

                customer["name"] = new_name
                customer["phone"] = new_phone
                customer["address"] = new_address

                save_data(
                    FILE_NAME,
                    customers
                )

                print(
                    "Customer updated successfully"
                )

                found = True

                break

        if not found:

            print(
                "Customer not found"
            )

        while True:

            another = input(
                "\nUpdate another customer? (y/n): "
            ).strip().lower()

            if another == "y":

                break

            elif another == "n":

                return

            else:

                print(
                    "Please enter only y or n"
                )