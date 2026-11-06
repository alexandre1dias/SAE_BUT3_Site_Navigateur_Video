# SAE BUT3 - Site Navigateur Vidéo

**Sujet du projet :**
Conception et développement d'une plateforme web interactive de visionnage d'interviews offrant une navigation dynamique et non linéaire.
L'utilisateur peut explorer les vidéos de manière fluide, que ce soit par artiste (lecture linéaire) ou par thématique abordée (lecture transversale).

## Équipe
- DESGRANGES Lucas
- DIAS Alexandre
- DRAME Zakharia
- SCHMIT Clément

---

## Fonctionnalités

- **Mode Lecture** (page d'accueil) : une interview « à la une », des carrousels d'extraits et d'interviews complètes, et des filtres par **genre musical**, **lieu** et **artiste**.
- **Mode Carte Mentale** : un arbre à déplier, *artiste → interview → extraits* (lecture linéaire) et *question → extraits* (lecture transversale).
- **Fiches vidéo dans une fenêtre modale** : chaque interview et chaque extrait a sa fiche, avec des bifurcations (« Même question posée à… », « Voir l'interview complète », extraits suivants). On passe d'une fiche à l'autre sans recharger la page.
- **Lecteur YouTube ou Vimeo** au choix, qui démarre directement au bon timecode pour un extrait.
- **Administration des vidéos** : on colle l'URL d'une vidéo YouTube ou Vimeo et le formulaire se pré-remplit (titre, miniature, durée, description, artiste deviné). Ajout, modification et suppression des interviews et des extraits, avec alerte en cas de doublon.
- **Site responsive** : accueil, carte mentale, modale et administration s'adaptent aux écrans de téléphone.

---

## Stack Technique

### Côté Serveur (Back-end)
- **Framework :** Django 6.1
- **Base de données :** SQLite (via l'ORM Django)
- **Infos vidéo :** oEmbed YouTube / Vimeo (aucune clé d'API nécessaire)

### Côté Client (Front-end)
- **Templates :** Django (tout le HTML est généré côté serveur)
- **Style :** CSS, sans framework
- **Interactions :** JavaScript, sans framework (ouverture des fiches, filtres, carte mentale)
- **Intégration Vidéo :** lecteurs intégrés YouTube & Vimeo (iframe)

### Outils
- **Gestion de version :** Git & GitHub
- **Tests :** tests Django (`manage.py test`)

---

## Lancer le projet (installation automatique)

> ℹ️ **Le code du site se trouve sur la branche `app`**, la branche `main` ne contient que ce README. Avant de lancer le projet, placez-vous sur la branche `app` :
>
> ```bash
> git clone https://github.com/alexandre1dias/SAE_BUT3_Site_Navigateur_Video.git
> cd SAE_BUT3_Site_Navigateur_Video
> git checkout app
> ```
>
> Sur GitHub, vous pouvez aussi choisir la branche `app` dans le menu des branches, puis faire **Code → Download ZIP**.

Prérequis : **Python 3.12 ou plus récent** ([python.org/downloads](https://www.python.org/downloads/)).
Sous Windows, cochez **« Add python.exe to PATH »** pendant l'installation.

| Système | Commande |
| --- | --- |
| Windows | double-cliquer sur `lancer.bat` |
| Linux / macOS | `./lancer.sh` dans un terminal (ou `bash lancer.sh`) |

Le script, à lancer depuis la racine du dépôt (sur la branche `app`) :
1. vérifie que Python 3.12+ est installé ;
2. crée un environnement virtuel `.venv/` (une seule fois, ou le recrée s'il est cassé) ;
3. installe les dépendances de `requirements.txt` ;
4. prépare la base SQLite (`migrate`), la remplit avec les données de démonstration si elle est vide, et crée le compte administrateur s'il n'existe pas ;
5. lance le serveur et ouvre le navigateur sur http://127.0.0.1:8000/

Le script peut être relancé autant de fois que voulu : il réutilise le venv et ne touche pas à une base déjà remplie.
Pour arrêter le site : `Ctrl+C` dans la fenêtre du terminal (ou fermer la fenêtre sous Windows).
Pour repartir d'une base neuve : supprimer `SaeProj/db.sqlite3` puis relancer le script.

Problèmes fréquents :
- *« Python introuvable »* : installer Python 3.12+ (et sous Windows, cocher « Add to PATH »), puis relancer.
- *« Permission denied »* sous Linux/macOS : `chmod +x lancer.sh`.
- *Port 8000 déjà utilisé* : fermer l'autre serveur lancé, ou modifier `PORT=8000` en haut du script.

### Lancement manuel

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cd SaeProj
python manage.py migrate
python manage.py shell -c "from rec117 import peuplement_reel; peuplement_reel.run()"
python manage.py creer_admin
python manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/

> ⚠️ `peuplement_reel.run()` **vide toute la base** avant de la remplir (2 artistes, 4 questions, 2 interviews, 8 extraits, et un utilisateur `testeur` / `password123`).

### Lancer les tests

```bash
cd SaeProj
python manage.py test rec117
```

Les tests simulent les réponses de YouTube et Vimeo : pas besoin d'Internet.

---

## Pages du site

| URL | Page |
| --- | --- |
| `/` | redirige vers `/rec117/` |
| `/rec117/` | Mode Lecture (accueil) |
| `/rec117/mindmap/` | Mode Carte Mentale |
| `/rec117/administration/` | administration des vidéos |
| `/rec117/administration/connexion/` | connexion à l'administration |
| `/rec117/administration/<interview\|extrait>/ajouter/` | ajout d'une vidéo (`?url=…` pour pré-remplir) |
| `/rec117/administration/<interview\|extrait>/<id>/modifier/` | modification |
| `/rec117/administration/<interview\|extrait>/<id>/supprimer/` | suppression (avec confirmation) |
| `/admin/` | administration Django standard (artistes, genres, lieux, questions, comptes) |

---

## Administration

- Compte créé automatiquement par le script : **`admin` / `rec117`** (à changer sur `/admin/` si le site est mis en ligne).
- Le réglage `ADMINISTRATION_OUVERTE` dans `SaeProj/SaeProj/settings.py` décide qui peut gérer les vidéos :
  - `True` (valeur actuelle) : tout le monde, sans connexion, pratique pour les démos ;
  - `False` : seulement les comptes « staff », les autres sont envoyés vers la page de connexion.
- Pour ajouter une vidéo : coller son URL YouTube ou Vimeo dans `/rec117/administration/`, vérifier les champs pré-remplis (badges « ✓ auto »), compléter le reste puis enregistrer. L'artiste, le lieu ou la question peuvent être choisis dans la liste ou créés directement depuis le formulaire.

---

## Structure du projet

```
SAE_BUT3_Site_Navigateur_Video/
├── README.md
├── requirements.txt          ← dépendances (Django 6.1.2, asgiref, sqlparse)
├── lancer.sh / lancer.bat    ← installation + lancement en un clic
└── SaeProj/                  ← projet Django
    ├── manage.py
    ├── SaeProj/              ← configuration (settings.py, urls.py, wsgi.py, asgi.py)
    └── rec117/               ← l'application
        ├── models.py             ← GenreMusical, Artiste, Lieu, Question, Interview, Extrait, ProfilUtilisateur
        ├── urls.py               ← routes de l'application
        ├── views.py              ← pages publiques (accueil, carte mentale)
        ├── views_admin.py        ← administration des vidéos
        ├── forms.py              ← formulaires de l'administration
        ├── infos_video.py        ← récupération automatique des infos YouTube / Vimeo
        ├── peuplement_reel.py    ← données de démonstration
        ├── tests.py              ← tests automatiques
        ├── management/commands/creer_admin.py
        ├── templatetags/videos.py   ← filtres de template (miniature, durée)
        ├── migrations/
        ├── templates/rec117/     ← HTML (pages, partials, administration)
        └── static/rec117/        ← CSS et JavaScript
```

**Modèle de données :** un **extrait** appartient à une **interview** (lecture linéaire) et répond à une **question** (lecture transversale). C'est ce lien qui permet de passer de « la suite de l'interview » à « la même question posée à un autre artiste ».

