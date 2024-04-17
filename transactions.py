
class DepositManager:
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    def list_deposits(self):
        try:
            query = "MATCH (n:Deposit) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No deposits found.")
                return
            for deposit in result:
                print(deposit)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def make_deposit(self):
        pass

class WithdrawalManager:
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn
    
    def list_withdrawal(self):
        try:
            query = "MATCH (n:Withdrawal) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No withdrawals found.")
                return
            for withdrawal in result:
                print(withdrawal)
        except Exception as e:
            print(f"An error occurred: {e}")

    def make_withdrawal(self):
        pass

class RecordManager:
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    def list_records(self):
        try:
            query = "MATCH (n:Record) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No records found.")
                return
            for record in result:
                print(record)
        except Exception as e:
            print(f"An error occurred: {e}")