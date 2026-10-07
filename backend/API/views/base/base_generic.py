from django.http import HttpRequest
from django.db.models.query import QuerySet
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from neomodel.exceptions import DoesNotExist
from neomodel.sync_.match import NodeSet, RawCypher
from neomodel import StructuredNode, db
from neo4j.exceptions import ServiceUnavailable
from ...errors import NotFound, ConnexionDB, OrderError

class BaseGenericViewSet(GenericViewSet):
    """
    Classe de base générique contenant les méthodes pour les viewsets de l'api

    Gestion de la recherche, de l'ordonnancement, de la pagination et de la récupération d'instance

    Champs :
        - lookup_field : champ utilisé pour la recherche d'une instance
        - permission_classes : permissions utilisées pour les viewsets enfants (ici, utilise les permissions par défaut, voir settings.py)

    Raises:
        ValidationError: Données du mauvais type
        ConnexionDB: Base de données indisponible
        NotFound: Instance introuvable
        OrderError: Erreur dans le champ pour ordonner
    """
    # permission_classes = []  # Remplace les permissions par défaut

    lookup_field = "uuid"

    def __init__(
        self,
        serializer_class: Serializer,
        model_class: StructuredNode,
        search_field: str = None,
        **kwargs,
    ):
        """
        ViewSet générique contenant toutes les méthodes pour les ViewSets enfants

        Args:
            serializer_class (Serializer): Serializer du ViewSet
            model_class (StructuredNode): type de node du ViewSet
            search_field (str, optional): Champ utiliser pour la recherche si fourni. Defaults to None.
        """
        super().__init__(**kwargs)
        self.serializer_class: Serializer = serializer_class
        self.model_class: StructuredNode = model_class
        self.search_field: str = search_field

    def get_nodeset(self) -> NodeSet:
        """
        Récupère le nodeset (neomodel) de la view,
        même chose qu'un queryset mais pour neomodel

        Méthode overrideable pour les viewsets enfants, pour appliquer des filtres par défaut sur le nodeset (sous nodeset)

        Returns:
            NodeSet: ensemble de StructuredNode du modèle
        """
        return self.model_class.nodes

    def get_queryset(self) -> QuerySet:
        """
        Récupère le queryset (django) de la view

        Applique les filtres de recherche, d'ordonnancement et de pagination sur le queryset

        Raises:
            ValidationError: Les données dans les paramètres d'url ne sont pas du bon type
            ConnexionDB: La base de données n'est pas disponible

        Returns:
            QuerySet: queryset filtrer et ordonner
        """
        queryset: NodeSet = self.get_nodeset()
        request: HttpRequest = self.request

        # Recherche (search)
        if self.search_field:
            queryset = self.search_nodeset(
                queryset, request.GET.get("search", "").strip()
            )

        # Ordonne (order)
        order = request.GET.get("order", "").strip()
        if order != "":
            queryset = self.order_nodeset(queryset, order)

        # Pagination (size) (page)
        size = request.GET.get("size", None)
        page = request.GET.get("page", 0)
        if size:
            try:
                size, page = int(size), int(page)
            except:
                raise ValidationError()
            queryset = self.pagination_nodeset(queryset, size, page)

        # Skip les premiers éléments (skip)
        skip = request.GET.get("skip", None)
        if skip:
            try:
                skip = int(skip)
            except:
                raise ValidationError()
            queryset = self.skip_nodeset(queryset, skip)
        try:
            return queryset.all()
        # Dans le cas ou la base de données est inaccessible
        except ServiceUnavailable:  # pragma: no cover
            raise ConnexionDB()  # pragma: no cover

    def get_object(self) -> StructuredNode:
        """
        Récupère l'objet dans le nodeset

        Raises:
            NotFound: L'objet rechercher n'a pas été trouvé
            ConnexionDB: La base de données n'est pas disponnible

        Returns:
            StructuredNode: Intance rechercher
        """
        try:
            return self.get_nodeset().get(uuid=self.kwargs[self.lookup_field])
        except DoesNotExist:
            raise NotFound(self.model_class)
        # Dans le cas ou la base de données est inaccessible
        except ServiceUnavailable:  # pragma: no cover
            raise ConnexionDB()  # pragma: no cover

    def search_nodeset(self, nodeset: NodeSet, search: str) -> NodeSet:
        """
        Filtre le nodeset en fonction de la recherche

        Args:
            nodeset (NodeSet): nodeset dans lequel on effectue la recherche
            search (str): champ recherche

        Returns:
            NodeSet: nodeset filtré
        """
        for term in search.split(","):
            if term:
                # Le search field n'étant pas identique pour tous les models,
                # il est nécessaire de filtrer ainsi
                nodeset = nodeset.filter(**{f"{self.search_field}__icontains": term})
        return nodeset

    def order_nodeset(self, nodeset: NodeSet, orders: str) -> NodeSet:
        """
        Ordonne le nodeset en fonction du champ renseigner
        Ne fonctionne que si les éléments rechercher existent sinon renvoie une erreur

        Args:
            nodeset (NodeSet): nodeset que l'on ordonne
            order (str): champ sur lequel on ordonne

        Returns:
            NodeSet: nodeset ordonné
        """
        ordering = []
        # ($n)-[r:relationship]-(s) pour ne pas se soucier du sens de la relation
        for order in orders.split(","):
            if "__" in order:
                fields_list = order.split("__")
                if len(fields_list) > 2:
                    raise OrderError("Too many fields")
                elif len(fields_list) < 2:
                    raise OrderError("Not enough fields")

                # Dernière relation et Field d'ordering
                relationship, property = fields_list

                # Sens de l'ordre
                sens = "DESC" if relationship[0] == "-" else "ASC"
                if sens == "DESC":
                    relationship = relationship[1:]

                if relationship.upper() in [
                    # Liste des relationships valides
                    relationship_brut[0]
                    for relationship_brut in db.cypher_query(
                        # Request CYPHER
                        f"MATCH (n:`{self.model_class.__name__}`)-[r]-(m) RETURN DISTINCT TYPE(r)"
                    )[0]
                ]:
                    if property in [
                        # Liste des properties valides
                        property_brut[0]
                        for property_brut in db.cypher_query(
                            # Request CYPHER
                            f"MATCH (n:`{self.model_class.__name__}`)-[r:{relationship.upper()}]-(m) RETURN DISTINCT keys(m)"
                        )[0][0]
                    ]:
                        # Ordonner le queryset
                        ordering.append(
                            RawCypher(
                                f"head([($n)-[r:{relationship.upper()}]-(s) | s.{property}]) {sens}"
                            )
                        )
                    else:
                        raise OrderError(property)
                else:
                    raise OrderError(fields_list[0])

            elif "|" in order:
                fields_list = order.split("|")
                if len(fields_list) > 2:
                    raise OrderError("Too many fields")
                if len(fields_list) < 2:
                    raise OrderError("Not enough fields")

                # Dernière relation et Field d'ordering
                relationship, property = fields_list

                # Sens de l'ordre
                sens = "DESC" if relationship[0] == "-" else "ASC"
                if sens == "DESC":
                    relationship = relationship[1:]

                if fields_list[0].upper() in [
                    # Liste des relationships valides
                    relationship_brut[0]
                    for relationship_brut in db.cypher_query(
                        # Request CYPHER
                        f"MATCH (n:`{self.model_class.__name__}`)-[r]-(m) RETURN DISTINCT TYPE(r)"
                    )[0]
                ]:
                    if property in [
                        # Liste des properties valides
                        property_brut[0]
                        for property_brut in db.cypher_query(
                            # Request CYPHER
                            f"MATCH (n:`{self.model_class.__name__}`)-[r:{relationship.upper()}]-(m) RETURN DISTINCT keys(r)"
                        )[0][0]
                    ]:
                        ordering.append(
                            RawCypher(
                                f"head([($n)-[r:{relationship.upper()}]-(s) | r.{property}]) {sens}"
                            )
                        )
                    else:
                        raise OrderError(property)
                else:
                    raise OrderError(fields_list[0])

            else:
                # Fonctionnement classique.
                if (
                    order[0] == "-" and self.model_class.__dict__.get(order[1:], None)
                ) or self.model_class.__dict__.get(order, None):
                    ordering.append(order)
                else:
                    raise OrderError(order)
        return nodeset.order_by(*ordering)

    def pagination_nodeset(self, nodeset: NodeSet, size: int, page: int) -> NodeSet:
        """
        Pagination du nodeset avec une taille de page et le numéro de la page actuelle

        Args:
            nodeset (NodeSet): nodeset sur lequel est appliqué la pagination
            size (int): entier strictement positif correspondant à la taille d'une page
            page (int): entier strictement positif correspondant au numéro de la page

        Returns:
            NodeSet: extrait du nodeset correspondant à la taille et la page
        """
        if size < 1:
            return nodeset
        # Pagination commence à la page 1
        if (page) < 1:
            page = 1
        return nodeset[(page - 1) * size : page * size]

    def skip_nodeset(self, nodeset: NodeSet, skip: int) -> NodeSet:
        """
        Passe les premiers éléments du nodeset, le faisant commencer après

        Args:
            nodeset (NodeSet): nodeset exploiter
            skip (int): entier strictement positif correspondant aux n premiers éléments passer

        Returns:
            NodeSet: nodeset modifier
        """
        return nodeset[skip if skip > 0 else 0 :]
