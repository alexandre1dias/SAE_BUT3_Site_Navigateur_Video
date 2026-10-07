from django.test import TestCase
from neomodel import db, config
from ..management.commands.install_labels import Command

TEST_BOLT_URL = "bolt://neo4j:testtest@localhost:17687"


def _count_nodes_by_label_and_property(label, prop, value):
    q = f"""
    MATCH (n:{label} {{{prop}: $value}})
    RETURN count(n) AS c
    """
    results, meta = db.cypher_query(q, {"value": value})
    return int(results[0][0])


class Neo4jTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Nettoyage initial de la base
        db.cypher_query("MATCH (n) DETACH DELETE n")

    def tearDown(self):
        # Nettoyage après chaque test pour isoler les données
        db.cypher_query("MATCH (n) DETACH DELETE n")
