class UserManager:

    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    def list_users(self):
        try:
            query = "MATCH (n:Users) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No users found.")
                return
            for user in result:
                print(user)
        except Exception as e:
            print(f"An error occurred: {e}")
            
    '''añadir usuarios'''
    def add_users(self):
        users = []
        while True:
            print("Enter user details or type 'done' to finish:")

            # Collecting user details
            name = input("Name (leave blank if done): ")
            if name.lower() == 'done' or name == '':
                break
            age = input("Age: ")
            user_dpi = input("DPI: ")
            salary = input("Salary: ")
            account_number = input("Account Number: ")

            # Storing each user's details in a dictionary
            user_details = {
                'name': name,
                'age': int(age),
                'dpi': user_dpi,
                'salary': float(salary),
                'account_number': account_number
            }
            users.append(user_details)

        # Processing the list of users
        for user in users:
            try:
                query = """
                CREATE (u:Users {name: $name, age: $age, dpi: $dpi, salary: $salary, account_number: $account_number})
                RETURN u
                """
                parameters = {
                    'name': user['name'],
                    'age': user['age'],
                    'dpi': user['dpi'],
                    'salary': user['salary'],
                    'account_number': user['account_number']
                }
                result = self.neo4j_conn.query(query, parameters)
                print(f"Added user: {result[0]['u'] if result else 'No result returned'}")
            except Exception as e:
                print(f"An error occurred: {e}")

    '''Remover usuarios'''
    def remove_users(self):
        print("Delete Users")
        dpi_list = []
        while True:
            user_dpi = input("Enter the DPI of the user to delete (or type 'done' to finish): ")
            if user_dpi.lower() == 'done':
                break
            dpi_list.append(user_dpi)

        if not dpi_list:
            print("No DPI entered; no users deleted.")
            return

        deleted_users = 0
        errors = 0
        for dpi in dpi_list:
            try:
                # Check if the user exists before deleting
                check_query = "MATCH (u:Users {dpi: $dpi}) RETURN u"
                check_result = self.neo4j_conn.query(check_query, {'dpi': dpi})
                if not check_result:
                    print(f"No user found with DPI: {dpi}")
                    continue

                # Proceed to delete if the user exists
                delete_query = "MATCH (u:Users {dpi: $dpi}) DELETE u"
                self.neo4j_conn.query(delete_query, {'dpi': dpi})
                print(f"User deleted successfully with DPI: {dpi}")
                deleted_users += 1
            except Exception as e:
                print(f"An error occurred while trying to delete the user with DPI {dpi}: {e}")
                errors += 1

        print(f"Completed deletions. Total deleted: {deleted_users}. Errors encountered: {errors}.")


    '''actualizar nodos'''
    def update_users(self):
        print("Update User")
        user_dpi = input("Enter the DPI of the user to update: ")

        # Check if the user exists
        try:
            fetch_query = "MATCH (u:Users {dpi: $dpi}) RETURN u"
            user = self.neo4j_conn.query(fetch_query, {'dpi': user_dpi})
            if not user:
                print("No user found with DPI:", user_dpi)
                return
            print("Current user details:", user[0]['u'])
        except Exception as e:
            print(f"An error occurred while fetching the user: {e}")
            return

        # Collect new details from the user
        new_name = input("Enter new name (or leave blank to keep current): ")
        new_age = input("Enter new age (or leave blank to keep current): ")
        new_salary = input("Enter new salary (or leave blank to keep current): ")
        new_account_number = input("Enter new account number (or leave blank to keep current): ")

        # Collect information about any new properties
        new_property_key = input("Enter new property key (or leave blank if none): ")
        new_property_value = input("Enter new property value (or leave blank if none): ")

        # Update the user details
        try:
            update_query = """
            MATCH (u:Users {dpi: $dpi})
            SET u.name = CASE WHEN $name IS NULL OR $name = '' THEN u.name ELSE $name END,
                u.age = CASE WHEN $age IS NULL OR $age = '' THEN u.age ELSE toInteger($age) END,
                u.salary = CASE WHEN $salary IS NULL OR $salary = '' THEN u.salary ELSE toFloat($salary) END,
                u.account_number = CASE WHEN $account_number IS NULL OR $account_number = '' THEN u.account_number ELSE $account_number END
            """

            # Dynamically add new property if specified
            if new_property_key and new_property_value:
                update_query += f"SET u.{new_property_key} = $new_property_value "

            update_query += "RETURN u"

            parameters = {
                'dpi': user_dpi,
                'name': new_name if new_name.strip() != '' else None,
                'age': new_age if new_age.strip() != '' else None,
                'salary': new_salary if new_salary.strip() != '' else None,
                'account_number': new_account_number if new_account_number.strip() != '' else None,
                'new_property_value': new_property_value if new_property_value.strip() != '' else None
            }

            updated_user = self.neo4j_conn.query(update_query, parameters)
            print("User updated successfully. New details:", updated_user[0]['u'])
        except Exception as e:
            print(f"An error occurred while updating the user: {e}")

    def search_users(self):
        print("Search Users")
        field = input("Enter the field to search by (e.g., name, dpi): ")
        value = input(f"Enter the value for {field}: ")

        # Construct the Cypher query dynamically based on user input
        try:
            # Sanitize input to prevent Cypher injection
            if field not in ['name', 'dpi', 'age', 'salary', 'account_number']:  # list valid fields
                print(f"Invalid field: {field}. Searchable fields are name, dpi, age, salary, account_number.")
                return

            query = f"MATCH (u:Users {{{field}: $value}}) RETURN u"
            result = self.neo4j_conn.query(query, {'value': value})

            if not result:
                print(f"No users found with {field} = {value}")
                return

            print(f"Users found with {field} = {value}:")
            for record in result:
                print(record['u'])  # Assuming that the result is a node

        except Exception as e:
            print(f"An error occurred while searching for users: {e}")
