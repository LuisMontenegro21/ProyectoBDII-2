
import datetime
import uuid
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


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
        print("Creating a new deposit:")
        # User inputs
        account_number = input("Enter the account number (destinatary): ")
        amount = input("Enter the amount of the deposit: ")

        try:
            if not amount.isdigit() or float(amount) <= 0:
                print("Invalid amount, must be a positive number.") 
                return
            if not account_number.isdigit():
                print("Invalid account number, must be numeric")
                return

            # Neo4j query to create the deposit node and update the account balance
            query = """
            WITH $amount AS depositAmount, $accountNumber AS accountNumber
            MATCH (a:Accounts {account_number: accountNumber})
            CREATE (d:Deposit {
                id: randomUUID(),
                account_number: a.account_number,
                tran_date: date(),
                amount: depositAmount,
                action: 'Deposit',
                is_valid: true  // Assumes valid, will update if not
            })
            SET d.is_valid = depositAmount <= (2 * toFloat(a.balance))
            WITH a, d, depositAmount
            WHERE d.is_valid
            SET a.balance = toFloat(a.balance) + depositAmount  // Update balance assuming deposit is valid
            RETURN d, a.balance AS accountBalance, d.is_valid AS isDepositValid
            """
            parameters = {
                'accountNumber': account_number,
                'amount': float(amount)  # Convert amount to float
            }

            result = self.neo4j_conn.query(query, parameters)
            if result:
                for record in result:
                    print("Deposit created successfully:", record['d'])
                    print("New Account Balance:", record['accountBalance'])
                    print("Is Deposit Valid?", "Yes" if record['isDepositValid'] else "No")
            else:
                print("Failed to create the deposit. Please check the account number and try again.")

        except Exception as e:
            print(f"An error occurred: {e}")

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
        print("Creating a new withdrawal:")
        # User inputs
        account_number = input("Enter the account number: ")
        amount = input("Enter the amount of the withdrawal: ")
        description = input("Enter a description for the withdrawal: ")

        try:
            amount = float(amount)
            if amount <= 0:
                print("Invalid withdrawal: Amount must be greater than zero.")
                return
            if amount > 10000:  # High amount might need special handling or checks
                print("Warning: High withdrawal amount, subject to review.")

            # Generate unique identifiers
            withdrawal_id = str(uuid.uuid4())
            record_id = str(uuid.uuid4())
            tran_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # Neo4j query to create the withdrawal node and verify it against account balance
            query = """
            WITH $amount AS withdrawalAmount, $accountNumber AS accountNumber
            MATCH (a:Accounts {account_number: accountNumber})
            CREATE (w:Withdrawal {
                id: randomUUID(),
                account_number: a.account_number,
                tran_date: date(),
                amount: withdrawalAmount,
                action: 'Withdrawal',
                description: $description,
                is_valid: true  // Initially assumed true
            })
            WITH a, w, withdrawalAmount
            WITH a, w, withdrawalAmount <= (0.5 * toFloat(a.balance)) AS withinLimit
            SET w.is_valid = withinLimit
            WITH a, w, withinLimit
            WHERE NOT withinLimit
            CREATE (r:Record {
                id: $record_id,
                account_number: a.account_number,
                date: $tran_date,
                description: $description,
                transaction_type: 'Withdrawal'
            })
            RETURN w, a.balance AS accountBalance, w.is_valid AS isWithdrawalValid, r
            """
            parameters = {
                'accountNumber': account_number,
                'amount': amount,
                'description': description,
                'record_id': record_id,
                'tran_date': tran_date
            }

            result = self.neo4j_conn.query(query, parameters)
            if result:
                for record in result:
                    if record.get('r'):
                        print("Withdrawal flagged as invalid and recorded:", record['r'])
                    print("Withdrawal created successfully:", record['w'])
                    print("Account Balance:", record['accountBalance'])
                    print("Is Withdrawal Valid?", "Yes" if record['isWithdrawalValid'] else "No")
            else:
                print("Failed to create the withdrawal. Please check the account number and try again.")

        except ValueError:
            print("Invalid input: Please enter a numeric amount.")
        except Exception as e:
            print(f"An error occurred: {e}")

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

    def analyze_records(self):
        option = str(input("Select an option:\n- transactions\n" ))
        if option == "transactions":
            self.accounts_with_most_transactions()
        elif option == "frauds":
            self.accounts_with_most_frauds()
        else:
            print("Option not valid")
            return


    def accounts_with_most_transactions(self):
        deposit_query = """
        MATCH (a:Accounts)-[r:DEPOSITA]->(d:Deposit)
        RETURN a.account_number, count(r) as num_deposits
        ORDER BY num_deposits DESC
        LIMIT 3
        """
        withdrawal_query = """
        MATCH (a:Accounts)-[r:RETIRA]->(:Withdrawal)
        RETURN a.account_number, count(r) as num_withdrawals
        ORDER BY num_withdrawals DESC
        LIMIT 3
        """
        try:
            print("Accounts with the most deposits:")
            deposit_results = self.neo4j_conn.query(deposit_query)
            if not deposit_results:
                print("No results found")
            for record in deposit_results:
                print(record['a.account_number'], record['num_deposits'])

            print("Accounts with the most withdrawals:")
            withdrawal_results = self.neo4j_conn.query(withdrawal_query)
            if not withdrawal_results:
                print("No results found")
            for record in withdrawal_results:
                print(record['a.account_number'], record['num_withdrawals'])

        except Exception as e:
            print(f"An error occurred: {e}")

    def accounts_with_most_frauds(self):
        pass

    # implementar regresión logística para detectar fraudes
    # TODO no implementado ni terminado aún
    def train_fraud_detection_model(self, features, labels):
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        print(classification_report(y_test, predictions))