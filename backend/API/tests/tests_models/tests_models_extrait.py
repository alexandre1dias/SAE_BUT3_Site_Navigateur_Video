from neomodel.exceptions import UniqueProperty
from neomodel.exceptions import DoesNotExist
from datetime import date
from ...tests import Neo4jTestCase
from ...models import Artiste, Extrait, Interview, Question, Tag


class ExtraitTestCase(Neo4jTestCase):

    def test_creation_extrait(self):
        """Test de création simple"""
        extrait = Extrait(
            titre="Extrait 1",
            description="Un extrait de test",
            youtube_url="https://youtube.com/watch?v=abc123",
            vimeo_url="https://vimeo.com/123",
            lieu="Paris",
            duree=120,
        ).save()

        self.assertIsNotNone(extrait.uuid)
        self.assertEqual(extrait.titre, "Extrait 1")
        self.assertEqual(extrait.duree, 120)
        self.assertEqual(extrait.lieu, "Paris")
        self.assertIsInstance(extrait.uploaded_at, date)

    def test_update_description(self):
        """Mise à jour de la description"""
        extrait = Extrait(
            titre="Extrait modif",
            youtube_url="https://youtube.com/watch?v=xyz",
            vimeo_url="https://vimeo.com/xyz",
            duree=180,
        ).save()
        extrait.description = "Nouvelle description"
        extrait.save()

        updated = Extrait.nodes.get(uuid=extrait.uuid)
        self.assertEqual(updated.description, "Nouvelle description")

    def test_delete_extrait(self):
        """Suppression d'un extrait"""
        extrait = Extrait(
            titre="À supprimer",
            youtube_url="https://youtube.com/watch?v=del",
            vimeo_url="https://vimeo.com/del",
            duree=90,
        ).save()
        uuid = extrait.uuid
        extrait.delete()
        with self.assertRaises(DoesNotExist):
            Extrait.nodes.get(uuid=uuid)

    def test_relation_interviewer(self):
        """Relation PARTICIPER (Extrait → Artiste)"""
        extrait = Extrait(
            titre="Interview avec un artiste",
            youtube_url="https://youtube.com/watch?v=artist",
            vimeo_url="https://vimeo.com/artist",
            duree=200,
        ).save()
        artiste = Artiste(name="Angèle").save()

        extrait.interviewer.connect(artiste)
        connected = extrait.interviewer.all()
        self.assertEqual(len(connected), 1)
        self.assertEqual(connected[0].name, "Angèle")

    def test_relation_question(self):
        """Relation POSE (Extrait → Question)"""
        extrait = Extrait(
            titre="Question posée",
            youtube_url="https://youtube.com/watch?v=q1",
            vimeo_url="https://vimeo.com/q1",
            duree=100,
        ).save()
        question = Question(texte="Quel est ton parcours ?").save()

        extrait.question.connect(question)
        connected = extrait.question.all()
        self.assertEqual(len(connected), 1)
        self.assertEqual(connected[0].texte, "Quel est ton parcours ?")

    def test_relation_tags(self):
        """Relation TAGS_EXTRAIT (Extrait → Tag)"""
        extrait = Extrait(
            titre="Extrait tagué",
            youtube_url="https://youtube.com/watch?v=tg1",
            vimeo_url="https://vimeo.com/tg1",
            duree=150,
        ).save()
        t1 = Tag(name="musique").save()
        t2 = Tag(name="interview").save()

        extrait.tags_extrait.connect(t1)
        extrait.tags_extrait.connect(t2)

        tags = [t.name for t in extrait.tags_extrait.all()]
        self.assertCountEqual(tags, ["musique", "interview"])

    def test_relation_interviews_with_position(self):
        """Relation APPARTIENT_A (Extrait → Interview) avec position"""
        extrait = Extrait(
            titre="Extrait interviewé",
            youtube_url="https://youtube.com/watch?v=int1",
            vimeo_url="https://vimeo.com/int1",
            duree=210,
        ).save()
        interview = Interview(titre="Interview de test").save()

        # Connect avec relation contenant la propriété position
        extrait.interviews.connect(interview, {"position": 3})

        rels = extrait.interviews.relationship(interview)
        self.assertIsNotNone(rels)
        self.assertEqual(rels.position, 3)

    def test_getters_and_properties(self):
        """Test des getters et des propriétés"""
        extrait = Extrait(
            titre="Getter test",
            youtube_url="https://youtube.com/watch?v=getter",
            vimeo_url="https://vimeo.com/getter",
            duree=300,
        ).save()
        props = extrait.__properties__
        self.assertIn("uuid", props)
        self.assertEqual(props["titre"], "Getter test")
        self.assertEqual(props["duree"], 300)
