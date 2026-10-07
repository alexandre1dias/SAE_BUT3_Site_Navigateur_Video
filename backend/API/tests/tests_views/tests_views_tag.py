from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Tag
from ...tests import Neo4jTestCase


class TagViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.tag1 = Tag(name=f"Tag_{uuid4()}").save()
        self.tag2 = Tag(name=f"Tag_{uuid4()}").save()

    def test_list_tags(self):
        """
        Vérifie que la liste des tags est correctement renvoyée
        """
        url = reverse("tag-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertTrue(any(t["uuid"] == self.tag1.uuid for t in data))
        self.assertTrue(any(t["uuid"] == self.tag2.uuid for t in data))

    def test_retrieve_tag(self):
        """
        Vérifie qu'un tag peut être récupéré individuellement
        """
        url = reverse("tag-detail", kwargs={"uuid": self.tag1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.tag1.uuid)

    def test_retrieve_nonexistent_tag(self):
        """
        Vérifie qu'une requête sur un tag inexistant renvoie 404
        """
        url = reverse(
            "tag-detail", kwargs={"uuid": "00000000-0000-0000-0000-000000000000"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
