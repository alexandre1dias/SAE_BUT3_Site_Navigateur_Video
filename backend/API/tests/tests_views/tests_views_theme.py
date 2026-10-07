from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Theme
from ...tests import Neo4jTestCase


class ThemeViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.theme1 = Theme(name=f"Theme_{uuid4()}", description="Description 1").save()
        self.theme2 = Theme(name=f"Theme_{uuid4()}", description="Description 2").save()

    def test_list_themes(self):
        """
        Vérifie que la liste des thèmes est correctement renvoyée
        """
        url = reverse("theme-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertTrue(any(t["uuid"] == self.theme1.uuid for t in data))
        self.assertTrue(any(t["uuid"] == self.theme2.uuid for t in data))

    def test_retrieve_theme(self):
        """
        Vérifie qu'un thème peut être récupéré individuellement
        """
        url = reverse("theme-detail", kwargs={"uuid": self.theme1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.theme1.uuid)

    def test_retrieve_nonexistent_theme(self):
        """
        Vérifie qu'une requête sur un thème inexistant renvoie 404
        """
        url = reverse(
            "theme-detail", kwargs={"uuid": "00000000-0000-0000-0000-000000000000"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
