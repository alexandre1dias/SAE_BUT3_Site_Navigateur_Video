# SAE_BUT3
Navigateur de contenus vidéos

Monorepo contenant le service backend et le service frontend

## Installation et lancement local

### Prérequis
- Python 3.8+ et pip
- Node.js 16+ et npm
- Serveur Neo4j (optionnel, pour tester en local)

### Configuration initiale

#### 1. **Installer les dépendances** :
```bash
make install
```

Cette commande :
- Crée un environnement virtuel Python (`venv`)
- Installe les dépendances backend depuis `backend/requirements.txt`
- Installe les dépendances frontend avec npm


#### 2. **Initialiser les bases de données**
```bash
make migration
```

Cette commande :
- Initialise la base de données sqlite3 avec les configurations Django
- Initialise la base de données Neo4j en envoyant le schéma du model à la base de données (label et index)
    - supprime le précédent schéma du model (pas de gestion de migration de Django)

### Lancement de l'application

Terminal 1 - Backend (API Django) :
```bash
make run_back
```
Le serveur démarre sur `http://localhost:8000`

Terminal 2 - Frontend (Vue.js avec Vite) :
```bash
make run_front
```
Le serveur démarre sur `http://localhost:5173` (ou un autre port disponible)

### Exécuter les tests

**Tests backend** :
```bash
make tests
```

**Tests frontend** :
```bash
make tests_front
```

**Couverture des tests (backend)** :
```bash
make coverage
```

### Autres commandes utiles

Migrations Django :
```bash
make migration
```

Shell Django interactif :
```bash
make shell
```

Charger les données par défaut :
```bash
make load_bd
```

Créer un utilisateur administrateur (Neo4j / frontend) :
```bash
make neo4j_create_admin pseudo=<pseudo> password=<password> email=<email>
```


Créer un utilisateur administrateur Django par défaut :
```bash
make default_admin_user
# Username: admin, Password: admin
```

Nettoyer les fichiers temporaires :
```bash
make clean
```

## Backend - API

Création d'un fichier `.env` contenant les informations pour une connexion à une base de données Neo4j :

```
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_HOST=localhost
NEO4J_PORT=7687
YOUTUBE_API_KEY=cle_api_youtube
VIMEO_ACCESS_TOKEN=token_vimeo
```


## Analyse

Vous pouvez accéder à différent diagramme d'analyse qui explquent le fonctionnement de l'application
sur ce lien : https://drive.google.com/file/d/1NtczicyzqroLYPXIKMU5J1TaDGLkbJWk/view?usp=sharing
ou vous pouvez aussi trouver les diagrammes dans le dossier `docs/diagrams` du projet.

## Architecture de l'application

L'application est structurée en deux parties principales : le backend et le frontend.

### Backend
- **Framework** : Django + Django REST Framework (DRF) pour exposer une API REST.
- **Rôle** : gère les données, la logique métier, l'authentification, les permissions et les intégrations avec Neo4j.
- **Structure** : application `API/` modulaire (models, serializers/, views/, urls.py, permissions, auth, errors, tests).
- **Base de données** : Neo4j pour stocker les relations entre contenus vidéo (artistes, interviews, extraits, tags, etc.).
- **Port** : `http://localhost:8000` en développement.
- Voir [backend/README.md](backend/README.md) pour les détails.

### Frontend
- **Framework** : Vue 3 + Vite (bundler rapide).
- **Rôle** : interface utilisateur réactive et moderne pour naviguer les contenus et interagir avec l'API.
- **Structure** : modulaire (src/components/, src/views/, src/model/, src/router.js).
- **Services** : centralisés dans `src/model/` (apiClient, services métiers).
- **Port** : `http://localhost:5173` en développement (Vite dev server).
- Voir [frontend/README.md](frontend/README.md) pour les détails.

### Communication
- RESTful API : le frontend consomme les endpoints du backend via `fetch`.
- Authentification : tokens JWT ou session (à définir) injectés dans les en-têtes HTTP.
- CORS : à configurer côté backend pour autoriser l'origine du frontend.

## API youtube et vimeo

#### youtube
https://developers.google.com/youtube/v3/getting-started?hl=fr

video  
https://www.youtube.com/watch?v=7_22jCiq4nk

#### vimeo
https://developer.vimeo.com/api/guides/start

video   
https://www.youtube.com/watch?v=DY-Hw4YJX2s

une fois terminer completer metté les clef api dans le fichier .env
