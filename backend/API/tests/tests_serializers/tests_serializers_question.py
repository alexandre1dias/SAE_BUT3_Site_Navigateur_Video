from uuid import uuid4
from django.test import RequestFactory

from ...serializers import QuestionSerializer
from ...errors import ValidatorUnique, NotFound
from ...models import Question, Theme
from ...tests import Neo4jTestCase


class QuestionSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Méthodes de lecture ---
    def test_get_theme_and_extraits_urls(self):
        theme = Theme(name="Thème1").save()
        question = Question(texte="Q1").save()
        question.theme.connect(theme)

        serializer = QuestionSerializer(question, context={"request": self.request})
        data = serializer.data

        self.assertIn(str(theme.uuid), data["theme"])
        self.assertIn(str(question.uuid), data["extraits"])

    # --- Création ---
    def test_create_success_with_theme(self):
        theme = Theme(name="Thème2").save()
        payload = {"texte": "Question avec thème", "theme_uuid": theme.uuid}
        serializer = QuestionSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        question = serializer.save()
        self.assertEqual(question.texte, "Question avec thème")
        self.assertEqual([t.name for t in question.theme.all()], ["Thème2"])

    def test_create_raises_uniqueproperty(self):
        Question(texte="DupQ").save()
        payload = {"texte": "DupQ", "theme_uuid": Theme(name="Theme test").save().uuid}  # doublon
        serializer = QuestionSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    def test_create_with_nonexistent_theme_raises_notfound(self):
        payload = {
            "texte": "QThemeFail",
            "theme_uuid": "00000000-0000-0000-0000-000000000000",
        }
        serializer = QuestionSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success_change_texte_and_theme(self):
        theme_old = Theme(name="ThOld").save()
        theme_new = Theme(name="ThNew").save()
        question = Question(texte="QOld").save()
        question.theme.connect(theme_old)

        payload = {"texte": "QUpdated", "theme_uuid": theme_new.uuid}
        serializer = QuestionSerializer(
            instance=question, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        self.assertEqual(updated.texte, "QUpdated")
        self.assertEqual([t.name for t in updated.theme.all()], ["ThNew"])

    def test_update_with_nonexistent_theme_raises_notfound(self):
        question = Question(texte="QNoTheme").save()

        # Création theme
        self.theme = Theme(name="Theme test").save()
        question.theme.connect(self.theme)

        payload = {"theme_uuid": "00000000-0000-0000-0000-000000000000"}
        serializer = QuestionSerializer(
            instance=question,
            data=payload,
            context={"request": self.request},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    def test_update_raises_uniqueproperty(self):
        Question(texte="Q1").save()
        question = Question(texte="Q2").save()
        payload = {"texte": "Q1"}  # conflit unique
        serializer = QuestionSerializer(
            instance=question,
            data=payload,
            context={"request": self.request},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
