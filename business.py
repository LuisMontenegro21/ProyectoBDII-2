import csv

class BusinessManager:
    
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn

    def list_businesses(self):
        try:
            query = "MATCH (n:Business) RETURN n"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No businesses found.")
                return
            for business in result:
                print(business)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def add_label(self):
        business_name = input("Enter the name of the business to add labels to: ")
        labels = input("Enter the labels to add, separated by commas (e.g., Local,Internacional): ").split(',')

        for label in labels:
            if label not in ['Local', 'Internacional']:
                print("Incorrect label input. Only Local and Internacional are valid")
                return

        try:
            # Fetch the business node first to ensure it exists
            fetch_query = "MATCH (b:Business) WHERE b.name = $name RETURN b"
            fetch_result = self.neo4j_conn.query(fetch_query, {'name': business_name})
            if not fetch_result:
                print("No business found with the specified name.")
                return
            
            # Construct the query to add labels
            add_labels_query = "MATCH (b:Business {name: $name}) "
            for label in labels:
                # Ensure the label is valid (simple validation to avoid Cypher injection)
                clean_label = ''.join(e for e in label if e.isalnum())
                add_labels_query += f"SET b:{clean_label} "

            add_labels_query += "RETURN b"
            result = self.neo4j_conn.query(add_labels_query, {'name': business_name})
            print("Labels added successfully:", result)

        except Exception as e:
            print(f"An error occurred while adding labels: {e}")

    def remove_labels(self):
        business_name = input("Enter the name of the business to remove labels from: ")
        labels = input("Enter the labels to remove, separated by commas (e.g., Local,Internacional): ").split(',')

        for label in labels:
            if label not in ['Local', 'Internacional']:
                print("Incorrect label input. Only Local and Internacional are valid")
                return

        try:
            # Fetch the business node first to ensure it exists
            fetch_query = "MATCH (b:Business) WHERE b.name = $name RETURN b"
            fetch_result = self.neo4j_conn.query(fetch_query, {'name': business_name})
            if not fetch_result:
                print("No business found with the specified name.")
                return
            
            # Construct the query to remove labels
            remove_labels_query = "MATCH (b:Business {name: $name}) "
            for label in labels:
                # Ensure the label is valid (simple validation to avoid Cypher injection)
                clean_label = ''.join(e for e in label if e.isalnum())
                remove_labels_query += f"REMOVE b:{clean_label} "

            remove_labels_query += "RETURN b"
            result = self.neo4j_conn.query(remove_labels_query, {'name': business_name})
            print("Labels removed successfully:", [r['b'] for r in result])

        except Exception as e:
            print(f"An error occurred while removing labels: {e}")

class TaxManager:
    def __init__(self, neo4j_conn):
        self.neo4j_conn = neo4j_conn
    
    def list_taxes(self):
        try:
            query = "MATCH (n:Taxes) RETURN n LIMIT 100"
            result = self.neo4j_conn.query(query)
            if not result:
                print("No taxes found.")
                return
            for tax in result:
                print(tax)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def download_csv(self):
        print("Downloading tax data to CSV...")
        query = "MATCH (t:Taxes) RETURN t"
        try:
            result = self.neo4j_conn.query(query)
            if not result:
                print("No data found")
                return
            
            with open('csv_files/tax_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = result[0]['t'].keys()  # Assuming all nodes have the same structure
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for record in result:
                    writer.writerow({field: record['t'][field] for field in fieldnames})

            print("Download complete. Data written to 'tax_data.csv'")
        except Exception as e:
            print(f"An error occurred: {e}")

    def upload_csv(self):
        print("Uploading tax data from CSV...")
        try:
            query = """
            LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/LuisMontenegro21/ProyectoBDII-2/main/csv_files/tax.csv' AS row
            MERGE (t:Taxes {
                id: row.id,
                supplier: row.supplier,
                client: row.client,
                emission_date: row.emission_date,
                amount: toFloat(row.amount)  // assuming amount should be a float
            })
            """
            self.neo4j_conn.query(query)
            print("Upload complete. Tax data has been imported into the database.")
        except Exception as e:
            print(f"An error occurred: {e}")