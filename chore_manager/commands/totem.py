from typing import Any, Dict

from ..utils.console import get_console
from ..utils.file_manager import CONFIG_PATH, TOTEM_PATH, load_json, save_json
from ..utils.totem_manager import normalize_totem


def _load_normalized_totem():
    config = load_json(CONFIG_PATH)
    totem_raw = load_json(TOTEM_PATH)
    normalized = normalize_totem(totem_raw, config["users"])
    return config, normalized


def show_totem_status() -> Dict[str, Any]:
    console = get_console()
    _, totem = _load_normalized_totem()

    console.print("[bold cyan]\n🛡️ Totem d'immunité\n[/]")

    if not totem["immune"]:
        console.print("[grey70]Aucun utilisateur immunisé.[/]")
    else:
        console.print("[bold]Immunisés:[/]")
        for user in totem["immune"]:
            console.print(f"[yellow]  • {user}[/]")

    if not totem["safe"]:
        console.print("[grey70]\nAucun utilisateur à l'abri.[/]")
    else:
        console.print("[bold]\nÀ l'abri:[/]")
        for user in totem["safe"]:
            console.print(f"[cyan]  • {user}[/]")

    if not totem["forcedQueue"]:
        console.print("[grey70]\nAucune sélection forcée en attente.[/]")
    else:
        console.print("[bold]\nFile forcée (prochains tours):[/]")
        for user in totem["forcedQueue"]:
            console.print(f"[cyan]  • {user}[/]")

    console.print("")
    return {"totem": totem}


def add_totem_user(user_name: str) -> Dict[str, Any]:
    console = get_console()
    if not user_name:
        console.print("\n[red]❌ Spécifiez un utilisateur.\n[/]")
        return {"error": "missing_user"}

    config, totem = _load_normalized_totem()
    if user_name not in config["users"]:
        console.print(f"\n[red]❌ Utilisateur \"{user_name}\" introuvable.\n[/]")
        return {"error": "unknown_user"}

    if user_name in totem["immune"]:
        console.print(f"\n[yellow]⚠️  \"{user_name}\" est déjà immunisé.\n[/]")
        return {"error": "already_immune"}

    totem["immune"].append(user_name)
    save_json(TOTEM_PATH, totem)
    console.print(f"\n[green]✓ Totem attribué à \"{user_name}\".\n[/]")
    return {"totem": totem}


def add_safe_user(user_name: str) -> Dict[str, Any]:
    console = get_console()
    if not user_name:
        console.print("\n[red]❌ Spécifiez un utilisateur.\n[/]")
        return {"error": "missing_user"}

    config, totem = _load_normalized_totem()
    if user_name not in config["users"]:
        console.print(f"\n[red]❌ Utilisateur \"{user_name}\" introuvable.\n[/]")
        return {"error": "unknown_user"}

    if user_name in totem["safe"]:
        console.print(f"\n[yellow]⚠️  \"{user_name}\" est déjà à l'abri.\n[/]")
        return {"error": "already_safe"}

    totem["safe"].append(user_name)
    save_json(TOTEM_PATH, totem)
    console.print(f"\n[green]✓ \"{user_name}\" est désormais à l'abri.\n[/]")
    return {"totem": totem}


def remove_totem_user(user_name: str) -> Dict[str, Any]:
    console = get_console()
    if not user_name:
        console.print("\n[red]❌ Spécifiez un utilisateur.\n[/]")
        return {"error": "missing_user"}

    _, totem = _load_normalized_totem()
    before_immune = len(totem["immune"])
    before_forced = len(totem["forcedQueue"])
    before_safe = len(totem["safe"])

    totem["immune"] = [user for user in totem["immune"] if user != user_name]
    totem["forcedQueue"] = [user for user in totem["forcedQueue"] if user != user_name]
    totem["safe"] = [user for user in totem["safe"] if user != user_name]

    if (
        len(totem["immune"]) == before_immune
        and len(totem["forcedQueue"]) == before_forced
        and len(totem["safe"]) == before_safe
    ):
        console.print(f"\n[yellow]⚠️  \"{user_name}\" n'était pas dans le totem.\n[/]")
        return {"error": "not_found"}

    save_json(TOTEM_PATH, totem)
    console.print(f"\n[green]✓ Totem retiré pour \"{user_name}\".\n[/]")
    return {"totem": totem}


def clear_totem() -> Dict[str, Any]:
    console = get_console()
    totem = {"immune": [], "forcedQueue": [], "safe": []}
    save_json(TOTEM_PATH, totem)
    console.print("\n[green]✓ Totem réinitialisé.\n[/]")
    return {"totem": totem}


def remove_safe_user(user_name: str) -> Dict[str, Any]:
    console = get_console()
    if not user_name:
        console.print("\n[red]❌ Spécifiez un utilisateur.\n[/]")
        return {"error": "missing_user"}

    _, totem = _load_normalized_totem()
    before_safe = len(totem["safe"])

    totem["safe"] = [user for user in totem["safe"] if user != user_name]

    if len(totem["safe"]) == before_safe:
        console.print(f"\n[yellow]⚠️  \"{user_name}\" n'était pas à l'abri.\n[/]")
        return {"error": "not_found"}

    save_json(TOTEM_PATH, totem)
    console.print(f"\n[green]✓ \"{user_name}\" n'est plus à l'abri.\n[/]")
    return {"totem": totem}


def clear_safe() -> Dict[str, Any]:
    console = get_console()
    _, totem = _load_normalized_totem()
    if not totem["safe"]:
        console.print("\n[yellow]⚠️  Aucun utilisateur à l'abri.\n[/]")
        return {"error": "empty_safe"}
    totem["safe"] = []
    save_json(TOTEM_PATH, totem)
    console.print("\n[green]✓ Liste \"à l'abri\" réinitialisée.\n[/]")
    return {"totem": totem}
