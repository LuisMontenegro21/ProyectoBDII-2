from faker import Faker
from datetime import datetime
import random
import csv


faker = Faker()
#possible_salaries_users = [random.randint(5000, 7000)]
banks = ['Banco Industrial', 'Banco Azteca', 'Banrural', 'G&T', 'Ficohsa', 'BAM', 'Bantrab']
businesses = ['Socios S.A.' , 'Lavanderías Lara', 'Kinotipedia', 'EPA', 'Cemaco', 'Antillon', 'Farmacias R&R', 'Productos Toledo',
            'Q&A', 'HH', 'Ferreterías Coronado', 'Muebles El Roble', 'Farmacias Andoni-Mazza', 'Supermercados Fahsen', 'Repuestos Aioli',
            'FIHCA S.A', 'Fertilizantes Mayafer', 'Distribuidora Mariscal', 'Repuestos Acquoni', 'Salsas Don Justo']
descriptions = ["El usuario excedió el doble de su sueldo mensual", "Al usuario se le acreditó dos veces su saldo en la cuenta bancaria",
                "La empresa transfiere más de lo facturado facturado a la fecha", "A la empresa se le depositó más de dos veces el saldo de su cuenta"]
min_earnings = 5000
max_earnings = 7000
start = datetime(2010,1,1)
end = datetime(2024,1,1)

#Genera .csv de las cuentas bancarias
def generate_accounts(n):
    with open('accounts.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_number', 'bank', 'balance', 'creation_date', 'insurance'])
        for _ in range(n):
            writer.writerow([random.randint(1000000000, 9000000000), random.choice(banks), random.randint(0,7000), faker.date_between(start_date=start, end_date=end), faker.boolean()])

#Genera .csv de los usuarios
def generate_users(n):
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'age', 'dpi', 'salary', 'email'])
        for _ in range(n):
            # para generar un dpi más realista 
            # que el número inicial sea de 2-5
            prefix = str(random.randint(2,5))
            # asumimos son capitalinos
            postfix = "0101"
            # longitud del dpi tipo xxxx xxxxx xxxx
            total_length = 13
            middle_length = total_length - len(postfix) - len(prefix)
            middle = ''.join([str(random.randint(1,9)) for _ in range(middle_length)])
            dpi = prefix + middle + postfix

            # Generar un salario aleatorio entre 5000 y 7000 para cada usuario
            salary = random.randint(5000, 7000)

            writer.writerow([faker.name(), random.randint(18,80), int(dpi), salary, faker.email()])

