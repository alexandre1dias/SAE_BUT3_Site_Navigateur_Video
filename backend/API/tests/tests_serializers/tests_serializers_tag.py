from django.test import RequestFactory

from ...serializers import TagSerializer
from ...errors import ValidatorUnique
from ...models import Tag
from ...tests import Neo4jTestCase


class TagSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Méthodes de lecture ---
    def test_get_interviews_and_extraits_urls(self):
        tag = Tag(name="TagTest").save()
        serializer = TagSerializer(tag, context={"request": self.request})
        data = serializer.data
        self.assertIn(str(tag.uuid), data["interviews"])
        self.assertIn(str(tag.uuid), data["extraits"])

    # --- Création ---
    def test_create_success(self):
        payload = {"name": "NouveauTag"}
        serializer = TagSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        tag = serializer.save()
        reloaded = Tag.nodes.get(uuid=tag.uuid)
        self.assertEqual(reloaded.name, "NouveauTag")

    def test_create_raises_uniqueproperty(self):
        Tag(name="UniqueTag").save()
        payload = {"name": "UniqueTag"}  # doublon
        serializer = TagSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success(self):
        tag = Tag(name="TagOld").save()
        payload = {"name": "TagUpdated"}
        serializer = TagSerializer(
            instance=tag, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.name, "TagUpdated")

    def test_update_raises_uniqueproperty(self):
        Tag(name="TagExist").save()
        tag = Tag(name="TagToUpdate").save()
        payload = {"name": "TagExist"}  # conflit
        serializer = TagSerializer(
            instance=tag, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
