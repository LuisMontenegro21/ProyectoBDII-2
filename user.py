class UserManager:

    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    def list_users(self):
        try:
            query = "MATCH (n:User) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No users found.")
                return
            for user in result:
                print(user)
        except Exception as e:
            print(f"An error occurred: {e}")
            

    def add_user(self, user_details):
        # Implementation for adding a user
        name = user_details['name']
        age = user_details['age']
        id = user_details['id']
        salary = user_details['salary']
        account_number = user_details['account_number']
        try:
            query = """CREATE (u:User {
            name: $name, 
            age: $age, 
            id: $id, 
            salary: $salary, 
            account_number: $account_number
        })"""
            return self.neo4j_conn.query(query)
        except Exception as e:
             print(f"An error occurred: {e}")
             return []