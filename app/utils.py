import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from typing import Dict
import json

#---------------------------------------------
# Utils 
#---------------------------------------------

import re
import requests
from bs4 import BeautifulSoup

def get_youtube_infos(url):
    """ Récupère l'ID et la durée d'une vidéo YouTube """
    try:
        # Extraction de l'ID de la vidéo YouTube
        video_id_match = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|watch\?v=)([a-zA-Z0-9_-]{11})", url)
        if not video_id_match:
            return None

        video_id = video_id_match.group(1)
        response = requests.get(url)
        response.raise_for_status()

        # Recherche des métadonnées JSON dans la page
        json_match = re.search(r'var ytInitialPlayerResponse = ({.*?});', response.text)
        if not json_match:
            return None

        video_data = json.loads(json_match.group(1))
        duration = int(video_data["videoDetails"]["lengthSeconds"])

        return {"id": video_id, "duration": duration}

    except Exception:
        return None

def get_vimeo_infos(url):
    """ Récupère l'ID et la durée d'une vidéo Vimeo via l'API publique """
    try:
        # Extraction de l'ID de la vidéo Vimeo
        video_id_match = re.search(r"vimeo\.com/(\d+)", url)
        if not video_id_match:
            return None

        video_id = video_id_match.group(1)
        api_url = f"https://vimeo.com/api/v2/video/{video_id}.json"

        response = requests.get(api_url)
        response.raise_for_status()

        video_data = response.json()[0]  # L'API retourne une liste avec un seul élément
        duration = int(video_data.get("duration", 0))

        return {"id": video_id, "duration": duration}

    except Exception:
        return None
    
def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en'])

        # Affichez les données brutes pour inspection
        for item in transcript[:5]:  # Limiter pour éviter trop de logs
            print(repr(item['text']))

        lines = [f"[{item['start']:.2f}s] {item['text']}" for item in transcript]
        return "\n".join(lines)
    except TranscriptsDisabled:
        return "Transcriptions are disabled for this video."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def seconds_to_hms(duration: int) -> Dict[str, int]:
    """
    Convertit une durée en secondes en un dictionnaire contenant les heures, minutes et secondes.

    :param duration: Durée en secondes (int)

    :return: Un dictionnaire avec les clés 'hours', 'minutes', et 'seconds'.
    """
    if duration < 0:
        raise ValueError("La durée doit être un entier positif.")

    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60

    return {
        "hours": str(hours).zfill(2),
        "minutes": str(minutes).zfill(2),
        "seconds": str(seconds).zfill(2)
    }