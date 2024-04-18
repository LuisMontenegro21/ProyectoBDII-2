class AccountManager:
    
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    def list_accounts(self):
        try:
            query = "MATCH (n:Accounts) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No accounts found.")
                return
            for account in result:
                print(account)
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_account(self):
        account_number = input("Enter the account number to search for: ")
        try:
            query = "MATCH (a:Account {account_number: $account_number}) RETURN a"
            parameters = {'account_number': account_number}
            result = self.neo4j_conn.query(query, parameters)
            if not result:
                print(f"No account found with account number: {account_number}")
                return
            print(f"Account found: {result[0]['a']}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def create_relationships(self):
        account_number = input("Enter the account ID (account_number): ")
        entity_type = input("Link this account to a (user/business): ").lower()
        entity_id = input(f"Enter the {entity_type} ID to link to this account(If User, enter DPI, else enter Business name): ")

        if entity_type not in ['user', 'business']:
            print("Invalid type. Only 'user' or 'business' can be linked.")
            return

        # Check if the account is already linked
        check_query = f"""
        MATCH (a:Account {{account_number: $account_number}})-[r]->()
        RETURN r
        """
        if self.neo4j_conn.query(check_query, {'account_number': account_number}):
            print("This account is already linked to another entity.")
            return
        
        # Create the relationship
        rel_type = "TIENE" if entity_type == 'user' else "DISPONE"
        rel_id = "dpi" if entity_type == 'user' else "name"
        create_query = f"""
        MATCH (a:Account {{account_number: $account_number}}), (e:{entity_type.capitalize()} {{{rel_id}: $entity_id}})
        CREATE (a)-[:{rel_type}]->(e)
        RETURN type(r)
        """
        try:
            result = self.neo4j_conn.query(create_query, {'account_id': account_number, 'entity_id': entity_id})
            if result:
                print(f"Account successfully linked to {entity_type} with relationship '{result[0]}'")
            else:
                print("Failed to create the relationship. Please check the IDs and try again.")
        except Exception as e:
            print(f"An error occurred: {e}")



    def break_relationships(self):
        account_number = input("Enter the account ID (account_number): ")
        entity_type = input("Remove link from this account to a (user/business): ").lower()
        entity_id = input(f"Enter the {entity_type} ID to unlink from this account(If User, enter DPI, else enter Business name): ")

        if entity_type not in ['user', 'business']:
            print("Invalid type. Only 'user' or 'business' can be unlinked.")
            return

        rel_id = "dpi" if entity_type == 'user' else "name"
        rel_type = "TIENE" if entity_type == 'user' else "DISPONE"

        # Check if the relationship exists
        check_query = f"""
        MATCH (a:Account {{account_number: $account_number}})-[r:{rel_type}]->(e:{entity_type.capitalize()} {{{rel_id}: $entity_id}})
        RETURN r
        """
        if not self.neo4j_conn.query(check_query, {'account_number': account_number, 'entity_id': entity_id}):
            print(f"No existing relationship found between account {account_number} and {entity_type} {entity_id}.")
            return
        
        # Break the relationship
        delete_query = f"""
        MATCH (a:Account {{account_number: $account_number}})-[r:{rel_type}]->(e:{entity_type.capitalize()} {{{rel_id}: $entity_id}})
        DELETE r
        RETURN COUNT(r)
        """
        try:
            result = self.neo4j_conn.query(delete_query, {'account_number': account_number, 'entity_id': entity_id})
            if result and result[0]['COUNT(r)'] > 0:
                print(f"Relationship between account {account_number} and {entity_type} {entity_id} successfully removed.")
            else:
                print("Failed to remove the relationship.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def search_account(self):
        account_number = input("Enter the account number to search for: ")
        if not account_number.isnumeric():
            print("Account must be a number")
            return
        try:
            query = "MATCH (a:Account {account_number: $account_number}) RETURN a"
            parameters = {'account_number': account_number}
            result = self.neo4j_conn.query(query, parameters)
            if not result:
                print(f"No account found with account number: {account_number}")
                return
            print(f"Account found: {result[0]['a']}")
        except Exception as e:
            print(f"An error occurred: {e}")