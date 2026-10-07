from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Artiste, Utilisateur
from ...tests import Neo4jTestCase


class RecherchesArtistesViewSetAPITests(Neo4jTestCase):
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

        # Création de deux artistes
        self.artiste1 = Artiste(name=f"Artiste_{uuid4()}", info="Info1").save()
        self.artiste2 = Artiste(name=f"Artiste_{uuid4()}", info="Info2").save()

        # Connecter uniquement artiste1 comme recherché
        self.utilisateur.recherches_artistes.connect(self.artiste1)

    def test_list_recherches_artistes(self):
        """
        Vérifie que la liste des artistes recherchés par l'utilisateur est correcte
        """
        url = reverse(
            "artiste-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [a["uuid"] for a in response.json()]
        self.assertIn(self.artiste1.uuid, uuids)
        self.assertNotIn(self.artiste2.uuid, uuids)

    def test_retrieve_recherches_artiste(self):
        """
        Vérifie la récupération d'un artiste recherché spécifique
        """
        url = reverse(
            "artiste-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.artiste1.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.artiste1.uuid)

    def test_retrieve_nonexistent_recherches_artiste_raises_notfound(self):
        """
        Vérifie que get_object renvoie 404 si l'artiste n'est pas recherché par l'utilisateur
        """
        # On utilise un UUID qui existe mais qui n'est pas connecté à l'utilisateur
        url = reverse(
            "artiste-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.artiste2.uuid,  # artiste2 n'est pas connecté
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_utilisateur_not_found(self):
        """
        Vérifie qu'une requête sur un utilisateur inexistant renvoie 404
        """
        url = reverse("artiste-list", kwargs={"utilisateur_uuid": str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recherches_artistes_relation(self):
        """
        Vérifie la création d'une relation recherches_artistes
        """
        url = reverse(
            "artiste-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        payload = {"uuid": self.artiste2.uuid}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Vérifie que la relation a bien été créée dans la DB
        self.assertTrue(
            self.utilisateur.recherches_artistes.is_connected(self.artiste2)
        )

    def test_destroy_recherches_artistes_relation(self):
        """
        Vérifie la suppression de la relation recherches_artistes
        """
        url = reverse(
            "artiste-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.artiste1.uuid,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Vérifie que la relation a été supprimée
        self.assertFalse(
            self.utilisateur.recherches_artistes.is_connected(self.artiste1)
        )
