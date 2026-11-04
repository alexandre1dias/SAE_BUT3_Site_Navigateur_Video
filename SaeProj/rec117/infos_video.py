"""Récupère automatiquement les informations d'une vidéo YouTube ou Vimeo à partir de son URL.

Aucune clé d'API n'est nécessaire :
- oEmbed (YouTube et Vimeo) donne le titre, l'auteur (la chaîne) et la miniature ;
  Vimeo donne en plus la durée, la description et la date de mise en ligne.
- Pour YouTube, la page de la vidéo est lue en plus pour essayer d'obtenir
  la durée, la description et la date de mise en ligne.

Tout est fait « au mieux » : si une information n'est pas trouvée (vidéo privée,
pas de réseau, YouTube qui change sa page...), elle est simplement absente du résultat
et l'utilisateur la remplit à la main dans le formulaire.
"""
import datetime
import html
import json
import re
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import Request, urlopen

DELAI = 5  # secondes d'attente maximum pour chaque requête

# Un navigateur « normal » : certaines pages refusent les clients sans User-Agent
ENTETES = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
    # Évite la page « Avant d'accéder à YouTube » (consentement aux cookies en Europe)
    'Cookie': 'CONSENT=YES+1; SOCS=CAI',
}


# --- Reconnaissance de l'URL -------------------------------------------------

def analyser_url(url):
    """Retourne (plateforme, identifiant) ou (None, None) si l'URL n'est pas reconnue.
    plateforme vaut 'youtube' ou 'vimeo'."""
    url = (url or '').strip()
    if not url:
        return None, None
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    adresse = urlparse(url)
    hote = (adresse.hostname or '').lower().removeprefix('www.').removeprefix('m.')
    morceaux = [m for m in adresse.path.split('/') if m]

    if hote == 'youtu.be' and morceaux:
        return 'youtube', morceaux[0]
    if hote in ('youtube.com', 'music.youtube.com', 'youtube-nocookie.com'):
        if 'v' in parse_qs(adresse.query):
            return 'youtube', parse_qs(adresse.query)['v'][0]
        if len(morceaux) >= 2 and morceaux[0] in ('shorts', 'embed', 'live', 'v'):
            return 'youtube', morceaux[1]
    if hote in ('vimeo.com', 'player.vimeo.com'):
        # vimeo.com/123456, vimeo.com/123456/abcdef (vidéo non répertoriée),
        # player.vimeo.com/video/123456, vimeo.com/channels/xxx/123456...
        chiffres = [i for i, m in enumerate(morceaux) if m.isdigit()]
        if chiffres:
            i = chiffres[0]
            identifiant = morceaux[i]
            # Le hash des vidéos non répertoriées suit l'identifiant
            if i + 1 < len(morceaux) and re.fullmatch(r'[0-9a-f]{6,}', morceaux[i + 1]):
                identifiant += '/' + morceaux[i + 1]
            elif 'h' in parse_qs(adresse.query):
                identifiant += '/' + parse_qs(adresse.query)['h'][0]
            return 'vimeo', identifiant
    return None, None


def url_propre(plateforme, identifiant):
    """URL courte, au même format que les données existantes."""
    if plateforme == 'youtube':
        return f'https://youtu.be/{identifiant}'
    return f'https://vimeo.com/{identifiant}'


# --- Petits outils ------------------------------------------------------------

def _telecharger(adresse):
    requete = Request(adresse, headers=ENTETES)
    with urlopen(requete, timeout=DELAI) as reponse:
        return reponse.read().decode('utf-8', errors='replace')


def _date(texte):
    """'2025-01-15T10:00:00-08:00' ou '2025-01-15 10:00:00' -> date(2025, 1, 15)"""
    try:
        return datetime.date.fromisoformat(str(texte)[:10])
    except ValueError:
        return None


