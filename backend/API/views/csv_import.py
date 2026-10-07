"""Vues API pour l'import CSV d'extraits d'interviews.

Ce module fournit `CSVImportView` qui accepte l'upload d'un fichier CSV,
valide les en-têtes, crée un `CSVImportJob` en arrière-plan et traite le
fichier pour créer ou mettre à jour les nœuds `Extrait`, `Interview`,
`Artiste`, `Tag`, `Audio`, `Occasion` et `Question`.

L'import s'exécute dans un thread via `CSVImportView.run_import` qui
met à jour le statut du `CSVImportJob`. Le statut de l'import peut être
consulté via la vue `CSVImportJobStatusView` (fichier
`csv_import_job_status.py`).

Le format CSV attendu et les détails de traitement sont documentés dans
`docs/CSV_IMPORT.md`.
"""

import csv
import logging
from datetime import date as Date, datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsAdminOrReadOnly
from ..models import Artiste, Audio, CSVImportJob, Extrait, Interview, Occasion, Question, Tag, Theme
from ..serializers import (
    ArtisteSerializer,
    QuestionSerializer,
    TagSerializer,
    ExtraitSerializer,
    AudioSerializer,
    OccasionSerializer,
    AudiosSerializer,
    TagsExtraitRelationShipSerializer,
    InterviewSerializer,
    InterviewsSerializer,
)
import threading

logger = logging.getLogger(__name__)


