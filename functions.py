

'''Funciones para crear los nodos'''
def add_user(tx, username, age, dpi, salary, account_number):

    query = (
        "CREATE (u:User {user: $username, age: $age, dpi: $dpi, account_number: $account_number})"
    )
    return tx.run(query, user=username, age=age, dpi=dpi, salary=salary, account_number=account_number)

def add_tax(tx, id, supplier, client, emission_date, amount):
    query = (
        "CREATE (t:Tax {id: $id, supplier: $supplier, client: $client, emission_date: $emission_date, amount: $amount})"
    )
    return tx.run(query, id=id, supplier=supplier, client=client, emission_date=emission_date, amount=amount)

def add_account(tx, account_number, bank, account_name, balance, creation_date):
    query = (
        "CREATE (a:Account {account_number: $account_number, bank: $bank, account_name: $account_name, balance: $balance, creation_date: $creation_date})"
    )
    return tx.run(query, account_number=account_number, bank=bank, account_name=account_name, balance=balance, creation_date=creation_date)

def add_business(tx, name, email, address, phone_number, monthly_income):
    query = (
        "CREATE (b: Business{name: $name, email: $email, address: $address, phone_number: $phone_number, monthly_revenue: $monthly_revenue})"
    )
    return tx.run(query, name=name, email=email, address=address, phone_number=phone_number, monthly_income=monthly_income)

def add_deposit(tx, reminent, destinatary, amount, tran_date, description, is_valid):
    query = (
        "CREATE (d: Deposit {reminent: $reminent, destinatary: $destinatary, amount: $amount, tran_date: $tran_date, description: $description, is_valid: $is_valid})"
    )
    return tx.run(query, reminent=reminent, destinatary=destinatary, amount=amount, tran_date=tran_date, description=description, is_valid=is_valid)

def add_withdrawal(tx, account_num, amount, tran_date, description, is_valid):
    query = (
        "CREATE (w: Withdrawal {account_num: $account_num, amount: $amount, tran_date: $tran_date, description: $description, is_valid: $is_valid})"
    )
    return tx.run(query,account_num=account_num, amount=amount, tran_date=tran_date, description=description, is_valid=is_valid)

def add_history(tx, id, description, date, account_number, transaction_type):
    query = (
        "CREATE (h: History {id: $id, description: $description, date: $date, account_number: $account_number, transaction_type: $transaction_type})"
    )
    return tx.run(query, id=id, description=description, date=date, account_number=account_number, transaction_type=transaction_type)



'''Funciones para crear las relaciones'''

def create_has(tx, user_dpi, account_num, since):
    query = (
        "MATCH (u:User {dpi: $user_dpi}), (a:Account {account_num: $account_num}) "
        "CREATE (u)-[:HAS_ACCOUNT {since: $since}]->(a)"
    )
    return tx.run(query, user_dpi=user_dpi, account_num=account_num, since=since)

def create_performs(tx, account_num, deposit_id, transaction_id):

    query = (
        "MATCH (a: Account)"
    )


