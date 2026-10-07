from uuid import uuid4
from django.test import RequestFactory

from ...serializers import RecherchesQuestionsSerializer
from ...errors import ContextError, NotFound
from ...models import Utilisateur, Question, Theme, Extrait
from ...tests import Neo4jTestCase


class RecherchesQuestionsSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")
        unique_email = f"{uuid4()}@example.com"
        self.user = Utilisateur(
            pseudo=f"user_{uuid4()}",
            prenom="John",
            nom="Doe",
            email=unique_email,
            password="pwd",
            is_admin=False,
        ).save()
        self.theme = Theme(name=f"Theme{uuid4()}").save()
        self.question = Question(texte=f"Question{uuid4()}").save()
        self.question.theme.connect(self.theme)
        self.extrait = Extrait(titre="Extrait1", duree=100).save()
        self.extrait.question.connect(self.question)

    # --- Getters ---
    def test_getters_return_correct_data(self):
        self.user.recherches_questions.connect(self.question)
        serializer = RecherchesQuestionsSerializer(
            self.question, context={"request": self.request, "utilisateur": self.user}
        )
        data = serializer.data

        # date_heure is iso string
        self.assertIsInstance(data["date_heure"], str)
        self.assertEqual(data["texte"], self.question.texte)
        self.assertIn(str(self.theme.uuid), data["theme"])
        self.assertIn(str(self.question.uuid), data["extraits"])

    def test_get_date_heure_raises_contexterror_without_utilisateur(self):
        serializer = RecherchesQuestionsSerializer(
            self.question, context={"request": self.request}
        )
        with self.assertRaises(ContextError):
            serializer.get_date_heure(self.question)

    # --- create ---
    def test_create_connects_question_to_utilisateur(self):
        serializer = RecherchesQuestionsSerializer(
            data={"uuid": self.question.uuid},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        question = serializer.save()
        self.assertEqual(question.uuid, self.question.uuid)
        self.assertTrue(self.user.recherches_questions.is_connected(self.question))

    def test_create_raises_contexterror_without_utilisateur(self):
        serializer = RecherchesQuestionsSerializer(
            data={"uuid": self.question.uuid}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = RecherchesQuestionsSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000"},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_question_from_utilisateur(self):
        self.user.recherches_questions.connect(self.question)
        serializer = RecherchesQuestionsSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        question = serializer.delete(self.question.uuid)
        self.assertEqual(question.uuid, self.question.uuid)
        self.assertFalse(self.user.recherches_questions.is_connected(self.question))

    def test_delete_raises_contexterror_without_utilisateur(self):
        serializer = RecherchesQuestionsSerializer(context={"request": self.request})
        with self.assertRaises(ContextError):
            serializer.delete(self.question.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = RecherchesQuestionsSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
