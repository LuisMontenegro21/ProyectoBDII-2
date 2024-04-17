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
            

    def add_users(self):
        users = []
        while True:
            print("Enter user details or type 'done' to finish:")

            # Collecting user details
            name = input("Name (leave blank if done): ")
            if name.lower() == 'done' or name == '':
                break
            age = input("Age: ")
            user_id = input("ID: ")
            salary = input("Salary: ")
            account_number = input("Account Number: ")

            # Storing each user's details in a dictionary
            user_details = {
                'name': name,
                'age': int(age),
                'id': user_id,
                'salary': float(salary),
                'account_number': account_number
            }
            users.append(user_details)

        # Processing the list of users
        for user in users:
            try:
                query = """
                MATCH (u:Users {name: $name, age: $age, id: $id, salary: $salary, account_number: $account_number})
                RETURN u
                """
                parameters = {
                    'name': user['name'],
                    'age': user['age'],
                    'id': user['id'],
                    'salary': user['salary'],
                    'account_number': user['account_number']
                }
                result = self.neo4j_conn.query(query, parameters)
                print(f"Added user: {result[0]['u'] if result else 'No result returned'}")
            except Exception as e:
                print(f"An error occurred: {e}")
        
    def remove_users(self):
        pass

    def update_users(self):
        pass

    def search_users(self):
        pass