import os
import dotenv
from neo4j import GraphDatabase

class Neo4jConnection:
    """ Class to handle Neo4j database connections and queries. """
    def __init__(self):
        self.load_neo4j_env()
        self.driver = GraphDatabase.driver(self.URI, auth=self.AUTH)

    def load_neo4j_env(self):
        load_status = dotenv.load_dotenv("Neo4j-3bee0d58-Created-2024-04-17.txt")
        if not load_status:
            raise RuntimeError('Environment variables not loaded')
        self.URI = os.getenv("NEO4J_URI")
        self.USERNAME = os.getenv("NEO4J_USERNAME")
        self.PASSWORD = os.getenv("NEO4J_PASSWORD")
        self.AUTH = (self.USERNAME, self.PASSWORD)

    def query(self, query, parameters=None):
        with self.driver.session(database='neo4j') as session:
            result = session.run(query, parameters)
            return [record for record in result]

    def close(self):
        self.driver.close()




