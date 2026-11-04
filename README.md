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
 
## Stack Technique
 
### Côté Serveur (Back-end)
- **Framework :** Django
- **Base de données :** SQLite (via l'ORM Django)
### Côté Client (Front-end)
- **Templates :** Django
- **Style :** CSS
- **Interactions :** JavaScript
- **Intégration Vidéo :** YouTube & Vimeo
### Outils
- **Gestion de version :** Git & GitHub
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
2. crée un environnement virtuel `.venv/` (une seule fois) ;
3. installe les dépendances de `requirements.txt` ;
4. prépare la base SQLite (`migrate`) et la remplit avec les données de démonstration si elle est vide ;
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
cd SaeProj
python manage.py migrate
python manage.py shell -c "from rec117 import peuplement_reel; peuplement_reel.run()"
python manage.py runserver
```
 
Puis ouvrir http://127.0.0.1:8000/rec117/
 
---

 
## Organisation & Planification
 
Le suivi de l'avancement du projet, la répartition des tâches et le calendrier prévisionnel sont gérés via les outils suivants :
 
- 📋 **[Tableau de bord du projet (GitHub Projects)](https://github.com/users/alexandre1dias/projects/5)**
- 📊 **[Diagramme de Gantt (GanttPro)](https://app.ganttpro.com/#/project/1790688890295/gantt)**
