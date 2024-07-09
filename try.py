from neo4j import GraphDatabase
import csv

# Define the connection URI and authentication
uri = "bolt://localhost:7687/"
driver = GraphDatabase.driver(uri, auth=("neo4j", "YPgqUvMmeP23FsL"))

def create_bajan_relationship(tx, deity, bajan, meaning):
    query = (
        "MERGE (d:Deity {name: $deity}) "
        "MERGE (b:Bajan {name: $bajan, meaning: $meaning}) "
        "MERGE (d)-[:ASSOCIATED_WITH]->(b)"
    )
    tx.run(query, deity=deity, bajan=bajan, meaning=meaning)

with driver.session() as session:
    # Read CSV file
    with open('bhajans.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            deity = row['Deity']
            bajan = row['Bhajan']
            meaning = row['Meaning']
            # Execute the Cypher query within a transaction
            session.execute_write(create_bajan_relationship, deity, bajan, meaning)

driver.close()