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
 
## Lancer le projet
 
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
