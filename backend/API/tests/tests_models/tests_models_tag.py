from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from ...tests import Neo4jTestCase
from ...models import Tag


class TagTestCase(Neo4jTestCase):

    def test_creation_tag(self):
        """Création simple d'un tag"""
        t = Tag(name="rock").save()
        self.assertIsNotNone(t.uuid)
        self.assertEqual(t.name, "rock")

    def test_unique_name_constraint(self):
        """Le nom doit être unique"""
        Tag(name="jazz").save()
        with self.assertRaises(UniqueProperty):
            Tag(name="jazz").save()

    def test_update_name(self):
        """Mise à jour du nom du tag"""
        t = Tag(name="electro").save()
        t.name = "electro-pop"
        t.save()
        reloaded = Tag.nodes.get(uuid=t.uuid)
        self.assertEqual(reloaded.name, "electro-pop")

        # essayer de renommer sur un nom existant doit lever UniqueProperty
        Tag(name="blues").save()
        reloaded.name = "blues"
        with self.assertRaises(UniqueProperty):
            reloaded.save()

    def test_delete_tag(self):
        """Suppression d'un tag"""
        t = Tag(name="temp-tag").save()
        uuid = t.uuid
        t.delete()
        with self.assertRaises(DoesNotExist):
            Tag.nodes.get(uuid=uuid)

    def test_filtering_and_properties(self):
        """Filtrage via nodes.filter() et accès aux propriétés via __properties__"""
        Tag(name="hiphop").save()
        Tag(name="classical").save()

        found = Tag.nodes.filter(name="hiphop")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].name, "hiphop")

        props = found[0].__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["name"], "hiphop")
