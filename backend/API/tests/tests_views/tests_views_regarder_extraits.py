from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Artiste, Extrait, Question, Utilisateur
from ...tests import Neo4jTestCase


class RegarderExtraitsViewSetAPITests(Neo4jTestCase):
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

        # Création de deux extraits
        self.extrait1 = Extrait(
            titre=f"Extrait_{uuid4()}",
            description="desc1",
            youtube_url=f"url_{uuid4()}",
            vimeo_url=f"url_{uuid4()}",
            duree=120,
        ).save()
        self.extrait2 = Extrait(
            titre=f"Extrait_{uuid4()}",
            description="desc2",
            youtube_url=f"url_{uuid4()}",
            vimeo_url=f"url_{uuid4()}",
            duree=180,
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name="Artiste test").save()
        self.question = Question(texte="Question test").save()

        self.extrait1.interviewer.connect(self.artiste)
        self.extrait2.interviewer.connect(self.artiste)

        self.extrait1.question.connect(self.question)
        self.extrait2.question.connect(self.question)

        # Connecter seulement extrait1 comme regardé
        self.utilisateur.regarder_extraits.connect(self.extrait1)

    def test_list_regarder_extraits(self):
        url = reverse(
            "extrait-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [e["uuid"] for e in response.json()]
        self.assertIn(self.extrait1.uuid, uuids)
        self.assertNotIn(self.extrait2.uuid, uuids)

    def test_retrieve_regarder_extrait(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.extrait1.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.extrait1.uuid)

    def test_retrieve_nonexistent_regarder_extrait_raises_notfound(self):
        """
        Teste la branche `if not results: raise NotFound(Extrait)`
        """
        url = reverse(
            "extrait-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.extrait2.uuid,  # non connecté
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_utilisateur_not_found(self):
        url = reverse("extrait-list", kwargs={"utilisateur_uuid": str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_regarder_extrait_relation(self):
        url = reverse(
            "extrait-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        payload = {"uuid": self.extrait2.uuid}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que la relation a été créée
        self.assertTrue(self.utilisateur.regarder_extraits.is_connected(self.extrait2))

    def test_destroy_regarder_extrait_relation(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.extrait1.uuid,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifie que la relation a été supprimée
        self.assertFalse(self.utilisateur.regarder_extraits.is_connected(self.extrait1))

    def test_order_relationship_regarder_extraitOK(self):
        url = reverse(
            "extrait-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url + "?order=regarder_extraits|date_heure")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["uuid"], self.extrait1.uuid)

    def test_order_relationship_regarder_extraitKO(self):
        url = reverse(
            "extrait-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url + "?order=testttest|test")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("Order error", data.keys())
        self.assertEqual("testttest", data["Order error"])

    def test_order_relationship_regarder_extrait_propertyKO(self):
        url = reverse(
            "extrait-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url + "?order=regarder_extraits|test")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertIn("Order error", data.keys())
        self.assertEqual("test", data["Order error"])
