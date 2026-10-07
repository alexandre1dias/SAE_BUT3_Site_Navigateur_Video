from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .queries import Query
import re
from yt_dlp import YoutubeDL
from neomodel import (
    StructuredNode,
    StringProperty,
    FloatProperty,
    IntegerProperty,
    RelationshipTo,
    RelationshipFrom,
    db,
    UniqueIdProperty,
    #StructuredRel,
)

# Create your models here.
class Admin(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True)

@receiver(post_save, sender=User)
def sync_with_neo4j(sender, instance, created, **kwargs):
    if created:
        Admin(username=instance.username).save()

class Interview(StructuredNode):
    title = StringProperty(required=True)
    visibility = IntegerProperty(required=True) # 0: public, 1: private, 2+: on vera plus tard

    is_from = RelationshipTo('Host', 'HOSTED_ON')
    author = RelationshipTo('Author', 'PUBLISHED_BY')
    videos = RelationshipTo('Video', 'CONTAINS')

    def get_thumbnail(self):
        return self.videos.single().get_thumbnail()

    def get_themes(self):
        results, _ = db.cypher_query(Query.INTERVIEWS_THEMES, {"video_id": self.element_id_property})

        themes = [Theme.inflate(row[0]) for row in results]
        return themes
    
    def get_duration(self) -> int:
        return sum([video.duration for video in self.videos.all()])

    def get_readable_duration(self) -> str:
        """
        Convertit la durée en secondes au format lisible (heures, minutes, secondes).

        Returns :
        str : Une chaîne représentant la durée dans un format lisible, comme "2 min" ou "1h 1 min 10s".
        """
        seconds = self.get_duration()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes} min")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")

        return " ".join(parts)

    def get_artists(self):
        results, _ = db.cypher_query(Query.INTERVIEWS_ARTISTS, {"video_id": self.element_id_property})

        artists = [Artist.inflate(row[0]) for row in results]
        return artists
    
    def get_total_videos(self):
        return len(self.videos.all())
    
    def get_author(self):
        return self.author.single()

class Host(StructuredNode):
    name = StringProperty(required=True)
    interviews = RelationshipFrom('Interview', 'HOSTED_ON')

class Author(StructuredNode):
    name = StringProperty(required=True)
    website = StringProperty()
    interviews = RelationshipFrom('Interview', 'PUBLISHED_BY')

class Video(StructuredNode):    
    transcription = StringProperty(required=True)
    link = StringProperty(required=True)
    position = IntegerProperty(required=True)
    duration = IntegerProperty(required=True)
    count_views = IntegerProperty(required=True)
    artist = RelationshipFrom('Artist', 'RESPONDS')
    interview = RelationshipFrom('Interview', 'CONTAINS')
    question = RelationshipFrom('Question', 'HAS_ANSWERS')
    def is_popular(self):
        return self.count_views >= 4 
    def update_views(self):
        ydl_opts = {}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.link, download=False)
            views = info.get("view_count", 0)
            self.count_views = views
            self.save()
    def get_artist_name(self):
        return self.artist.single().name
    
    def get_question_titled(self):
        return self.question.single().titled

    def get_host_name(self):
        return self.interview.single().host.single().name

    def get_author(self):
        results, _ = db.cypher_query(Query.VIDEO_AUTHOR, {"video_id": self.element_id_property})
        author = Author.inflate(results[0][0])
        return author
    def get_themes(self):
        results, _ = db.cypher_query(Query.VIDEO_THEMES, {"video_id": self.element_id_property})

        themes = [Theme.inflate(row[0]) for row in results]
        return themes
    
    def get_title(self):
        return f"{self.interview.single().title} - {self.position}/{self.interview.single().get_total_videos()}"
    
    def get_readable_duration(self) -> str:
        seconds = self.duration
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes} min")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")

        return " ".join(parts)

    def get_thumbnail(self):
        if "youtube.com" not in self.link and "youtu.be" not in self.link:
            return None
        video_id = self.get_link_id()
        return f"https://img.youtube.com/vi/{video_id}/0.jpg"
    
    def get_link_id(self):
        if "youtube.com" not in self.link and "youtu.be" not in self.link:
            return None
        match = re.search(r'(?:youtu\.be/|v=)([a-zA-Z0-9_-]{11})', self.link) # Regex ID vidéo ( lien youtube.com/watch?v=... ou youtu.be/... )
        if not match:
            return None
        return match.group(1)
    
    def to_playlist(self):
        return {
            "id": self.element_id_property,
            "title": self.get_title(),
            "thumbnail": self.get_thumbnail(),
            "duration": self.get_readable_duration()
        }

class Question(StructuredNode):
    titled = StringProperty(required=True)

    videos = RelationshipTo('Video', 'HAS_ANSWERS')
    themes = RelationshipTo('Theme', 'IS_THEMED')

class Theme(StructuredNode):
    name = StringProperty(required=True)

    questions = RelationshipFrom('Question', 'IS_THEMED')

    def get_videos(self):
        results, _ = db.cypher_query(Query.THEME_VIDEOS, {"theme_id": self.element_id_property})

        videos = [Video.inflate(row[0]) for row in results]
        return videos 

class Artist(StructuredNode):
    name = StringProperty(required=True)
    website = StringProperty()

    answers = RelationshipTo('Video', 'RESPONDS')
    styles = RelationshipTo('Musical_style', 'HAS_STYLE')
    
    def get_videos(self):
        results, _ = db.cypher_query(Query.ARTIST_VIDEOS, {"artist_id": self.element_id_property})
        
        videos = [Video.inflate(row[0]) for row in results]
        return videos
    def get_prefered_theme(self):
        try:
            results, _ = db.cypher_query(Query.ARTIST_PREFERRED_THEMES, {"artist_id": self.element_id_property})
            if results and results[0][0]:
                theme = Theme.inflate(results[0][0])
                return theme
            
            return "Pas encore de theme"
        except Exception as e:
            print(f"Erreur lors de la récupération du thème : {e}")
            return "Pas encore de theme"
    

class Musical_style(StructuredNode):
    name = StringProperty(required=True)
    artists = RelationshipFrom('Artist', 'HAS_STYLE')
