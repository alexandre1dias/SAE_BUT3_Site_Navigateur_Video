from rest_framework.exceptions import ValidationError


class ValidatorUnique(ValidationError):
    """
    Erreur de validation du champ
    Une valeur déjà existante a été renseigné

    Utiliser pour les champs uniques des nodes à la place de l'erreur inexploitable de neomodel
    """

    def __init__(self, detail: str = ""):
        """
        Renvoie une erreur de validation avec un message d'erreur indiquant le champ qui a une valeur déjà existante

        Args:
            detail (str, optional): Nom du champ avec une valeur déjà existante. Defaults to "".
        """
        super().__init__({"Unique Property": detail})
