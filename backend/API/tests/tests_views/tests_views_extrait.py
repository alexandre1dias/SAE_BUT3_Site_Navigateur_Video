from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

from ...errors import NotFound
from ...views import InterviewExtraitViewSet
from ...models import Extrait, Interview, Question, Tag, Artiste
from ...tests import Neo4jTestCase


class ExtraitViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        self.extrait1 = Extrait(
            titre="Extrait One",
            description="Description 1",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=120,
        ).save()
        self.extrait2 = Extrait(
            titre="Extrait Two",
            description="Description 2",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=90,
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name=f"Artiste test {uuid4()}").save()
        self.question = Question(texte=f"Question test {uuid4()}").save()

        self.extrait1.interviewer.connect(self.artiste)
        self.extrait2.interviewer.connect(self.artiste)

        self.extrait1.question.connect(self.question)
        self.extrait2.question.connect(self.question)

    def test_list_extraits(self):
        url = reverse("extrait-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(e["uuid"] == self.extrait1.uuid for e in response.json()))
        self.assertTrue(any(e["uuid"] == self.extrait2.uuid for e in response.json()))

    def test_search_extraits(self):
        url = reverse("extrait-list") + "?search=Two"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["uuid"], self.extrait2.uuid)

    def test_retrieve_extrait(self):
        url = reverse("extrait-detail", kwargs={"uuid": self.extrait1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.extrait1.uuid)

    def test_retrieve_nonexistent_extrait(self):
        url = reverse(
            "extrait-detail", kwargs={"uuid": "00000000-0000-0000-0000-000000000000"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class QuestionExtraitViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()
        self.question = Question(texte=f"Question {uuid4()}").save()

        self.extrait1 = Extrait(
            titre=f"Réponse à la question {uuid4()}",
            description="Desc 1",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=150,
        ).save()
        # <-- ici : titre sans le mot "Réponse" pour rendre la recherche univoque
        self.extrait2 = Extrait(
            titre=f"Autre sujet intéressant {uuid4()}",
            description="Desc 2",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=200,
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name=f"Artiste test {uuid4()}").save()
        self.question = Question(texte=f"Question test {uuid4()}").save()

        self.extrait1.interviewer.connect(self.artiste)
        self.extrait2.interviewer.connect(self.artiste)

        self.extrait1.question.connect(self.question)
        self.extrait2.question.connect(self.question)

    def test_list_extraits_by_question(self):
        url = reverse("extrait-list", kwargs={"question_uuid": self.question.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(e["uuid"] == self.extrait1.uuid for e in response.json()))
        self.assertTrue(any(e["uuid"] == self.extrait2.uuid for e in response.json()))

    def test_search_extraits_by_question(self):
        url = (
            reverse("extrait-list", kwargs={"question_uuid": self.question.uuid})
            + "?search=Réponse"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["uuid"], self.extrait1.uuid)

    def test_retrieve_extrait_by_question(self):
        url = reverse(
            "extrait-detail",
            kwargs={"question_uuid": self.question.uuid, "uuid": self.extrait2.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.extrait2.uuid)

    def test_retrieve_nonexistent_extrait_by_question(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "question_uuid": self.question.uuid,
                "uuid": "00000000-0000-0000-0000-000000000000",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class InterviewExtraitViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        # Création d'une interview
        self.interview = Interview(
            titre="Interview Exemple",
            date=None,
            occasion="Occasion",
            description="Desc interview",
            lieu="Lieu",
        ).save()

        # Création de deux extraits liés à l'interview avec positions différentes
        self.extrait_pos2 = Extrait(
            titre="Extrait position 2",
            description="Desc 2",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=110,
        ).save()
        self.extrait_pos1 = Extrait(
            titre="Extrait position 1",
            description="Desc 1",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=95,
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name="Artiste test").save()
        self.question = Question(texte="Question test").save()

        self.extrait_pos1.interviewer.connect(self.artiste)
        self.extrait_pos2.interviewer.connect(self.artiste)

        self.extrait_pos1.question.connect(self.question)
        self.extrait_pos2.question.connect(self.question)

        # Connexions avec la relation APPARTIENT_A et position
        # On met extrait_pos2 en position 2 et extrait_pos1 en position 1
        self.extrait_pos2.interviews.connect(self.interview, {"position": 2})
        self.extrait_pos1.interviews.connect(self.interview, {"position": 1})

    def test_list_extraits_by_interview_ordered(self):
        url = reverse("extrait-list", kwargs={"interview_uuid": self.interview.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Vérifie que les deux extraits sont présents
        self.assertTrue(any(e["uuid"] == self.extrait_pos1.uuid for e in data))
        self.assertTrue(any(e["uuid"] == self.extrait_pos2.uuid for e in data))
        # Vérifie l'ordre par position (position 1 doit apparaître avant position 2)
        self.assertGreaterEqual(len(data), 2)
        self.assertEqual(data[0]["uuid"], self.extrait_pos2.uuid)
        self.assertEqual(data[1]["uuid"], self.extrait_pos1.uuid)

    def test_retrieve_extrait_by_interview(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "interview_uuid": self.interview.uuid,
                "uuid": self.extrait_pos2.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.extrait_pos2.uuid)

    def test_retrieve_nonexistent_extrait_by_interview(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "interview_uuid": self.interview.uuid,
                "uuid": "00000000-0000-0000-0000-000000000000",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_interview_not_found_raises_NotFound(self):
        url = reverse(
            "extrait-list",
            kwargs={
                "interview_uuid": str(uuid4()),
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagExtraitViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        # Création d'un tag
        self.tag = Tag(name=f"Tag_{uuid4()}").save()

        # Création de deux extraits, seul l'un d'eux aura le tag recherché
        self.extrait_tagged = Extrait(
            titre="Extrait tagué",
            description="Desc tagué",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=80,
        ).save()
        self.extrait_untagged = Extrait(
            titre="Extrait non tagué",
            description="Desc non tagué",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=70,
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name="Artiste test").save()
        self.question = Question(texte="Question test").save()

        self.extrait_tagged.interviewer.connect(self.artiste)
        self.extrait_untagged.interviewer.connect(self.artiste)

        self.extrait_tagged.question.connect(self.question)
        self.extrait_untagged.question.connect(self.question)

        # Connexion du tag uniquement sur extrait_tagged
        self.extrait_tagged.tags_extrait.connect(self.tag)

    def test_list_extraits_by_tag(self):
        url = reverse("extrait-list", kwargs={"tag_uuid": self.tag.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [e["uuid"] for e in response.json()]
        self.assertIn(self.extrait_tagged.uuid, uuids)
        self.assertNotIn(self.extrait_untagged.uuid, uuids)

    def test_retrieve_extrait_by_tag(self):
        url = reverse(
            "extrait-detail",
            kwargs={"tag_uuid": self.tag.uuid, "uuid": self.extrait_tagged.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.extrait_tagged.uuid)

    def test_retrieve_nonexistent_extrait_by_tag(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "tag_uuid": self.tag.uuid,
                "uuid": "00000000-0000-0000-0000-000000000000",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ArtisteExtraitViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        # Création d'un artiste
        self.artiste = Artiste(name=f"Artiste_{uuid4()}", info="info").save()

        # Création de deux extraits, seul l'un d'eux aura la relation PARTICIPER vers l'artiste
        self.extrait_with_artist = Extrait(
            titre=f"Extrait avec artiste {uuid4()}",
            description="Desc artiste",
            youtube_url=f"https://youtu.be/{uuid4()}",
            vimeo_url=f"https://vimeo.com/{uuid4()}",
            duree=140,
        ).save()

        # Création d'artiste et question
        self.artiste = Artiste(name=f"Artiste test {uuid4()}").save()
        self.question = Question(texte=f"Question test {uuid4()}").save()

        self.extrait_with_artist.interviewer.connect(self.artiste)
        self.extrait_with_artist.question.connect(self.question)

    def test_retrieve_extrait_by_artiste(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "artiste_uuid": self.artiste.uuid,
                "uuid": self.extrait_with_artist.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.extrait_with_artist.uuid)

    def test_retrieve_nonexistent_extrait_by_artiste(self):
        url = reverse(
            "extrait-detail",
            kwargs={
                "artiste_uuid": self.artiste.uuid,
                "uuid": "00000000-0000-0000-0000-000000000000",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
