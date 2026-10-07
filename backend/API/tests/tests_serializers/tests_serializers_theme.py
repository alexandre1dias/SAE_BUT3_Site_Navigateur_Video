from django.test import RequestFactory

from ...serializers import ThemeSerializer
from ...errors import ValidatorUnique
from ...models import Theme
from ...tests import Neo4jTestCase


class ThemeSerializerTests(Neo4jTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Méthodes de lecture ---
    def test_get_questions_returns_correct_url(self):
        theme = Theme(name="ThèmeTest", description="Desc").save()
        serializer = ThemeSerializer(theme, context={"request": self.request})
        data = serializer.data
        self.assertIn(str(theme.uuid), data["questions"])

    # --- Création ---
    def test_create_success(self):
        payload = {"name": "ThèmeNouveau"}
        serializer = ThemeSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        theme = serializer.save()
        reloaded = Theme.nodes.get(uuid=theme.uuid)
        self.assertEqual(reloaded.name, "ThèmeNouveau")

    def test_create_raises_uniqueproperty(self):
        Theme(name="ThèmeUnique").save()
        payload = {"name": "ThèmeUnique", "description": "Desc"}  # doublon
        serializer = ThemeSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success(self):
        theme = Theme(name="ThèmeOld").save()
        payload = {"name": "ThèmeUpdated"}
        serializer = ThemeSerializer(
            instance=theme, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.name, "ThèmeUpdated")

    def test_update_raises_uniqueproperty(self):
        Theme(name="ThèmeExist").save()
        theme = Theme(name="ThèmeToUpdate").save()
        payload = {"name": "ThèmeExist", "description": "Desc"}  # conflit
        serializer = ThemeSerializer(
            instance=theme, data=payload, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(ValidatorUnique):
            serializer.save()
