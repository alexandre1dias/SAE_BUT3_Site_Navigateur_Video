import datetime
from django.contrib.auth.models import User
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
    print("=== Début de la population de test élargie ===")

    # 1. Nettoyage
    Extrait.objects.all().delete()
    Interview.objects.all().delete()
    Question.objects.all().delete()
    Lieu.objects.all().delete()
    Artiste.objects.all().delete()
    GenreMusical.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    print("[1/6] Base réinitialisée.")

    # 2. Genres & Couleurs musicales
    rock = GenreMusical.objects.create(nomGenre="Rock", codeCouleur="#E50914")
    jazz = GenreMusical.objects.create(nomGenre="Jazz", codeCouleur="#1DB954")
    electro = GenreMusical.objects.create(nomGenre="Électro", codeCouleur="#3B82F6")
    hiphop = GenreMusical.objects.create(nomGenre="Hip-Hop", codeCouleur="#F59E0B")
    pop = GenreMusical.objects.create(nomGenre="Pop", codeCouleur="#EC4899")

    print("[2/6] 5 genres créés.")

    # 3. Lieux
    paris = Lieu.objects.create(nomLieu="Studio Gabriel", villeLieu="Paris", paysLieu="France")
    londres = Lieu.objects.create(nomLieu="Abbey Road Studios", villeLieu="Londres", paysLieu="Royaume-Uni")
    berlin = Lieu.objects.create(nomLieu="Funkhaus Berlin", villeLieu="Berlin", paysLieu="Allemagne")
    ny = Lieu.objects.create(nomLieu="Electric Lady Studios", villeLieu="New York", paysLieu="États-Unis")

    print("[3/6] 4 lieux créés.")

    # 4. Artistes
    a1 = Artiste.objects.create(nomArtiste="Miles Davis Tribute (Jazz)")
    a1.genres.add(jazz)

    a2 = Artiste.objects.create(nomArtiste="Daft Vibe (Électro)")
    a2.genres.add(electro)

    a3 = Artiste.objects.create(nomArtiste="The Rockers (Rock)")
    a3.genres.add(rock)

    a4 = Artiste.objects.create(nomArtiste="MC Lyricist (Hip-Hop)")
    a4.genres.add(hiphop)

    a5 = Artiste.objects.create(nomArtiste="Clara Pop (Pop)")
    a5.genres.add(pop)

    a6 = Artiste.objects.create(nomArtiste="Fusion Band (Jazz/Rock)")
    a6.genres.add(jazz, rock)

    print("[4/6] 6 artistes créés.")

    # 5. Questions récurrentes (socle des carrefours)
    q1 = Question.objects.create(
        texteQuestion="Comment commences-tu ton processus de composition ?"
    )
    q2 = Question.objects.create(
        texteQuestion="Quelle est ta plus grande source d'inspiration sur scène ?"
    )
    q3 = Question.objects.create(
        texteQuestion="Comment perçois-tu l'évolution du streaming aujourd'hui ?"
    )
    q4 = Question.objects.create(
        texteQuestion="Quel est le tout premier morceau qui t'a donné envie de faire de la musique ?"
    )
    q5 = Question.objects.create(
        texteQuestion="Comment gères-tu le doute ou le blocage créatif ?"
    )

    print("[5/6] 5 questions croisées créées.")

    # 6. Interviews & Extraits
    dataset_interviews = [
        {
            "artiste": a1,
            "titre": "Miles Davis Tribute - L'art de l'improvisation",
            "date": datetime.date(2025, 1, 10),
            "lieu": paris,
            "extraits": [
                (1, q1, "L'improvisation au piano", 0, 90, "Je pose mes mains sur les touches sans réfléchir et je laisse la mélodie venir."),
                (2, q2, "La complicité avec les musiciens", 91, 180, "C'est l'écoute mutuelle entre la trompette et la batterie qui crée la magie."),
                (3, q4, "Kind of Blue de Miles", 181, 260, "So What a changé ma vision de l'harmonie quand j'avais 12 ans."),
                (4, q5, "Accepter les erreurs", 261, 340, "En jazz, il n'y a pas de fausses notes, seulement des résolutions inattendues.")
            ]
        },
        {
            "artiste": a2,
            "titre": "Daft Vibe - Dans les coulisses des machines",
            "date": datetime.date(2025, 2, 14),
            "lieu": berlin,
            "extraits": [
                (1, q1, "Les synthétiseurs modulaires", 0, 110, "Tout commence par la recherche d'une texture sonore ou d'une ligne de basse."),
                (2, q3, "La musique accessible partout", 111, 200, "Le streaming permet à un morceau produit dans sa chambre d'être écouté à Tokyo."),
                (3, q5, "Changer de machine", 201, 290, "Quand je bloque, je change de synthétiseur ou je sors marcher.")
            ]
        },
        {
            "artiste": a3,
            "titre": "The Rockers - Le son des amplis",
            "date": datetime.date(2025, 3, 5),
            "lieu": londres,
            "extraits": [
                (1, q1, "Le riff de guitare", 0, 100, "Un bon riff brut sur une guitare acoustique, si ça marche là, ça marchera en électrique."),
                (2, q2, "L'énergie du public", 101, 195, "Sentir la foule sauter à l'unisson donne une adrénaline impossible à retrouver ailleurs."),
                (3, q4, "Back in Black d'AC/DC", 196, 275, "Le premier coup de médiator sur cette intro m'a marqué à vie.")
            ]
        },
        {
            "artiste": a4,
            "titre": "MC Lyricist - La plume et le rythme",
            "date": datetime.date(2025, 3, 20),
            "lieu": ny,
            "extraits": [
                (1, q1, "Écrire sur une prod", 0, 85, "J'écoute le beat en boucle pendant des heures avant d'écrire un seul mot."),
                (2, q3, "Les playlists et les algorithmes", 86, 175, "Il faut sortir des singles souvent mais ne jamais sacrifier l'écriture."),
                (3, q4, "N.Y. State of Mind de Nas", 176, 255, "La poésie de ce morceau m'a montré qu'un texte pouvait être du cinéma.")
            ]
        },
        {
            "artiste": a5,
            "titre": "Clara Pop - La voix et l'émotion",
            "date": datetime.date(2025, 4, 2),
            "lieu": paris,
            "extraits": [
                (1, q1, "Mélodie piano-voix", 0, 95, "Je fredonne des idées sur le dictaphone de mon téléphone au quotidien."),
                (2, q2, "Les regards au premier rang", 96, 185, "Voir les gens chanter mes paroles en cœur me donne la force d'être vulnérable."),
                (3, q5, "Prendre du recul", 186, 270, "Si la chanson ne vient pas en deux heures, je ferme le piano et je reviens le lendemain.")
            ]
        },
        {
            "artiste": a6,
            "titre": "Fusion Band - Entre deux mondes",
            "date": datetime.date(2025, 4, 18),
            "lieu": berlin,
            "extraits": [
                (1, q2, "L'improvisation collective sur scène", 0, 120, "On ne sait jamais exactement comment le morceau va se terminer en concert."),
                (2, q3, "L'accès illimité au catalogue mondial", 121, 210, "Les jeunes écoutent du rock des années 70 et de l'électro dans la même heure."),
                (3, q4, "Shine On You Crazy Diamond de Pink Floyd", 211, 310, "Cette montée progressive nous a appris à prendre notre temps.")
            ]
        }
    ]

    count_extraits = 0
    for data in dataset_interviews:
        interview = Interview.objects.create(
            titreInterview=data["titre"],
            dateTournage=data["date"],
            descriptionInterview=f"Interview de {data['artiste'].nomArtiste} tournée à {data['lieu'].nomLieu}.",
            urlYoutube="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            urlVimeo="https://vimeo.com/76979871",
            artiste=data["artiste"],
            lieu=data["lieu"]
        )

        for seq, q, titre, debut, fin, txt in data["extraits"]:
            Extrait.objects.create(
                titreExtrait=titre,
                ordreSequence=seq,
                timecodeDebut=debut,
                timecodeFin=fin,
                urlYoutube="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                urlVimeo="https://vimeo.com/76979871",
                transcription=txt,
                interview=interview,
                question=q
            )
            count_extraits += 1

    print(f"[6/6] {len(dataset_interviews)} interviews et {count_extraits} extraits créés.")

    # 7. Utilisateurs de test
    u1, _ = User.objects.get_or_create(username="enseignant1", email="prof@ecole.fr")
    u1.set_password("prof123")
    u1.save()
    ProfilUtilisateur.objects.get_or_create(user=u1, lecteurPrefere="YOUTUBE")

    u2, _ = User.objects.get_or_create(username="fan_musique", email="fan@music.com")
    u2.set_password("fan123")
    u2.save()
    ProfilUtilisateur.objects.get_or_create(user=u2, lecteurPrefere="VIMEO")

    print("=== Population de test terminée avec succès ! ===")

if __name__ == "__main__":
    run()