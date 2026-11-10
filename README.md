
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
- **Interviews complètes en playlist** : une interview complète n'est plus une vidéo à part entière, c'est une **playlist de ses extraits**, lus les uns après les autres dans l'ordre de l'interview.
- **Mode Carte Mentale** : un arbre à déplier, *artiste → interview → extraits* (lecture linéaire) et *question → extraits* (lecture transversale).
- **Fiches vidéo dans une fenêtre modale** : chaque interview et chaque extrait a sa fiche, avec des bifurcations (« Même question posée à… », « Voir l'interview complète », extraits suivants). On passe d'une fiche à l'autre sans recharger la page.
- **Lecteur YouTube ou Vimeo** au choix, qui démarre directement au bon timecode de l'extrait.
- **Administration des vidéos** : on colle l'URL d'une vidéo YouTube ou Vimeo et le formulaire se pré-remplit (titre, miniature, durée, description, artiste deviné). Ajout, modification et suppression des interviews (les playlists) et des extraits (les vidéos), avec alerte en cas de doublon.
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
 
Prérequis : **Python 3.12 ou plus récent** ([python.org/downloads](https://www.python.org/downloads/)).
Sous Windows, cochez **« Add python.exe to PATH »** pendant l'installation.
 
| Système | Commande |
| --- | --- |
| Windows | double-cliquer sur `lancer.bat` |
| Linux / macOS | `./lancer.sh` dans un terminal (ou `bash lancer.sh`) |
 
Le script, à lancer depuis la racine du dépôt :
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
---
 
## Lancement manuel
 
Sans les scripts, depuis la racine du dépôt, avec Python 3.12+ :
 
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
 
Les fois suivantes, il suffit d'activer le venv puis de lancer `python manage.py runserver` depuis `SaeProj/`.
 
> ⚠️ `peuplement_reel.run()` **vide toute la base** avant de la remplir (2 artistes, 4 questions, 2 interviews, 8 extraits, et un utilisateur `testeur` / `password123`).
 
## Lancer les tests
 
```bash
cd SaeProj
python manage.py test rec117
```
 
Les tests simulent les réponses de YouTube et Vimeo : pas besoin d'Internet.
 
---
