# 🚀 Guide d'Installation - Agent IA pour Auto-Pubmed

Ce guide vous accompagne pas à pas pour installer et utiliser l'Agent IA avec votre workflow PubMed automatique.

## 📋 Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Prérequis](#prérequis)
3. [Installation](#installation)
4. [Configuration n8n](#configuration-n8n)
5. [Configuration des clés API](#configuration-des-clés-api)
6. [Utilisation](#utilisation)
7. [Dépannage](#dépannage)

---

## 🎯 Vue d'ensemble

L'Agent IA est un assistant intelligent qui enrichit vos emails de veille scientifique PubMed :

### ✨ Fonctionnalités

- **Bouton dans l'email** : Un nouveau bouton "🤖 Agent IA — Explorer le sujet" apparaît dans vos emails
- **Interface conversationnelle** : Interface web locale pour poser des questions sur l'article
- **Recherche intelligente** : Utilise Perplexity pour trouver des sources fiables et récentes
- **Synthèse claire** : Claude génère des réponses structurées et pédagogiques
- **Historique** : Toutes vos conversations sont sauvegardées localement

### 🏗️ Architecture

```
Email PubMed
    ↓
[Bouton Agent IA] → Interface Web (localhost:5000)
    ↓
Question posée
    ↓
Backend Flask
    ↓
├── Perplexity (recherche)
    ↓
└── Claude (rédaction)
    ↓
Réponse affichée + Sources
```

---

## 📦 Prérequis

### 1. Python 3.8+

Vérifiez que Python est installé :

```bash
python3 --version
# ou sur Windows
python --version
```

Si Python n'est pas installé : https://www.python.org/downloads/

### 2. Clés API

Vous aurez besoin de deux clés API :

#### Perplexity AI
- 🌐 Site : https://www.perplexity.ai/
- 💰 Prix : ~$0.20 / 1M tokens (~1-2 centimes par question)
- 📝 S'inscrire et obtenir une clé sur : https://www.perplexity.ai/settings/api

#### Claude (Anthropic)
- 🌐 Site : https://www.anthropic.com/
- 💰 Prix : ~$3-15 / 1M tokens (~1-2 centimes par question)
- 📝 S'inscrire et obtenir une clé sur : https://console.anthropic.com/

**💡 Coût estimé : ~2-4 centimes par question posée**

### 3. n8n (workflow automation)

Votre workflow n8n doit être accessible et modifiable.

---

## 🔧 Installation

### Étape 1 : Installer les dépendances Python

```bash
cd agent-ia
pip install -r requirements.txt
```

Sur Windows :
```cmd
cd agent-ia
pip install -r requirements.txt
```

### Étape 2 : Tester le serveur

Linux/Mac :
```bash
./start.sh
```

Windows :
```cmd
start.bat
```

Ou manuellement :
```bash
python app.py
```

Vous devriez voir :
```
🚀 Démarrage du serveur sur http://localhost:5000
```

### Étape 3 : Vérifier l'accès

Ouvrez votre navigateur et allez sur :
```
http://localhost:5000
```

Vous devriez voir l'interface Agent IA.

---

## ⚙️ Configuration n8n

### Méthode 1 : Importer le workflow modifié

1. **Localisez le fichier modifié** :
   ```
   PUBMED- Performance & Entraînement (1)_modified.json
   ```

2. **Dans n8n** :
   - Ouvrez votre interface n8n
   - Allez dans "Workflows"
   - Cliquez sur les 3 points → "Import from File"
   - Sélectionnez le fichier `*_modified.json`
   - Le nouveau workflow avec le bouton Agent IA est importé !

3. **Activez le workflow** :
   - Cliquez sur le bouton "Active" pour activer le workflow

### Méthode 2 : Modification manuelle

Si vous préférez modifier manuellement votre workflow existant :

1. **Ouvrez n8n** et votre workflow PubMed

2. **Trouvez le nœud "Générer Emails"**

3. **Modifiez le code JavaScript** :

   Trouvez cette section :
   ```javascript
   <div style="text-align: center;">
     <a href="${article.pubmed_url || '#'}" class="button" target="_blank">
       🔗 Lire l'article sur PubMed
     </a>
   </div>
   ```

   Ajoutez juste après :
   ```javascript

   <!-- Bouton Agent IA -->
   <div style="text-align: center; margin-top: 15px;">
     <a href="http://localhost:5000/?title=${encodeURIComponent(titreTraduction)}&abstract=${encodeURIComponent(abstractTraduction)}&pmid=${article.pmid || ''}" class="button" target="_blank" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
       🤖 Agent IA — Explorer le sujet
     </a>
   </div>
   ```

4. **Sauvegardez** le nœud et activez le workflow

---

## 🔑 Configuration des clés API

### Dans l'interface Agent IA

1. **Lancez le serveur** (si pas déjà fait) :
   ```bash
   cd agent-ia
   ./start.sh  # ou start.bat sur Windows
   ```

2. **Ouvrez l'interface** :
   ```
   http://localhost:5000
   ```

3. **Cliquez sur "⚙️ Configuration des API"**

4. **Entrez vos clés** :
   - Clé Perplexity : `pplx-...`
   - Clé Claude : `sk-ant-...`

5. **Cliquez sur "💾 Enregistrer les clés"**

Les clés sont sauvegardées dans votre navigateur (localStorage) et ne sont jamais envoyées au serveur.

---

## 🎯 Utilisation

### Workflow complet

1. **Recevoir l'email** :
   - Votre workflow n8n envoie l'email quotidien avec l'article PubMed
   - L'email contient maintenant 2 boutons :
     - 🔗 Lire l'article sur PubMed
     - 🤖 Agent IA — Explorer le sujet

2. **Lancer le serveur Agent IA** :
   ```bash
   cd agent-ia
   ./start.sh
   ```
   ⚠️ Le serveur doit être lancé AVANT de cliquer sur le bouton dans l'email

3. **Cliquer sur le bouton Agent IA** :
   - Dans l'email, cliquez sur "🤖 Agent IA — Explorer le sujet"
   - L'interface s'ouvre avec les détails de l'article

4. **Configurer les clés API** (première fois seulement) :
   - Cliquez sur "⚙️ Configuration des API"
   - Entrez vos clés
   - Enregistrez

5. **Poser des questions** :
   - Tapez votre question dans la zone de texte
   - Appuyez sur Entrée ou cliquez sur "📤 Envoyer"
   - L'Agent IA recherche et génère une réponse (10-30 secondes)

### Exemples de questions

**Contexte et applications** :
- "Quelles sont les applications pratiques de cette découverte ?"
- "Comment cette recherche s'inscrit-elle dans le contexte actuel ?"

**Approfondissement** :
- "Y a-t-il des études récentes qui confirment ces résultats ?"
- "Quelles sont les limites de cette étude ?"

**Vulgarisation** :
- "Peux-tu expliquer simplement le concept de X mentionné dans l'article ?"
- "Quels sont les mécanismes biologiques en jeu ?"

**Controverse et débat** :
- "Quelles sont les controverses autour de ce sujet ?"
- "Y a-t-il des avis divergents dans la communauté scientifique ?"

---

## 🐛 Dépannage

### Le serveur ne démarre pas

**Erreur** : `command not found: python`

**Solution** :
```bash
# Essayez python3
python3 app.py

# Ou installez Python
# Linux (Ubuntu/Debian)
sudo apt install python3 python3-pip

# Mac (avec Homebrew)
brew install python3

# Windows : téléchargez sur python.org
```

### "Clés API manquantes"

**Problème** : Le message d'erreur apparaît quand vous posez une question

**Solutions** :
1. Vérifiez que vous avez configuré les clés dans l'interface (⚙️ Configuration des API)
2. Videz le cache du navigateur (Ctrl+Shift+Del) et reconfigurez
3. Vérifiez que les clés sont valides :
   - Perplexity : doit commencer par `pplx-`
   - Claude : doit commencer par `sk-ant-`

### Le bouton Agent IA ne fonctionne pas dans l'email

**Erreur** : "Site inaccessible" ou "Connexion refusée"

**Solutions** :
1. **Vérifiez que le serveur est lancé** :
   ```bash
   cd agent-ia
   ./start.sh
   ```
   Vous devriez voir : `🚀 Démarrage du serveur sur http://localhost:5000`

2. **Testez l'accès direct** :
   Ouvrez votre navigateur et allez sur http://localhost:5000

3. **Vérifiez le port** :
   Si le port 5000 est occupé, modifiez `app.py` :
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Changez le port
   ```
   Et mettez à jour le bouton dans le workflow n8n

### Timeout ou pas de réponse

**Problème** : La recherche prend trop de temps ou échoue

**Solutions** :
1. **Vérifiez votre connexion internet**
2. **Consultez les logs du serveur** dans le terminal
3. **Vérifiez vos crédits API** :
   - Perplexity : https://www.perplexity.ai/settings/api
   - Claude : https://console.anthropic.com/

4. **Relancez le serveur** :
   - Arrêtez avec Ctrl+C
   - Relancez avec `./start.sh`

### Erreur "Invalid API key"

**Solutions** :
1. **Vérifiez le format** :
   - Perplexity : `pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Claude : `sk-ant-api03-xxxxx`

2. **Générez de nouvelles clés** si nécessaire

3. **Vérifiez les quotas** sur les plateformes respectives

### L'historique ne se sauvegarde pas

**Problème** : Les conversations ne sont pas enregistrées

**Solutions** :
1. **Vérifiez les permissions** du dossier `agent-ia/data/`
   ```bash
   ls -la agent-ia/data/
   ```

2. **Créez le dossier** s'il n'existe pas :
   ```bash
   mkdir -p agent-ia/data
   ```

3. **Consultez les logs** du serveur pour voir les erreurs de sauvegarde

---

## 📊 Monitoring des coûts

### Suivre votre consommation

**Perplexity** :
- https://www.perplexity.ai/settings/api
- Onglet "Usage"

**Claude** :
- https://console.anthropic.com/settings/usage
- Onglet "Usage & billing"

### Estimation des coûts

| Action | Perplexity | Claude | Total |
|--------|-----------|---------|-------|
| 1 question | ~$0.001-0.002 | ~$0.01-0.02 | ~$0.02-0.04 |
| 10 questions | ~$0.01-0.02 | ~$0.10-0.20 | ~$0.20-0.40 |
| 100 questions | ~$0.10-0.20 | ~$1-2 | ~$2-4 |

**💡 Astuce** : Les premiers crédits sont souvent gratuits lors de l'inscription !

---

## 🔒 Sécurité et confidentialité

### Où sont stockées les données ?

- ✅ **Clés API** : Dans votre navigateur (localStorage), jamais sur le serveur
- ✅ **Historique** : Fichiers locaux dans `agent-ia/data/`
- ✅ **Serveur** : Tourne en local sur votre machine (localhost)

### Recommandations

1. **Ne partagez JAMAIS vos clés API**
2. **Sauvegardez régulièrement** le dossier `agent-ia/data/`
3. **En production** : Utilisez HTTPS et des variables d'environnement

---

## 🎨 Personnalisation

### Changer les modèles IA

Éditez `agent-ia/app.py` :

```python
# Modèles plus performants (mais plus chers)
PERPLEXITY_MODEL = "llama-3.1-sonar-huge-128k-online"
CLAUDE_MODEL = "claude-3-opus-20240229"

# Modèles économiques
PERPLEXITY_MODEL = "llama-3.1-sonar-small-128k-online"
CLAUDE_MODEL = "claude-3-haiku-20240307"
```

### Modifier le style de l'interface

Éditez `agent-ia/static/css/style.css` pour personnaliser les couleurs, polices, etc.

### Changer le port du serveur

Éditez `agent-ia/app.py` :

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Changez 5000 en 8080
```

N'oubliez pas de mettre à jour le lien dans le workflow n8n !

---

## 📚 Ressources

- **Documentation Perplexity** : https://docs.perplexity.ai/
- **Documentation Claude** : https://docs.anthropic.com/
- **Documentation Flask** : https://flask.palletsprojects.com/
- **Documentation n8n** : https://docs.n8n.io/

---

## ✅ Checklist de démarrage

Avant de commencer, vérifiez que vous avez :

- [ ] Python 3.8+ installé
- [ ] Dépendances Python installées (`pip install -r requirements.txt`)
- [ ] Clé API Perplexity obtenue
- [ ] Clé API Claude obtenue
- [ ] Workflow n8n modifié avec le bouton Agent IA
- [ ] Serveur Agent IA lancé (`./start.sh`)
- [ ] Clés API configurées dans l'interface
- [ ] Test réussi avec une question

---

## 🙋 Support

Si vous rencontrez des problèmes :

1. **Consultez les logs** du serveur dans le terminal
2. **Vérifiez la console** du navigateur (F12 → Console)
3. **Relisez ce guide** section par section
4. **Créez une issue** sur GitHub avec :
   - Description du problème
   - Messages d'erreur (logs serveur + console)
   - Système d'exploitation
   - Version de Python

---

## 🎉 Félicitations !

Vous avez installé et configuré l'Agent IA avec succès !

Profitez de votre nouvel assistant scientifique pour approfondir vos connaissances et explorer les articles de manière interactive.

**Bonne veille scientifique ! 📚🤖**
