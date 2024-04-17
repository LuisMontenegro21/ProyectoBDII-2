from py2neo import Graph, NodeMatcher, Node, DatabaseError
import csv
import random

# Conexión a Neo4j
try:
    graph = Graph("neo4j+s://3bee0d58.databases.neo4j.io", auth=("neo4j", "9bmUxCJKULbvvNVZSanGdLKTIDGlWJBe34cxNegjKmU"))
    # Realiza una consulta simple para probar la conexión
    graph.run("MATCH (n) RETURN COUNT(n) LIMIT 1")
    print("Conexión establecida exitosamente.")
except DatabaseError as e:
    print("Error al conectar a la base de datos: ", e)
except Exception as e:
    print("Error no especificado: ", e)

def load_csv(filename, label, headers):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                node = Node(label, **{key: row[key] for key in headers})
                graph.merge(node, label, "name")  # Asumiendo que 'name' es un campo único para el MERGE
        print(f"Datos cargados exitosamente desde {filename}")
    except Exception as e:
        print(f"Error al cargar datos desde {filename}: ", e)

'''
def create_random_relationships(label1, label2, relationship_type):
    matcher = NodeMatcher(graph)
    nodes1 = list(matcher.match(label1))
    nodes2 = list(matcher.match(label2))
    random.shuffle(nodes1)
    random.shuffle(nodes2)

    for node1, node2 in zip(nodes1, nodes2):
        graph.merge(node1.relationship_to(node2, relationship_type))

# Carga de datos desde CSV
load_csv('users.csv', 'Users', ['name', 'age', 'dpi', 'salary', 'email'])
load_csv('business.csv', 'Business', ['name', 'email', 'address', 'phone_number', 'monthly_income'])
load_csv('accounts.csv', 'Accounts', ['account_number', 'bank', 'balance', 'creation_date', 'insurance'])
load_csv('tax.csv', 'Taxes', ['id', 'supplier', 'client', 'emission_date', 'amount'])
load_csv('deposit.csv', 'Deposit', ['id', 'reminent', 'destinatary', 'amount', 'tran_date', 'description', 'is_valid'])
load_csv('withdrawal.csv', 'Withdrawal', ['id','account_num', 'amount', 'tran_date', 'description', 'is_valid'])
load_csv('history.csv', 'Record', ['id', 'description', 'date', 'account_number', 'transaction_type'])


# Crear relaciones aleatorias sin repetirse
create_random_relationships('Business', 'Taxes', 'EMITE')
create_random_relationships('Users', 'Business', 'POSEE')
create_random_relationships('Business', 'Accounts', 'TIENE')
create_random_relationships('Users', 'Accounts', 'TIENE')
create_random_relationships('Accounts', 'Deposit', 'Realiza')
create_random_relationships('Accounts', 'Withdrawal', 'Realiza')
create_random_relationships('Deposit', 'Record', 'Generan')
create_random_relationships('Withdrawal', 'Record', 'Generan')
'''