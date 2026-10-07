from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Question, Theme, Utilisateur
from ...tests import Neo4jTestCase


class RecherchesQuestionsViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.user = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom1",
            nom="Nom1",
            email=f"user1_{uuid4()}@example.com",
            password=make_password("password"),
            is_admin=True
        ).save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Création d'un utilisateur
        self.utilisateur = Utilisateur(
            pseudo=f"pseudo_{uuid4()}",
            prenom="Prenom",
            nom="Nom",
            email=f"user_{uuid4()}@example.com",
            password="password",
        ).save()

        # Création de deux questions
        self.question1 = Question(texte=f"Question_{uuid4()}").save()
        self.question2 = Question(texte=f"Question_{uuid4()}").save()

        # Création theme
        self.theme = Theme(name=f"Theme test {uuid4()}").save()
        self.question1.theme.connect(self.theme)
        self.question2.theme.connect(self.theme)

        # Connecter seulement question1 comme recherchée par l'utilisateur
        self.utilisateur.recherches_questions.connect(self.question1)

    def test_list_recherches_questions(self):
        url = reverse(
            "question-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [q["uuid"] for q in response.json()]
        self.assertIn(self.question1.uuid, uuids)
        self.assertNotIn(self.question2.uuid, uuids)

    def test_retrieve_recherches_question(self):
        url = reverse(
            "question-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.question1.uuid,
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.question1.uuid)

    def test_retrieve_nonexistent_recherches_question_raises_notfound(self):
        """
        Teste la branche `if not results: raise NotFound(Question)`
        """
        url = reverse(
            "question-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.question2.uuid,  # question2 n'est pas connectée
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_utilisateur_not_found(self):
        url = reverse("question-list", kwargs={"utilisateur_uuid": str(uuid4())})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recherches_questions_relation(self):
        url = reverse(
            "question-list", kwargs={"utilisateur_uuid": self.utilisateur.uuid}
        )
        payload = {"uuid": self.question2.uuid}
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que la relation a été créée
        self.assertTrue(
            self.utilisateur.recherches_questions.is_connected(self.question2)
        )

    def test_destroy_recherches_questions_relation(self):
        url = reverse(
            "question-detail",
            kwargs={
                "utilisateur_uuid": self.utilisateur.uuid,
                "uuid": self.question1.uuid,
            },
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Vérifie que la relation a été supprimée
        self.assertFalse(
            self.utilisateur.recherches_questions.is_connected(self.question1)
        )
