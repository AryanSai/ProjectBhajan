from neo4j import GraphDatabase
import csv

uri = "bolt://localhost:7687/"
driver = GraphDatabase.driver(uri, auth=("neo4j", "YPgqUvMmeP23FsL"))

def create_bajan_relationship(tx, title, deity, level, tempo, language, raga):
    query = (
        "MERGE (t:Title {name: $title}) "
        "MERGE (d:Deity {name: $deity}) "
        "MERGE (l:Level {name: $level}) "
        "MERGE (t:Tempo {name: $tempo}) "
        "MERGE (lang:Language {name: $language}) "
        "MERGE (r:Raga {name: $raga}) "
        "MERGE (b:Bajan {name: $title}) "
        "MERGE (t)-[:ASSOCIATED_WITH]->(b) "
        "MERGE (d)-[:ASSOCIATED_WITH]->(b) "
        "MERGE (l)-[:ASSOCIATED_WITH]->(b) "
        "MERGE (t)-[:ASSOCIATED_WITH]->(b) "
        "MERGE (lang)-[:ASSOCIATED_WITH]->(b) "
        "MERGE (r)-[:ASSOCIATED_WITH]->(b)"
    )
    tx.run(query, title=title, deity=deity, level=level, tempo=tempo, language=language, raga=raga)

with driver.session() as session:
    with open('Bajans_FullDetails.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row['Title']
            deity = row['Deity']
            level = row['Level']
            tempo = row['Tempo']
            language = row['Language']
            raga = row['Raga']
            # execute the Cypher query within a transaction
            session.execute_write(create_bajan_relationship, title, deity, level, tempo, language, raga)

driver.close()
