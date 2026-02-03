from typing import Any, Dict, List

from ..utils.console import get_console
from ..utils.date_helper import get_today_date
from ..utils.file_manager import ASSIGNMENTS_PATH, CONFIG_PATH, HISTORY_PATH, TOTEM_PATH, load_json
from ..utils.totem_manager import normalize_totem


def show_status() -> Dict[str, Any]:
    console = get_console()
    config = load_json(CONFIG_PATH)
    history = load_json(HISTORY_PATH)
    assignments = load_json(ASSIGNMENTS_PATH)

    console.print("[bold cyan]\n📊 Statut des corvées\n[/]")

    console.print("[bold]Historique total :[/]")
    for user, count in sorted(history.items(), key=lambda item: item[1]):
        bar = "█" * count
        console.print(
            f"[yellow]{user.ljust(30)}[/] [cyan]{bar}[/] [grey70]({count})[/]"
        )

    console.print("")

    today = get_today_date()
    today_assignments = [a for a in assignments if a.get("date") == today]

    if today_assignments:
        console.print(f"[bold]Attributions du jour ({today}) :[/]")
        for assignment in today_assignments:
            status = "[green]✓[/]" if assignment.get("completed") else "[grey70]○[/]"
            console.print(
                f"{status} [bold]{assignment['chore'].ljust(15)}[/] → [yellow]{assignment['user']}[/]"
            )
    else:
        console.print("[grey70]Aucune attribution pour aujourd'hui.[/]")

    totem_raw = load_json(TOTEM_PATH)
    totem = normalize_totem(totem_raw, config["users"])
    console.print("[bold]\nTotem d'immunité :[/]")
    if not totem["immune"]:
        console.print("[grey70]  Immunisés : aucun[/]")
    else:
        console.print("[grey70]  Immunisés :[/] [yellow]" + ", ".join(totem["immune"]) + "[/]")
    if not totem["safe"]:
        console.print("[grey70]  À l'abri : aucun[/]")
    else:
        console.print("[grey70]  À l'abri :[/] [cyan]" + ", ".join(totem["safe"]) + "[/]")
    if not totem["forcedQueue"]:
        console.print("[grey70]  File forcée : aucune[/]")
    else:
        console.print("[grey70]  File forcée :[/] [cyan]" + ", ".join(totem["forcedQueue"]) + "[/]")

    recent_assignments = [a for a in assignments if a.get("date") != today][-5:][::-1]
    if recent_assignments:
        console.print("[bold]\nDernières attributions :[/]")
        for assignment in recent_assignments:
            console.print(
                f"[grey70]{assignment['date']}[/] │ {assignment['chore'].ljust(15)} → [yellow]{assignment['user']}[/]"
            )

    console.print("")

    return {
        "history": history,
        "today_assignments": today_assignments,
        "totem": totem,
        "recent_assignments": recent_assignments,
    }


def show_today_status() -> Dict[str, Any]:
    console = get_console()
    assignments = load_json(ASSIGNMENTS_PATH)
    today = get_today_date()
    today_assignments = [a for a in assignments if a.get("date") == today]

    if not today_assignments:
        return {"today_assignments": []}

    console.print("[bold cyan]📋 Statut du jour:\n[/]")

    completed = len([a for a in today_assignments if a.get("completed")])
    total = len(today_assignments)
    percentage = round((completed / total) * 100)

    for assignment in today_assignments:
        status = "[green]✓[/]" if assignment.get("completed") else "[grey70]○[/]"
        console.print(
            f"{status} [bold]{assignment['chore'].ljust(15)}[/] → [yellow]{assignment['user']}[/]"
        )

    console.print("")
    console.print(f"[cyan]Progression: {completed}/{total} ({percentage}%)[/]")

    if completed == total:
        console.print("[bold green]🎊 Toutes les corvées sont terminées ! Bravo ! 🎊[/]")

    console.print("")

    return {
        "today_assignments": today_assignments,
        "completed": completed,
        "total": total,
        "percentage": percentage,
    }
