from django.test import RequestFactory
from django.contrib.auth.hashers import check_password

from ...serializers import UtilisateurSerializer
from ...errors import ValidatorUnique
from ...models import Utilisateur
from ...tests import Neo4jTestCase


class UtilisateurSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Lecture des URLs ---
    def test_get_relationships_urls(self):
        user = Utilisateur(
            pseudo="user1",
            prenom="John",
            nom="Doe",
            email="john@example.com",
            password="pwd",
            is_admin=False,
        ).save()

        serializer = UtilisateurSerializer(user, context={"request": self.request})
        data = serializer.data

        self.assertIn(str(user.uuid), data["recherches_artistes"])
        self.assertIn(str(user.uuid), data["regarder_interviews"])
        self.assertIn(str(user.uuid), data["regarder_extraits"])
        self.assertIn(str(user.uuid), data["recherches_questions"])

    # --- Création ---
    def test_create_success(self):
        payload = {
            "pseudo": "newuser",
            "prenom": "Alice",
            "nom": "Smith",
            "email": "alice@example.com",
            "password": "secret123",
        }
        serializer = UtilisateurSerializer(
            data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        reloaded = Utilisateur.nodes.get(uuid=user.uuid)
        self.assertEqual(reloaded.pseudo, "newuser")
        self.assertEqual(reloaded.prenom, "Alice")
        self.assertEqual(reloaded.nom, "Smith")
        self.assertEqual(reloaded.email, "alice@example.com")
        self.assertTrue(check_password("secret123", reloaded.password))
        self.assertFalse(reloaded.is_admin)

    def test_create_raises_uniqueproperty(self):
        Utilisateur(
            pseudo="dupuser",
            prenom="John",
            nom="Doe",
            email="dup@example.com",
            password="pwd",
            is_admin=False,
        ).save()

        payload = {
            "pseudo": "dupuser",
            "prenom": "Alice",
            "nom": "Smith",
            "email": "alice2@example.com",
            "password": "secret123",
            "is_admin": False,
        }
        serializer = UtilisateurSerializer(
            data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success_with_password_change(self):
        user = Utilisateur(
            pseudo="updateuser",
            prenom="Bob",
            nom="Brown",
            email="bob@example.com",
            password="oldpwd",
            is_admin=True,
        ).save()

        payload = {
            "pseudo": "updateuser2",
            "prenom": "Robert",
            "password": "newsecret",
        }
        serializer = UtilisateurSerializer(
            instance=user, data=payload, context={"request": self.request}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        self.assertEqual(updated.pseudo, "updateuser2")
        self.assertEqual(updated.prenom, "Robert")
        self.assertTrue(updated.is_admin)
        self.assertTrue(check_password("newsecret", updated.password))

    def test_update_raises_uniqueproperty(self):
        Utilisateur(
            pseudo="existuser",
            prenom="Jane",
            nom="Doe",
            email="exist@example.com",
            password="pwd",
            is_admin=False,
        ).save()

        user = Utilisateur(
            pseudo="toUpdate",
            prenom="Mark",
            nom="Smith",
            email="mark@example.com",
            password="pwd",
            is_admin=False,
        ).save()

        payload = {"pseudo": "existuser"}
        serializer = UtilisateurSerializer(
            instance=user, data=payload, context={"request": self.request}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
