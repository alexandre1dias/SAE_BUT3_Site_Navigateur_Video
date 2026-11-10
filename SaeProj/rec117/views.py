from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse

from rec117.forms import InscriptionForm
from rec117.models import GenreMusical, Artiste, Lieu, Question, Interview, Extrait


class ConnexionUtilisateurView(LoginView):
    template_name = "rec117/administration/connexion_utilisateur.html"
    redirect_authenticated_user = True

    def get_default_redirect_url(self):
        return reverse("home")


class HomeView(TemplateView):
    template_name = "rec117/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Données pour les filtres
        context['genres'] = GenreMusical.objects.all()
        context['lieux'] = Lieu.objects.all()
        context['artistes'] = Artiste.objects.all()

        # Données pour les carrousels et les fiches de la modale
        context['extraits'] = Extrait.objects.all()
        context['interviews'] = Interview.objects.order_by('idInterview')

        # Interview à la une : la dernière ajoutée en base
        context['interview_a_la_une'] = Interview.objects.order_by('idInterview').last()

        return context


class MindMapView(TemplateView):
    template_name = "rec117/mindmap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Données pour les branches de la carte
        context['artistes'] = Artiste.objects.all()
        context['questions'] = Question.objects.all()

        # Données pour les fiches de la modale
        context['interviews'] = Interview.objects.order_by('idInterview')
        context['extraits'] = Extrait.objects.all()

        return context


def inscription(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = InscriptionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        utilisateur = form.save()
        login(request, utilisateur)
        return redirect('home')

    return render(request, 'rec117/administration/inscription.html', {'form': form})
