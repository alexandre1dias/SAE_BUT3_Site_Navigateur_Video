from django.test.runner import DiscoverRunner
from neomodel import db, config
from API.management.commands.install_labels import Command as install_labels
from API.management.commands.basic_load_bd import Command as basic_load_bd

# Configuration de la base de données de test Neo4j, à adapter en fonction de votre configuration locale
# TODO : Mettre cette configuration dans un fichier de configuration séparé pour éviter de la hardcoder dans le code
TEST_BOLT_URL = "bolt://neo4j:testtest@localhost:17687"


class CustomTestRunner(DiscoverRunner):
    """
    Custom test runner pour initialiser la base de données Neo4j avant les tests et la nettoyer après les tests
    """
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        print("=== Initialisation Neo4j avant tous les tests ===")
        config.DATABASE_URL = TEST_BOLT_URL
        install_labels().handle()
        basic_load_bd().handle()
        db.cypher_query("MATCH (n) DETACH DELETE n")

    def teardown_test_environment(self, **kwargs):
        db.cypher_query("MATCH (n) DETACH DELETE n")
        super().teardown_test_environment(**kwargs)
