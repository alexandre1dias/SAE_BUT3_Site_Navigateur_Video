from uuid import uuid4
from django.test import RequestFactory
from ...serializers import RecherchesArtistesSerializer
from ...errors import ContextError, NotFound
from ...models import Utilisateur, Artiste, Extrait
from ...tests import Neo4jTestCase


class RecherchesArtistesSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")
        unique_email = f"{uuid4()}@example.com"
        self.user = Utilisateur(
            pseudo=f"user_{uuid4()}",
            prenom="John",
            nom="Doe",
            email=unique_email,
            password="pwd",
            is_admin=False,
        ).save()
        self.artiste = Artiste(name="Artiste1", info="Info1").save()
        self.extrait = Extrait(titre="Extrait1", duree=100).save()
        self.extrait.interviewer.connect(self.artiste)

    # --- Getters ---
    def test_getters_return_correct_data(self):
        self.user.recherches_artistes.connect(self.artiste)
        serializer = RecherchesArtistesSerializer(
            self.artiste, context={"request": self.request, "utilisateur": self.user}
        )
        data = serializer.data

        # date_heure is iso string
        self.assertIsInstance(data["date_heure"], str)
        self.assertEqual(data["name"], self.artiste.name)
        self.assertIn(str(self.artiste.uuid), data["extraits"])

    def test_get_date_heure_raises_contexterror_without_utilisateur(self):
        serializer = RecherchesArtistesSerializer(
            self.artiste, context={"request": self.request}
        )
        with self.assertRaises(ContextError):
            serializer.get_date_heure(self.artiste)

    # --- create ---
    def test_create_connects_artiste_to_utilisateur(self):
        serializer = RecherchesArtistesSerializer(
            data={"uuid": self.artiste.uuid},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        artiste = serializer.save()
        self.assertEqual(artiste.uuid, self.artiste.uuid)
        self.assertTrue(self.user.recherches_artistes.is_connected(self.artiste))

    def test_create_raises_contexterror_without_utilisateur(self):
        serializer = RecherchesArtistesSerializer(
            data={"uuid": self.artiste.uuid}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = RecherchesArtistesSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000"},
            context={"utilisateur": self.user, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_artiste_from_utilisateur(self):
        self.user.recherches_artistes.connect(self.artiste)
        serializer = RecherchesArtistesSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        artiste = serializer.delete(self.artiste.uuid)
        self.assertEqual(artiste.uuid, self.artiste.uuid)
        self.assertFalse(self.user.recherches_artistes.is_connected(self.artiste))

    def test_delete_raises_contexterror_without_utilisateur(self):
        serializer = RecherchesArtistesSerializer(context={"request": self.request})
        with self.assertRaises(ContextError):
            serializer.delete(self.artiste.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = RecherchesArtistesSerializer(
            context={"utilisateur": self.user, "request": self.request}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
