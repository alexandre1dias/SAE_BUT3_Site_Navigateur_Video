from neomodel import db
from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Question, Theme


class ThemeTestCase(Neo4jTestCase):

    def test_creation_theme(self):
        """Création simple d'un theme"""
        t = Theme(name="Musique", description="Tout ce qui est lié à la musique").save()
        self.assertIsNotNone(t.uuid)
        self.assertEqual(t.name, "Musique")
        self.assertEqual(t.description, "Tout ce qui est lié à la musique")

    def test_unique_name_constraint(self):
        """Le nom du theme doit être unique"""
        Theme(name="Cinéma").save()
        with self.assertRaises(UniqueProperty):
            Theme(name="Cinéma").save()

    def test_update_name(self):
        """Mise à jour du nom et de la description"""
        t = Theme(name="OldName").save()
        t.name = "NewName"
        t.save()

        reloaded = Theme.nodes.get(uuid=t.uuid)
        self.assertEqual(reloaded.name, "NewName")

        # tenter de renommer sur un nom existant doit lever UniqueProperty
        Theme(name="ExistName").save()
        reloaded.name = "ExistName"
        with self.assertRaises(UniqueProperty):
            reloaded.save()

    def test_delete_theme(self):
        """Suppression d'un theme"""
        t = Theme(name="À supprimer").save()
        uuid = t.uuid
        t.delete()
        with self.assertRaises(DoesNotExist):
            Theme.nodes.get(uuid=uuid)

    def test_filtering_and_properties(self):
        """Filtrage via nodes.filter() et accès aux propriétés via __properties__"""
        Theme(name="Art").save()
        Theme(name="Science").save()

        found = Theme.nodes.filter(name="Art")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "Art")

        props = found[0].__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["name"], "Art")
        # description absent -> None
        self.assertIsNone(props.get("description"))

    def test_question_relation_integration(self):
        """Vérifie qu'une Question peut se relier à un Theme (test d'intégration relationnel)"""
        theme = Theme(name="Histoire").save()
        q = Question(texte="Parlez-nous de l'histoire locale").save()

        # Connecte la question au theme
        q.theme.connect(theme)

        # Vérifie via Cypher que la relation existe
        result, _ = db.cypher_query(
            "MATCH (q:Question {uuid:$q_uuid})-[:A_THEME]->(t:Theme {uuid:$t_uuid}) RETURN count(*)",
            {"q_uuid": q.uuid, "t_uuid": theme.uuid},
        )
        self.assertEqual(int(result[0][0]), 1)
