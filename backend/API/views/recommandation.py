from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from neo4j.exceptions import ServiceUnavailable
from neomodel import db
from ..models import Extrait, Interview, Utilisateur
from ..serializers import ExtraitSerializer, InterviewSerializer
from ..errors import ConnexionDB


class Recommandation(APIView):
    """
    Actuel:
        Vidéo similaire à celle en cours
        Créer un score à partir des poids de Thèmes, Artistes et Questions en commun avec la vidéo regarder
        Trier par score puis par récente
        Non visionner si connecter

    Objectif:
        TODO get x derniers Interview/extrait regardés
        TODO - proposées proportion interview/extrait en fonction de ce que l'utilisateur regarde le plus
            si user regarde plus extrait commencé par proposées x extraits, max 4 extrait 1 interview vise versa
            donc 4 pour 1 max pour choisir extrait/interview on fait classement de tags des x derniers regardés sup 70%
        classement des thèmes
        classement des artistes
        classement des questions
        TODO regarder le chemin d'entrée sur le lecteur video
            TODO si c'est par une playlist on propose plus d'interview
            TODO si c'est par une question on propose plus d'extrait
            si c'est par artiste on ajoute un poids sur ce classement des artistes
            si c'est par thème  on ajoute un poids sur ce classement des thèmes
        TODO si pas de user ou pas assez de data on propose les video les plus regardé / récentes
        caper le nombre de données récupérées
        récupérer égalment les interviews
    """

    permission_classes = [AllowAny]

    def post(self, request: HttpRequest) -> Response:
        """L'Algorithme de recommandation de vidéos (Extrait / Interview)
            request.GET:
             - video: str, uuid de la vidéo actuellement regarder
             - size: int, nombre de vidéo maximum à renvoyer. default=10
             - page: int, numéro de page de la pagination. default=0
            request.data:
             - weights : dict (Thème, Question, Artiste)
                key: Nom de la classe du node
                value: weight de la classe (number)
             - filters : dict (Thème, Question, Artiste, Tag, Audio)
                key: Nom de la classe du filtre
                value: uuid de l'instance

        Args:
            request (HttpRequest): Requête vers l'api

        Raises:
            ValidationError: Si un champ n'a pas un valeur du bon type
            ConnexionDB: Si la base de données est indisponnible

        Returns:
            Response: Les vidéos (Extrait / Interview)
        """
        data: dict = request.data
        poids = data.get("weights", {})
        filtres = data.get("filters", {})

        user = request.user

        user: Utilisateur = user if type(user) != AnonymousUser else None

        context = {"request": request}

        video = request.GET.get("video", False)
        size: str = request.GET.get("size", "10")
        if size.isnumeric():
            try:
                size: int = int(size)
            except:
                raise ValidationError(detail="{size: numeric not string}")
        page: str = request.GET.get("page", "0")
        if page.isnumeric():
            try:
                page: int = int(page)
            except:
                raise ValidationError(detail="{page: numeric not string}")

        # Modulabilité du modèle
        video_class = Extrait.__name__
        playlist_class = Interview.__name__

        # Algo complet
        # Construction des parties de la requête
        parts = {
            "match": [],
            "where": ["TRUE"],
            "optional_match": [],
            "with_clauses": [],
            "return": [],
        }

        # === MATCH CLAUSE ===
        if user:
            parts["match"].append("(u:Utilisateur {uuid: $current_user})")

        if video:
            parts["match"].append(f"(c:{video_class}|{playlist_class} {{uuid: $uuid}})")

        parts["match"].append(f"(v:{video_class}|{playlist_class})")

        # === WHERE CLAUSE ===
        if video:
            parts["where"].append("v.uuid <> c.uuid")

        if user:
            parts["where"].append(
                "NOT ((u:Utilisateur)-[:REGARDER_EXTRAITS|REGARDER_INTERVIEWS]-(v))"
            )

        # Filtres dynamiques
        filter_configs = {
            "Thème": ("Theme", "*..3"),
            "Artiste": ("Artiste", "*..2"),
            "Question": ("Question", "*..2"),
            "Tag": ("Tag", "*..3"),
            "Audio": ("Audio", "*..2"),
        }
        # Pour des causes de retro compatibilités avec les anciennes versions de Neo4j server
        # filter_configs = {
        #     "Thème": ("Theme", "*2..3"),
        #     "Artiste": ("Artiste", "*..2"),
        #     "Question": ("Question", "*..2"),
        #     "Tag": ("Tag", "*0..3"),
        #     "Audio": ("Audio", "*..2"),
        # }

        excluded_relations = [
            "REGARDER_EXTRAITS",
            "REGARDER_INTERVIEWS",
            "RECHERCHES_ARTISTES",
            "RECHERCHES_QUESTIONS",
        ]

        for filtre_key, (node_type, path_length) in filter_configs.items():
            if filtres.get(filtre_key):
                # Gestion spéciale pour Tag avec le préfixe '!'
                node_pattern = (
                    f"!:{node_type}" if filtre_key == "Tag" else f"t:{node_type}"
                )
                node_var = "!" if filtre_key == "Tag" else "t"
                # Pour des questions de retro compatibilité avec les anciennes versions de Neo4j server
                # filter_clause = f"""EXISTS {{
                #     MATCH p = SHORTEST 1 (v)-[{path_length}]-({node_pattern})
                #     WHERE {node_var}.uuid = '{filtres[filtre_key]}'
                #     AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                #     AND NONE(r IN relationships(p) WHERE type(r) IN {excluded_relations})
                # }}"""
                filter_clause = f"""EXISTS {{
                    MATCH p = shortestPath((v:{video_class}|{playlist_class})-[{path_length}]-({node_pattern}))
                    WHERE {node_var}.uuid = '{filtres[filtre_key]}'
                    AND NONE(n IN nodes(p) WHERE n:Utilisateur)
                    AND NONE(r IN relationships(p) WHERE type(r) IN {excluded_relations})
                }}"""
                parts["where"].append(filter_clause)

        # === OPTIONAL MATCH pour le scoring ===
        # Pour des questions de retro compatibilité avec les anciennes versions de Neo4j server
        # score_configs = {
        #     "Thème": ("Theme", "*..3", "c_t", "v_t"),
        #     "Artiste": ("Artiste", "*0..2", "c_a", "v_a"),
        #     "Question": ("Question", "*0..2", "c_q", "v_q"),
        # }
        score_configs = {
            "Thème": ("Theme", "*..3", "c_t", "v_t"),
            "Artiste": ("Artiste", "*..2", "c_a", "v_a"),
            "Question": ("Question", "*..2", "c_q", "v_q"),
        }

        collections = []
        score_parts = []

        if video and poids:
            for poids_key, (
                node_type,
                path_length,
                c_var,
                v_var,
            ) in score_configs.items():
                if poids.get(poids_key):
                    parts["optional_match"].extend(
                        [
                            f"OPTIONAL MATCH (c)-[{path_length}]-({c_var}:{node_type})",
                            f"OPTIONAL MATCH (v)-[{path_length}]-({v_var}:{node_type})",
                        ]
                    )

                    collections.append(
                        f"collect(DISTINCT {c_var}) AS {c_var}s, "
                        f"collect(DISTINCT {v_var}) AS {v_var}s"
                    )

                    count_var = f"nb{node_type}s"
                    parts["with_clauses"].append(
                        f"size([x IN {c_var}s WHERE x IN {v_var}s]) AS {count_var}"
                    )

                    score_parts.append(f"{count_var} * {poids[poids_key]}")

        # === Construction de la requête finale ===
        query_parts = []

        # MATCH
        query_parts.append("MATCH " + ",\n      ".join(parts["match"]))

        # WHERE
        query_parts.append("WHERE " + "\n  AND ".join(parts["where"]))

        # OPTIONAL MATCH
        if parts["optional_match"]:
            query_parts.append("\n".join(parts["optional_match"]))

        # WITH (collections)
        if collections:
            with_items = ["c"] if video else []
            with_items.extend(collections)
            with_items.append("v")
            query_parts.append("WITH " + ", ".join(with_items))

        # WITH (counts + date)
        if parts["with_clauses"] or video:
            with_items = ["c"] if video else []
            with_items.extend(parts["with_clauses"])
            with_items.extend(["v", "coalesce(v.date, v.uploaded_at) AS date"])
            query_parts.append("WITH " + ", ".join(with_items))
        else:
            query_parts.append("WITH v, coalesce(v.date, v.uploaded_at) AS date")

        # RETURN
        score_formula = " + ".join(score_parts) if score_parts else "0"
        query_parts.append(f"RETURN v, {score_formula} AS score")

        # ORDER BY
        query_parts.append("ORDER BY score DESC, date DESC")

        # SKIP
        query_parts.append("SKIP $size * $page")

        # LIMIT
        query_parts.append("LIMIT $size")

        # Assemblage final
        query = "\n".join(query_parts)

        # Paramètres
        params = {
            "uuid": video,
            "current_user": user.uuid if user else None,
            "size": size,
            "page": page,
        }
        try:
            recommandations_cypher = db.cypher_query(query, params)[0]
        except ServiceUnavailable:
            raise ConnexionDB()

        # Convertir le retour de la requête CYPHER en liste d'Extrait et Interview en json
        recommandations = [
            (
                {
                    "value": ExtraitSerializer(
                        Extrait.inflate(recommandation[0]), context=context
                    ).data,
                    "type": list(recommandation[0].labels)[0],
                }
                if "Extrait" in recommandation[0].labels
                else (
                    {
                        "value": InterviewSerializer(
                            Interview.inflate(recommandation[0]), context=context
                        ).data,
                        "type": list(recommandation[0].labels)[0],
                    }
                    if "Interview" in recommandation[0].labels
                    else {
                        "value": recommandation[0],
                        "type": list(recommandation[0].labels)[0],
                    }
                )
            )
            for recommandation in recommandations_cypher
        ]

        return Response(recommandations)

