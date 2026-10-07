from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Extrait, Tag, Utilisateur
from ...tests import Neo4jTestCase


class TagsExtraitRelationShipViewSetAPITests(Neo4jTestCase):
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
            youtube_url=str(uuid4()),
            vimeo_url=str(uuid4()),
            duree=120,
        ).save()

        # Création de deux tags
        self.tag1 = Tag(name=f"Tag_{uuid4()}").save()
        self.tag2 = Tag(name=f"Tag_{uuid4()}").save()

        # Connecter seulement tag1
        self.extrait.tags_extrait.connect(self.tag1)

    def test_list_tags_of_extrait(self):
        url = reverse("tag-list", kwargs={"extrait_uuid": self.extrait.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [t["uuid"] for t in response.json()]
        self.assertIn(self.tag1.uuid, uuids)
        self.assertNotIn(self.tag2.uuid, uuids)

    def test_retrieve_tag_of_extrait(self):
        url = reverse(
            "tag-detail",
            kwargs={"extrait_uuid": self.extrait.uuid, "uuid": self.tag1.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.tag1.uuid)

    def test_retrieve_nonexistent_tag_raises_notfound(self):
        url = reverse(
            "tag-detail",
            kwargs={
                "extrait_uuid": self.extrait.uuid,
                "uuid": self.tag2.uuid,  # non connecté
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_extrait_not_found_raises_notfound(self):
        url = reverse("tag-list", kwargs={"extrait_uuid": str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_tag_relation(self):
        url = reverse("tag-list", kwargs={"extrait_uuid": self.extrait.uuid})
        payload = {"uuid": self.tag2.uuid}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que la relation a été créée
        self.assertTrue(self.extrait.tags_extrait.is_connected(self.tag2))

    def test_destroy_tag_relation(self):
        url = reverse(
            "tag-detail",
            kwargs={"extrait_uuid": self.extrait.uuid, "uuid": self.tag1.uuid},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifie que la relation a été supprimée
        self.assertFalse(self.extrait.tags_extrait.is_connected(self.tag1))
