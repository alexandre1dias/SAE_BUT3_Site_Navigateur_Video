from django.db import models
from django.contrib.auth.models import User


class GenreMusical(models.Model):
    idGenre = models.AutoField(primary_key=True)
    nomGenre = models.CharField(max_length=100)
    codeCouleur = models.CharField(max_length=7, help_text="Ex: #1DB954")

    def __str__(self):
        return self.nomGenre


class Artiste(models.Model):
    idArtiste = models.AutoField(primary_key=True)
    nomArtiste = models.CharField(max_length=150)

    genres = models.ManyToManyField(GenreMusical, related_name="artistes")

    def __str__(self):
        return self.nomArtiste


class Lieu(models.Model):
    idLieu = models.AutoField(primary_key=True)
    nomLieu = models.CharField(max_length=150)
    villeLieu = models.CharField(max_length=100)
    paysLieu = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nomLieu} ({self.villeLieu})"


class Question(models.Model):
    idQuestion = models.AutoField(primary_key=True)
    texteQuestion = models.TextField()

    def __str__(self):
        return self.texteQuestion[:50]


class Interview(models.Model):
    idInterview = models.AutoField(primary_key=True)
    titreInterview = models.CharField(max_length=200)
    dateTournage = models.DateField(null=True, blank=True)
    descriptionInterview = models.TextField(blank=True, null=True)
    urlYoutube = models.URLField(blank=True, null=True)
    urlVimeo = models.URLField(blank=True, null=True)

    artiste = models.ForeignKey(Artiste, on_delete=models.CASCADE, related_name="interviews")
    lieu = models.ForeignKey(Lieu, on_delete=models.SET_NULL, null=True, blank=True, related_name="interviews")

    def __str__(self):
        return f"{self.artiste.nomArtiste} - {self.titreInterview}"


class Extrait(models.Model):
    idExtrait = models.AutoField(primary_key=True)
    titreExtrait = models.CharField(max_length=200)
    ordreSequence = models.PositiveIntegerField(help_text="Ordre dans l'interview")
    timecodeDebut = models.PositiveIntegerField(default=0, help_text="En secondes")
    timecodeFin = models.PositiveIntegerField(null=True, blank=True, help_text="En secondes")
    urlYoutube = models.URLField(blank=True, null=True)
    urlVimeo = models.URLField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True, help_text="Retranscription pour la recherche")

    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name="extraits")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="extraits")

    class Meta:
        ordering = ["ordreSequence"]
        unique_together = ("interview", "ordreSequence")

    def __str__(self):
        return f"{self.interview.artiste.nomArtiste} - Q: {self.question.texteQuestion[:30]}"


class ProfilUtilisateur(models.Model):
    idProfil = models.AutoField(primary_key=True)
    CHOIX_LECTEUR = [
        ("YOUTUBE", "YouTube"),
        ("VIMEO", "Vimeo"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    lecteurPrefere = models.CharField(max_length=10, choices=CHOIX_LECTEUR, default="YOUTUBE")

    def __str__(self):
        return f"Profil de {self.user.username}"

