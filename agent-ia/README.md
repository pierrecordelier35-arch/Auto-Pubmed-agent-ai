# 🤖 Agent IA - Assistant Scientifique

Agent IA intelligent pour explorer et approfondir les articles scientifiques de votre veille PubMed.

## 🌟 Fonctionnalités

- 🔍 **Recherche intelligente** : Utilise Perplexity pour trouver des sources récentes et fiables
- ✍️ **Synthèse claire** : Claude génère des réponses structurées et pédagogiques
- 💬 **Interface conversationnelle** : Posez des questions naturellement
- 📚 **Historique sauvegardé** : Toutes vos interactions sont enregistrées
- 🔒 **Local et sécurisé** : Vos clés API restent dans votre navigateur

## 📋 Prérequis

- Python 3.8 ou supérieur
- Clé API Perplexity (https://www.perplexity.ai/)
- Clé API Claude/Anthropic (https://console.anthropic.com/)

## 🚀 Installation

### 1. Installer les dépendances

```bash
cd agent-ia
pip install -r requirements.txt
```

### 2. Lancer le serveur

```bash
python app.py
```

Le serveur démarre sur `http://localhost:5000`

## 🔧 Configuration

1. **Obtenir vos clés API** :
   - **Perplexity** : Créez un compte sur https://www.perplexity.ai/settings/api
   - **Claude** : Créez un compte sur https://console.anthropic.com/

2. **Configurer dans l'interface** :
   - Ouvrez l'interface Agent IA
   - Cliquez sur "⚙️ Configuration des API"
   - Collez vos clés API
   - Cliquez sur "💾 Enregistrer les clés"

Les clés sont sauvegardées localement dans votre navigateur (localStorage).

## 📖 Utilisation

### Accès via l'email

Lorsque vous recevez un email de veille scientifique, cliquez sur le bouton **"🤖 Agent IA - Explorer le sujet"**.

### Accès direct

Vous pouvez aussi accéder directement à l'interface :

```
http://localhost:5000/?title=TITRE_ARTICLE&abstract=RESUME_ARTICLE&pmid=12345678
```

### Poser des questions

Exemples de questions que vous pouvez poser :

- "Quelles sont les applications pratiques de cette découverte ?"
- "Y a-t-il des études récentes qui confirment ces résultats ?"
- "Peux-tu expliquer simplement le concept de X mentionné dans l'article ?"
- "Quelles sont les controverses autour de ce sujet ?"
- "Comment cette recherche s'inscrit-elle dans le contexte actuel ?"

## 🏗️ Architecture

```
agent-ia/
├── app.py                  # Serveur Flask principal
├── requirements.txt        # Dépendances Python
├── templates/
│   └── index.html         # Interface utilisateur
├── static/
│   ├── css/
│   │   └── style.css      # Styles
│   └── js/
│       └── app.js         # Logique frontend
└── data/
    └── history_*.json     # Historiques des conversations
```

## 🔄 Workflow

1. **Utilisateur pose une question** dans l'interface
2. **Frontend envoie** la question + contexte de l'article au backend
3. **Backend appelle Perplexity** pour rechercher des sources fiables
4. **Backend appelle Claude** pour synthétiser en réponse structurée
5. **Frontend affiche** la réponse avec les sources
6. **Historique sauvegardé** localement

## 🎯 Modèles utilisés

- **Perplexity** : `llama-3.1-sonar-small-128k-online`
  - Meilleur rapport qualité/prix
  - Recherche en temps réel sur le web
  - Citations automatiques

- **Claude** : `claude-3-5-sonnet-20241022`
  - Rédaction claire et structurée
  - Compréhension excellente du contexte
  - Réponses naturelles

## 💰 Coûts estimés

### Perplexity
- Modèle : `llama-3.1-sonar-small-128k-online`
- Prix : ~$0.20 / 1M tokens
- Coût par requête : ~$0.001-0.002 (environ 1-2 centimes)

### Claude
- Modèle : `claude-3-5-sonnet-20241022`
- Prix : $3 / 1M tokens (input), $15 / 1M tokens (output)
- Coût par requête : ~$0.01-0.02 (environ 1-2 centimes)

**Total par question : ~2-4 centimes**

## 🔒 Sécurité

- ✅ Clés API stockées uniquement dans le navigateur (localStorage)
- ✅ Pas de stockage côté serveur des clés
- ✅ Communication HTTPS recommandée en production
- ✅ Historique stocké localement sur votre machine

## 🐛 Dépannage

### Le serveur ne démarre pas

```bash
# Vérifiez que Python est installé
python --version

# Réinstallez les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur "Clés API manquantes"

1. Vérifiez que vous avez bien configuré les clés dans l'interface
2. Videz le cache du navigateur et reconfigurez
3. Vérifiez que les clés sont valides sur les sites respectifs

### Pas de réponse / Timeout

1. Vérifiez votre connexion internet
2. Les requêtes peuvent prendre 10-30 secondes (recherche + rédaction)
3. Consultez les logs du serveur dans le terminal

## 📝 Personnalisation

### Changer les modèles

Éditez `app.py` :

```python
PERPLEXITY_MODEL = "llama-3.1-sonar-huge-128k-online"  # Modèle plus puissant
CLAUDE_MODEL = "claude-3-opus-20240229"  # Modèle premium
```

### Modifier le style

Éditez `static/css/style.css` pour personnaliser l'apparence.

## 📞 Support

Pour toute question ou problème :
1. Consultez les logs du serveur
2. Vérifiez la console du navigateur (F12)
3. Créez une issue sur GitHub

## 📜 Licence

Ce projet est fourni tel quel pour un usage personnel et éducatif.

## 🙏 Remerciements

- **Perplexity AI** pour l'API de recherche
- **Anthropic** pour l'API Claude
- **Flask** pour le framework web
