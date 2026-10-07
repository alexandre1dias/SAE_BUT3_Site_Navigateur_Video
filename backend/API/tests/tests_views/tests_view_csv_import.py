"""Tests unitaires pour la vue d'import CSV (`CSVImportView`).

Les tests couvrent:
- la validation d'entrée du endpoint POST (fichier absent, mauvais format,
    en-têtes manquants/extra);
- le déclenchement du job en arrière-plan pour un CSV valide;
- le comportement des méthodes internes `save_data`, `save_row` et
    `save_interview` à l'aide de mocks.
"""

import io
from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

from ...serializers.extrait import Extrait
from ...models import Utilisateur
from ...views.csv_import import CSVImportView
from ...tests import Neo4jTestCase



class TestCSVImportView(Neo4jTestCase):

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.url = reverse("csv_import")
        
        # Create an admin user
        self.admin_user = Utilisateur(
            pseudo=f"admin_{uuid4()}",
            prenom="Admin",
            nom="Test",
            email=f"admin_{uuid4()}@test.com",
            password="password123",
            is_admin=True,
        ).save()
        
        # Authenticate the client with the admin user
        self.client.force_authenticate(user=self.admin_user)

    # =========================
    # POST endpoint
    # =========================

    def test_no_file_sent(self):
        response = self.client.post(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Aucun fichier envoyé"

    def test_wrong_file_extension(self):
        fake_file = io.BytesIO(b"not a csv")
        fake_file.name = "test.txt"

        response = self.client.post(
            self.url, {"file": fake_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Le fichier doit être un CSV"


    def test_empty_csv_file(self):
        csv_file = io.BytesIO(b"")
        csv_file.name = "empty.csv"

        response = self.client.post(
            self.url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "CSV vide"


    def test_csv_missing_headers(self):
        csv_content = "Artiste,Question,Date\nTest,Q?,2024-01-01"
        csv_file = io.BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "bad.csv"

        response = self.client.post(
            self.url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "missing" in response.data


    def test_csv_extra_headers(self):
        csv_content = (
            "Artiste,Position,Question,Audios,Tags,Origine,Date,"
            "Evenement,Ville,Youtube,Vimeo,Auteur,Extra\n"
            "Test,1,Q?,a.mp3,tag,FR,2024-01-01,Event,Paris,,,X"
        )

        csv_file = io.BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "bad.csv"

        response = self.client.post(
            self.url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "extra" in response.data


    @patch("API.views.csv_import.CSVImportView.run_import")
    def test_valid_csv_file(self, mock_run_import):
        csv_content = (
            "Ville,Artiste,Auteur,Date,Evenement,Position,Question,"
            "Audios,Tags,Origine,Youtube,Vimeo\n"
            "Paris,Test,Me,2024-01-01,Event,1,Q?,a.mp3,tag,FR,,"
        )

        csv_file = io.BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "test.csv"

        response = self.client.post(
            self.url, {"file": csv_file}, format="multipart"
        )

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert "Import CSV lancé" in response.data["message"]
        assert "job_id" in response.data

        mock_run_import.assert_called_once()




    # =========================
    # save_data
    # =========================

    def test_save_data(self):
        view = CSVImportView()

        csv_content = (
            "Ville,Artiste,Auteur,Date,Evenement,Position,Question,Audios,Tags,Origine,Youtube,Vimeo\n"
            "Paris,Artist1,Author1,2020-01-01,Event1,1,Q1,audio1,tag1,FR,,\n"
            "Paris,Artist1,Author2,2020-01-02,Event1,2,Q2,audio2,tag2,FR,,\n"
            "Paris,Artist1,Author3,2020-01-03,Event2,3,Q3,audio3,tag3,FR,,\n"
        )

        csv_file = io.BytesIO(csv_content.encode("utf-8"))
        csv_file.name = "test.csv"

        with patch.object(view, "save_row", return_value="EXTRAIT") as mock_save_row, \
             patch.object(view, "save_interview") as mock_save_interview:

            view.save_data(csv_file)

            assert mock_save_row.call_count == 3
            assert mock_save_interview.call_count == 2


    # =========================
    # save_row
    # =========================

    @patch("API.views.csv_import.TagsExtraitRelationShipSerializer")
    @patch("API.views.csv_import.AudiosSerializer")
    @patch("API.views.csv_import.ExtraitSerializer.create")
    @patch("API.views.csv_import.AudioSerializer.create")
    @patch("API.views.csv_import.TagSerializer.create")
    @patch("API.views.csv_import.OccasionSerializer.create")
    @patch("API.views.csv_import.QuestionSerializer.create")
    @patch("API.views.csv_import.ArtisteSerializer.create")
    def test_save_row_creates_extrait(
        self,
        mock_artiste_create,
        mock_question_create,
        mock_occasion_create,
        mock_tag_create,
        mock_audio_create,
        mock_extrait_create,
        mock_audios_rel_serializer,
        mock_tags_rel_serializer,
    ):
        view = CSVImportView()

        # objets retournés avec uuid
        mock_artiste_create.return_value = Mock(uuid="artiste-uuid")
        mock_question_create.return_value = Mock(uuid="question-uuid")
        mock_occasion_create.return_value = Mock(uuid="occasion-uuid")
        mock_tag_create.return_value = Mock(uuid="tag-uuid")
        mock_audio_create.return_value = Mock(uuid="audio-uuid")

        mock_extrait_create.return_value = Mock(uuid="extrait-uuid")

        # serializers de relation : no-op
        mock_rel_instance = Mock()
        mock_rel_instance.is_valid.return_value = True
        mock_rel_instance.create.return_value = None

        mock_audios_rel_serializer.return_value = mock_rel_instance
        mock_tags_rel_serializer.return_value = mock_rel_instance

        row = {
            "Artiste": "Daft Punk",
            "Question": "Pourquoi la musique ?",
            "Evenement": "Interview 2020",
            "Tags": "electro; robots",
            "Audios": "audio1",
            "Youtube": "https://youtu.be/abcd1234",
            "Vimeo": "",
            "Date": "2020-01-01",
            "Ville": "Paris",
            "Position": "1",
        }

        extrait = view.save_row(row)

        assert extrait is not None
        mock_extrait_create.assert_called_once()

        # Vérifie que les relations ont été créées
        mock_artiste_create.assert_called_once_with({"name": "Daft Punk"})
        mock_question_create.assert_called_once_with({"texte": "Pourquoi la musique ?"})
        mock_tag_create.assert_any_call({"name": "electro"})
        mock_tag_create.assert_any_call({"name": "robots"})
        mock_audio_create.assert_called_once()


    @patch("API.views.csv_import.TagsExtraitRelationShipSerializer")
    @patch("API.views.csv_import.AudiosSerializer")
    @patch("API.views.csv_import.Tag")
    @patch("API.views.csv_import.Audio")
    @patch("API.views.csv_import.Extrait")
    @patch("API.views.csv_import.TagSerializer")
    @patch("API.views.csv_import.AudioSerializer")
    @patch("API.views.csv_import.ArtisteSerializer")
    @patch("API.views.csv_import.QuestionSerializer")
    @patch("API.views.csv_import.ExtraitSerializer")
    def test_save_row_update_extrait(
        self,
        mock_extrait_serializer,
        mock_question_serializer,
        mock_artiste_serializer,
        mock_audio_serializer,
        mock_tag_serializer,
        mock_extrait_class,
        mock_audio_class,
        mock_tag_class,
        mock_audios_serializer_class,
        mock_tags_serializer_class,
    ):
        view = CSVImportView()

        # --- Mock de l'extrait existant pour UPDATE ---
        mock_existing_extrait = Mock()
        mock_existing_extrait.titre = ""
        mock_existing_extrait.artiste_uuid = None
        mock_existing_extrait.question_uuid = None
        mock_existing_extrait.youtube_url = None
        mock_existing_extrait.vimeo_url = None
        mock_existing_extrait.position = None
        mock_existing_extrait.lieu = None
        mock_existing_extrait.uploaded_at = None
        mock_existing_extrait.save = Mock()

        # Mock de Extrait.nodes.get
        def mock_nodes_get_side_effect(**kwargs):
            if "youtube_url" in kwargs and kwargs["youtube_url"]:
                return mock_existing_extrait
            if "vimeo_url" in kwargs and kwargs["vimeo_url"]:
                return mock_existing_extrait
            raise Extrait.DoesNotExist()

        mock_extrait_class.nodes.get.side_effect = mock_nodes_get_side_effect
        mock_extrait_class.DoesNotExist = Extrait.DoesNotExist

        # --- Mock Artiste et Question ---
        artiste_instance = Mock(uuid="artiste-uuid")
        question_instance = Mock(uuid="question-uuid")
        mock_artiste_serializer.return_value.create.return_value = artiste_instance
        mock_question_serializer.return_value.create.return_value = question_instance

        # --- Mock Audio et Tag pour forcer l'utilisation de nodes.get (except block) ---
        audio_instance = Mock(uuid="audio-uuid")
        tag_instance1 = Mock(uuid="tag-uuid-1")
        tag_instance2 = Mock(uuid="tag-uuid-2")
        
        # AudioSerializer.create lance une exception pour forcer le except
        mock_audio_serializer.return_value.create.side_effect = Exception("Already exists")
        mock_audio_class.nodes.get.return_value = audio_instance
        
        # TagSerializer.create lance une exception pour forcer le except
        mock_tag_serializer.return_value.create.side_effect = Exception("Already exists")
        mock_tag_class.nodes.get.side_effect = [tag_instance1, tag_instance2]

        # --- Mock des serializers de relation ---
        delete_calls = []
        create_calls = []

        def make_audio_serializer_instance(*args, **kwargs):
            instance = Mock()
            instance.is_valid.return_value = True
            instance.delete = Mock(side_effect=lambda uuid: delete_calls.append(('audio', uuid)))
            instance.create = Mock(side_effect=lambda data: create_calls.append(('audio', data)))
            return instance

        def make_tags_serializer_instance(*args, **kwargs):
            instance = Mock()
            instance.is_valid.return_value = True
            instance.delete = Mock(side_effect=lambda uuid: delete_calls.append(('tag', uuid)))
            instance.create = Mock(side_effect=lambda data: create_calls.append(('tag', data)))
            return instance

        mock_audios_serializer_class.side_effect = make_audio_serializer_instance
        mock_tags_serializer_class.side_effect = make_tags_serializer_instance

        # --- Ligne CSV simulée ---
        row = {
            "Artiste": "Daft Punk",
            "Question": "Pourquoi la musique ?",
            "Evenement": "Interview 2020",
            "Tags": "electro; robots",
            "Audios": "audio1",
            "Youtube": "https://youtu.be/abcd1234",
            "Vimeo": "",
            "Date": "2020-01-01",
            "Ville": "Paris",
            "Position": "1",
        }

        # --- Appel de save_row ---
        extrait = view.save_row(row)

        # Vérifie que c'est bien l'objet existant qui a été mis à jour
        assert extrait is mock_existing_extrait

        # Vérifie que save() a été appelé
        mock_existing_extrait.save.assert_called_once()

        # Vérifie que les champs ont été mis à jour
        assert mock_existing_extrait.titre == "Daft Punk - Interview 2020 - Pourquoi la musique ? - 2020-01-01"
        assert mock_existing_extrait.artiste_uuid == "artiste-uuid"
        assert mock_existing_extrait.question_uuid == "question-uuid"
        assert mock_existing_extrait.youtube_url == "abcd1234"
        assert mock_existing_extrait.vimeo_url == ""
        assert mock_existing_extrait.position == 1
        assert mock_existing_extrait.lieu == "Paris"

        # Now we should have 3 delete calls and 3 create calls (1 audio + 2 tags)
        assert len(delete_calls) == 3, f"Expected 3 delete calls, got {len(delete_calls)}: {delete_calls}"
        assert len(create_calls) == 3, f"Expected 3 create calls, got {len(create_calls)}: {create_calls}"
        
        # Vérifie les types
        audio_deletes = [call for call in delete_calls if call[0] == 'audio']
        tag_deletes = [call for call in delete_calls if call[0] == 'tag']
        assert len(audio_deletes) == 1
        assert len(tag_deletes) == 2



    # =========================
    # save_interview
    # =========================

    @patch("API.views.csv_import.InterviewsSerializer")
    @patch("API.views.csv_import.InterviewSerializer")
    @patch("API.views.csv_import.Occasion")
    def test_save_interview_creates_interview(
        self,
        mock_occasion_class,
        mock_interview_serializer_class,
        mock_interviews_serializer_class,
    ):
        view = CSVImportView()

        fake_artiste = Mock()
        fake_artiste.name = "Artist"  # Définir explicitement l'attribut name
        
        fake_occasion = Mock()
        fake_occasion.name = "Event"  # Définir explicitement l'attribut name
        fake_occasion.uuid = "uuid-event"
        
        fake_extrait = Mock(
            uploaded_at="2020-01-01",
            position=1,
            interviewer=Mock(single=lambda: fake_artiste),
        )

        # Mock Occasion.nodes.get
        mock_occasion_class.nodes.get.return_value = fake_occasion

        mock_interview_node = Mock(uuid="uuid-interview")
        mock_interview_serializer = Mock()
        mock_interview_serializer.create.return_value = mock_interview_node
        mock_interview_serializer_class.return_value = mock_interview_serializer

        mock_interviews_instance = Mock()
        mock_interviews_instance.is_valid.return_value = True
        mock_interviews_serializer_class.return_value = mock_interviews_instance

        view.save_interview([fake_extrait], "Event")

        # Vérifie que l'interview a été créée
        mock_interview_serializer.create.assert_called_once_with({
            "titre": "Interview de Artist pour Event",
            "date": "2020-01-01",
            "description": "",
            "occasion_uuid": "uuid-event",
        })

        # Vérifie que la relation extrait-interview a été créée
        self.assertEqual(mock_interviews_serializer_class.call_count, 1)
        mock_interviews_instance.is_valid.assert_called_once()
        mock_interviews_instance.create.assert_called_once()


    @patch("API.views.csv_import.InterviewsSerializer")
    @patch("API.views.csv_import.InterviewSerializer")
    @patch("API.views.csv_import.Occasion")
    def test_save_interview_no_occasion(
        self,
        mock_occasion_class,
        mock_interview_serializer_class,
        mock_interviews_serializer_class,
    ):
        """Test save_interview quand l'occasion est une chaîne vide"""
        view = CSVImportView()

        fake_artiste = Mock()
        fake_artiste.name = "Artist"
        
        fake_extrait = Mock(
            uploaded_at="2020-01-01",
            position=1,
            interviewer=Mock(single=lambda: fake_artiste),
        )

        mock_interview_node = Mock(uuid="uuid-interview")
        mock_interview_serializer = Mock()
        mock_interview_serializer.create.return_value = mock_interview_node
        mock_interview_serializer_class.return_value = mock_interview_serializer

        mock_interviews_instance = Mock()
        mock_interviews_instance.is_valid.return_value = True
        mock_interviews_serializer_class.return_value = mock_interviews_instance

        # Passer une chaîne vide pour occasion (le code ne cherchera pas l'occasion)
        view.save_interview([fake_extrait], "")

        # Vérifie que l'interview a quand même été créée avec occasion_uuid=None
        mock_interview_serializer.create.assert_called_once()
        call_args = mock_interview_serializer.create.call_args[0][0]
        self.assertIsNone(call_args["occasion_uuid"])
        self.assertIn("une occasion inconnue", call_args["titre"])
        
        # Vérifie que Occasion.nodes.get n'a PAS été appelé
        mock_occasion_class.nodes.get.assert_not_called()


    @patch("API.views.csv_import.InterviewsSerializer")
    @patch("API.views.csv_import.InterviewSerializer")
    @patch("API.views.csv_import.Occasion")
    def test_save_interview_multiple_extraits(
        self,
        mock_occasion_class,
        mock_interview_serializer_class,
        mock_interviews_serializer_class,
    ):
        """Test save_interview avec plusieurs extraits"""
        view = CSVImportView()

        fake_artiste = Mock()
        fake_artiste.name = "Artist"
        
        fake_occasion = Mock()
        fake_occasion.name = "Event"
        fake_occasion.uuid = "uuid-event"
        
        fake_extrait1 = Mock(
            uploaded_at="2020-01-01",
            position=1,
            interviewer=Mock(single=lambda: fake_artiste),
        )
        fake_extrait2 = Mock(
            uploaded_at="2020-01-01",
            position=2,
            interviewer=Mock(single=lambda: fake_artiste),
        )
        fake_extrait3 = Mock(
            uploaded_at="2020-01-01",
            position=3,
            interviewer=Mock(single=lambda: fake_artiste),
        )

        # Mock Occasion.nodes.get
        mock_occasion_class.nodes.get.return_value = fake_occasion

        mock_interview_node = Mock(uuid="uuid-interview")
        mock_interview_serializer = Mock()
        mock_interview_serializer.create.return_value = mock_interview_node
        mock_interview_serializer_class.return_value = mock_interview_serializer

        mock_interviews_instance = Mock()
        mock_interviews_instance.is_valid.return_value = True
        mock_interviews_serializer_class.return_value = mock_interviews_instance

        view.save_interview([fake_extrait1, fake_extrait2, fake_extrait3], "Event")

        # Vérifie que l'interview a été créée une seule fois
        mock_interview_serializer.create.assert_called_once()

        # Vérifie que 3 relations ont été créées (une par extrait)
        self.assertEqual(mock_interviews_serializer_class.call_count, 3)
        self.assertEqual(mock_interviews_instance.create.call_count, 3)


    @patch("API.views.csv_import.InterviewsSerializer")
    @patch("API.views.csv_import.InterviewSerializer")
    @patch("API.views.csv_import.Occasion")
    def test_save_interview_handles_exception(
        self,
        mock_occasion_class,
        mock_interview_serializer_class,
        mock_interviews_serializer_class,
    ):
        """Test que save_interview gère les exceptions lors de la création"""
        view = CSVImportView()

        fake_artiste = Mock()
        fake_artiste.name = "Artist"
        
        fake_occasion = Mock()
        fake_occasion.name = "Event"
        fake_occasion.uuid = "uuid-event"
        
        fake_extrait = Mock(
            uploaded_at="2020-01-01",
            position=1,
            interviewer=Mock(single=lambda: fake_artiste),
        )

        # Mock Occasion.nodes.get
        mock_occasion_class.nodes.get.return_value = fake_occasion

        mock_interview_serializer = Mock()
        mock_interview_serializer.create.side_effect = Exception("Database error")
        mock_interview_serializer_class.return_value = mock_interview_serializer

        # Ne doit pas lever d'exception
        try:
            view.save_interview([fake_extrait], "Event")
        except Exception:
            self.fail("save_interview a levé une exception alors qu'elle devait la gérer.")

        # Vérifie que la tentative de création a été faite
        mock_interview_serializer.create.assert_called_once()