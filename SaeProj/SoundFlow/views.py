from django.views.generic import TemplateView
from SoundFlow.models import GenreMusical, Artiste, Lieu, Question, Interview, Extrait, ProfilUtilisateur

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
        
        return context

class MindMapView(TemplateView):
    template_name = "SoundFlow/mindmap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['interviews'] = Interview.objects.all()
        context['extraits'] = Extrait.objects.all()
        context['questions'] = Question.objects.all()
        
        return context