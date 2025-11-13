// Variables globales
let articleData = null;
let conversationHistory = [];
let apiKeys = {
    perplexity: '',
    claude: ''
};

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    loadArticleFromURL();
    loadSavedAPIKeys();
    setupEventListeners();
});

// Initialiser l'application
function initializeApp() {
    console.log('🚀 Agent IA initialisé');
    adjustTextareaHeight();
}

// Charger les données de l'article depuis l'URL
function loadArticleFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const title = urlParams.get('title');
    const abstract = urlParams.get('abstract');
    const pmid = urlParams.get('pmid');

    if (title && abstract) {
        articleData = {
            title: decodeURIComponent(title),
            abstract: decodeURIComponent(abstract),
            pmid: pmid || 'N/A'
        };

        displayArticleInfo();
    } else {
        // Données de test si pas de paramètres
        articleData = {
            title: "Article de test",
            abstract: "Résumé de l'article...",
            pmid: "00000000"
        };
        displayArticleInfo();
    }
}

// Afficher les informations de l'article
function displayArticleInfo() {
    if (!articleData) return;

    document.getElementById('articleTitle').textContent = articleData.title;
    document.getElementById('articleAbstract').textContent = articleData.abstract;
}

// Charger les clés API sauvegardées
function loadSavedAPIKeys() {
    const savedPerplexity = localStorage.getItem('perplexity_api_key');
    const savedClaude = localStorage.getItem('claude_api_key');

    if (savedPerplexity) {
        apiKeys.perplexity = savedPerplexity;
        document.getElementById('perplexityKey').value = savedPerplexity;
    }

    if (savedClaude) {
        apiKeys.claude = savedClaude;
        document.getElementById('claudeKey').value = savedClaude;
    }
}

// Configuration des écouteurs d'événements
function setupEventListeners() {
    // Toggle configuration
    document.getElementById('configToggle').addEventListener('click', toggleConfig);

    // Sauvegarde des clés API
    document.getElementById('saveConfigBtn').addEventListener('click', saveAPIKeys);

    // Bouton d'envoi
    document.getElementById('sendButton').addEventListener('click', sendMessage);

    // Textarea auto-resize et Enter pour envoyer
    const textarea = document.getElementById('userInput');
    textarea.addEventListener('input', adjustTextareaHeight);
    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Historique (si implémenté)
    document.getElementById('historyToggle').addEventListener('click', showHistory);
}

// Basculer l'affichage de la configuration
function toggleConfig() {
    const content = document.getElementById('configContent');
    const isVisible = content.style.display === 'block';
    content.style.display = isVisible ? 'none' : 'block';
}

// Sauvegarder les clés API
function saveAPIKeys() {
    const perplexityKey = document.getElementById('perplexityKey').value.trim();
    const claudeKey = document.getElementById('claudeKey').value.trim();
    const statusDiv = document.getElementById('configStatus');

    if (!perplexityKey || !claudeKey) {
        statusDiv.textContent = '❌ Veuillez renseigner les deux clés API';
        statusDiv.className = 'config-status error';
        return;
    }

    // Validation basique du format
    if (!perplexityKey.startsWith('pplx-')) {
        statusDiv.textContent = '❌ Format de clé Perplexity invalide (doit commencer par "pplx-")';
        statusDiv.className = 'config-status error';
        return;
    }

    if (!claudeKey.startsWith('sk-ant-')) {
        statusDiv.textContent = '❌ Format de clé Claude invalide (doit commencer par "sk-ant-")';
        statusDiv.className = 'config-status error';
        return;
    }

    // Sauvegarder dans le localStorage
    localStorage.setItem('perplexity_api_key', perplexityKey);
    localStorage.setItem('claude_api_key', claudeKey);

    apiKeys.perplexity = perplexityKey;
    apiKeys.claude = claudeKey;

    statusDiv.textContent = '✅ Clés API sauvegardées avec succès';
    statusDiv.className = 'config-status success';

    setTimeout(() => {
        statusDiv.style.display = 'none';
    }, 3000);
}

