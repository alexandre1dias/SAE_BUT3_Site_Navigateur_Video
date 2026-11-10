"""Page d'administration des vidéos : ajout à partir d'une URL, liste, modification, suppression.

Accès : réglage ADMINISTRATION_OUVERTE dans settings.py.
True = ouverte à tous ; False = réservée aux comptes « staff » (équipe) de Django.
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ExtraitForm, InterviewForm, UrlForm
from .infos_video import recuperer_infos
from .models import Artiste, Extrait, Interview

# Interview ou Extrait selon le type demandé dans l'URL
MODELES = {
    'interview': (Interview, InterviewForm, 'idInterview'),
    'extrait': (Extrait, ExtraitForm, 'idExtrait'),
}

# Champs signalés « à remplir » quand ils n'ont pas pu être récupérés depuis l'URL
CHAMPS_PRINCIPAUX = {
    'interview': {'titreInterview', 'urlMiniature', 'duree', 'artiste', 'dateTournage', 'lieu', 'descriptionInterview'},
    'extrait': {'titreExtrait', 'urlMiniature', 'interview', 'question', 'timecodeFin', 'transcription'},
}


def staff_requis(vue):
    """Réserve les vues d'administration aux comptes actifs de l'équipe."""
    return user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url='admin_connexion',
    )(vue)


class ConnexionView(LoginView):
    template_name = 'rec117/administration/connexion.html'
    redirect_authenticated_user = False

    def get_success_url(self):
        if not self.request.user.is_staff:
            return reverse('home')
        return super().get_success_url()


@staff_requis
def accueil(request):
    """Formulaire d'URL + liste de toutes les vidéos."""
    return render(request, 'rec117/administration/accueil.html', {
        'form_url': UrlForm(),
        'interviews': Interview.objects.select_related('artiste', 'lieu').prefetch_related('extraits')
                                       .order_by('artiste__nomArtiste', 'idInterview'),
        'extraits': Extrait.objects.select_related('interview__artiste', 'question')
                                   .order_by('interview__artiste__nomArtiste', 'interview', 'ordreSequence'),
    })


def _page_formulaire(request, form, type_video, **contexte):
    """Affiche le formulaire, champs regroupés en blocs (voir l'attribut groupes des formulaires)."""
    contexte.setdefault('auto', set())
    return render(request, 'rec117/administration/formulaire.html', {
        'form': form,
        'type_video': type_video,
        'groupes': [(titre, [form[nom] for nom in noms]) for titre, noms in form.groupes],
        **contexte,
    })


def _deviner_artiste(infos):
    """Cherche un artiste existant dont le nom apparaît dans le titre ou l'auteur de la vidéo."""
    texte = f"{infos.get('titre') or ''} {infos.get('auteur') or ''}".lower()
    for artiste in Artiste.objects.all():
        if artiste.nomArtiste.lower() in texte:
            return artiste
    return None


def _valeurs_initiales(type_video, infos):
    """Pré-remplit le formulaire avec ce qui a été trouvé.
    Retourne (valeurs, noms des champs remplis automatiquement)."""
    champ_url = 'urlYoutube' if infos['plateforme'] == 'youtube' else 'urlVimeo'
    valeurs = {champ_url: infos['url'], 'urlMiniature': infos['miniature']}
    artiste = _deviner_artiste(infos)

    if type_video == 'interview':
        valeurs.update({
            'titreInterview': infos['titre'],
            'descriptionInterview': infos['description'],
            'dateTournage': infos['date'],
            'duree': infos['duree'],
        })
        if artiste:
            valeurs['artiste'] = artiste.pk
        elif infos['auteur']:
            valeurs['nouvel_artiste'] = infos['auteur']
    else:
        valeurs.update({
            'titreExtrait': infos['titre'],
            'transcription': infos['description'],
            'timecodeFin': infos['duree'],
        })
        if artiste:
            derniere = artiste.interviews.order_by('idInterview').last()
            if derniere:
                valeurs['interview'] = derniere.pk

    valeurs = {cle: valeur for cle, valeur in valeurs.items() if valeur not in (None, '')}
    return valeurs, set(valeurs)


def _doublons(url):
    """Vidéos déjà enregistrées avec la même URL."""
    if not url:
        return []
    filtre = Q(urlYoutube=url) | Q(urlVimeo=url)
    return list(Interview.objects.filter(filtre)) + list(Extrait.objects.filter(filtre))


@staff_requis
def ajouter(request, type_video):
    """GET ?url=... : récupère les infos et affiche le formulaire pré-rempli.
    POST : enregistre la vidéo."""
    if type_video not in MODELES:
        return redirect('admin_videos')
    modele, Formulaire, _ = MODELES[type_video]
    infos, auto = None, set()

    if request.method == 'POST':
        form = Formulaire(request.POST)
        auto = set(request.POST.getlist('_auto'))
        if form.is_valid():
            video = form.save()
            messages.success(request, f'« {video} » a été ajouté(e).')
            return redirect('admin_videos')
    else:
        url = request.GET.get('url', '').strip()
        if not url:
            form = Formulaire()
        else:
            infos = recuperer_infos(url)
            if not infos['plateforme']:
                messages.error(request, infos['erreur'])
                return redirect('admin_videos')
            valeurs, auto = _valeurs_initiales(type_video, infos)
            form = Formulaire(initial=valeurs)
            for video in _doublons(infos['url']):
                messages.warning(request, f'Attention : cette vidéo est déjà enregistrée (« {video} »).')

    return _page_formulaire(
        request, form, type_video, infos=infos, auto=auto,
        champs_principaux=CHAMPS_PRINCIPAUX[type_video],
        titre_page='Ajouter une interview' if type_video == 'interview' else 'Ajouter un extrait')


@staff_requis
def modifier(request, type_video, pk):
    if type_video not in MODELES:
        return redirect('admin_videos')
    modele, Formulaire, _ = MODELES[type_video]
    video = get_object_or_404(modele, pk=pk)
    form = Formulaire(request.POST or None, instance=video)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'« {video} » a été modifié(e).')
        return redirect('admin_videos')
    return _page_formulaire(request, form, type_video, video=video, titre_page=f'Modifier : {video}')


@staff_requis
def supprimer(request, type_video, pk):
    """GET : page de confirmation. POST : suppression."""
    if type_video not in MODELES:
        return redirect('admin_videos')
    modele, _, _ = MODELES[type_video]
    video = get_object_or_404(modele, pk=pk)
    if request.method == 'POST':
        nom = str(video)
        video.delete()
        messages.success(request, f'« {nom} » a été supprimé(e).')
        return redirect('admin_videos')
    return render(request, 'rec117/administration/supprimer.html', {
        'video': video,
        'type_video': type_video,
        'extraits_lies': video.extraits.all() if type_video == 'interview' else [],
    })
