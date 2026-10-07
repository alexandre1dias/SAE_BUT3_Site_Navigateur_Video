# Backend (Django)

Ce backend est une application Django organisée pour séparer les responsabilités entre l'API, la configuration du projet et les dépendances.

Structure principale du répertoire `backend/` :

- `manage.py` : utilitaire d'administration Django (migrations, serveur de dev, commandes custom).
- `requirements.txt` : dépendances Python du projet.
- `dockerfile` : image Docker pour le backend.
- `API/` : application Django regroupant les endpoints REST (serializers, viewsets, urls, admin, tests).
- `backend/` : configuration du projet Django (settings, urls, wsgi/asgi, initialisation).

Organisation et bonnes pratiques :


- `API/` contient les modules principaux (structure modulaire) :
 	- `models.py` : définition des modèles de données.

 	- `serializers/` : package regroupant les serializers par domaine (ex. `artiste.py`, `audio.py`, `extrait.py`, `utilisateur.py`, ...).
 	  - Rôle : transformer les instances de modèles Django en représentations JSON (sérialisation) et valider / convertir les payloads entrants en données Python (désérialisation).
 	  - Organisation recommandée : un fichier par domaine/ressource, et éventuellement un `base.py` pour sérializers partagés (champs communs, mixins).
 	  - Validation : implémentez `validate_<field>` et `validate(self, data)` pour règles spécifiques

 	- `views/` : package regroupant les vues / viewsets par domaine (ex. `artiste.py`, `audio.py`, `interviews.py`, `utilisateur.py`, ...).
 	  - Rôle : exposer les endpoints HTTP (list, retrieve, create, update, destroy) et orchestrer les serializers, permissions, filtres et pagination.
      - Organisation recommandée : un fichier par domaine/ressource, et éventuellement un `base.py` pour viewsets partagés.
            
 	- `urls.py` : routes spécifiques à l'application (généralement en important et en enregistrant les `ViewSet` via un `router`).

 	- `admin.py` : enregistrements des modèles pour l'interface d'administration.

 	- `permissions.py` : permissions personnalisées (ex. `IsStaffOrReadOnly`, `IsOwnerOrReadOnly`). Classes réutilisables pour contrôler l'accès aux endpoints selon les droits de l'utilisateur.

 	- `auth.py` : logique d'authentification spécifique (tokens, JWT, stratégies custom). Peut inclure des classes ou fonctions pour générer/valider les credentials.

 	- `errors/` : dossier regroupant les exceptions et erreurs personnalisées (ex. `connexion_db.py`, `not_found.py`, `validator_required.py`). Permet une gestion cohérente des erreurs et des réponses HTTP dans toute l'API.

 	- `tests/` : dossier regroupant les tests unitaires et d'intégration (ex. `test_views.py`, `test_serializers.py`). Exécutez avec `python manage.py test`.

 	- `migrations/` : dossier généré automatiquement par Django pour tracker les changements de schéma database. Ne pas éditer manuellement ; générez via `python manage.py makemigrations`.

 	- `management/` : dossier optionnel pour commandes Django custom (ex. `management/commands/load_data.py`). Exécutables via `python manage.py <command_name>`.



- `backend/` (le dossier de configuration) contient :
	- `settings.py` : configuration du projet (séparer les settings dev/prod si nécessaire).
	- `urls.py` : routeur principal qui inclut les routes de `API/`.
	- `wsgi.py` / `asgi.py` : points d'entrée pour les serveurs d'applications.

- Tests : placez les tests unitaires et d'intégration dans les applications (`API/tests/`) et exécutez-les avec `python manage.py test`.

Flux d'intégration avec le frontend :
- L'API expose des endpoints REST (ou GraphQL) consommés par le frontend. Centralisez la logique d'authentification et la gestion des permissions côté backend.

Commandes utiles :

```bash
# installation des dépendances
pip install -r requirements.txt

# appliquer les migrations
python manage.py migrate

# lancer le serveur de développement
python manage.py runserver

# exécuter les tests
python manage.py test
```

Notes :
- Pour la production, configurez une base de données dédiée (Postgres/MySQL) et séparez les settings (fichiers ou variables d'environnement). Mettez en place Gunicorn/uvicorn + reverse proxy (Nginx) ou conteneurisez via Docker.

