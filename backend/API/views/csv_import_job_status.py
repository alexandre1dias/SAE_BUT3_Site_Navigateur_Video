"""Vue exposant le statut d'un job d'import CSV.

Ce module implémente `CSVImportJobStatusView` qui fournit un endpoint
en lecture seule retournant les champs `uuid`, `status` et `message`
d'un `CSVImportJob`. Le pattern d'URL est défini dans
`backend/API/urls.py` : `csv_import/status/<job_uuid>/`.

Le endpoint renvoie HTTP 404 lorsque le job est introuvable.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import CSVImportJob

class CSVImportJobStatusView(APIView):
    """Vue API retournant le statut et le message d'un job d'import CSV.

    Méthodes
    --------
    get(request, job_uuid)
        Retourne un objet JSON contenant `uuid`, `status` et `message` pour
        le job identifié par `job_uuid`. Renvoie HTTP 404 si le job n'existe pas.
    """

    def get(self, request, job_uuid, *args, **kwargs):
        try:
            job = CSVImportJob.nodes.get(uuid=job_uuid)
        except CSVImportJob.DoesNotExist:
            return Response({"error": "Job introuvable"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "uuid": job.uuid,
            "status": job.status,
            "message": job.message,
        })
