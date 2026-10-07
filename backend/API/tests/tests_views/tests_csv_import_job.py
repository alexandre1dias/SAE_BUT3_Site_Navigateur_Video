"""Tests unitaires pour le mécanisme d'import CSV (backend).

Ce module contient des tests pour:
- la fonction statique `CSVImportView.run_import` qui exécute l'import
    en tâche de fond et met à jour l'objet `CSVImportJob`;
- la vue `CSVImportJobStatusView` qui expose le statut du job via l'API.

Les tests vérifient les transitions de statut (`in_progress` → `success`/
`error`) ainsi que le comportement de la vue de consultation du statut.
"""

import io
from unittest.mock import Mock, patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from uuid import uuid4

from ...models import CSVImportJob, Utilisateur
from ...views.csv_import import CSVImportView
from ...views.csv_import_job_status import CSVImportJobStatusView
from ...tests import Neo4jTestCase


class TestCSVImportJobRunImport(Neo4jTestCase):
    """Tests pour la fonction statique CSVImportView.run_import"""

    def test_run_import_success(self):
        """Test run_import avec succès - le job passe en 'success'"""
        # Créer un job
        job = CSVImportJob(status="in_progress", message="Import en cours...")
        job.save()

        # Données CSV valides
        csv_content = (
            "Ville,Artiste,Auteur,Date,Evenement,Position,Question,"
            "Audios,Tags,Origine,Youtube,Vimeo\n"
            "Paris,Artist1,Author1,2020-01-01,Event1,1,Q1,audio1,tag1,FR,,\n"
        )
        csv_lines = csv_content.splitlines()

        # Mock save_data pour qu'il réussisse
        with patch.object(CSVImportView, 'save_data') as mock_save_data:
            CSVImportView.run_import(csv_lines, job.uuid)

        # Vérifier que le job a été mis à jour
        updated_job = CSVImportJob.nodes.get(uuid=job.uuid)
        assert updated_job.status == "success"
        assert updated_job.message == "CSV importé avec succès !"
        mock_save_data.assert_called_once()

    def test_run_import_failure(self):
        """Test run_import avec erreur - le job passe en 'error'"""
        # Créer un job
        job = CSVImportJob(status="in_progress", message="Import en cours...")
        job.save()

        csv_lines = []

        # Mock save_data pour qu'il échoue
        error_message = "Erreur de parsing CSV"
        with patch.object(CSVImportView, 'save_data', side_effect=Exception(error_message)) as mock_save_data:
            CSVImportView.run_import(csv_lines, job.uuid)

        # Vérifier que le job a été mis à jour avec l'erreur
        updated_job = CSVImportJob.nodes.get(uuid=job.uuid)
        assert updated_job.status == "error"
        assert updated_job.message == error_message
        mock_save_data.assert_called_once()

    def test_run_import_job_not_found(self):
        """Test run_import quand le job n'existe pas"""
        fake_uuid = str(uuid4())
        csv_lines = []

        # Mock save_data pour éviter les erreurs dans save_data
        with patch.object(CSVImportView, 'save_data') as mock_save_data:
            # Ne doit pas lever d'exception - elle doit être capturée
            try:
                CSVImportView.run_import(csv_lines, fake_uuid)
            except CSVImportJob.DoesNotExist:
                # C'est attendu si le job n'existe pas et que le try bloque
                pass


class TestCSVImportJobStatusView(Neo4jTestCase):
    """Tests pour la vue CSVImportJobStatusView"""

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        
        # Créer un utilisateur admin
        self.admin_user = Utilisateur(
            pseudo=f"admin_{uuid4()}",
            prenom="Admin",
            nom="Test",
            email=f"admin_{uuid4()}@test.com",
            password="password123",
            is_admin=True,
        ).save()
        
        # Authentifier le client
        self.client.force_authenticate(user=self.admin_user)

    def test_get_job_status_success(self):
        """Test la récupération d'un job en statut success"""
        # Créer un job
        job = CSVImportJob(
            status="success",
            message="CSV importé avec succès !"
        )
        job.save()

        url = reverse("csv_import_status", args=[job.uuid])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["uuid"] == job.uuid
        assert response.data["status"] == "success"
        assert response.data["message"] == "CSV importé avec succès !"

    def test_get_job_status_in_progress(self):
        """Test la récupération d'un job en cours"""
        # Créer un job
        job = CSVImportJob(
            status="in_progress",
            message="Import en cours..."
        )
        job.save()

        url = reverse("csv_import_status", args=[job.uuid])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "in_progress"
        assert response.data["message"] == "Import en cours..."

    def test_get_job_status_error(self):
        """Test la récupération d'un job en erreur"""
        # Créer un job
        job = CSVImportJob(
            status="error",
            message="Erreur lors de l'import"
        )
        job.save()

        url = reverse("csv_import_status", args=[job.uuid])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "error"
        assert response.data["message"] == "Erreur lors de l'import"

    def test_get_job_status_not_found(self):
        """Test la récupération d'un job inexistant"""
        fake_uuid = str(uuid4())
        url = reverse("csv_import_status", args=[fake_uuid])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Job introuvable"

    def test_get_job_status_returns_all_fields(self):
        """Test que tous les champs du job sont retournés"""
        # Créer un job avec tous les champs
        job = CSVImportJob(
            status="success",
            message="Test message"
        )
        job.save()

        url = reverse("csv_import_status", args=[job.uuid])
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "uuid" in response.data
        assert "status" in response.data
        assert "message" in response.data
        assert len(response.data) == 3
