from rest_framework.exceptions import NotFound as nf
from neomodel import StructuredNode


class NotFound(nf):
    """
    L'instance de Node n'a pas été trouvé avec l'uuid fourni
    Plus d'informations sur l'erreur que le message d'erreur 404 de base
    """

    def __init__(self, Class: StructuredNode = None):
        """
        Renvoie une erreur avec le message d'erreur indiquant le node qui n'a pas été trouvé

        Args:
            Class (StructuredNode, optional): Classe du node non trouvé. Defaults to None.
        """
        super().__init__({"Not Found": Class.__name__ if Class is not None else None})
