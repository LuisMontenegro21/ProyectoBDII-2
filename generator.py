from faker import Faker
import random
import csv




faker = Faker()
possible_salaries_users = [2800,3000,3700,7000,14000,20000,28000,35000,40000, 45000]
banks = ['Banco Industrial', 'Banco Azteca', 'Banrural', 'G&T', 'Ficohsa', 'BAM', 'Bantrab']




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

def generate_business(n):
    with open('business.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'email', 'address', 'phone_number', 'monthly_income'])
        for _ in range(n):
            writer.writerow([faker.name(), faker.email(), faker.street_address(), random.randint(1000000, 90000000), random.randint(10000,100000)])

def generate_tax(n):
    with open('business.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'supplier', 'client', 'emission_date', 'amount'])
        for _ in range(n):
            writer.writerow([random.randint()])
            


