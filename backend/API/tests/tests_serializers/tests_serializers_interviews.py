from datetime import date
from django.test import RequestFactory

from ...serializers import InterviewsSerializer
from ...errors import ContextError, NotFound
from ...models import Extrait, Interview
from ...tests import Neo4jTestCase


class InterviewsSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")
        self.extrait = Extrait(titre="Extrait1", duree=120).save()
        self.interview = Interview(
            titre="Interview1",
            date=date(2024, 1, 1),
            occasion="Occasion1",
            description="Desc1",
            lieu="Lieu1",
        ).save()

    # --- Getters ---
    def test_get_extraits_and_tags_urls(self):
        serializer = InterviewsSerializer(
            self.interview, context={"request": self.request}
        )
        data = serializer.data
        self.assertIn(str(self.interview.uuid), data["extraits"])
        self.assertIn(str(self.interview.uuid), data["tags"])
        self.assertEqual(data["titre"], "Interview1")
        self.assertEqual(data["date"], "2024-01-01")
        self.assertEqual(data["occasion"], "Occasion1")
        self.assertEqual(data["description"], "Desc1")

    # --- create ---
    def test_create_connects_interview_to_extrait(self):
        serializer = InterviewsSerializer(
            data={"uuid": self.interview.uuid, "position": 1},
            context={"request": self.request, "extrait": self.extrait},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save()
        self.assertEqual(result.uuid, self.interview.uuid)
        rels = list(self.extrait.interviews.all())
        self.assertIn(self.interview, rels)

    def test_create_raises_contexterror_without_extrait(self):
        serializer = InterviewsSerializer(
            data={"uuid": self.interview.uuid, "position": 1},
            context={"request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = InterviewsSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000", "position": 1},
            context={"request": self.request, "extrait": self.extrait},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_interview_from_extrait(self):
        self.extrait.interviews.connect(self.interview, {"position": 1})
        serializer = InterviewsSerializer(
            context={"request": self.request, "extrait": self.extrait}
        )
        result = serializer.delete(self.interview.uuid)
        self.assertEqual(result.uuid, self.interview.uuid)
        self.assertFalse(self.extrait.interviews.is_connected(self.interview))

    def test_delete_raises_contexterror_without_extrait(self):
        serializer = InterviewsSerializer(context={"request": self.request})
        with self.assertRaises(ContextError):
            serializer.delete(self.interview.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = InterviewsSerializer(
            context={"request": self.request, "extrait": self.extrait}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
