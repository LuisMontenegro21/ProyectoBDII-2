from py2neo import Graph, NodeMatcher, Node, DatabaseError, Relationship
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



def create_random_relationships(label1, label2, relationship_type):
    try:
        matcher = NodeMatcher(graph)
        nodes1 = list(matcher.match(label1))
        nodes2 = list(matcher.match(label2))
        random.shuffle(nodes1)
        random.shuffle(nodes2)

        for node1, node2 in zip(nodes1, nodes2):
            rel = Relationship(node1, relationship_type, node2)
            graph.merge(rel)
        
        print(f"Creación exitosa de {relationship_type}")
    except Exception as e:
        print(f"Error al hacer relación {relationship_type}: ", e)




def create_one_to_many_relationships(source_label, target_label, relationship_type, source_property, target_property):
    try:
        matcher = NodeMatcher(graph)
        source_nodes = list(matcher.match(source_label))
        target_nodes = list(matcher.match(target_label))

        for node1 in source_nodes:
            matched_nodes = [node2 for node2 in target_nodes if node2[target_property] == node1[source_property]]
            for node2 in matched_nodes:
                rel = Relationship(node1, relationship_type, node2)
                graph.merge(rel)

        print(f"Creación exitosa de relaciones uno a muchos {relationship_type} de {source_label} a {target_label} basadas en {source_property} y {target_property}")
    except Exception as e:
        print(f"Error al hacer relación uno a muchos {relationship_type} de {source_label} a {target_label} basadas en {source_property} y {target_property}: ", e)

# Carga de datos desde CSV
'''load_csv('users.csv', 'Users', ['name', 'age', 'dpi', 'salary', 'email'])
load_csv('business.csv', 'Business', ['name', 'email', 'address', 'phone_number', 'monthly_income'])
load_csv('accounts.csv', 'Accounts', ['account_number', 'bank', 'balance', 'creation_date', 'insurance'])
load_csv('tax.csv', 'Taxes', ['id', 'supplier', 'client', 'emission_date', 'amount'])
load_csv('deposit.csv', 'Deposit', ['id', 'reminent', 'destinatary', 'amount', 'tran_date', 'description', 'is_valid'])
load_csv('withdrawal.csv', 'Withdrawal', ['id','account_num', 'amount', 'tran_date', 'description', 'is_valid'])
load_csv('history.csv', 'Record', ['id', 'description', 'date', 'account_number', 'transaction_type'])'''


# Crear relaciones aleatorias sin repetirse
#create_one_to_many_relationships('Business', 'Taxes', 'EMITE', 'name', 'supplier')
create_random_relationships('Users', 'Business', 'POSEE')
create_random_relationships('Business', 'Accounts', 'DISPONE')
create_random_relationships('Users', 'Accounts', 'TIENE')
create_random_relationships('Accounts', 'Deposit', 'DEPOSITA')
create_random_relationships('Accounts', 'Withdrawal', 'RETIRA')
create_random_relationships('Deposit','Record', 'GENERA')
create_random_relationships( 'Withdrawal', 'Record', 'CREA')
