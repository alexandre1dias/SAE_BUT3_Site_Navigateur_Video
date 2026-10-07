from rest_framework.exceptions import APIException
from rest_framework import status


class ConnexionDB(APIException):
    """
    Erreur de connexion à la base de données
    Base de données indisponible

    Remplace le message d'erreur 500 d'erreur interne du serveur
    Donne plus d'informations sur l'erreur
    """

    def __init__(self):
        """
        Erreur de connexion à la base de données
        """
        super().__init__(
            {"DataBase Connexion Failed": "Retry After"},
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )  # pragma: no cover
        self.status_code = status.HTTP_503_SERVICE_UNAVAILABLE  # pragma: no cover
