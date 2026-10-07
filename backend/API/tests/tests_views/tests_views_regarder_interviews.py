from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Interview, Utilisateur
from ...tests import Neo4jTestCase


class RegarderInterviewsViewSetAPITests(Neo4jTestCase):
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

        # Création d'un utilisateur
        self.utilisateur = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom",
            nom="Nom",
            email=f"user_{uuid4()}@example.com",
            password="password",
        ).save()

        # Création de deux interviews
        self.interview1 = Interview(
            titre=f"Interview_{uuid4()}",
            occasion="Occasion1",
            description="desc1",
            lieu="Lieu1",
        ).save()
        self.interview2 = Interview(
            titre=f"Interview_{uuid4()}",
            occasion="Occasion2",
            description="desc2",
            lieu="Lieu2",
        ).save()

        # Connecter seulement interview1 comme regardée
        self.utilisateur.regarder_interviews.connect(self.interview1)

    def test_list_regarder_interviews(self):
        url = reverse(
            "interview-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [i["uuid"] for i in response.json()]
        self.assertIn(self.interview1.uuid, uuids)
        self.assertNotIn(self.interview2.uuid, uuids)

    def test_retrieve_regarder_interview(self):
        url = reverse(
            "interview-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.interview1.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.interview1.uuid)

    def test_retrieve_nonexistent_regarder_interview_raises_notfound(self):
        """
        Teste la branche `if not results: raise NotFound(Interview)`
        """
        url = reverse(
            "interview-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.interview2.uuid,  # non connecté
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_utilisateur_not_found(self):
        url = reverse("interview-list", kwargs={"utilisateur_uuid": str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_regarder_interview_relation(self):
        url = reverse(
            "interview-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        payload = {"uuid": self.interview2.uuid}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que la relation a été créée
        self.assertTrue(
            self.utilisateur.regarder_interviews.is_connected(self.interview2)
        )

    def test_destroy_regarder_interview_relation(self):
        url = reverse(
            "interview-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.interview1.uuid,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifie que la relation a été supprimée
        self.assertFalse(
            self.utilisateur.regarder_interviews.is_connected(self.interview1)
        )
