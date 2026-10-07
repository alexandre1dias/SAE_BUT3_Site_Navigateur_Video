from rest_framework.exceptions import ValidationError
from neomodel import StructuredNode


class ContextError(ValidationError):
    """
    Erreur dans le context
    Node de context manquant

    Utiliser pour les vues qui ont besoin d'un node de context pour fonctionner (relationship viewset, sub base viewset)
    """

    def __init__(self, Class: StructuredNode = None):
        """
        Renvoie une erreur de validation avec un message d'erreur indiquant le node de context manquant

        Args:
            Class (StructuredNode, optional): Classe du node de context manquant. Defaults to None.
        """
        super().__init__(
            {"Context error": Class.__name__ if Class is not None else None}
        )
