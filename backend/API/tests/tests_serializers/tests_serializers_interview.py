from datetime import date
from django.test import RequestFactory

from ...serializers import InterviewSerializer
from ...models import Interview
from ...tests import Neo4jTestCase


class InterviewSerializerTests(Neo4jTestCase):
    """
    Tests unitaires du serializer InterviewSerializer
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Méthodes de lecture ---
    def test_get_extraits_and_tags_return_urls(self):
        interview = Interview(titre="Interview1", date=date(2024, 1, 1)).save()
        serializer = InterviewSerializer(interview, context={"request": self.request})
        data = serializer.data

        # URLs doivent contenir l'UUID de l'interview
        self.assertIn(str(interview.uuid), data["extraits"])
        self.assertIn(str(interview.uuid), data["tags"])

    # --- Création ---
    def test_create_interview_success(self):
        payload = {
            "titre": "New Interview",
            "date": date(2024, 3, 15),
            "description": "Description test",
        }
        serializer = InterviewSerializer(
            data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        interview = serializer.save()

        # Vérification que l'interview est bien enregistrée
        reloaded = Interview.nodes.get(uuid=interview.uuid)
        self.assertEqual(reloaded.titre, "New Interview")
        self.assertEqual(reloaded.date, date(2024, 3, 15))
        self.assertEqual(reloaded.description, "Description test")

    # --- Mise à jour ---
    def test_update_interview_success(self):
        interview = Interview(
            titre="Old Title",
            date=date(2024, 1, 1),
            occasion="Old Occasion",
            description="Old Desc",
        ).save()

        payload = {
            "titre": "Updated Title",
            "date": date(2024, 4, 1),
            "occasion": "Updated Occasion",
            "description": "Updated Desc",
        }
        serializer = InterviewSerializer(
            instance=interview, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        # Vérifie que les champs ont bien été mis à jour
        ex = Interview.nodes.get(uuid=updated.uuid)
        self.assertEqual(ex.titre, "Updated Title")
        self.assertEqual(ex.date, date(2024, 4, 1))
        self.assertEqual(ex.description, "Updated Desc")
