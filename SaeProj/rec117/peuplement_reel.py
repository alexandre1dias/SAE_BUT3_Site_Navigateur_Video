import datetime
from django.contrib.auth.models import User

# Remplace 'app' par le nom de ton application Django (ex: 'videos')
from .models import (
    GenreMusical,
    Artiste,
    Lieu,
    Question,
    Interview,
    Extrait,
    ProfilUtilisateur,
)


def run():
    print("=== Population de la base avec les liens réels (Rivkah & Gontard) ===")

    # 1. Nettoyage de la base
    Extrait.objects.all().delete()
    Interview.objects.all().delete()
    Question.objects.all().delete()
    Lieu.objects.all().delete()
    Artiste.objects.all().delete()
    GenreMusical.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    print("[1/6] Anciennes données supprimées.")

    # 2. Genres & Couleurs musicales
    pop_indie = GenreMusical.objects.create(nomGenre="Pop / Indie", codeCouleur="#EC4899")
    chanson_rock = GenreMusical.objects.create(nomGenre="Chanson / Rock", codeCouleur="#E50914")

    print("[2/6] Genres musicaux créés.")

    # 3. Artistes
    rivkah = Artiste.objects.create(nomArtiste="Rivkah")
    rivkah.genres.add(pop_indie)

    gontard = Artiste.objects.create(nomArtiste="Gontard")
    gontard.genres.add(chanson_rock)

    print("[3/6] Artistes Rivkah et Gontard créés.")

    # 4. Lieu de tournage
    lieu = Lieu.objects.create(
        nomLieu="Studio d'enregistrement",
        villeLieu="Orléans",
        paysLieu="France"
    )

    # 5. Questions croisées (communes aux 2 artistes)
    q1 = Question.objects.create(
        texteQuestion="Question 1 : Présentation et univers musical"
    )
    q2 = Question.objects.create(
        texteQuestion="Question 2 : Processus de création et écriture"
    )
    q3 = Question.objects.create(
        texteQuestion="Question 3 : Rapport à la scène et au public"
    )
    q4 = Question.objects.create(
        texteQuestion="Question 4 : Projets futurs et mot de la fin"
    )

    print("[4/6] 4 questions croisées créées.")

    # 6. Interview Rivkah
    interview_rivkah = Interview.objects.create(
        titreInterview="Interview Rivkah",
        dateTournage=datetime.date(2025, 1, 15),
        descriptionInterview="Interview complète de Rivkah décortiquée en 4 extraits.",
        urlYoutube="https://youtu.be/1NYQ65FTEC8",
        urlVimeo="https://vimeo.com/1128762950",
        artiste=rivkah,
        lieu=lieu,
    )

    extraits_rivkah = [
        {
            "titre": "Rivkah - Extrait 1",
            "ordre": 1,
            "question": q1,
            "vimeo": "https://vimeo.com/1128762950",
            "youtube": "https://youtu.be/1NYQ65FTEC8",
        },
        {
            "titre": "Rivkah - Extrait 2",
            "ordre": 2,
            "question": q2,
            "vimeo": "https://vimeo.com/1128763050",
            "youtube": "https://youtu.be/ux6ZtL1o0R0",
        },
        {
            "titre": "Rivkah - Extrait 3",
            "ordre": 3,
            "question": q3,
            "vimeo": "https://vimeo.com/1128763155",
            "youtube": "https://youtu.be/WpFoiw2uP0w",
        },
        {
            "titre": "Rivkah - Extrait 4",
            "ordre": 4,
            "question": q4,
            "vimeo": "https://vimeo.com/1128763765",
            "youtube": "https://youtu.be/2PDvQ3P8c64",
        },
    ]

    for data in extraits_rivkah:
        Extrait.objects.create(
            titreExtrait=data["titre"],
            ordreSequence=data["ordre"],
            timecodeDebut=0,
            urlVimeo=data["vimeo"],
            urlYoutube=data["youtube"],
            transcription=f"Transcription de l'extrait {data['ordre']} de Rivkah.",
            interview=interview_rivkah,
            question=data["question"],
        )

    # 7. Interview Gontard
    interview_gontard = Interview.objects.create(
        titreInterview="Interview Gontard",
        dateTournage=datetime.date(2025, 1, 15),
        descriptionInterview="Interview complète de Gontard décortiquée en 4 extraits.",
        urlYoutube="https://youtu.be/9eLoUEBF6no",
        urlVimeo="https://vimeo.com/1128786403",
        artiste=gontard,
        lieu=lieu,
    )

    extraits_gontard = [
        {
            "titre": "Gontard - Extrait 1",
            "ordre": 1,
            "question": q1,
            "vimeo": "https://vimeo.com/1128786403",
            "youtube": "https://youtu.be/9eLoUEBF6no",
        },
        {
            "titre": "Gontard - Extrait 2",
            "ordre": 2,
            "question": q2,
            "vimeo": "https://vimeo.com/1128786928",
            "youtube": "https://youtu.be/Wt14RXtzZxI",
        },
        {
            "titre": "Gontard - Extrait 3",
            "ordre": 3,
            "question": q3,
            "vimeo": "https://vimeo.com/1128788337",
            "youtube": "https://youtu.be/IqLw5KDf9Fg",
        },
        {
            "titre": "Gontard - Extrait 4",
            "ordre": 4,
            "question": q4,
            "vimeo": "https://vimeo.com/1128790175",
            "youtube": "https://youtu.be/uwIyaln-k8A",
        },
    ]

    for data in extraits_gontard:
        Extrait.objects.create(
            titreExtrait=data["titre"],
            ordreSequence=data["ordre"],
            timecodeDebut=0,
            urlVimeo=data["vimeo"],
            urlYoutube=data["youtube"],
            transcription=f"Transcription de l'extrait {data['ordre']} de Gontard.",
            interview=interview_gontard,
            question=data["question"],
        )

    print("[5/6] 2 interviews et 8 extraits créés.")

    # 8. Création d'un utilisateur de test
    user, created = User.objects.get_or_create(username="testeur", email="testeur@example.com")
    if created:
        user.set_password("password123")
        user.save()
        ProfilUtilisateur.objects.create(user=user, lecteurPrefere="YOUTUBE")

    print("[6/6] Utilisateur 'testeur' créé (mot de passe: password123).")
    print("=== Base de données peuplée avec succès ! ===")


if __name__ == "__main__":
    run()