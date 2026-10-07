from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from urllib.parse import unquote
from django.urls import reverse
from django.core.cache import cache
from django.core.paginator import Paginator
from neomodel import db
import re
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.
from .forms import CreateVideoForm
from .models import *
from .utils import get_youtube_infos, get_vimeo_infos, get_video_transcript, seconds_to_hms
from django.contrib.auth import authenticate, login, logout
from typing import List
from django.core.handlers.wsgi import WSGIRequest


def get_videos_with_thumbnails(videos: List[Video]):
    videos_with_thumbnails = [video for video in videos if video.link and 'youtu' in video.link]
    return videos_with_thumbnails

def get_videos_with_thumbnails_home(videos: List[Video]):
    videos_with_thumbnails = [video for video in videos if video.link and 'youtube.com' in video.link]
    return videos_with_thumbnails

class HomeView(TemplateView):
    template_name = "home.html"


    def get_context_data(self, **kwargs):
        videos = Video.nodes.all()
        videos_with_thumbnails = get_videos_with_thumbnails_home(videos)

        interviews = Interview.nodes.all()

        artists = Artist.nodes.all()
        authors = Author.nodes.all()
        themes = Theme.nodes.all()

        artist_names = [artist.name for artist in artists]
        author_names = [author.name for author in authors]
        theme_names = [theme.name for theme in themes]

        context = super(HomeView, self).get_context_data(**kwargs)
        context["videos_with_thumbnails"] = videos_with_thumbnails
        context["filtersData"] = {
            "artist": artist_names,
            "author": author_names,
            "theme": theme_names
        }
        context["param"] = self.kwargs.get("param", "")
        context["interviews"] = interviews
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)


def get_artists(request):
    artists = Artist.nodes.all()
    # print(type(artists))
    return render(request, 'artists.html', {'artists': artists})


def get_graph_data(request):
    # Utilisation d'un cache pour éviter les calculs redondants
    graph_data = cache.get('graph_data')
    if not graph_data:
        # Récupérer toutes les données avec une requête Cypher optimisée
        results, _ = db.cypher_query(Query.GRAPH)

        nodes = []
        edges = []

        for node_data, rels, targets in results:
            # Extraire les informations du nœud
            node_id = node_data.element_id  # Utiliser l'attribut element_id pour l'ID
            node_labels = list(node_data.labels)  # Labels pour déterminer le type
            node_properties = dict(node_data)  # Convertir les propriétés en dictionnaire

            # Déterminer un label significatif pour le type
            node_type = node_labels[0] if node_labels else "Unknown"
            print(node_type)
            # Ajouter le nœud à la liste
            nodes.append({
                'id': node_id,
                'label': node_properties.get('title') or node_properties.get('name', 'Unknown'),
                'type': node_type,
                'properties': node_properties
            })

            # Traiter les relations et cibles
            for rel, target in zip(rels, targets):
                target_id = target.element_id  # ID cible
                edges.append({
                    'source': node_id,
                    'target': target_id,
                    'type': rel.type  # Type de la relation
                })

        #print(nodes)
        #print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        #print(edges)
        graph_data = {'nodes': nodes, 'edges': edges}
        cache.set('graph_data', graph_data, timeout=3600)

    return JsonResponse(graph_data, safe=False)


def get_video(request: WSGIRequest, video_id):
    video = Video(element_id_property=video_id)
    video.refresh()
    #video.update_views()

    context = {}
    
    if not video:
        return render(request, '404.html', status=404)
    else:
        context['id'] = video.element_id_property
        context['title'] = video.get_title()
        context['youtube_id'] = video.get_link_id()
        context['artist'] = video.artist.single().name
        context['question'] = video.question.single().titled
        context['answer'] = video.transcription
        context['interview'] = video.interview.single().element_id_property

    if 'playlist' not in request.session:
        request.session['playlist'] = {
            'current': 0,
            'list': [video.to_playlist()]
        }
    elif video.to_playlist() not in request.session['playlist']['list']:
        request.session['playlist']['list'].append(video.to_playlist())
    
    context['playlist'] = request.session['playlist']
    return render(request, 'lecteur.html', context)

