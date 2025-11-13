#!/usr/bin/env python3
"""
Agent IA - Serveur Flask pour l'interface d'exploration scientifique
Intègre Perplexity pour la recherche et Claude pour la rédaction
"""

from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from datetime import datetime
from urllib.parse import unquote

app = Flask(__name__)

# Configuration
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Modèles à utiliser
PERPLEXITY_MODEL = "llama-3.1-sonar-small-128k-online"  # Meilleur rapport qualité/prix
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"  # Modèle le plus récent et performant


@app.route('/')
def index():
    """Page d'accueil de l'Agent IA"""
    return render_template('index.html')


@app.route('/api/query', methods=['POST'])
def handle_query():
    """
    Gère les requêtes de l'utilisateur
    1. Recherche avec Perplexity
    2. Synthèse avec Claude
    """
    try:
        data = request.get_json()

        question = data.get('question', '')
        article = data.get('article', {})
        history = data.get('history', [])
        api_keys = data.get('api_keys', {})

        # Validation
        if not question:
            return jsonify({'error': 'Question manquante'}), 400

        if not api_keys.get('perplexity') or not api_keys.get('claude'):
            return jsonify({'error': 'Clés API manquantes'}), 400

        # Étape 1: Recherche avec Perplexity
        print(f"📡 Recherche Perplexity pour: {question}")
        search_results = search_with_perplexity(
            question,
            article,
            api_keys['perplexity']
        )

        if not search_results:
            return jsonify({'error': 'Erreur lors de la recherche'}), 500

        # Étape 2: Rédaction avec Claude
        print(f"✍️ Rédaction avec Claude")
        response_text = generate_response_with_claude(
            question,
            article,
            search_results,
            history,
            api_keys['claude']
        )

        if not response_text:
            return jsonify({'error': 'Erreur lors de la génération de la réponse'}), 500

        # Extraire les sources
        sources = extract_sources(search_results)

        # Sauvegarder l'interaction
        save_interaction(article, question, response_text)

        return jsonify({
            'response': response_text,
            'sources': sources,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        print(f"❌ Erreur dans handle_query: {str(e)}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500


def search_with_perplexity(question, article, api_key):
    """
    Recherche d'informations avec Perplexity AI

    Args:
        question: Question de l'utilisateur
        article: Données de l'article (titre, abstract)
        api_key: Clé API Perplexity

    Returns:
        dict: Résultats de la recherche
    """
    try:
        # Construire le contexte de recherche
        search_prompt = f"""Vous êtes un assistant de recherche scientifique.

Article de référence:
Titre: {article.get('title', 'N/A')}
Résumé: {article.get('abstract', 'N/A')}

Question de l'utilisateur: {question}

Votre tâche:
1. Identifiez le sujet principal de la question
2. Recherchez au moins 5 sources scientifiques récentes et fiables (articles, études, revues systématiques)
3. Fournissez des informations factuelles et vérifiables
4. Privilégiez les sources de moins de 3 ans
5. Incluez des données chiffrées si pertinent

Répondez de manière structurée avec:
- Les principales découvertes récentes
- Les consensus scientifiques actuels
- Les débats ou controverses s'il y en a
- Les applications pratiques

Citez systématiquement vos sources."""

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": PERPLEXITY_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a scientific research assistant. Provide accurate, well-sourced information from recent scientific literature. Always cite your sources."
                },
                {
                    "role": "user",
                    "content": search_prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 2000,
            "return_citations": True,
            "return_related_questions": True
        }

        response = requests.post(
            PERPLEXITY_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ Erreur Perplexity: {response.status_code} - {response.text}")
            return None

        result = response.json()
        print(f"✅ Recherche Perplexity réussie")

        return result

    except Exception as e:
        print(f"❌ Erreur search_with_perplexity: {str(e)}")
        return None


def generate_response_with_claude(question, article, search_results, history, api_key):
    """
    Génère une réponse synthétique avec Claude

    Args:
        question: Question de l'utilisateur
        article: Données de l'article
        search_results: Résultats de Perplexity
        history: Historique de conversation
        api_key: Clé API Claude

    Returns:
        str: Réponse générée
    """
    try:
        # Extraire le contenu de Perplexity
        perplexity_content = ""
        if 'choices' in search_results and len(search_results['choices']) > 0:
            perplexity_content = search_results['choices'][0]['message']['content']

        # Construire l'historique de conversation
        history_text = ""
        if history:
            history_text = "\n\nHistorique de la conversation:\n"
            for i, exchange in enumerate(history[-3:], 1):  # Derniers 3 échanges
                history_text += f"Q{i}: {exchange['question']}\n"
                history_text += f"R{i}: {exchange['response'][:200]}...\n\n"

        # Prompt pour Claude
        claude_prompt = f"""Vous êtes un assistant IA spécialisé en vulgarisation scientifique.

ARTICLE DE RÉFÉRENCE:
Titre: {article.get('title', 'N/A')}
Résumé: {article.get('abstract', 'N/A')}

QUESTION DE L'UTILISATEUR:
{question}

RÉSULTATS DE LA RECHERCHE:
{perplexity_content}

{history_text}

VOTRE TÂCHE:
Rédigez une réponse claire, structurée et pédagogique qui:

1. **Introduction** (1-2 phrases)
   - Contextualise la question par rapport à l'article
   - Annonce ce que vous allez développer

2. **Développements récents** (3-4 paragraphes)
   - Présentez les découvertes et informations trouvées
   - Utilisez des données chiffrées quand c'est pertinent
   - Expliquez les concepts complexes de manière accessible
   - Faites des liens avec l'article de référence

3. **Ce qu'il faut retenir** (liste à puces)
   - 3-5 points clés essentiels
   - Synthèse claire et mémorable

4. **Pour aller plus loin** (1-2 phrases)
   - Suggérez des aspects à approfondir
   - Encouragez l'utilisateur à poser d'autres questions

CONSIGNES STRICTES:
✅ Utilisez uniquement les informations trouvées par la recherche
✅ Adoptez un ton pédagogique et accessible
✅ Structurez avec des paragraphes aérés
✅ Ne mentionnez PAS les liens ou URLs dans le texte
✅ N'inventez AUCUNE donnée
✅ Si une information n'est pas sûre, dites-le clairement

❌ Ne copiez pas l'article original
❌ Ne soyez pas trop technique
❌ N'utilisez pas de jargon sans l'expliquer
❌ Ne mentionnez pas les sources dans le texte (elles seront affichées séparément)

Rédigez une réponse en français, claire et engageante."""

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": CLAUDE_MODEL,
            "max_tokens": 2000,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": claude_prompt
                }
            ]
        }

        response = requests.post(
            CLAUDE_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            print(f"❌ Erreur Claude: {response.status_code} - {response.text}")
            return None

        result = response.json()

        # Extraire le texte de la réponse
        if 'content' in result and len(result['content']) > 0:
            response_text = result['content'][0]['text']
            print(f"✅ Réponse Claude générée ({len(response_text)} caractères)")
            return response_text

        return None

    except Exception as e:
        print(f"❌ Erreur generate_response_with_claude: {str(e)}")
        return None


def extract_sources(search_results):
    """
    Extrait les sources citées des résultats Perplexity

    Args:
        search_results: Résultats de Perplexity

    Returns:
        list: Liste des sources
    """
    sources = []

    try:
        if 'citations' in search_results:
            sources = search_results['citations'][:8]  # Max 8 sources

        # Si pas de citations, essayer d'extraire du texte
        if not sources and 'choices' in search_results:
            content = search_results['choices'][0]['message'].get('content', '')
            # Extraction basique des URLs
            import re
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
            sources = urls[:8]

    except Exception as e:
        print(f"⚠️ Erreur extraction sources: {str(e)}")

    return sources


def save_interaction(article, question, response):
    """
    Sauvegarde l'interaction dans un fichier JSON local

    Args:
        article: Données de l'article
        question: Question posée
        response: Réponse générée
    """
    try:
        # Créer le dossier data s'il n'existe pas
        os.makedirs('data', exist_ok=True)

        # Nom du fichier basé sur le PMID
        pmid = article.get('pmid', 'unknown')
        filename = f"data/history_{pmid}.json"

        # Charger l'historique existant
        history = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                history = json.load(f)

        # Ajouter la nouvelle interaction
        history.append({
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response,
            'article_title': article.get('title', 'N/A')
        })

        # Sauvegarder
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

        print(f"💾 Interaction sauvegardée dans {filename}")

    except Exception as e:
        print(f"⚠️ Erreur sauvegarde interaction: {str(e)}")


@app.route('/api/history/<pmid>', methods=['GET'])
def get_history(pmid):
    """
    Récupère l'historique des interactions pour un article

    Args:
        pmid: Identifiant PubMed de l'article

    Returns:
        JSON: Historique des interactions
    """
    try:
        filename = f"data/history_{pmid}.json"

        if not os.path.exists(filename):
            return jsonify({'history': []})

        with open(filename, 'r', encoding='utf-8') as f:
            history = json.load(f)

        return jsonify({'history': history})

    except Exception as e:
        print(f"❌ Erreur get_history: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de santé pour vérifier que le serveur fonctionne"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🤖 Agent IA - Serveur Flask")
    print("=" * 60)
    print("📡 Intégration: Perplexity + Claude")
    print(f"🔧 Modèles: {PERPLEXITY_MODEL} + {CLAUDE_MODEL}")
    print("=" * 60)
    print()
    print("🚀 Démarrage du serveur sur http://localhost:5000")
    print("⚠️  Assurez-vous d'avoir configuré vos clés API dans l'interface")
    print()

    app.run(debug=True, host='0.0.0.0', port=5000)
