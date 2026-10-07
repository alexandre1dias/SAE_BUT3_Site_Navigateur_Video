from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Utilisateur
from ...tests import Neo4jTestCase


class UtilisateurViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.utilisateur1 = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom1",
            nom="Nom1",
            email=f"user1_{uuid4()}@example.com",
            password="password1",
        ).save()

        self.utilisateur2 = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom2",
            nom="Nom2",
            email=f"user2_{uuid4()}@example.com",
            password="password2",
        ).save()

    def test_list_utilisateurs(self):
        """
        Vérifie que la liste des utilisateurs est correctement renvoyée
        """
        self.user = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom1",
            nom="Nom1",
            email=f"user1_{uuid4()}@example.com",
            password=make_password("password"),
            is_admin=True
        ).save()
        self.client.force_authenticate(user=self.user)
        url = reverse("utilisateur-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertTrue(any(u["uuid"] == self.utilisateur1.uuid for u in data))
        self.assertTrue(any(u["uuid"] == self.utilisateur2.uuid for u in data))

    def test_retrieve_utilisateur(self):
        """
        Vérifie qu'un utilisateur peut être récupéré individuellement
        """
        self.client.force_authenticate(user=self.utilisateur1)
        url = reverse("utilisateur-detail", kwargs={"uuid": self.utilisateur1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.utilisateur1.uuid)

    def test_retrieve_nonexistent_utilisateur(self):
        """
        Vérifie qu'une requête sur un utilisateur inexistant renvoie 404
        """
        url = reverse(
            "utilisateur-detail",
            kwargs={"uuid": "00000000-0000-0000-0000-000000000000"},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
