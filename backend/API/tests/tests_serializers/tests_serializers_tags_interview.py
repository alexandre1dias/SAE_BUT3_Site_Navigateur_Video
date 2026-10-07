from django.test import RequestFactory
from uuid import uuid4

from ...serializers import TagsInterviewRelationShipSerializer
from ...errors import ContextError, NotFound
from ...models import Interview, Tag
from ...tests import Neo4jTestCase


class TagsInterviewRelationShipSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")
        self.interview = Interview(titre=f"Interview_{uuid4()}").save()
        self.tag = Tag(name=f"Tag_{uuid4()}").save()

    def test_get_interviews_and_extraits_returns_urls(self):
        serializer = TagsInterviewRelationShipSerializer(
            self.tag, context={"request": self.request}
        )
        data = serializer.data
        self.assertIn(str(self.tag.uuid), data["interviews"])
        self.assertIn(str(self.tag.uuid), data["extraits"])

    def test_create_connects_tag_to_interview(self):
        serializer = TagsInterviewRelationShipSerializer(
            data={"uuid": self.tag.uuid},
            context={"interview": self.interview, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        tag = serializer.save()
        self.assertEqual(tag.uuid, self.tag.uuid)
        self.assertTrue(self.interview.tags_interview.is_connected(self.tag))

    def test_create_raises_contexterror_without_interview(self):
        serializer = TagsInterviewRelationShipSerializer(
            data={"uuid": self.tag.uuid}, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ContextError):
            serializer.save()

    def test_create_raises_notfound_with_invalid_uuid(self):
        serializer = TagsInterviewRelationShipSerializer(
            data={"uuid": "00000000-0000-0000-0000-000000000000"},
            context={"interview": self.interview, "request": self.request},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    def test_delete_disconnects_tag_from_interview(self):
        self.interview.tags_interview.connect(self.tag)
        serializer = TagsInterviewRelationShipSerializer(
            context={"interview": self.interview, "request": self.request}
        )
        tag = serializer.delete(self.tag.uuid)
        self.assertEqual(tag.uuid, self.tag.uuid)
        self.assertFalse(self.interview.tags_interview.is_connected(self.tag))

    def test_delete_raises_contexterror_without_interview(self):
        serializer = TagsInterviewRelationShipSerializer(
            context={"request": self.request}
        )
        with self.assertRaises(ContextError):
            serializer.delete(self.tag.uuid)

    def test_delete_raises_notfound_with_invalid_uuid(self):
        serializer = TagsInterviewRelationShipSerializer(
            context={"interview": self.interview, "request": self.request}
        )
        with self.assertRaises(NotFound):
            serializer.delete("00000000-0000-0000-0000-000000000000")