def artist_detail(request, node_id):
    artist = Artist(element_id_property=node_id)
    artist.refresh()
    
    styles = artist.styles.all()
    videos = artist.get_videos()

    videos_with_thumbnails = get_videos_with_thumbnails(videos)

    # Pagination : 3 vidéos par page
    paginator = Paginator(videos_with_thumbnails, 3)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    print(videos_with_thumbnails)

    return render(request, 'artist_detail.html', {
        'artist': artist,
        'styles': styles,
        'page_obj': page_obj
    })

def theme_detail(request, node_id):

    print(node_id)
    # Rechercher le thème dans la base de données
    theme = Theme(element_id_property=node_id)
    theme.refresh()
    
    print(theme)

    videos = theme.get_videos()

    print(videos)

    videos_with_thumbnails = get_videos_with_thumbnails(videos)

    # Pagination : 3 vidéos par page
    paginator = Paginator(videos_with_thumbnails, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    # Renvoyer la page avec les détails du thème
    return render(request, 'theme_detail.html', {
        'theme': theme,
        'page_obj': page_obj
        })

def watch_interview(request, interview_id):
    interview = Interview(element_id_property=interview_id)
    interview.refresh()

    videos: List[Video] = interview.videos.all()
    videos.sort(key=lambda v: v.position)

    request.session['playlist'] = {
        'current': 0,
        'list': [video.to_playlist() for video in videos]
    } 

    return redirect('lecteur', video_id=request.session['playlist']['list'][0].get('id'))


def api_search(request):
    # Récupérer les termes de recherche
    search_term = request.GET.get('term', None)
    
    # Recherche dans les vidéos, les auteurs et les artistes
    interviews = Interview.nodes.filter(title__icontains=search_term)
    authors = Author.nodes.filter(name__icontains=search_term)
    artists = Artist.nodes.filter(name__icontains=search_term)
    
    # Créer une liste de résultats
    results = {
        'videos': [],
        'authors': [],
        'artists': []
    }
    
    # Ajouter les vidéos correspondantes
    for video in interviews:
        results['videos'].append({
            'id': video.element_id_property,
            'label': video.title,
            'url': f'/interview/{video.element_id_property}/'
        })

    # Ajouter les auteurs correspondants
    for author in authors:
        results['authors'].append({
            'id': author.element_id_property,
            'label': author.name,
            'url': author.website
        })
    
    # Ajouter les artistes correspondants
    for artist in artists:
        results['artists'].append({
            'id': artist.element_id_property,
            'label': artist.name,
            'url': f'/artist/{artist.element_id_property}'
        })
    
    return JsonResponse(results, safe=False)
@staff_member_required
def download_transcription(request, url):
    # Décoder l'URL encodée
    original_url = unquote(url)

    # Récupérer l'ID de la vidéo
    id_video = extraire_id_video(original_url)

    # Récupérer la transcription
    transcription = get_video_transcript(id_video)
    if transcription:
        response = HttpResponse(
            transcription,
            content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = (
            f'attachment; filename="transcription.txt"'
        )
        return response
    else:
        return HttpResponse("Aucune transcription disponible.", status=404)
    
@staff_member_required
def add_interview(request):
    if request.method == 'POST':
        author_id = request.POST.get('author')
        title = request.POST.get('title')
        visibility = request.POST.get('visibility')
        
        # lier l'interview à son autheur et sa source
        interview = Interview(title=title, visibility=visibility)
        host = Host(name="Youtube")
        interview.save()
        interview.is_from.connect(host)
        author = Author(element_id_property=author_id)
        interview.author.connect(author)
        interview.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
@staff_member_required
def add_author(request):
    if request.method == 'POST':
        author_name = request.POST.get('name')
        author = Author(name=author_name)
        author.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
@staff_member_required   
def chose_interview(request):
    interviews = Interview.nodes.all()
    hosts = Host.nodes.all()
    authors = Author.nodes.all()
    if request.method == 'POST':
        interview_id = request.POST.get('interview')
        return redirect('create_video', interview_id=interview_id)
    return render(request, "chose_interview.html",{"interviews":interviews,"hosts":hosts, "authors":authors})
    


@staff_member_required
def create_video(request, interview_id):
    artists = Artist.nodes.all()
    styles = Musical_style.nodes.all()
    themes = Theme.nodes.all()
    questions = Question.nodes.all()
    if request.method == 'POST':
        question_id = request.POST.get('question')
        artist_id = request.POST.get('artist')
        link  = request.POST.get('link')
        transcription = request.POST.get('transcription')
        
        interview = Interview(element_id_property=interview_id)
        question = Question(element_id_property =question_id)
        artist = Artist(element_id_property=artist_id)
    
        
        infos = get_youtube_infos(link)
        
        if infos == None:
            pass
        else:
            position = interview.get_total_videos() +1
            video = Video(link=link, duration=infos["duration"], transcription=transcription, position =position )
            video.save()
            video.interview.connect(interview)
            video.question.connect(question)
            video.artist.connect(artist)
            video.save()
            return redirect('update_interview', interview_id=interview_id)
    
    return render(request, "create_video.html",{"interview_id": interview_id,"questions":questions, "themes":themes, "artists":artists,"styles":styles})
    
@staff_member_required
def update_interview(request, interview_id):
    authors = Author.nodes.all()
    
    interview = Interview(element_id_property=interview_id)
    interview.refresh()
    videos = sorted(interview.videos.all(), key=lambda video: video.position)
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = Author(element_id_property=  author_id)
        visibility = request.POST.get('visibility') 
        
        interview.title = title
        interview.author.disconnect_all()
        interview.author.connect(author)
        interview.visibility = visibility 
        interview.save()
        interview.refresh()
         
    return render(request, "update_interview.html", {"interview": interview, "videos": videos, "authors":authors})


@staff_member_required
def update_video(request, video_id):
    # Récupérer la vidéo à partir de son `element_id`
    video = Video(element_id_property=video_id)
    video.refresh()
    
    artists = Artist.nodes.all()
    questions = Question.nodes.all()
    styles = Musical_style.nodes.all()
    themes = Theme.nodes.all()
    
    context={}
    context["video"]= video
    context["artists"]= artists
    context["questions"]= questions
    context["styles"]= styles
    context["themes"]= themes
    
    if request.method == "POST":
        transcription = request.POST.get('transcription')
        artist_id = request.POST.get('artist')
        question_id = request.POST.get('question')
        
        artist = Artist(element_id_property=artist_id)
        question = Question(element_id_property=question_id)
        video.transcription = transcription
        video.artist.disconnect_all()
        video.question.disconnect_all()
        video.artist.connect(artist)
        video.question.connect(question)
        video.save()
        video.refresh()
    return render(request, "update_video.html", context)

@staff_member_required
def add_question(request):
    if request.method == 'POST':
        titled = request.POST['titled']
        theme_ids = request.POST.getlist('themes')
        question = Question(titled=titled)
        question.save()
        
        # Ajouter des relations avec les thèmes
        for theme_id in theme_ids:
            theme = Theme(element_id_property=theme_id)
            question.themes.connect(theme)
        
        return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirection vers la page précédente
    
@staff_member_required
def add_artist(request):
    if request.method == 'POST':
        name = request.POST['name']
        website = request.POST['website']
        style_id = request.POST['style']
        
        artist = Artist(name=name, website=website)
        artist.save()
        artist.refresh()

        style = Musical_style(element_id_property=style_id)
        style.refresh()
        artist.styles.connect(style)
        return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirection vers la page précédente
    
@staff_member_required
def add_theme(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # Créer un nouveau thème
            theme = Theme(name=name)
            theme.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
@staff_member_required
def add_style(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            # Créer un nouveau thème
            style = Musical_style(name=name)
            style.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Replace 'home' with the name of your home page URL
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    else:
        return render(request, 'login.html')
    

def logout_view(request):
    logout(request)
    return redirect('home') # Replace 'login' with the name of your login 

def clear_graph_cache(request):
    if request.method == "POST":
        # Supprimer la clé 'graph_data' du cache
        cache.delete('graph_data')
        return JsonResponse({'status': 'success', 'message': 'Cache cleared successfully.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
