from rest_framework.exceptions import ValidationError


class ValidatorRequired(ValidationError):
    """
    Erreur, code status et message pour champ unique
    Tentative de création ou de mise à jour d'une ressource sans fournir un champ obligatoire
    """

    def __init__(self, detail: str = ""):
        """
        Renvoie une erreur de validation avec un message d'erreur indiquant le champ obligatoire qui n'a pas été fourni

        Args:
            detail (str, optional): Nom du champ obligatoire manquant. Defaults to "".
        """
        super().__init__({"Required Property": detail})
