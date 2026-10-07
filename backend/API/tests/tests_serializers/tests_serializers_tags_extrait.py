from django.test import RequestFactory
from uuid import uuid4
from ...serializers import TagsExtraitRelationShipSerializer
from ...errors import ContextError, NotFound
from ...models import Extrait, Tag
from ...tests import Neo4jTestCase


class TagsExtraitRelationShipSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")
        self.extrait = Extrait(titre=f"Extrait_{uuid4()}", duree=120).save()
        self.tag = Tag(name=f"Tag_{uuid4()}").save()

    # --- Getters ---
    def test_get_interviews_and_extraits_returns_urls(self):
        serializer = TagsExtraitRelationShipSerializer(
            self.tag, context={"request": self.request, "extrait": self.extrait}
        )
        interviews_url = serializer.get_interviews(self.tag)
        extraits_url = serializer.get_extraits(self.tag)
        self.assertIn(str(self.tag.uuid), interviews_url)
        self.assertIn(str(self.tag.uuid), extraits_url)

    # --- create ---
    def test_create_connects_tag_to_extrait(self):
        serializer = TagsExtraitRelationShipSerializer(
            data={"uuid": self.tag.uuid},
            context={"extrait": self.extrait, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        tag = serializer.save()
        self.assertEqual(tag.uuid, self.tag.uuid)
        self.assertTrue(self.extrait.tags_extrait.is_connected(self.tag))

    def test_create_raises_contexterror_without_extrait(self):
        serializer = TagsExtraitRelationShipSerializer(
            data={"uuid": self.tag.uuid}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = TagsExtraitRelationShipSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000"},
            context={"extrait": self.extrait, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- delete ---
    def test_delete_disconnects_tag_from_extrait(self):
        self.extrait.tags_extrait.connect(self.tag)
        serializer = TagsExtraitRelationShipSerializer(
            context={"extrait": self.extrait, "request": self.request}
        )
        tag = serializer.delete(self.tag.uuid)
        self.assertEqual(tag.uuid, self.tag.uuid)
        self.assertFalse(self.extrait.tags_extrait.is_connected(self.tag))

    def test_delete_raises_contexterror_without_extrait(self):
        serializer = TagsExtraitRelationShipSerializer(
            context={"request": self.request}
        )
        with self.assertRaises(ContextError):
            serializer.delete(self.tag.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = TagsExtraitRelationShipSerializer(
            context={"extrait": self.extrait, "request": self.request}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