class CSVImportView(APIView):
    """
    Vue API permettant l'import d'un fichier CSV contenant des extraits
    d'interviews (artistes, questions, tags, audios, occasions, etc.).

    Chaque ligne du CSV correspond à un extrait. Les extraits sont ensuite
    regroupés par artiste et événement afin de créer automatiquement
    des interviews.
    """

    permission_classes = [IsAdminOrReadOnly]

    _EXPECTED_HEADERS = {
        "Artiste",
        "Position",
        "Question",
        "Audios",
        "Tags",
        "Origine",
        "Date",
        "Evenement",
        "Ville",
        "Youtube",
        "Vimeo",
        "Auteur",
    }


    @staticmethod
    def run_import(csv_lines, job_uuid):
        job = CSVImportJob.nodes.get(uuid=job_uuid)
        try:
            CSVImportView().save_data(csv_lines)
            job.status = "success"
            job.message = "CSV importé avec succès !"
        except Exception as e:
            job.status = "error"
            job.message = str(e)
        finally:
            job.save()

    def post(self, request, *args, **kwargs):
        """
        Endpoint POST pour importer un fichier CSV.

        Attend un fichier CSV envoyé via le champ `file` du formulaire.
        Effectue une validation basique (présence du fichier et extension),
        puis déclenche le traitement et l'enregistrement des données.

        :param request: Requête HTTP contenant le fichier CSV
        :return: Réponse HTTP indiquant le succès ou l'erreur
        """
        # Vérifie s'il existe déjà un import en cours
        try:
            existing_job = CSVImportJob.nodes.get(status="in_progress")
            return Response(
                {"error": "Un import CSV est déjà en cours. Veuillez attendre sa fin."},
                status=409,
            )
        except CSVImportJob.DoesNotExist:
            pass  # aucun job en cours, on peut continuer




        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "Aucun fichier envoyé"}, status=400)

        if not csv_file.name.endswith(".csv"):
            return Response({"error": "Le fichier doit être un CSV"}, status=400)

        try:
            decoded_file = csv_file.read().decode("utf-8").splitlines()
        except UnicodeDecodeError:
            return Response({"error": "Encodage invalide"}, status=400)

        reader = csv.reader(decoded_file)
        headers = next(reader, None)
        if not headers:
            return Response({"error": "CSV vide"}, status=400)

        headers_set = {h.strip() for h in headers}
        missing = self._EXPECTED_HEADERS - headers_set
        extra = headers_set - self._EXPECTED_HEADERS
        if missing or extra:
            return Response(
                {"error": "CSV incorrect", "missing": sorted(missing), "extra": sorted(extra)},
                status=400,
            )

        # Crée un job
        job = CSVImportJob(status="in_progress", message="Import en cours...")
        job.save()

        # Lance le traitement en arrière-plan
        thread = threading.Thread(
            target=CSVImportView.run_import,
            args=(decoded_file, job.uuid),
            daemon=True,
        )
        thread.start()

        return Response({"job_id": job.uuid, "message": "Import CSV lancé"}, status=202)

    def save_data(self, csv_file):
        """
        Lit et parcourt le fichier CSV ligne par ligne.

        Les extraits sont regroupés par artiste et événement.
        Lorsqu'un changement d'artiste ou d'événement est détecté,
        une interview est créée à partir des extraits accumulés.

        :param csv_file: Fichier CSV envoyé par l'utilisateur (liste de strings ou BytesIO)
        """
        # Gérer les deux types d'entrée: liste de strings ou BytesIO
        if isinstance(csv_file, (list, tuple)):
            # Si c'est une liste de strings, créer un DictReader
            reader = csv.DictReader(csv_file)
        else:
            # Si c'est un fichier (BytesIO ou similaire), le décoder d'abord
            content = csv_file.read().decode("utf-8")
            lines = content.splitlines()
            reader = csv.DictReader(lines)

        artiste = None
        occasion = None
        liste_extraits = []
        for row in reader:
            if artiste != None:
                if (
                    artiste != row["Artiste"].strip()
                    or occasion != row["Evenement"].strip()
                ):
                    self.save_interview(liste_extraits, occasion)
                    liste_extraits = []
                    artiste = row["Artiste"].strip()
                    occasion = row["Evenement"].strip()
            else:
                artiste = row["Artiste"].strip()
                occasion = row["Evenement"].strip()

            extrait = self.save_row(row)
            liste_extraits.append(extrait)

        # Sauvegarde de la dernière interview
        if liste_extraits:
            self.save_interview(liste_extraits, occasion)

    def save_row(self, row):
        """
        Traite une ligne du CSV et crée (ou récupère) les entités associées :
        artiste, question, tags, audios, occasion, puis crée l'extrait.

        Gère également les relations entre l'extrait et les tags / audios.

        :param row: Dictionnaire représentant une ligne du CSV
        :return: Instance de l'extrait créé
        """

        # crée (ou récupère) artiste
        serializer_artiste = ArtisteSerializer()
        artiste = row["Artiste"].strip()
        artiste_uuid = None
        if artiste != "" and artiste is not None:
            try:
                artiste_uuid = serializer_artiste.create({"name": artiste}).uuid
            except:
                artiste_uuid = Artiste.nodes.get(name=artiste).uuid

        # crée (ou récupère) question
        serializer_question = QuestionSerializer()
        question = row["Question"].strip()
        question_uuid = None
        if question != "" and question is not None:
            try:
                question_uuid = serializer_question.create({"texte": question}).uuid
            except:
                question_uuid = Question.nodes.get(texte=question).uuid

        # crée (ou récupère) occasion
        serializer_occasion = OccasionSerializer()
        evenement = row["Evenement"].strip()
        if evenement != "" and evenement is not None:
            try:
                serializer_occasion.create({"name": evenement}).uuid
            except:
                pass

        # crée (ou récupère) tags
        serializer_tag = TagSerializer()
        tags = [tag.strip() for tag in row["Tags"].split("; ")]
        tags_uuids = []
        for tag in tags:
            if tag != "" and tag is not None:
                try:
                    tag_uuid = serializer_tag.create({"name": tag}).uuid
                except:
                    tag_uuid = Tag.nodes.get(name=tag).uuid
                tags_uuids.append(tag_uuid)

        # crée (ou récupère) audio
        serializer_audio = AudioSerializer()
        audios = [audio.strip() for audio in row["Audios"].split("; ")]
        audios_uuids = []
        for audio in audios:
            if audio != "" and audio is not None:
                try:
                    audio_uuid = serializer_audio.create({"name": audio}).uuid
                except:
                    audio_uuid = Audio.nodes.get(name=audio).uuid
                    audios_uuids.append(audio_uuid)

        # récupère le code de la vidéo YouTube
        youtube_url = self.get_code_yt(row["Youtube"].strip())
        vimeo_url = self.get_code_vimeo(row["Vimeo"].strip())

        # création du titre
        date = row["Date"].strip()
        titre = artiste + " - " + evenement + " - " + question + " - " + date

        # création ou update de l'extrait
        serializer_extrait = ExtraitSerializer()
        extrait_node = None

        # 1. Recherche par Vimeo
        if vimeo_url:
            try:
                extrait_node = Extrait.nodes.get(vimeo_url=vimeo_url)
            except Extrait.DoesNotExist:
                extrait_node = None

        # 2. Recherche par YouTube (si pas trouvé via Vimeo)
        if not extrait_node and youtube_url:
            try:
                extrait_node = Extrait.nodes.get(youtube_url=youtube_url)
            except Extrait.DoesNotExist:
                extrait_node = None

        # 3. UPDATE si l'extrait existe déjà
        if extrait_node:
            extrait_node.titre = titre
            extrait_node.artiste_uuid = artiste_uuid
            extrait_node.question_uuid = question_uuid
            extrait_node.uploaded_at = (
                self.parse_date(row["Date"].strip()) if date else None
            )
            extrait_node.lieu = row["Ville"].strip()
            extrait_node.youtube_url = youtube_url
            extrait_node.vimeo_url = vimeo_url
            extrait_node.position = (
                int(row["Position"].strip()) if row["Position"].strip() else None
            )
            extrait_node.save()

            context = {"extrait": extrait_node}

            for audio_uuid in audios_uuids:
                serializer = AudiosSerializer(
                    data={"uuid": audio_uuid}, context=context
                )
                serializer.delete(audio_uuid)

            for tag_uuid in tags_uuids:
                serializer = TagsExtraitRelationShipSerializer(
                    data={"uuid": tag_uuid}, context=context
                )
                serializer.delete(tag_uuid)

        # 4. CREATE sinon
        else:
            extrait_node = serializer_extrait.create(
                {
                    "titre": titre,
                    "artiste_uuid": artiste_uuid,
                    "question_uuid": question_uuid,
                    "uploaded_at": (
                        self.parse_date(row["Date"].strip()) if date else None
                    ),
                    "lieu": row["Ville"].strip(),
                    "youtube_url": youtube_url,
                    "vimeo_url": vimeo_url,
                    "position": (
                        int(row["Position"].strip())
                        if row["Position"].strip()
                        else None
                    ),
                    "duree": 0,
                    "description": "",
                }
            )

        context = {"extrait": extrait_node}

        for audio_uuid in audios_uuids:
            serializer = AudiosSerializer(data={"uuid": audio_uuid}, context=context)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)

        for tag_uuid in tags_uuids:
            serializer = TagsExtraitRelationShipSerializer(
                data={"uuid": tag_uuid}, context=context
            )
            if serializer.is_valid():
                serializer.create(serializer.validated_data)

        return extrait_node

    def save_interview(self, liste_extraits, occasion):
        """
        Crée une interview à partir d'une liste d'extraits
        partageant le même artiste et la même occasion.

        Chaque extrait est ensuite rattaché à l'interview
        avec sa position.

        :param liste_extraits: Liste d'extraits à regrouper
        :param occasion: Nom de l'événement associé
        """
        if not liste_extraits:
            return

        serializer_interview = InterviewSerializer()
        first_extrait = liste_extraits[0]
        artiste_node = first_extrait.interviewer.single()

        occasion_node = None  # Initialiser à None
        if occasion != "" and occasion is not None:
            try:  # Ajouter try/except
                occasion_node = Occasion.nodes.get(name=occasion)
            except:
                pass  # occasion_node reste None

        titre = f"Interview de {artiste_node.name} pour {occasion_node.name if occasion_node else 'une occasion inconnue'}"
        if titre in [interview.titre for interview in Interview.nodes.all()]:
            logger.warning(f"Interview déjà existante - {titre}")
            return
        try:
            interview_node = serializer_interview.create(
                {
                    "titre": titre,
                    "date": first_extrait.uploaded_at,
                    "description": "",
                    "occasion_uuid": occasion_node.uuid if occasion_node else None,
                }
            )

            for extrait in liste_extraits:
                context = {"extrait": extrait}
                serializer = InterviewsSerializer(
                    data={"uuid": interview_node.uuid, "position": extrait.position},
                    context=context,
                )
                if serializer.is_valid():
                    serializer.create(serializer.validated_data)

        except Exception as e:
            logger.debug(f"Erreur lors de la création de l'interview: {e}")

    def get_code_yt(self, url):
        """
        Extrait l'identifiant vidéo depuis une URL YouTube.

        Supporte les formats :
        - youtube.com/watch?v=XXXX
        - youtu.be/XXXX

        :param url: URL YouTube complète
        :return: Code vidéo ou l'URL si aucun format connu n'est détecté
        """
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1]
        return url

    def get_code_vimeo(self, url):
        """
        Extrait l'identifiant vidéo d'une URL Vimeo.

        Formats supportés :
        - https://vimeo.com/123456789
        - https://player.vimeo.com/video/123456789
        - https://vimeo.com/123456789?h=xxxx

        :param url: URL Vimeo complète
        :return: Identifiant de la vidéo ou l'URL si aucun format connu n'est détecté
        """
        if not url:
            return url

        if "vimeo.com/" in url:
            # Cas player.vimeo.com/video/XXXX
            if "/video/" in url:
                code = url.split("/video/")[1]
            else:
                code = url.split("vimeo.com/")[1]

            # Supprime les paramètres éventuels (?h=..., &...)
            return code.split("?")[0].split("&")[0]

        return url

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            return Date(dt.year, dt.month, dt.day)
        except ValueError:
            return None
