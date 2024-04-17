class BusinessManager:
    
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    
    def list_businesses(self):
        try:
            query = "MATCH (n:Business) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No businesses found.")
                return
            for business in result:
                print(business)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def add_businesses(self):
        pass