from datetime import date
from uuid import uuid4
from django.test import RequestFactory

from ...serializers import ExtraitSerializer
from ...errors import ValidatorUnique, NotFound
from ...models import Extrait, Artiste, Question, Interview, Tag
from ...tests import Neo4jTestCase


class ExtraitSerializerTests(Neo4jTestCase):
    """
    Tests unitaires du serializer ExtraitSerializer
    avec youtube_url et vimeo_url stockant uniquement le code
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/api/")

    # --- Initialisation ---
    def test_init_without_interview_removes_position_field(self):
        serializer = ExtraitSerializer(context={"request": self.request})
        self.assertNotIn("position", serializer.fields)

    def test_init_with_interview_keeps_position_field(self):
        interview = Interview(titre="I1", date=date(2024, 1, 1)).save()
        serializer = ExtraitSerializer(
            context={"request": self.request, "interview": interview}
        )
        self.assertIn("position", serializer.fields)

    # --- Méthodes de lecture ---
    def test_get_artiste_question_interviews_tags_urls(self):
        artiste = Artiste(name="Artiste1").save()
        question = Question(texte="Quel est ton nom ?").save()
        extrait = Extrait(
            titre="Exemple",
            youtube_url="yt1",  # code seul
            vimeo_url="vm1",  # code seul
            duree=42,
        ).save()
        extrait.interviewer.connect(artiste)
        extrait.question.connect(question)
        tag = Tag(name="tag1").save()
        extrait.tags_extrait.connect(tag)

        serializer = ExtraitSerializer(extrait, context={"request": self.request})
        data = serializer.data

        self.assertIn(str(artiste.uuid), data["artiste"])
        self.assertIn(str(question.uuid), data["question"])
        self.assertIn(str(extrait.uuid), data["interviews"])
        self.assertIn(str(extrait.uuid), data["tags"])

    def test_get_position_returns_correct_value(self):
        extrait = Extrait(
            titre="PosTest", youtube_url="ytpos", vimeo_url="vmpos", duree=10
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name=f"Artiste test {uuid4()}").save()
        self.question = Question(texte=f"Question test {uuid4()}").save()

        extrait.interviewer.connect(self.artiste)
        extrait.question.connect(self.question)

        interview = Interview(titre="InterviewPos", date=date(2024, 2, 2)).save()
        extrait.interviews.connect(interview, {"position": 7})

        serializer = ExtraitSerializer(
            extrait, context={"request": self.request, "interview": interview}
        )
        data = serializer.data
        self.assertEqual(data["position"], 7)

    # --- Création ---
    def test_create_success_with_relations(self):
        artiste = Artiste(name="CreateArtist").save()
        question = Question(texte="CreateQ").save()
        payload = {
            "titre": "C1",
            "youtube_url": "yt1",  # code seul
            "vimeo_url": "vm1",  # code seul
            "duree": 123,
            "artiste_uuid": artiste.uuid,
            "question_uuid": question.uuid,
        }
        serializer = ExtraitSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        extrait = serializer.save()

        reloaded = Extrait.nodes.get(uuid=extrait.uuid)
        self.assertEqual(reloaded.titre, "C1")
        self.assertEqual(reloaded.youtube_url, "yt1")
        self.assertEqual(reloaded.vimeo_url, "vm1")
        self.assertEqual([a.name for a in reloaded.interviewer.all()], ["CreateArtist"])
        self.assertEqual([q.texte for q in reloaded.question.all()], ["CreateQ"])

    def test_create_with_nonexistent_question_artiste_raises_notfound(self):
        payload = {
            "titre": "NoQ",
            "youtube_url": "ytq",
            "vimeo_url": "vmq",
            "duree": 11,
            "question_uuid": "00000000-0000-0000-0000-000000000000",
            "artiste_uuid": "00000000-0000-0000-0000-000000000000",
        }
        serializer = ExtraitSerializer(data=payload, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    # --- Mise à jour ---
    def test_update_success_updates_fields_and_relations(self):
        artiste_old = Artiste(name="OldA").save()
        artiste_new = Artiste(name="NewA").save()
        q_old = Question(texte="Qold").save()
        q_new = Question(texte="Qnew").save()

        extrait = Extrait(
            titre="UpdateMe", youtube_url="ytold", vimeo_url="vmold", duree=30
        ).save()
        extrait.interviewer.connect(artiste_old)
        extrait.question.connect(q_old)

        payload = {
            "titre": "Updated",
            "youtube_url": "ytnew",
            "vimeo_url": "vmnew",
            "duree": 99,
            "lieu": "Paris",
            "artiste_uuid": artiste_new.uuid,
        }
        serializer = ExtraitSerializer(
            instance=extrait, data=payload, context={"request": self.request}, partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        ex = Extrait.nodes.get(uuid=updated.uuid)
        self.assertEqual(ex.titre, "Updated")
        self.assertEqual(ex.youtube_url, "ytnew")
        self.assertEqual(ex.vimeo_url, "vmnew")
        self.assertEqual(ex.duree, 99)
        self.assertEqual(ex.lieu, "Paris")
        self.assertEqual([a.name for a in ex.interviewer.all()], ["NewA"])

    def test_update_with_nonexistent_question_raises_notfound(self):
        extrait = Extrait(
            titre="UpdQFail", youtube_url="ytqfail", vimeo_url="vmqfail", duree=20
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name=f"Artiste test {uuid4()}").save()
        self.question = Question(texte=f"Question test {uuid4()}").save()

        extrait.interviewer.connect(self.artiste)
        extrait.question.connect(self.question)

        payload = {"question_uuid": "00000000-0000-0000-0000-000000000000"}
        serializer = ExtraitSerializer(
            instance=extrait,
            data=payload,
            context={"request": self.request},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    def test_update_with_nonexistent_artiste_raises_notfound(self):
        extrait = Extrait(
            titre="UpdAFail", youtube_url="ytafail", vimeo_url="vmafail", duree=25
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name=f"Artiste test {uuid4()}").save()
        self.question = Question(texte=f"Question test {uuid4()}").save()

        extrait.interviewer.connect(self.artiste)
        extrait.question.connect(self.question)

        payload = {"artiste_uuid": "00000000-0000-0000-0000-000000000000"}
        serializer = ExtraitSerializer(
            instance=extrait,
            data=payload,
            context={"request": self.request},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        with self.assertRaises(NotFound):
            serializer.save()

    def test_update_disconnect_question_ignores_when_none(self):
        # Crée un extrait sans relation question
        question = Question(texte="Question test").save()
        extrait = Extrait(
            titre="NoQuestion", youtube_url="ytx", vimeo_url="vmx", duree=15
        ).save()
        extrait.question.connect(question)

        # Fournit un nouveau question_uuid → doit connecter sans erreur
        new_question = Question(texte="Qnew").save()
        payload = {"question_uuid": new_question.uuid}
        serializer = ExtraitSerializer(
            instance=extrait,
            data=payload,
            context={"request": self.request},
            partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)

        # Vérifie que l'update réussit même si la relation à déconnecter n'existait pas
        updated = serializer.save()
        qs = [q.texte for q in updated.question.all()]
        self.assertEqual(qs, ["Qnew"])
