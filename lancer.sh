#!/usr/bin/env bash
# rec117 : installe puis lance le site (Linux / macOS).
# Usage : ./lancer.sh   (ou : bash lancer.sh)
set -e
cd "$(dirname "$0")"

PORT=8000
URL="http://127.0.0.1:$PORT/"

echo "=== rec117 : installation et lancement ==="

# 1. Python 3.12 ou plus (requis par Django 6.1)
PY=""
for cmd in python3 python; do
    if command -v "$cmd" >/dev/null 2>&1 && "$cmd" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
        PY="$cmd"; break
    fi
done
if [ -z "$PY" ]; then
    echo ""
    echo "ERREUR : Python 3.12 (ou plus recent) est introuvable."
    echo "  - Ubuntu/Debian : sudo apt install python3 python3-venv"
    echo "  - macOS         : https://www.python.org/downloads/  (ou : brew install python)"
    echo "Installez-le puis relancez ce script."
    exit 1
fi
echo "[1/5] Python trouve : $("$PY" --version)"

# 2. Environnement virtuel (recree s'il est absent ou casse)
if [ ! -x .venv/bin/python ] || ! .venv/bin/python -c 'import sys' >/dev/null 2>&1; then
    echo "[2/5] Creation de l'environnement virtuel (.venv)..."
    rm -rf .venv
    if ! "$PY" -m venv .venv; then
        echo "ERREUR : impossible de creer le venv. Sous Ubuntu/Debian : sudo apt install python3-venv"
        exit 1
    fi
else
    echo "[2/5] Environnement virtuel deja present."
fi
VPY="$PWD/.venv/bin/python"

# 3. Dependances
echo "[3/5] Installation des dependances (requirements.txt)..."
"$VPY" -m pip install --disable-pip-version-check -q -r requirements.txt

# 4. Base de donnees SQLite : tables + donnees de demo si la base est vide
echo "[4/5] Preparation de la base de donnees..."
cd SaeProj
"$VPY" manage.py migrate --noinput
"$VPY" manage.py shell -c "from SoundFlow.models import Interview; from SoundFlow import peuplement_reel; print('Base deja remplie.') if Interview.objects.exists() else peuplement_reel.run()"

# 5. Lancement + ouverture du navigateur apres 3 s
echo "[5/5] Lancement du site sur $URL"
echo "      (Ctrl+C pour arreter le serveur)"
"$VPY" -c "import time, webbrowser; time.sleep(3); webbrowser.open('$URL')" >/dev/null 2>&1 &
exec "$VPY" manage.py runserver "127.0.0.1:$PORT"
