from neo4j import GraphDatabase
import dotenv
import os
import logging





def main():
    logging.basicConfig(level=logging.DEBUG)
    load_status =  dotenv.load_dotenv("Neo4j-b8d4977a-Created-2024-04-11.txt")
    # chequear si el contenido es obtenido
    if load_status is False:
        raise RuntimeError('Environment variables not loaded')
    # acceder y obtener datos relevantes
    
    URI = os.getenv("NEO4J_URI")
    AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

    # verificar conectividad
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
            with driver.session() as session:
                result = session.run("RETURN 'HELLO WORLD' AS text")
                for record in result:
                    print(record['text'])

    except Exception as e:
        print(f"Exception : {e}")  
    
    driver.close()




if __name__ == "__main__":
    main()