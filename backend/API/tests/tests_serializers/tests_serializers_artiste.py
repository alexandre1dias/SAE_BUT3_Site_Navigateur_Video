from django.test import RequestFactory
from ...serializers import ArtisteSerializer
from ...errors import ValidatorUnique, NotFound
from ...models import Artiste
from ...tests import Neo4jTestCase


class ArtisteSerializerTests(Neo4jTestCase):
    """
    Tests du serializer ArtisteSerializer
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    def test_get_extraits_urls(self):
        """Vérifie que get_extraits renvoient des URLs valides"""
        artiste = Artiste(name="ArtistLinks").save()
        serializer = ArtisteSerializer(artiste, context={"request": self.request})
        data = serializer.data
        self.assertIn(str(artiste.uuid), data["extraits"])

    def test_create_raises_uniqueproperty(self):
        """Création en doublon -> ValidatorUnique"""
        Artiste(name="Daft Punk").save()
        payload = {"name": "Daft Punk", "info": "duo"}

        serializer = ArtisteSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    def test_update_raises_unique_on_conflict(self):
        """Tentative de renommage en un nom déjà existant -> ValidatorUnique"""
        a1 = Artiste(name="Existing1").save()
        a2 = Artiste(name="Existing2").save()

        payload = {"name": "Existing2", "info": "oops"}
        serializer = ArtisteSerializer(
            instance=a1, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
