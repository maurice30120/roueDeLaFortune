# 🏠 Application de répartition des corvées

Une application Python en ligne de commande (et notebook) pour gérer la répartition équitable des corvées entre plusieurs utilisateurs.

## 📋 Fonctionnalités

- ✅ Répartition équitable basée sur l'historique
- 📊 Suivi des tâches effectuées par chaque personne
- 💾 Sauvegarde automatique dans des fichiers JSON
- 🎨 Interface CLI colorée et élégante
- 🔄 Gestion de l'historique et des statistiques
- 📓 Notebook de démonstration (Jupyter/Colab)

## 🚀 Installation

1. **Installer les dépendances Python**
```bash
python -m pip install -r requirements.txt
```

2. **(Optionnel) Créer un environnement virtuel**
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 📖 Utilisation (CLI)

### Commandes principales

#### Répartir les corvées du jour
```bash
python app.py assign
```
Attribue automatiquement 3 corvées `talomi` à 3 personnes en mode auto (équivaut à `--count 3 --auto talomi`).

**Options :**
```bash
# Par défaut : 3 corvées talomi à 3 personnes en mode auto
python app.py assign

# Attribuer la corvée talomi 3 fois (à 3 personnes)
python app.py assign --count 3

# Attribuer une corvée spécifique 3 fois (à 3 personnes différentes)
python app.py assign Aspirateur --count 3

# Attribuer la vaisselle 2 fois
python app.py assign Vaisselle --count 2

# Combiner avec le mode auto
python app.py assign --count 2 --auto

# Forcer l'attribution même si déjà fait aujourd'hui
python app.py assign --force

# Désactiver les animations (utile en CI/notebook)
python app.py assign --no-anim

# Forcer les animations (même sans TTY/notebook)
python app.py assign --anim
```

#### Voir le statut
```bash
python app.py status
```
Affiche l'historique total et les dernières attributions.

#### Marquer une corvée comme terminée
```bash
python app.py complete
```
Marque par défaut toutes les occurrences de `talomi` pour les 3 personnes ciblées (équivaut à `talomi --all`).

**Exemples :**
```bash
# Marquer toutes les occurrences de talomi (par défaut, 3 personnes)
python app.py complete

# Marquer toutes les occurrences de talomi explicitement
python app.py complete talomi --all

# Marquer la première corvée comme terminée
python app.py complete 1

# Marquer par nom de corvée
python app.py complete Vaisselle

# Spécifier l'utilisateur si plusieurs personnes ont la même corvée
python app.py complete Vaisselle -p Alice

# Marquer TOUTES les occurrences d'une corvée avec --all
python app.py complete Aspirateur --all

# Marquer toutes les occurrences d'une corvée spécifique
python app.py complete Vaisselle --all
```

#### Totem d'immunité
Un utilisateur immunisé ne peut pas être sélectionné sur le tour courant. Si la roue tombe sur lui, il est reporté automatiquement au prochain tour (file de forçage). Le totem est consommé quand il déclenche.
Un utilisateur "à l'abri" annule le tour si la roue tombe sur lui : un ASCII art s'affiche et on relance jusqu'à trouver quelqu'un de non protégé.

```bash
# Voir l'état du totem
python app.py totem

# Ajouter un utilisateur immunisé
python app.py totem add "Alice Dupont"

# Retirer un utilisateur immunisé
python app.py totem remove "Alice Dupont"

# Voir la liste "à l'abri"
python app.py totem safe

# Ajouter un utilisateur à l'abri
python app.py totem safe add "Alice Dupont"

# Retirer un utilisateur à l'abri
python app.py totem safe remove "Alice Dupont"

# Réinitialiser la liste "à l'abri"
python app.py totem safe clear

# Réinitialiser le totem
python app.py totem clear
```

#### Réinitialiser l'historique
```bash
python app.py reset
```
Remet à zéro tous les compteurs et l'historique.

#### Afficher l'aide
```bash
python app.py help
```

### Options

- `--auto` : Mode automatique, ignore les attributions déjà faites aujourd'hui (activé par défaut pour `assign`)
- `--count N` : Attribuer seulement N corvées (par défaut `N = 3` pour `assign`)
- `--force` / `-f` : Forcer l'attribution même si déjà fait aujourd'hui
- `--no-anim` : Désactiver les animations (terminal non-TTY / notebook)
- `--anim` : Forcer les animations (même sans TTY/notebook)
- `assign` sans corvée explicite utilise `talomi` par défaut (3 personnes)
- `complete` sans corvée explicite marque toutes les occurrences de `talomi` (`--all`, 3 personnes)
- `complete` utilise `-p/--person` pour préciser l'utilisateur
- `totem` gère l'immunité et la liste "à l'abri" (tour annulé si la roue tombe sur un utilisateur protégé)

## 📓 Notebook (en ligne)

Un notebook de démonstration est disponible : `notebooks/demo.ipynb`.

- Il utilise le module Python (`chore_manager`) pour exécuter les mêmes actions.
- En environnement Jupyter/Colab, les animations sont désactivées par défaut.
- Vous pouvez forcer les animations en passant `animate=True` si l'environnement le supporte.

## 🧩 Utilisation en module Python

```python
from chore_manager import assign_chores, show_status, complete_chore

assign_chores(count=2, specific_chore="Vaisselle", auto_mode=True, force_mode=True, animate=False)
show_status()
complete_chore("Vaisselle", all_mode=True)
```

## ⚙️ Configuration

Modifiez le fichier `config.json` pour personnaliser les utilisateurs et les corvées :

```json
{
  "users": [
    "Alice",
    "Bob",
    "Clara",
    "David"
  ],
  "chores": [
    "Vaisselle",
    "Aspirateur",
    "Courses",
    "Poubelles"
  ]
}
```

## 🧮 Algorithme de répartition

L'application utilise un algorithme équitable :

1. **Comptage de l'historique** : Chaque utilisateur a un compteur de tâches effectuées
2. **Sélection des moins chargés** : Trouve les utilisateurs ayant fait le moins de tâches
3. **Choix aléatoire** : Si plusieurs utilisateurs sont à égalité, sélection aléatoire
4. **Mise à jour** : Incrémente le compteur de l'utilisateur sélectionné

### Exemple

```json
{
  "Alice": 3,
  "Bob": 2,
  "Clara": 4,
  "David": 2
}
```

Bob et David ont effectué 2 tâches → candidats → sélection aléatoire entre eux.

## 📁 Structure des données

### history.json
Stocke le nombre total de tâches par utilisateur.

```json
{
  "Alice": 5,
  "Bob": 4,
  "Clara": 6,
  "David": 4
}
```

### assignments.json
Stocke toutes les attributions avec leur date.

```json
[
  {
    "date": "2025-10-22",
    "chore": "Vaisselle",
    "user": "Bob",
    "completed": false
  }
]
```

### totem.json
Stocke l'état du totem d'immunité.

```json
{
  "immune": [
    "Alice Dupont"
  ],
  "forcedQueue": [
    "Bob Martin"
  ],
  "safe": [
    "Clara"
  ]
}
```

## 🗃️ Ancienne version Node.js

L'ancienne CLI Node.js a été déplacée dans `legacy/node/` pour archival. Les formats de données restent identiques.

## 📝 Licence

MIT
