# CLI Python – Roue de la Fortune

Cette CLI Python permet de répartir équitablement les corvées, consulter le statut, marquer des tâches comme terminées et gérer le totem.

## Installation

### Option simple (recommandée)
```bash
cd /Users/dhuyet/Documents/roueDeLaFortune
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Vérifier Python
```bash
python3 --version
```

## Lancer la CLI

```bash
python3 app.py help
```

## Fonctions principales (commandes)

### Répartir les corvées
```bash
python3 app.py assign
```
Par défaut : `talomi` x3, mode auto.

Options utiles :
```bash
python3 app.py assign --count 3
python3 app.py assign Vaisselle --count 2
python3 app.py assign --force
python3 app.py assign --no-anim
```

### Voir le statut
```bash
python3 app.py status
```

### Marquer comme terminé
```bash
python3 app.py complete
```
Exemples :
```bash
python3 app.py complete 1
python3 app.py complete Vaisselle
python3 app.py complete Vaisselle -p Alice
python3 app.py complete Aspirateur --all
```

### Totem d’immunité
```bash
python3 app.py totem
python3 app.py totem add "Alice Dupont"
python3 app.py totem remove "Alice Dupont"
python3 app.py totem safe
python3 app.py totem safe add "Alice Dupont"
python3 app.py totem safe remove "Alice Dupont"
python3 app.py totem safe clear
python3 app.py totem clear
```

### Réinitialiser l’historique
```bash
python3 app.py reset
```

## Astuce
Si tu es en notebook ou si ton terminal n’affiche pas bien les animations, utilise `--no-anim`.
