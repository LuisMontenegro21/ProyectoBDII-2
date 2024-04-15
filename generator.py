from faker import Faker
import random
import csv




faker = Faker()
possible_salaries_users = [2800,3000,3700,7000,14000,20000,28000,35000,40000, 45000]
banks = ['Banco Industrial', 'Banco Azteca', 'Banrural', 'G&T', 'Ficohsa', 'BAM', 'Bantrab']
businesses = ['Socios S.A.' , 'Lavanderías Lara', 'Kinotipedia', 'EPA', 'Cemaco', 'Antillon', 'Farmacias R&R', 'Productos Toledo',
            'Q&A', 'HH', 'Ferreterías Coronado', 'Muebles El Roble', 'Farmacias Andoni-Mazza']



def generate_accounts(n):
    with open('accounts.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_number', 'bank', 'balance', 'creation_date'])
        for _ in range(n):
            writer.writerow([random.randint(1000000000, 9000000000), random.choice(banks), random.randint(0,1000000), faker.date()])


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

def generate_tax(n):
    with open('business.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'supplier', 'client', 'emission_date', 'amount'])
        for i in range(n):
            supplier = random.choice(businesses)
            client = random.choice(businesses)

            writer.writerow([i, supplier, client, faker.date(), random.randint(10,100000)])


def generate_deposit(n):
    with open('deposit.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'reminent', 'destinatary', 'amount', 'tran_date', 'description', 'is_valid'])
        

def generate_withdrawal(n):
    with open('withdrawal.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_num', 'amount', 'tran_date', 'description', 'is_valid'])

def generate_history(n):
    with open('history.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'description', 'date', 'account_number', 'transaction_type'])
