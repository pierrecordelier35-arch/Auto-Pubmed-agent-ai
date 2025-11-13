#!/bin/bash

# Script de démarrage de l'Agent IA

echo "======================================================"
echo "🤖 Agent IA - Assistant Scientifique"
echo "======================================================"
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "   Installez Python 3.8 ou supérieur : https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python installé : $(python3 --version)"
echo ""

# Vérifier si les dépendances sont installées
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installation des dépendances..."
    pip3 install -r requirements.txt
    echo ""
fi

# Créer le dossier data s'il n'existe pas
mkdir -p data

echo "🚀 Démarrage du serveur..."
echo ""
echo "📍 L'interface sera accessible sur : http://localhost:5000"
echo ""
echo "⚠️  N'oubliez pas de configurer vos clés API dans l'interface !"
echo ""
echo "Pour arrêter le serveur : Ctrl+C"
echo ""
echo "======================================================"
echo ""

# Lancer le serveur
python3 app.py
