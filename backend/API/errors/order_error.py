from rest_framework.exceptions import ValidationError


class OrderError(ValidationError):
    """
    Le champ avec lequel l'order a été éxécuté n'est pas correct

    Concernet tout les types d'erreur d'order
    Champ du node inexistant
    Trop de champs pour l'order (séparer par __ pour les champs de relationship)
    """

    def __init__(self, order: str):
        """
        Renvoie une erreur de validation avec un message d'erreur indiquant quel error d'order a été rencontré

        Args:
            order (str): erreur d'order rencontré
        """
        super().__init__({"Order error": order})
