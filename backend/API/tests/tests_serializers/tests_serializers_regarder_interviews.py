from datetime import datetime
from django.test import RequestFactory
from uuid import uuid4
from ...serializers import RegarderInterviewsSerializer
from ...errors import ContextError, NotFound
from ...models import Utilisateur, Interview, Extrait, Tag
from ...tests import Neo4jTestCase


class RegarderInterviewsSerializerTests(Neo4jTestCase):
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

        self.interview = Interview(titre=f"Interview_{uuid4()}").save()

    # --- Getters ---
    def test_getters_return_correct_data(self):
        self.user.regarder_interviews.connect(self.interview)
        serializer = RegarderInterviewsSerializer(
            self.interview, context={"request": self.request, "utilisateur": self.user}
        )
        data = serializer.data

        self.assertIsInstance(data["date_heure"], str)
        self.assertEqual(data["titre"], self.interview.titre)
        self.assertEqual(data["date"], self.interview.date)
        self.assertEqual(data["description"], self.interview.description)
        self.assertIn(str(self.interview.uuid), data["extraits"])
        self.assertIn(str(self.interview.uuid), data["tags"])

    def test_get_date_heure_raises_contexterror_without_utilisateur(self):
        serializer = RegarderInterviewsSerializer(
            self.interview, context={"request": self.request}
        )
        with self.assertRaises(ContextError):
            serializer.get_date_heure(self.interview)

    # --- create ---
    def test_create_connects_interview_to_utilisateur(self):
        serializer = RegarderInterviewsSerializer(
            data={"uuid": self.interview.uuid},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        interview = serializer.save()
        self.assertEqual(interview.uuid, self.interview.uuid)
        self.assertTrue(self.user.regarder_interviews.is_connected(self.interview))

    def test_create_raises_contexterror_without_utilisateur(self):
        serializer = RegarderInterviewsSerializer(
            data={"uuid": self.interview.uuid}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = RegarderInterviewsSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000"},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_interview_from_utilisateur(self):
        self.user.regarder_interviews.connect(self.interview)
        serializer = RegarderInterviewsSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        interview = serializer.delete(self.interview.uuid)
        self.assertEqual(interview.uuid, self.interview.uuid)
        self.assertFalse(self.user.regarder_interviews.is_connected(self.interview))

    def test_delete_raises_contexterror_without_utilisateur(self):
        serializer = RegarderInterviewsSerializer(context={"request": self.request})
        with self.assertRaises(ContextError):
            serializer.delete(self.interview.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = RegarderInterviewsSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
