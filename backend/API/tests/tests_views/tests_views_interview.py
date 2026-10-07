from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4
from ...models import Interview, Tag
from ...tests import Neo4jTestCase


class InterviewViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        self.interview1 = Interview(
            titre="Interview One",
            date=None,
            occasion="Occ1",
            description="Desc 1",
            lieu="Lieu 1",
        ).save()
        self.interview2 = Interview(
            titre="Interview Two",
            date=None,
            occasion="Occ2",
            description="Desc 2",
            lieu="Lieu 2",
        ).save()

    def test_list_interviews(self):
        url = reverse("interview-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(i["uuid"] == self.interview1.uuid for i in response.json()))
        self.assertTrue(any(i["uuid"] == self.interview2.uuid for i in response.json()))

    def test_search_interviews(self):
        url = reverse("interview-list") + "?search=Two"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["uuid"], self.interview2.uuid)

    def test_retrieve_interview(self):
        url = reverse("interview-detail", kwargs={"uuid": self.interview1.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.interview1.uuid)

    def test_retrieve_nonexistent_interview(self):
        url = reverse(
            "interview-detail", kwargs={"uuid": "00000000-0000-0000-0000-000000000000"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TagInterviewViewSetAPITests(Neo4jTestCase):
    def setUp(self):
        self.client = APIClient()

        # Création d'un tag
        self.tag = Tag(name=f"Tag_{uuid4()}").save()

        # Création de deux interviews, seul l'un d'eux aura le tag
        self.interview_tagged = Interview(
            titre="Interview tagged",
            date=None,
            occasion="Occ",
            description="Desc tagged",
            lieu="Lieu",
        ).save()
        self.interview_untagged = Interview(
            titre="Interview not tagged",
            date=None,
            occasion="Occ",
            description="Desc not tagged",
            lieu="Lieu",
        ).save()

        # Connexion du tag uniquement sur interview_tagged
        self.interview_tagged.tags_interview.connect(self.tag)

    def test_list_interviews_by_tag(self):
        url = reverse("interview-list", kwargs={"tag_uuid": self.tag.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        uuids = [i["uuid"] for i in response.json()]
        self.assertIn(self.interview_tagged.uuid, uuids)
        self.assertNotIn(self.interview_untagged.uuid, uuids)

    def test_retrieve_interview_by_tag(self):
        url = reverse(
            "interview-detail",
            kwargs={"tag_uuid": self.tag.uuid, "uuid": self.interview_tagged.uuid},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["uuid"], self.interview_tagged.uuid)

    def test_retrieve_nonexistent_interview_by_tag(self):
        url = reverse(
            "interview-detail",
            kwargs={
                "tag_uuid": self.tag.uuid,
                "uuid": "00000000-0000-0000-0000-000000000000",
            },
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
