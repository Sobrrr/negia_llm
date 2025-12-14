# 🤖 NEGIA_LLM : Système de Négociation de Prix Automatisé
## Contexte
Projet académique réalisé dans le cadre du cours **NLP (Natural Language Processing)** dirigé par **M. Gracieux HOUNNA**.  
## Groupe 1 
### Membres du Groupe
BALOGOUN Sobour
BOSSOU Amola

## Institut de Formation et de Recherche en Informatique (UAC)

**NEGIA_LLM** est un **agent conversationnel** capable de simuler des négociations commerciales réalistes et d’évaluer la persuasion des échanges.

### Objectifs
- Simuler des scénarios de vente (Vendeur IA vs Client Humain)  
- Défendre un prix selon une stratégie prédéfinie  
- Évaluer la pertinence et la force de persuasion  

## Fonctionnalités Clés
- **Moteur IA LLaMA** via l’API Groq pour génération de texte rapide  
- **Architecture modulaire** : séparation prompts, mémoire, logique métier, interface  
- **Multi-scénarios** : Automobile, Immobilier, Tech (`data/scenarios.json`)  
- **Prompt Engineering** : persona du vendeur dans `prompts/seller.txt`  
- **Mémoire conversationnelle** (`utils/memory.py`)  
- **Évaluation automatique des réponses** (`utils/evaluator.py`)  

## Structure du Projet
```plaintext
NEGIA_LLM/
│
├── .venv/                 # Environnement virtuel
├── data/                  # Données statiques
│   ├── history.json       # Sauvegarde des conversations
│   ├── intro.json         # Messages d'accueil
│   └── scenarios.json     # Configuration des scénarios de vente
│
├── models/                # Logique d'interaction avec le LLM
│   └── llm_groq.py        # Interface avec l'API Groq (LLaMA)
│
├── prompts/               # Templates de prompts
│   ├── sell_prompt.txt    # Prompt de structure
│   └── seller.txt         # Persona du vendeur (Stratégie)
│
├── utils/                 # Fonctions utilitaires
│   ├── evaluator.py       # Algorithme d'évaluation des réponses
│   └── memory.py          # Gestion de la mémoire à court terme
│
├── .env.clé_api           # Template pour les variables d'environnement
├── app.py                 # Point d'entrée de l'application Streamlit
├── pyproject.toml         # Configuration du projet
├── requirements.in        # Dépendances brutes
├── uv.lock                # Verrouillage des versions (UV)
└── README.md              # Documentation

