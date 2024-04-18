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
    
    def add_businesses(self):
        pass


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
            with open('csv_files/tax_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    query = """
                    MERGE    (t:Taxes {amount: $amount, supplier: $supplier, client: $client, id: $id, emission_date:$emission_date})
                    """
                    parameters = {
                        'amount': row['amount'],
                        'supplier': row['supplier'],
                        'client': row['client'],
                        'id': row['id'],
                        'emission_date': row['emission_date']
                    }
                    self.neo4j_conn.query(query, parameters)
            print("Upload complete. Tax data has been imported into the database.")
        except Exception as e:
            print(f"An error occurred: {e}")