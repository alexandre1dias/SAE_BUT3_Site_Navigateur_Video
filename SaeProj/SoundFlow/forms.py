"""Formulaires de la page d'administration des vidéos."""
import re

from django import forms
from django.db.models import Max

from .models import Artiste, Extrait, GenreMusical, Interview, Lieu, Question


# --- Champ « durée » : accepte 253, 4:13 ou 1:04:13 ---------------------------

def formater_duree(secondes):
    """253 -> '4:13' ; 3853 -> '1:04:13'"""
    if secondes in (None, ''):
        return ''
    secondes = int(secondes)
    h, reste = divmod(secondes, 3600)
    m, s = divmod(reste, 60)
    return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'


class DureeField(forms.CharField):
    """Saisie d'une durée ou d'un timecode, stockée en secondes."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', 'En secondes (253) ou en minutes:secondes (4:13 ou 1:04:13)')
        kwargs.setdefault('widget', forms.TextInput(attrs={'placeholder': 'ex : 4:13'}))
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        if isinstance(value, int):
            return formater_duree(value)
        return value

    def to_python(self, value):
        value = (super().to_python(value) or '').strip()
        if not value:
            return None
        if not re.fullmatch(r'\d+(:\d{1,2}){0,2}', value):
            raise forms.ValidationError('Format attendu : 253, 4:13 ou 1:04:13')
        total = 0
        for morceau in value.split(':'):
            total = total * 60 + int(morceau)
        return total


class DateFrancaise(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        super().__init__(format='%Y-%m-%d', **kwargs)


# --- Interview -------------------------------------------------------------------

class InterviewForm(forms.ModelForm):
    # Regroupement des champs en blocs sur la page
    groupes = [
        ('🎬 La vidéo', ['titreInterview', 'urlYoutube', 'urlVimeo', 'urlMiniature', 'duree']),
        ('🎤 Artiste', ['artiste', 'nouvel_artiste', 'genres_nouvel_artiste']),
        ('📍 Tournage', ['dateTournage', 'lieu', 'nouveau_lieu', 'ville_nouveau_lieu', 'pays_nouveau_lieu']),
        ('📝 Description', ['descriptionInterview']),
    ]
    # Créer un artiste ou un lieu directement depuis le formulaire
    nouvel_artiste = forms.CharField(
        label='… ou nouvel artiste', required=False, max_length=150,
        help_text="Remplir seulement si l'artiste n'est pas dans la liste")
    genres_nouvel_artiste = forms.ModelMultipleChoiceField(
        label='Genres du nouvel artiste', required=False, queryset=GenreMusical.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    nouveau_lieu = forms.CharField(label='… ou nouveau lieu (nom)', required=False, max_length=150)
    ville_nouveau_lieu = forms.CharField(label='Ville du nouveau lieu', required=False, max_length=100)
    pays_nouveau_lieu = forms.CharField(label='Pays du nouveau lieu', required=False, max_length=100, initial='France')
    duree = DureeField(label='Durée', required=False)

    class Meta:
        model = Interview
        fields = ['titreInterview', 'urlYoutube', 'urlVimeo', 'urlMiniature', 'duree',
                  'artiste', 'nouvel_artiste', 'genres_nouvel_artiste',
                  'dateTournage', 'lieu', 'nouveau_lieu', 'ville_nouveau_lieu', 'pays_nouveau_lieu',
                  'descriptionInterview']
        labels = {
            'titreInterview': 'Titre',
            'urlYoutube': 'URL YouTube',
            'urlVimeo': 'URL Vimeo',
            'urlMiniature': 'Miniature (URL de l\'image)',
            'artiste': 'Artiste',
            'dateTournage': 'Date de tournage',
            'lieu': 'Lieu',
            'descriptionInterview': 'Description',
        }
        widgets = {
            'dateTournage': DateFrancaise(),
            'descriptionInterview': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artiste'].required = False
        self.fields['artiste'].empty_label = '— Choisir un artiste —'
        self.fields['lieu'].empty_label = '— Lieu non précisé —'

    def clean(self):
        donnees = super().clean()
        if not donnees.get('artiste') and not donnees.get('nouvel_artiste'):
            self.add_error('artiste', 'Choisissez un artiste dans la liste ou indiquez un nouvel artiste.')
        if not donnees.get('urlYoutube') and not donnees.get('urlVimeo'):
            self.add_error('urlYoutube', 'Indiquez au moins une URL YouTube ou Vimeo.')
        if donnees.get('nouveau_lieu') and not donnees.get('ville_nouveau_lieu'):
            self.add_error('ville_nouveau_lieu', 'Indiquez la ville du nouveau lieu.')
        return donnees

    def save(self, commit=True):
        interview = super().save(commit=False)
        donnees = self.cleaned_data
        if donnees.get('nouvel_artiste'):
            nom = donnees['nouvel_artiste'].strip()
            artiste = Artiste.objects.filter(nomArtiste__iexact=nom).first()
            if artiste is None:
                artiste = Artiste.objects.create(nomArtiste=nom)
            if donnees.get('genres_nouvel_artiste'):
                artiste.genres.add(*donnees['genres_nouvel_artiste'])
            interview.artiste = artiste
        if donnees.get('nouveau_lieu'):
            interview.lieu, _ = Lieu.objects.get_or_create(
                nomLieu=donnees['nouveau_lieu'].strip(),
                villeLieu=donnees['ville_nouveau_lieu'].strip(),
                paysLieu=(donnees.get('pays_nouveau_lieu') or '').strip(),
            )
        if commit:
            interview.save()
        return interview


# --- Extrait ---------------------------------------------------------------------

class ExtraitForm(forms.ModelForm):
    groupes = [
        ('🎬 La vidéo', ['titreExtrait', 'urlYoutube', 'urlVimeo', 'urlMiniature']),
        ("🔗 Place dans l'interview", ['interview', 'ordreSequence', 'timecodeDebut', 'timecodeFin']),
        ('❓ Question', ['question', 'nouvelle_question']),
        ('📝 Transcription', ['transcription']),
    ]
    nouvelle_question = forms.CharField(
        label='… ou nouvelle question', required=False, widget=forms.Textarea(attrs={'rows': 2}),
        help_text="Remplir seulement si la question n'est pas dans la liste")
    timecodeDebut = DureeField(label='Début dans l\'interview', required=False,
                               help_text="Utilisé seulement si l'extrait n'a pas sa propre vidéo. 0 par défaut.")
    timecodeFin = DureeField(label='Fin / durée', required=False)

    class Meta:
        model = Extrait
        fields = ['titreExtrait', 'urlYoutube', 'urlVimeo', 'urlMiniature',
                  'interview', 'question', 'nouvelle_question', 'ordreSequence',
                  'timecodeDebut', 'timecodeFin', 'transcription']
        labels = {
            'titreExtrait': 'Titre',
            'urlYoutube': 'URL YouTube',
            'urlVimeo': 'URL Vimeo',
            'urlMiniature': 'Miniature (URL de l\'image)',
            'interview': 'Interview complète',
            'question': 'Question',
            'ordreSequence': 'N° dans l\'interview',
            'transcription': 'Transcription / description',
        }
        help_texts = {
            'ordreSequence': 'Laisser vide pour le mettre à la suite des autres extraits',
        }
        widgets = {'transcription': forms.Textarea(attrs={'rows': 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].required = False
        self.fields['question'].empty_label = '— Choisir une question —'
        self.fields['interview'].empty_label = '— Choisir une interview —'
        self.fields['ordreSequence'].required = False

    def clean(self):
        donnees = super().clean()
        if not donnees.get('question') and not donnees.get('nouvelle_question'):
            self.add_error('question', 'Choisissez une question dans la liste ou écrivez-en une nouvelle.')
        interview = donnees.get('interview')
        if donnees.get('ordreSequence') is None and interview:
            autres = interview.extraits.exclude(pk=self.instance.pk)
            donnees['ordreSequence'] = (autres.aggregate(m=Max('ordreSequence'))['m'] or 0) + 1
        if donnees.get('timecodeDebut') is None:
            donnees['timecodeDebut'] = 0
        fin = donnees.get('timecodeFin')
        if fin is not None and fin <= donnees['timecodeDebut']:
            self.add_error('timecodeFin', 'La fin doit être après le début.')
        return donnees

    def save(self, commit=True):
        extrait = super().save(commit=False)
        texte = (self.cleaned_data.get('nouvelle_question') or '').strip()
        if texte:
            extrait.question = Question.objects.filter(texteQuestion__iexact=texte).first() \
                or Question.objects.create(texteQuestion=texte)
        if commit:
            extrait.save()
        return extrait


# --- Étape 1 : l'URL ---------------------------------------------------------------

class UrlForm(forms.Form):
    url = forms.CharField(label='URL de la vidéo', widget=forms.TextInput(
        attrs={'placeholder': 'https://youtu.be/…  ou  https://vimeo.com/…', 'autofocus': True}))
