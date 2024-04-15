from faker import Faker
from datetime import datetime
import random
import csv




faker = Faker()
possible_salaries_users = [2800,3000,3700,7000,14000,20000,28000,35000,40000, 45000]
banks = ['Banco Industrial', 'Banco Azteca', 'Banrural', 'G&T', 'Ficohsa', 'BAM', 'Bantrab']
businesses = ['Socios S.A.' , 'Lavanderías Lara', 'Kinotipedia', 'EPA', 'Cemaco', 'Antillon', 'Farmacias R&R', 'Productos Toledo',
            'Q&A', 'HH', 'Ferreterías Coronado', 'Muebles El Roble', 'Farmacias Andoni-Mazza', 'Supermercados Fahsen', 'Repuestos Aioli',
            'FIHCA S.A', 'Fertilizantes Mayafer', 'Distribuidora Mariscal', 'Repuestos Acquoni', 'Salsas Don Justo']
descriptions = ["El usuario excedió el doble de su sueldo mensual", "Al usuario se le acreditó dos veces su saldo en la cuenta bancaria",
                "La empresa transfiere más de lo facturado facturado a la fecha", "A la empresa se le depositó más de dos veces el saldo de su cuenta"]


def generate_accounts(n):
    start = datetime(2010,1,1)
    end = datetime(2024,1,1)
    with open('accounts.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_number', 'bank', 'balance', 'creation_date', 'insurance'])
        for _ in range(n):
            writer.writerow([random.randint(1000000000, 9000000000), random.choice(banks), random.randint(0,100000), faker.date_between(start_date=start, end_date=end), faker.boolean()])


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

            writer.writerow([faker.name(), random.randint(18,80), int(dpi), random.choice(possible_salaries_users), faker.email()])

def generate_business():
    with open('business.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'email', 'address', 'phone_number', 'monthly_income'])
        for _ in range(len(businesses)):
            local_var = businesses
            business = random.choice(local_var)
            writer.writerow([business, faker.email(), faker.street_address(), random.randint(1000000, 90000000), random.randint(10000,100000)])
            #evitar duplicados
            local_var.remove(business)

def read_business_names(filename):
    business_names = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Saltarse el encabezado si lo hay
        for row in reader:
            business_names.append(row[0])  # Asumimos que el nombre del negocio está en la primera columna
    return business_names


def generate_tax(n, users_filename):
    users = read_business_names(users_filename)  # Lee los negocios del archivo
    if not businesses:  # Verificar si la lista está vacía
        print("No businesses found in the file.")
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

            writer.writerow([i, supplier, client, faker.date(), random.randint(10, 3500)])


def generate_deposit(n):
    with open('deposit.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'reminent', 'destinatary', 'amount', 'tran_date', 'description', 'is_valid'])
        for i in range(n):
            writer.writerow([i])

def generate_withdrawal(n):
    with open('withdrawal.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_num', 'amount', 'tran_date', 'description', 'is_valid'])

def generate_history(n):
    with open('history.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'description', 'date', 'account_number', 'transaction_type'])





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
generate_tax(2000, 'users.csv')