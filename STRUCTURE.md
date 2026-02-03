# 📁 Structure du projet

Le projet a été migré vers Python tout en conservant l'ancienne CLI Node.js en archive. Voici l'organisation actuelle des fichiers :

## 🗂️ Structure

```
roueDeLaFortune/
├── app.py                          # Point d'entrée CLI Python
├── requirements.txt                # Dépendances Python (rich)
├── config.json
├── data/
│   ├── history.json
│   ├── assignments.json
│   └── totem.json                  # immune/forcedQueue/safe
├── chore_manager/
│   ├── __init__.py                 # API publique
│   ├── commands/
│   │   ├── assign.py               # Commande d'attribution des corvées
│   │   ├── status.py               # Affichage du statut
│   │   ├── complete.py             # Marquer comme terminé
│   │   ├── reset.py                # Réinitialisation
│   │   ├── totem.py                # Totem d'immunité
│   │   └── help.py                 # Aide
│   ├── utils/
│   │   ├── file_manager.py         # Gestion des fichiers JSON
│   │   ├── date_helper.py          # Gestion des dates
│   │   ├── user_selector.py        # Algorithme de sélection
│   │   ├── totem_manager.py        # Normalisation du totem
│   │   ├── env.py                  # Détection notebook/TTY
│   │   ├── gradient.py             # Dégradés couleur
│   │   └── console.py              # Console rich
│   └── animations/
│       └── spinner.py              # Animation de la roue + titre
├── notebooks/
│   └── demo.ipynb                  # Notebook de démonstration
└── legacy/
    └── node/                        # Ancienne CLI Node.js (archive)
```

## 📦 Modules Python

### 🎯 Commands (`chore_manager/commands/`)

Chaque commande est isolée dans son propre fichier :

- **assign.py** : Gère la répartition des corvées avec toutes ses options
- **status.py** : Affiche l'historique et le statut des corvées
- **complete.py** : Marque les corvées comme terminées
- **reset.py** : Réinitialise l'historique
- **totem.py** : Gère le totem d'immunité
- **help.py** : Affiche l'aide

### 🛠️ Utils (`chore_manager/utils/`)

Fonctions utilitaires réutilisables :

- **file_manager.py** : Lecture/écriture des fichiers JSON
- **date_helper.py** : Gestion des dates
- **user_selector.py** : Algorithme de sélection équitable
- **totem_manager.py** : Normalisation du totem
- **env.py** : Détection notebook/TTY
- **gradient.py** : Dégradés couleur
- **console.py** : Console Rich partagée

### 🎨 Animations (`chore_manager/animations/`)

Effets visuels :

- **spinner.py** : Animation de la roue de la fortune et titre

## 🚀 Utilisation

Les commandes restent identiques avec Python :

```bash
python app.py assign   # équivaut à --count 3 --auto talomi
python app.py status
python app.py complete # équivaut à talomi --all
```

## 📝 Notes

- L'ancienne CLI Node.js est conservée dans `legacy/node/`
- Les formats de données JSON restent inchangés
- Un notebook de démonstration est disponible dans `notebooks/demo.ipynb`
