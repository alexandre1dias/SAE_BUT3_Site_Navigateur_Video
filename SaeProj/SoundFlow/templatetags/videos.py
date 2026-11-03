import json
from functools import lru_cache
from urllib.parse import quote
from urllib.request import urlopen

from django import template

register = template.Library()

# Adresse oEmbed de chaque plateforme
OEMBED = {
    'youtube': 'https://www.youtube.com/oembed?format=json&url=',
    'vimeo': 'https://vimeo.com/api/oembed.json?url=',
}


@lru_cache(maxsize=None)
def miniature_oembed(plateforme, url_video):
    """Demande la miniature à YouTube ou Vimeo avec le protocole oEmbed.
    La réponse est un JSON qui contient notamment "thumbnail_url".
    lru_cache garde la réponse en mémoire : chaque vidéo n'est demandée qu'une fois
    tant que le serveur tourne."""
    adresse = OEMBED[plateforme] + quote(url_video, safe='')
    try:
        with urlopen(adresse, timeout=3) as reponse:
            return json.load(reponse).get('thumbnail_url', '')
    except Exception:
        # Vidéo privée, introuvable ou pas de réseau : pas de miniature
        return ''


@register.filter
def miniature(url_youtube, url_vimeo=''):
    """Miniature YouTube si la vidéo y est, sinon miniature Vimeo."""
    if url_youtube:
        return miniature_oembed('youtube', url_youtube)
    if url_vimeo:
        return miniature_oembed('vimeo', url_vimeo)
    return ''