// Ajuster automatiquement la hauteur du textarea
function adjustTextareaHeight() {
    const textarea = document.getElementById('userInput');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
}

// Envoyer un message
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;

    // Vérifier que les clés API sont configurées
    if (!apiKeys.perplexity || !apiKeys.claude) {
        showError('Veuillez configurer vos clés API avant de poser une question.');
        return;
    }

    // Ajouter le message de l'utilisateur
    addMessage(message, 'user');

    // Vider l'input
    input.value = '';
    adjustTextareaHeight();

    // Désactiver le bouton d'envoi
    const sendButton = document.getElementById('sendButton');
    sendButton.disabled = true;

    // Afficher le loading
    showLoading();

    try {
        // Envoyer la requête au backend
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: message,
                article: articleData,
                history: conversationHistory,
                api_keys: apiKeys
            })
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const data = await response.json();

        // Ajouter la réponse de l'agent
        addMessage(data.response, 'agent', data.sources);

        // Sauvegarder dans l'historique
        conversationHistory.push({
            question: message,
            response: data.response,
            timestamp: new Date().toISOString()
        });

        // Sauvegarder l'historique
        saveHistory();

    } catch (error) {
        console.error('Erreur:', error);
        showError('Une erreur est survenue lors de la recherche. Veuillez réessayer.');
    } finally {
        hideLoading();
        sendButton.disabled = false;
    }
}

// Ajouter un message à la conversation
function addMessage(content, type, sources = null) {
    const container = document.getElementById('messagesContainer');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Convertir les retours à la ligne en paragraphes
    const paragraphs = content.split('\n\n').filter(p => p.trim());
    paragraphs.forEach(p => {
        const pElement = document.createElement('p');
        pElement.innerHTML = formatText(p);
        contentDiv.appendChild(pElement);
    });

    // Ajouter les sources si présentes
    if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources-section';

        const sourcesTitle = document.createElement('div');
        sourcesTitle.className = 'sources-title';
        sourcesTitle.textContent = '📚 Sources consultées:';
        sourcesDiv.appendChild(sourcesTitle);

        sources.forEach((source, index) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            sourceItem.textContent = `${index + 1}. ${source}`;
            sourcesDiv.appendChild(sourceItem);
        });

        contentDiv.appendChild(sourcesDiv);
    }

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    container.appendChild(messageDiv);

    // Scroll vers le bas
    container.scrollTop = container.scrollHeight;
}

// Formater le texte (gras, italique, listes)
function formatText(text) {
    // Gras
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italique
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Listes à puces
    if (text.includes('•') || text.includes('-')) {
        const lines = text.split('\n');
        let html = '';
        let inList = false;

        lines.forEach(line => {
            if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
                if (!inList) {
                    html += '<ul>';
                    inList = true;
                }
                html += '<li>' + line.replace(/^[•\-]\s*/, '') + '</li>';
            } else {
                if (inList) {
                    html += '</ul>';
                    inList = false;
                }
                html += line + '<br>';
            }
        });

        if (inList) html += '</ul>';
        return html;
    }

    return text;
}

// Afficher une erreur
function showError(message) {
    addMessage(`❌ ${message}`, 'agent');
}

// Afficher le loading
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

// Masquer le loading
function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Sauvegarder l'historique
function saveHistory() {
    if (!articleData) return;

    const historyKey = `history_${articleData.pmid}`;
    localStorage.setItem(historyKey, JSON.stringify(conversationHistory));
}

// Afficher l'historique
function showHistory() {
    if (conversationHistory.length === 0) {
        alert('Aucun historique de conversation disponible.');
        return;
    }

    // Pour l'instant, simple alerte
    // Peut être amélioré avec une modale
    let historyText = 'Historique des conversations:\n\n';
    conversationHistory.forEach((item, index) => {
        historyText += `${index + 1}. Q: ${item.question}\n`;
        historyText += `   R: ${item.response.substring(0, 100)}...\n\n`;
    });

    alert(historyText);
}

// Fonction utilitaire pour encoder les paramètres URL
function encodeURLParams(params) {
    return Object.keys(params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
        .join('&');
}
