from neo4j import GraphDatabase
import dotenv
import os

load_status = dotenv.load_dotenv("Neo4j-b8d4977a-Created-2024-04-11.txt")
if load_status is False:
    raise RuntimeError('Environment variables not loaded')
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
AUTH = (USERNAME, PASSWORD)

try:
    driver = GraphDatabase(URI, auth=AUTH)
    with driver.session(database='neo4j') as session:
        result = session.run("RETURN 'Hello World' AS text")
        print([record for record in result]) 
except Exception as e:
    print(f"Exception : {e}") 