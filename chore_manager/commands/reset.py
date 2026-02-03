from typing import Any, Dict

from ..utils.console import get_console
from ..utils.file_manager import ASSIGNMENTS_PATH, CONFIG_PATH, HISTORY_PATH, TOTEM_PATH, load_json, save_json


def reset(confirm: bool = True) -> Dict[str, Any]:
    console = get_console()
    config = load_json(CONFIG_PATH)

    if confirm:
        console.print("\n[bold yellow]⚠️  Attention : Cette action va réinitialiser tout l'historique ![/]")
        console.print("[grey70]Appuyez sur Ctrl+C pour annuler, ou Entrée pour continuer...[/]")
        try:
            input()
        except KeyboardInterrupt:
            console.print("\n[grey70]Réinitialisation annulée.\n[/]")
            return {"cancelled": True}

    fresh_history = {user: 0 for user in config["users"]}
    fresh_assignments = []
    fresh_totem = {"immune": [], "forcedQueue": [], "safe": []}

    save_json(HISTORY_PATH, fresh_history)
    save_json(ASSIGNMENTS_PATH, fresh_assignments)
    save_json(TOTEM_PATH, fresh_totem)

    console.print("\n[green]✓ Historique réinitialisé avec succès !\n[/]")
    return {
        "history": fresh_history,
        "assignments": fresh_assignments,
        "totem": fresh_totem,
    }
