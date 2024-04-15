from neo4j import GraphDatabase
import dotenv
import os



def main():
    load_status = dotenv.load_dotenv("Neo4j-b8d4977a-Created-2024-04-11.txt")
    if load_status is False:
        raise RuntimeError('Environment variables not loaded')
    
    URI = os.getenv("NEO4J_URI")
    USERNAME = os.getenv("NEO4J_USERNAME")
    PASSWORD = os.getenv("NEO4J_PASSWORD")
    AUTH = (USERNAME, PASSWORD)

    # Print to debug
    print(f"URI: {URI}")
    print(f"Username: {USERNAME}")
    print(f"Password: {PASSWORD}")

    driver = None
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session(database='neo4j') as session:
                result = session.run("RETURN 'HELLO WORLD' AS text")
                for record in result:
                    print(record['text'])
    except Exception as e:
        print(f"Exception : {e}")  
    finally:
        if driver:
            driver.close()





if __name__ == "__main__":
    main()