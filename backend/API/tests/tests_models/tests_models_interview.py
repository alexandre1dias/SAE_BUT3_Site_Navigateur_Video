from datetime import date
from neomodel import db
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Interview, Tag


class InterviewTestCase(Neo4jTestCase):

    def test_creation_interview(self):
        """Création simple d'une interview et vérification des champs"""
        iv = Interview(
            titre="Rencontre avec X",
            date=date(2024, 5, 20),
            occasion="Festival",
            description="Description test",
            lieu="Paris",
        ).save()

        self.assertIsNotNone(iv.uuid)
        self.assertEqual(iv.titre, "Rencontre avec X")
        self.assertEqual(iv.date, date(2024, 5, 20))
        self.assertEqual(iv.occasion, "Festival")
        self.assertEqual(iv.lieu, "Paris")

    def test_update_fields(self):
        """Mise à jour des champs d'une interview"""
        iv = Interview(titre="Old title", date=date(2023, 1, 1)).save()
        iv.titre = "New title"
        iv.save()

        reloaded = Interview.nodes.get(uuid=iv.uuid)
        self.assertEqual(reloaded.titre, "New title")

    def test_delete_interview(self):
        """Suppression d'une interview"""
        iv = Interview(titre="Temp", date=date(2022, 2, 2)).save()
        uuid = iv.uuid
        iv.delete()
        with self.assertRaises(DoesNotExist):
            Interview.nodes.get(uuid=uuid)

    def test_tags_relation_connect_and_list(self):
        """Connecter plusieurs tags et vérifier la récupération"""
        iv = Interview(titre="Interview taguée", date=date(2024, 6, 1)).save()
        t1 = Tag(name="politique").save()
        t2 = Tag(name="culture").save()

        iv.tags_interview.connect(t1)
        iv.tags_interview.connect(t2)

        tags = [t.name for t in iv.tags_interview.all()]
        self.assertCountEqual(tags, ["politique", "culture"])

    def test_disconnect_tags_on_delete_interview(self):
        """Vérifier que la suppression de l'interview retire les relations (les tags subsistent)"""
        iv = Interview(titre="ToDelete", date=date(2024, 7, 7)).save()
        t = Tag(name="sport").save()
        iv.tags_interview.connect(t)

        # Vérifie relation avant suppression
        result_before, _ = db.cypher_query(
            "MATCH (i:Interview {uuid:$uuid})-[:TAGS_INTERVIEW]->(t:Tag) RETURN count(t)",
            {"uuid": iv.uuid},
        )
        self.assertEqual(int(result_before[0][0]), 1)

        iv.delete()

        # Le tag doit toujours exister
        tags_remaining = Tag.nodes.filter(name="sport")
        self.assertEqual(len(tags_remaining), 1)

        # Mais plus de relation depuis une interview vers ce tag
        result_after, _ = db.cypher_query(
            "MATCH (:Interview)-[:TAGS_INTERVIEW]->(t:Tag {name:$name}) RETURN count(*)",
            {"name": "sport"},
        )
        self.assertEqual(int(result_after[0][0]), 0)

    def test_filter_by_date(self):
        """Créer plusieurs interviews et filtrer par date"""
        Interview(titre="Iv1", date=date(2024, 1, 1)).save()
        Interview(titre="Iv2", date=date(2024, 1, 1)).save()
        Interview(titre="Iv3", date=date(2023, 12, 31)).save()

        found = Interview.nodes.filter(date=date(2024, 1, 1))
        titles = [i.titre for i in found]
        self.assertCountEqual(titles, ["Iv1", "Iv2"])

    def test_indexed_field_querying(self):
        """Vérifier qu'on peut filtrer sur le champ indexé 'titre'"""
        Interview(titre="UniqueTitreIndex", date=date(2024, 3, 3)).save()
        res = Interview.nodes.filter(titre="UniqueTitreIndex")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].titre, "UniqueTitreIndex")

    def test_properties_access(self):
        """Accès aux propriétés via __properties__"""
        iv = Interview(titre="PropsTest", date=date(2025, 1, 1), description="D").save()
        props = iv.__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["titre"], "PropsTest")
        self.assertEqual(props["description"], "D")
