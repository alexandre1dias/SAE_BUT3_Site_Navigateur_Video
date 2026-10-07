from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Interview, Extrait, Utilisateur
from ...serializers import PositionInputSerializer
from ...tests import Neo4jTestCase


class InterviewsViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.user = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom1",
            nom="Nom1",
            email=f"user1_{uuid4()}@example.com",
            password=make_password("password"),
            is_admin=True
        ).save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Création d'un extrait
        self.extrait = Extrait(
            titre=f"Extrait_{uuid4()}",
            description="desc",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=60,
        ).save()

        # Création de deux interviews
        self.interview1 = Interview(
            titre="Interview 1",
            date=None,
            occasion="Occ1",
            description="Desc1",
            lieu="Lieu1",
        ).save()

        self.interview2 = Interview(
            titre="Interview 2",
            date=None,
            occasion="Occ2",
            description="Desc2",
            lieu="Lieu2",
        ).save()

        # Connecter uniquement interview1 à l'extrait
        self.extrait.interviews.connect(self.interview1, {"position": 1})

    def test_list_interviews(self):
        url = reverse("interview-list", kwargs={"extrait_uuid": self.extrait.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [i["uuid"] for i in response.json()]
        self.assertIn(self.interview1.uuid, uuids)
        self.assertNotIn(self.interview2.uuid, uuids)

    def test_retrieve_interview(self):
        url = reverse(
            "interview-detail",
            kwargs={"extrait_uuid": self.extrait.uuid, "uuid": self.interview1.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.interview1.uuid)

    def test_get_extrait_not_found_raises_notfound(self):
        url = reverse("interview-list", kwargs={"extrait_uuid": str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Tests de création de relation
    def test_create_interview_relation(self):
        url = reverse("interview-list", kwargs={"extrait_uuid": self.extrait.uuid})
        payload = {"uuid": self.interview2.uuid, "position": 1}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["uuid"], payload["uuid"])

    # Tests de modification de position
    def test_partial_update_position(self):
        url = reverse(
            "interview-detail",
            kwargs={"extrait_uuid": self.extrait.uuid, "uuid": self.interview1.uuid},
        )
        payload = {"position": 5}
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rel = self.extrait.interviews.relationship(self.interview1)
        self.assertEqual(rel.position, 5)

    def test_partial_update_nonexistent_relation(self):
        url = reverse(
            "interview-detail",
            kwargs={"extrait_uuid": self.extrait.uuid, "uuid": self.interview2.uuid},
        )
        payload = {"position": 3}
        response = self.client.patch(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Interview", response.json()["Not Found"])

    def test_destroy_calls_serializer_delete(self):
        """
        Vérifie que perform_destroy appelle bien serializer.delete()
        """
        url = reverse(
            "interview-detail",
            kwargs={"extrait_uuid": self.extrait.uuid, "uuid": self.interview1.uuid},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
