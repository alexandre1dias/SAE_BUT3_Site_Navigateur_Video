@echo off
REM rec117 : installe puis lance le site (Windows).
REM Usage : double-cliquer sur lancer.bat
setlocal
cd /d "%~dp0"

set PORT=8000
set URL=http://127.0.0.1:%PORT%/

echo === rec117 : installation et lancement ===

REM 1. Python 3.12 ou plus (requis par Django 6.1). On essaie le lanceur "py" puis "python".
set PY=
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1 && set "PY=py -3"
if not defined PY (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)" >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo.
    echo ERREUR : Python 3.12 ^(ou plus recent^) est introuvable.
    echo Telechargez-le sur https://www.python.org/downloads/
    echo IMPORTANT : pendant l'installation, cochez "Add python.exe to PATH".
    echo Puis relancez ce script.
    echo.
    pause
    exit /b 1
)
for /f "delims=" %%v in ('%PY% --version') do echo [1/5] Python trouve : %%v

REM 2. Environnement virtuel (recree s'il est absent ou casse)
set "VPY=%~dp0.venv\Scripts\python.exe"
"%VPY%" -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo [2/5] Creation de l'environnement virtuel ^(.venv^)...
    if exist .venv rmdir /s /q .venv
    %PY% -m venv .venv
    if errorlevel 1 goto erreur
) else (
    echo [2/5] Environnement virtuel deja present.
)

REM 3. Dependances
echo [3/5] Installation des dependances ^(requirements.txt^)...
"%VPY%" -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 goto erreur

REM 4. Base de donnees SQLite : tables + donnees de demo si la base est vide
echo [4/5] Preparation de la base de donnees...
cd SaeProj
"%VPY%" manage.py migrate --noinput
if errorlevel 1 goto erreur
"%VPY%" manage.py shell -c "from SoundFlow.models import Interview; from SoundFlow import peuplement_reel; print('Base deja remplie.') if Interview.objects.exists() else peuplement_reel.run()"
if errorlevel 1 goto erreur

REM 5. Lancement + ouverture du navigateur apres 3 s
echo [5/5] Lancement du site sur %URL%
echo       ^(fermez cette fenetre ou Ctrl+C pour arreter le serveur^)
start "" /b "%VPY%" -c "import time, webbrowser; time.sleep(3); webbrowser.open('%URL%')"
"%VPY%" manage.py runserver 127.0.0.1:%PORT%
pause
exit /b 0

:erreur
echo.
echo ERREUR : une etape a echoue ^(voir le message ci-dessus^).
echo Verifiez votre connexion Internet puis relancez lancer.bat.
pause
exit /b 1
