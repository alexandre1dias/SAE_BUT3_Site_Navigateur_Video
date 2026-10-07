from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from neomodel import db
from uuid import uuid4
from ...models import Utilisateur
from ...tests import Neo4jTestCase
from django.contrib.auth.hashers import make_password


class LoginViewAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        # Création d'un utilisateur avec pseudo et email
        self.utilisateur = Utilisateur(
            pseudo=f"user_{uuid4()}",
            prenom=f"Dupond {uuid4()} du nom",
            nom=f"de l'arbre à {uuid4} feuilles",
            email=f"user_{uuid4()}@example.com",
            password=make_password("password123"),  # mot de passe hashé
        ).save()

    def test_login_with_email_success(self):
        url = reverse("login")
        response = self.client.post(
            url,
            data={"username": self.utilisateur.email, "password": "password123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertIn("utilisateur", data)

    def test_login_with_pseudo_success(self):
        url = reverse("login")
        response = self.client.post(
            url,
            data={"username": self.utilisateur.pseudo, "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertIn("utilisateur", data)

    def test_login_invalid_password(self):
        url = reverse("login")
        response = self.client.post(
            url,
            data={"username": self.utilisateur.email, "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Identifiants invalides")

    def test_login_nonexistent_user(self):
        url = reverse("login")
        response = self.client.post(
            url,
            data={"username": "doesnotexist@example.com", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Identifiants invalides")

    def test_login_missing_fields(self):
        url = reverse("login")
        response = self.client.post(url, data={}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.json().get("username", False))
