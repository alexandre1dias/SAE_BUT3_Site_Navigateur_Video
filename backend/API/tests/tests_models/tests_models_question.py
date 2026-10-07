from neomodel import db
from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Question, Theme


class QuestionTestCase(Neo4jTestCase):

    def test_creation_question(self):
        """Création simple d'une question"""
        q = Question(texte="Quel est ton style ?").save()
        self.assertIsNotNone(q.uuid)
        # db_property='name' => propriété stockée sous 'name'
        self.assertEqual(q.texte, "Quel est ton style ?")
        props = q.__properties__
        self.assertEqual(props["texte"], "Quel est ton style ?")

    def test_unique_texte_constraint(self):
        """Le texte doit être unique"""
        Question(texte="Unique?").save()
        with self.assertRaises(UniqueProperty):
            Question(texte="Unique?").save()

    def test_update_texte(self):
        """Mise à jour du texte"""
        q = Question(texte="Ancien texte").save()
        q.texte = "Nouveau texte"
        q.save()
        reloaded = Question.nodes.get(uuid=q.uuid)
        self.assertEqual(reloaded.texte, "Nouveau texte")

        # tenter de renamemer sur un texte existant lève UniqueProperty
        Question(texte="TexteExistant").save()
        reloaded.texte = "TexteExistant"
        with self.assertRaises(UniqueProperty):
            reloaded.save()

    def test_delete_question(self):
        """Suppression d'une question"""
        q = Question(texte="À supprimer").save()
        uuid = q.uuid
        q.delete()
        with self.assertRaises(DoesNotExist):
            Question.nodes.get(uuid=uuid)

    def test_filtering_and_properties(self):
        """Filtrage via nodes.filter() et accès aux propriétés"""
        Question(texte="Q1").save()
        Question(texte="Q2").save()

        found = Question.nodes.filter(texte="Q1")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].texte, "Q1")

        props = found[0].__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["texte"], "Q1")

    def test_relation_theme_connect_and_replace(self):
        """Connecter une Theme (A_THEME), vérifier, remplacer et déconnecter"""
        q = Question(texte="Sur quel thème ?").save()
        t1 = Theme(name="Musique").save()
        t2 = Theme(name="Culture").save()

        # Connecter t1
        q.theme.connect(t1)
        connected = q.theme.all()
        self.assertEqual(len(connected), 1)
        self.assertEqual(connected[0].name, "Musique")

        # Remplacer la theme : déconnecter t1 et connecter t2
        q.theme.reconnect(t1, t2)
        connected_after = q.theme.all()
        self.assertEqual(len(connected_after), 1)
        self.assertEqual(connected_after[0].name, "Culture")

    def test_relation_persists_theme_exists_after_question_delete(self):
        """La suppression d'une Question doit retirer la relation mais ne pas supprimer le Theme"""
        t = Theme(name="Histoire").save()
        q = Question(texte="Question temporaire").save()
        q.theme.connect(t)

        # Vérifie relation avant suppression
        result_before, _ = db.cypher_query(
            "MATCH (q:Question {uuid:$uuid})-[:A_THEME]->(t:Theme) RETURN count(t)",
            {"uuid": q.uuid},
        )
        self.assertEqual(int(result_before[0][0]), 1)

        # Supprime la question
        q.delete()

        # Le theme doit toujours exister
        themes_remaining = Theme.nodes.filter(name="Histoire")
        self.assertEqual(len(themes_remaining), 1)

        # Plus aucune relation depuis une question vers ce theme
        result_after, _ = db.cypher_query(
            "MATCH (:Question)-[:A_THEME]->(t:Theme {name:$name}) RETURN count(*)",
            {"name": "Histoire"},
        )
        self.assertEqual(int(result_after[0][0]), 0)
