import os
import time
from neomodel import db
from neo4j.exceptions import ServiceUnavailable

username    = os.getenv("NEO4J_USERNAME")
password    = os.getenv("NEO4J_PASSWORD")
url         = os.getenv("NEO4J_URL")

NEO4J_URL= f'bolt://{username}:{password}@{url}'

print("⏳ Attente de la disponibilité de Neo4j...")

while True:
    try:
        db.set_connection(NEO4J_URL)
        db.cypher_query("RETURN 1")  # Test de connexion
        print("Neo4j est prêt !")
        break
    except ServiceUnavailable:
        print("Neo4j non disponible, nouvelle tentative dans 2 secondes...")
        time.sleep(2)
