from django.views.generic import TemplateView
from SoundFlow.models import GenreMusical, Artiste, Lieu, Question, Interview, Extrait, ProfilUtilisateur


def donnees_pour_js():
    """Toute la base, une liste par table, pour le JavaScript du frontend (data.js).
    .values() renvoie chaque ligne sous forme de dictionnaire, avec les noms des champs du modèle
    (les clés étrangères deviennent artiste_id, lieu_id...).
    Le template l'écrit dans la page avec {{ donnees|json_script:"donnees" }}."""
    return {
        'GENRE_MUSICAL': list(GenreMusical.objects.values()),
        'ARTISTE': list(Artiste.objects.values()),
        'ARTISTE_GENRE': list(Artiste.genres.through.objects.values('artiste_id', 'genremusical_id')),
        'LIEU': list(Lieu.objects.values()),
        'QUESTION': list(Question.objects.values()),
        'INTERVIEW': list(Interview.objects.order_by('idInterview').values()),
        'EXTRAIT': list(Extrait.objects.values()),
    }


class HomeView(TemplateView):
    template_name = "SoundFlow/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Données pour les filtres 
        context['genres'] = GenreMusical.objects.all()
        context['lieux'] = Lieu.objects.all()
        context['artistes'] = Artiste.objects.all()
        
        # Données pour les carrousels 
        context['extraits'] = Extrait.objects.all()
        context['interviews'] = Interview.objects.all()

        # Données pour le JavaScript (home.js, modal.js)
        context['donnees'] = donnees_pour_js()
        
        return context

class MindMapView(TemplateView):
    template_name = "SoundFlow/mindmap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['interviews'] = Interview.objects.all()
        context['extraits'] = Extrait.objects.all()
        context['questions'] = Question.objects.all()

        # Données pour le JavaScript (mindmap.js, modal.js)
        context['donnees'] = donnees_pour_js()
        
        return context