#Genera .csv de las empresas
def generate_business():
    with open('business.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'email', 'address', 'phone_number', 'monthly_income'])
        for _ in range(len(businesses)):
            local_var = businesses
            business = random.choice(local_var)
            writer.writerow([business, faker.email(), faker.street_address(), random.randint(1000000, 90000000), random.randint(5000,7000)])
            #evitar duplicados
            local_var.remove(business)

#Genera .csv de las facturas
def read_first_line(filename):
    business_names = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Saltarse el encabezado si lo hay
        for row in reader:
            business_names.append(row[0])  # Asumimos que el nombre del negocio está en la primera columna
    return business_names
def generate_tax(n, users_filename):
    users = read_first_line(users_filename)  # Lee los negocios del archivo
    if not users:  # Verificar si la lista está vacía
        print("No users found in the file.")
        return
    
    with open('tax.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'supplier', 'client', 'emission_date', 'amount'])
        for i in range(n):
            supplier = random.choice(businesses)
            client = random.choice(users)
            # Asegurarse de que el proveedor y el cliente no sean el mismo
            while client == supplier:
                client = random.choice(businesses)

            writer.writerow([i, supplier, client, faker.date_between(start_date=start, end_date=end), random.randint(10, 3500)])

#Genera .csv de los depósitos
def read_first_line(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Saltarse el encabezado
        return [row[0] for row in reader]
def generate_deposit(n, accounts):
    acc_num = read_first_line(accounts)
    if not acc_num:
        print("No accounts found in the file")
        return 
    with open('deposit.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'reminent', 'destinatary', 'amount', 'tran_date', 'description', 'is_valid'])
        for i in range(1, n+1):
            reminent = random.choice(acc_num)
            destinatary = random.choice(acc_num)
            while reminent == destinatary:
                destinatary = random.choice(acc_num)
            amount = random.randint(1, 30000)
            tran_date = faker.date_between(start_date=datetime(2010, 1, 1), end_date=datetime(2024, 1, 1))
            description = "pagos varios"
            is_valid = amount <= 14000
            writer.writerow([i, reminent, destinatary, amount, tran_date, description, is_valid])

#Genera .csv de los retiros
def read_accounts_with_balances(filename):
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Saltarse el encabezado
        return {row[0]: float(row[2]) for row in reader}  # Guardar como diccionario {account_num: balance}
def generate_withdrawal(n):
    accounts_balances = read_accounts_with_balances('accounts.csv')
    if not accounts_balances:
        print("No accounts or balances found in the file")
        return
    if n > len(accounts_balances):
        print("Not enough unique accounts to generate", n, "withdrawals.")
        return
    
    used_accounts = set()  # Conjunto para llevar el registro de las cuentas ya utilizadas
    with open('withdrawal.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_num', 'amount', 'tran_date', 'description', 'is_valid'])
        while len(used_accounts) < n:
            account_num, balance = random.choice(list(accounts_balances.items()))
            if account_num not in used_accounts:
                max_withdrawal_amount = balance
                amount = round(random.uniform(1, max_withdrawal_amount), 2)
                tran_date = faker.date_between(start_date=datetime(2010, 1, 1), end_date=datetime(2024, 1, 1))
                description = "pagos varios"
                is_valid = amount <= (balance / 2)
                writer.writerow([account_num, amount, tran_date, description, is_valid])
                used_accounts.add(account_num)  # Añadir a los utilizados

#Genera .csv del historial de posibles fraudes
def read_invalid_transactions(filename, is_deposit):
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        result = []
        for row in reader:
            if row['is_valid'] == 'False':
                account_number = row['destinatary'] if is_deposit else row['account_num']
                result.append((row['tran_date'], account_number))
        return result
def generate_history():
    # Leer transacciones inválidas de ambos archivos
    invalid_deposits = read_invalid_transactions('deposit.csv', True)
    invalid_withdrawals = read_invalid_transactions('withdrawal.csv', False)
    
    all_invalid_transactions = invalid_deposits + invalid_withdrawals
    
    # Ordenar por fecha para mantener una cronología consistente
    all_invalid_transactions.sort()
    
    with open('history.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'description', 'date', 'account_number', 'transaction_type'])
        id = 1
        for date, account_number in all_invalid_transactions:
            description = "Deteccion de posible fraude"
            transaction_type = 'deposit' if (date, account_number) in invalid_deposits else 'withdrawal'
            writer.writerow([id, description, date, account_number, transaction_type])
            id += 1



import pandas as pd

def add_id_column_to_csv(input_file_path, output_file_path):
    # Cargar el archivo CSV
    data = pd.read_csv(input_file_path)
    
    # Agregar una nueva columna al inicio que sea el ID
    data.insert(0, 'id', range(1, len(data) + 1))
    
    # Guardar el archivo modificado en la ruta de salida especificada
    data.to_csv(output_file_path, index=False)

# Uso de la función
input_file = 'withdrawal.csv'
output_file = 'modified_withdrawal.csv'
add_id_column_to_csv(input_file, output_file)








# businesses 20
# users 700
# accounts 720
# tax 2000
# deposit 520
# withdrawal 520
# history 520

#generate_users(700)
#generate_business()
#generate_accounts(720)
#generate_tax(2000, 'users.csv')
#generate_deposit(520, 'accounts.csv')
#generate_withdrawal(520)
#generate_history()