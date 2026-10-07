from datetime import datetime
from django.test import RequestFactory
from uuid import uuid4
from ...serializers import RegarderExtraitsSerializer
from ...errors import ContextError, NotFound
from ...models import Utilisateur, Extrait, Artiste, Question, Interview, Tag
from ...tests import Neo4jTestCase


class RegarderExtraitsSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")
        self.user = Utilisateur(
            pseudo=f"user_{uuid4()}",
            prenom="John",
            nom="Doe",
            email=f"{uuid4()}@example.com",
            password="pwd",
            is_admin=False,
        ).save()

        self.artiste = Artiste(name=f"Artiste_{uuid4()}").save()
        self.question = Question(texte=f"Question_{uuid4()}").save()
        self.extrait = Extrait(titre=f"Extrait_{uuid4()}", duree=100).save()
        self.extrait.interviewer.connect(self.artiste)
        self.extrait.question.connect(self.question)

    # --- Getters ---
    def test_getters_return_correct_data(self):
        self.user.regarder_extraits.connect(self.extrait)
        serializer = RegarderExtraitsSerializer(
            self.extrait, context={"request": self.request, "utilisateur": self.user}
        )
        data = serializer.data

        # date_heure is iso string
        self.assertIsInstance(data["date_heure"], str)
        self.assertEqual(data["titre"], self.extrait.titre)
        self.assertEqual(data["description"], self.extrait.description)
        self.assertEqual(data["duree"], self.extrait.duree)
        self.assertEqual(data["lieu"], self.extrait.lieu)
        self.assertIn(str(self.artiste.uuid), data["artiste"])
        self.assertIn(str(self.question.uuid), data["question"])
        self.assertIn(str(self.extrait.uuid), data["interviews"])
        self.assertIn(str(self.extrait.uuid), data["tags"])

    def test_get_date_heure_raises_contexterror_without_utilisateur(self):
        serializer = RegarderExtraitsSerializer(
            self.extrait, context={"request": self.request}
        )
        with self.assertRaises(ContextError):
            serializer.get_date_heure(self.extrait)

    # --- create ---
    def test_create_connects_extrait_to_utilisateur(self):
        serializer = RegarderExtraitsSerializer(
            data={"uuid": self.extrait.uuid},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        extrait = serializer.save()
        self.assertEqual(extrait.uuid, self.extrait.uuid)
        self.assertTrue(self.user.regarder_extraits.is_connected(self.extrait))

    def test_create_raises_contexterror_without_utilisateur(self):
        serializer = RegarderExtraitsSerializer(
            data={"uuid": self.extrait.uuid}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = RegarderExtraitsSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000"},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_extrait_from_utilisateur(self):
        self.user.regarder_extraits.connect(self.extrait)
        serializer = RegarderExtraitsSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        extrait = serializer.delete(self.extrait.uuid)
        self.assertEqual(extrait.uuid, self.extrait.uuid)
        self.assertFalse(self.user.regarder_extraits.is_connected(self.extrait))

    def test_delete_raises_contexterror_without_utilisateur(self):
        serializer = RegarderExtraitsSerializer(context={"request": self.request})
        with self.assertRaises(ContextError):
            serializer.delete(self.extrait.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = RegarderExtraitsSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
