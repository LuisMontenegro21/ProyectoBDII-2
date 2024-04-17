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