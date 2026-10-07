from datetime import datetime
from rest_framework import serializers
from neomodel import RelationshipManager, db, StructuredRel, RelationshipTo
from ...models import DateHeureRel, Utilisateur, Artiste, Question, Extrait, Interview
from ...errors import ContextError
from . import BaseRelationShipSerializer


class RelationShipUtilisateurSerializer(BaseRelationShipSerializer):
    """
    Classe de base contenant les méthodes pour la gestion des relations concernant les utilisateurs

    Gestion des artistes, questions, extraits ou interviews liés à un utilisateur

    Champs aditionnels :
        Champs en read_only :
            - date_heure : date de la relationship

    Raises:
        ContextError: node de context manquant
    """

    # Outputs
    date_heure = serializers.SerializerMethodField(read_only=True)

    def __init__(
        self,
        node: Artiste | Question | Interview | Extrait,
        relationship: str,
        *args,
        **kwargs
    ):
        """Création du Serializer de RelationShip concernant les utilisateurs

        Args:
            node (Artiste|Question|Interview|Extrait): type de node, ayant un type de relationship existante avec Utilisateur
            relationship (str): le nom de la relation entre node et Utilisateur

            context_node : Utilisateur
        """
        super().__init__(node, Utilisateur, relationship, *args, **kwargs)

    def get_date_heure(self, instance: Artiste | Question | Interview | Extrait) -> str:
        """Renvoie la date de la relationship

        Args:
            instance (Artiste | Question | Interview | Extrait): instance du modèle

        Raises:
            ContextError: node de context manquant

        Returns:
            str: date de la relationship
        """
        context_node_name: str = str(self.context_node.__name__)
        utilisateur: Utilisateur = self.context.get(context_node_name.lower())
        if not utilisateur:
            raise ContextError(self.context_node)
        relationship_manager: RelationshipManager = getattr(
            utilisateur, self.relationship
        )
        relationship: DateHeureRel = relationship_manager.relationship(instance)
        date: datetime = relationship.date_heure
        return date.isoformat()
