from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Question, Theme
from ...tests import Neo4jTestCase


class QuestionViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.question1 = Question(texte=f"Question unique {uuid4()}").save()
        self.question2 = Question(texte=f"Question autre {uuid4()}").save()

        # Création theme
        self.theme = Theme(name=f"Theme test {uuid4()}").save()
        self.question1.theme.connect(self.theme)
        self.question2.theme.connect(self.theme)

    def test_list_questions(self):
        url = reverse("question-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(q["uuid"] == self.question1.uuid for q in response.json()))
        self.assertTrue(any(q["uuid"] == self.question2.uuid for q in response.json()))

    def test_search_questions(self):
        # recherche sur un mot contenu uniquement dans question2.texte
        term = self.question2.texte.split()[0]
        url = reverse("question-list") + f"?search={term}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        # Au moins une des questions doit correspondre ; on vérifie la présence de question2
        self.assertTrue(any(q["uuid"] == self.question2.uuid for q in data))

    def test_retrieve_question(self):
        url = reverse("question-detail", kwargs={"uuid": self.question1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.question1.uuid)

    def test_retrieve_nonexistent_question(self):
        url = reverse(
            "question-detail", kwargs={"uuid": "00000000-0000-0000-0000-000000000000"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ThemeQuestionViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        # Création d'un thème
        self.theme = Theme(
            name=f"Theme_{uuid4()}", description="Description thème"
        ).save()

        # Création de deux questions, seule l'une d'elles sera liée au thème
        self.question_linked = Question(texte="Question liée au thème").save()
        self.question_unlinked = Question(texte="Question non liée").save()

        # Liaison de question_linked au thème
        self.question_linked.theme.connect(self.theme)

    def test_list_questions_by_theme(self):
        url = reverse("question-list", kwargs={"theme_uuid": self.theme.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [q["uuid"] for q in response.json()]
        self.assertIn(self.question_linked.uuid, uuids)
        self.assertNotIn(self.question_unlinked.uuid, uuids)

    def test_retrieve_question_by_theme(self):
        url = reverse(
            "question-detail",
            kwargs={"theme_uuid": self.theme.uuid, "uuid": self.question_linked.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.question_linked.uuid)

    def test_retrieve_nonexistent_question_by_theme(self):
        url = reverse(
            "question-detail",
            kwargs={
                "theme_uuid": self.theme.uuid,
                "uuid": "00000000-0000-0000-0000-000000000000",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
