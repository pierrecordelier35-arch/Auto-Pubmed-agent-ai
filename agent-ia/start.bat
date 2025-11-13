@echo off
REM Script de démarrage de l'Agent IA pour Windows

echo ======================================================
echo 🤖 Agent IA - Assistant Scientifique
echo ======================================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    echo    Installez Python 3.8 ou supérieur : https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python installé
python --version
echo.

REM Vérifier si les dépendances sont installées
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation des dépendances...
    pip install -r requirements.txt
    echo.
)

REM Créer le dossier data s'il n'existe pas
if not exist "data" mkdir data

echo 🚀 Démarrage du serveur...
echo.
echo 📍 L'interface sera accessible sur : http://localhost:5000
echo.
echo ⚠️  N'oubliez pas de configurer vos clés API dans l'interface !
echo.
echo Pour arrêter le serveur : Ctrl+C
echo.
echo ======================================================
echo.

REM Lancer le serveur
python app.py

pause
