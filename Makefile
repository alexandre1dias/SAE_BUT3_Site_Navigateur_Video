APP = API
manage = ./backend/manage.py
npm = npm --prefix ./frontend

# Détection automatique du système d'exploitation
ifeq ($(OS),Windows_NT)
    venv = venv/Scripts
    python = $(venv)/python.exe
    pip = $(venv)/pip.exe
    python_cmd = python
    coverage = $(venv)/coverage.exe
    
    # Injection des variables d'environnement sous Windows CMD
    create_admin_cmd = set DJANGO_SUPERUSER_USERNAME=admin&& set DJANGO_SUPERUSER_PASSWORD=admin&& $(python) $(manage) createsuperuser --noinput --email ""
    
    # Macros de nettoyage pour l'invite de commande Windows (CMD)
    # Le tiret "-" initial permet de continuer même si le fichier/dossier n'existe pas
    clean_backend = -FOR /d /r .\backend\ %%d in (.mypy_cache .pytest_cache __pycache__) DO @rd /s /q "%%d" 2>nul
    clean_pyc = -del /s /q .\backend\*.pyc 2>nul
    clean_frontend = -FOR /d /r .\frontend\ %%d in (node_modules dist) DO @rd /s /q "%%d" 2>nul
    clean_lock = -del /s /q .\frontend\*.lock 2>nul
else
    venv = venv/bin
    python = $(venv)/python
    pip = $(venv)/pip
    python_cmd = python3
    coverage = $(venv)/coverage
    
    # Injection des variables d'environnement sous Linux/macOS
	create_admin_cmd = set DJANGO_SUPERUSER_USERNAME=admin&& set DJANGO_SUPERUSER_PASSWORD=admin&& "$(python)" "$(manage)" createsuperuser --noinput --email ""
    
    # Macros de nettoyage Linux (Bash)
    clean_backend = find ./backend/ -type d -name .mypy_cache -o -name .pytest_cache -o -name __pycache__ | xargs rm -rv || true
    clean_pyc = find ./backend/ -type f -name "*.pyc" | xargs rm -rv || true
    clean_frontend = find ./frontend/ -type d -name node_modules -o -name dist | xargs rm -rv || true
    clean_lock = find ./frontend/ -type f -name "*.lock" | xargs rm -rv || true
endif

.PHONY: install migration tests tests_front coverage run_back shell run_front neomodel_gen_diagram show_django_urls load_bd default_admin_user clean

run_back:
	$(python) $(manage) runserver

shell:
	$(python) $(manage) shell -v 2

run_front:
	$(npm) run dev

install:
	$(python_cmd) -m venv venv
	$(pip) install -r backend/requirements.txt
	$(npm) install

# Pour le backend
migration:
	$(python) $(manage) makemigrations $(APP)
	$(python) $(manage) migrate
	$(python) $(manage) install_labels

# Nécessite d'avoir un serveur Neo4j sur les ports 17474 et 17687
# docker run -d -p 17474:7474 -p 17687:7687 -e NEO4J_AUTH=neo4j/testtest neo4j:latest
tests:
	$(python) $(manage) test $(APP)

tests_front:
	$(npm) run test

coverage:
	$(coverage) run --source='$(APP)' $(manage) test ./backend/$(APP)/tests/$(package)
	$(coverage) report
	$(coverage) html

neomodel_gen_diagram:
	$(venv)/neomodel_generate_diagram ./backend/API/models.py --file-type arrows --write-to-dir schema

load_bd:
	$(python) $(manage) install_labels
	$(python) $(manage) basic_load_bd

show_django_urls:
	$(python) $(manage) show_urls

neo4j_create_admin:
	$(python) $(manage) create_admin $(pseudo) $(password) $(email)

default_admin_user:
	$(create_admin_cmd)

clean:
	@echo "Nettoyage Python..."
	$(clean_backend)
	$(clean_pyc)
	@echo "Nettoyage VueJS..."
	$(clean_frontend)
	$(clean_lock)