def _duree_iso(texte):
    """'PT1H4M13S' -> 3853 secondes"""
    m = re.fullmatch(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', texte or '')
    if not m or not any(m.groups()):
        return None
    j, h, mi, s = (int(x or 0) for x in m.groups())
    return ((j * 24 + h) * 60 + mi) * 60 + s


def _chaine_json(page, cle):
    """Lit "cle":"valeur" dans le JSON intégré à la page YouTube (gère les \\n, \\u00e9...)."""
    m = re.search(r'"%s":"((?:[^"\\]|\\.)*)"' % re.escape(cle), page)
    if not m:
        return None
    try:
        return json.loads('"' + m.group(1) + '"')
    except ValueError:
        return None


def _meta(page, nom):
    """Contenu d'une balise <meta property|name|itemprop="nom" content="...">"""
    for motif in (
        r'<meta[^>]+(?:property|name|itemprop)="%s"[^>]+content="([^"]*)"',
        r'<meta[^>]+content="([^"]*)"[^>]+(?:property|name|itemprop)="%s"',
    ):
        m = re.search(motif % re.escape(nom), page)
        if m:
            return html.unescape(m.group(1))
    return None


# --- Récupération ---------------------------------------------------------------

def _oembed(plateforme, url):
    if plateforme == 'youtube':
        adresse = 'https://www.youtube.com/oembed?format=json&url=' + quote(url, safe='')
    else:
        adresse = 'https://vimeo.com/api/oembed.json?url=' + quote(url, safe='')
    return json.loads(_telecharger(adresse))


def lire_oembed(plateforme, donnees):
    """Transforme la réponse oEmbed en dictionnaire d'informations."""
    infos = {
        'titre': donnees.get('title'),
        'auteur': donnees.get('author_name'),
        'miniature': donnees.get('thumbnail_url'),
    }
    if plateforme == 'vimeo':
        infos['duree'] = donnees.get('duration') or None
        infos['description'] = donnees.get('description') or None
        infos['date'] = _date(donnees.get('upload_date', ''))
    return infos


def lire_page_youtube(page):
    """Extrait durée, description et date de la page HTML d'une vidéo YouTube."""
    infos = {}
    secondes = _chaine_json(page, 'lengthSeconds')
    if secondes and secondes.isdigit():
        infos['duree'] = int(secondes)
    else:
        infos['duree'] = _duree_iso(_meta(page, 'duration'))
    infos['description'] = _chaine_json(page, 'shortDescription') or _meta(page, 'og:description')
    date = _chaine_json(page, 'publishDate') or _chaine_json(page, 'uploadDate') \
        or _meta(page, 'datePublished') or _meta(page, 'uploadDate')
    infos['date'] = _date(date) if date else None
    infos['titre'] = _meta(page, 'og:title')
    infos['auteur'] = _chaine_json(page, 'author') or _chaine_json(page, 'ownerChannelName')
    return infos


def recuperer_infos(url):
    """Point d'entrée : retourne un dictionnaire

        {'plateforme': 'youtube' | 'vimeo' | None,
         'url': URL nettoyée,
         'titre', 'auteur', 'miniature', 'duree' (secondes), 'description', 'date' (datetime.date),
         'erreur': message si rien n'a pu être récupéré}

    Les informations non trouvées valent None.
    """
    resultat = dict.fromkeys(['titre', 'auteur', 'miniature', 'duree', 'description', 'date'])
    plateforme, identifiant = analyser_url(url)
    resultat['plateforme'] = plateforme
    resultat['erreur'] = None
    if not plateforme:
        resultat['url'] = (url or '').strip()
        resultat['erreur'] = "Cette adresse n'est pas une vidéo YouTube ou Vimeo reconnue."
        return resultat
    resultat['url'] = url_propre(plateforme, identifiant)

    # 1. oEmbed
    try:
        for cle, valeur in lire_oembed(plateforme, _oembed(plateforme, resultat['url'])).items():
            resultat[cle] = valeur or None
    except Exception:
        pass

    # 2. Page YouTube pour ce que oEmbed ne donne pas
    if plateforme == 'youtube':
        try:
            page = _telecharger('https://www.youtube.com/watch?v=' + quote(identifiant))
            for cle, valeur in lire_page_youtube(page).items():
                if valeur and not resultat.get(cle):
                    resultat[cle] = valeur
        except Exception:
            pass
        if not resultat['miniature']:
            # L'adresse des miniatures YouTube est toujours la même : pas besoin du réseau
            resultat['miniature'] = f'https://i.ytimg.com/vi/{identifiant}/hqdefault.jpg'

    if not resultat['titre']:
        resultat['erreur'] = ("Impossible de joindre " + ('YouTube' if plateforme == 'youtube' else 'Vimeo')
                              + " (vidéo privée, supprimée ou pas de connexion Internet). "
                              "Remplissez les informations à la main.")
    return resultat
