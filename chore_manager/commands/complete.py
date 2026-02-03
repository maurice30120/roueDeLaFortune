from typing import Any, Dict, List, Optional

from ..utils.console import get_console
from ..utils.date_helper import get_today_date
from ..utils.file_manager import ASSIGNMENTS_PATH, load_json, save_json
from .status import show_today_status


def complete_chore(
    chore_name: Optional[str],
    user_name: Optional[str] = None,
    all_mode: bool = False,
) -> Dict[str, Any]:
    console = get_console()
    assignments = load_json(ASSIGNMENTS_PATH)
    today = get_today_date()

    today_assignments = [a for a in assignments if a.get("date") == today]

    if not today_assignments:
        console.print("\n[yellow]⚠️  Aucune corvée attribuée pour aujourd'hui.[/]")
        console.print("[grey70]Utilisez \"python app.py assign\" pour attribuer les corvées.\n[/]")
        return {"error": "no_assignments", "date": today}

    if not chore_name:
        console.print("[bold cyan]\n🏠 Corvées du jour\n[/]")
        console.print(f"[grey70]Date : {today}\n[/]")

        for index, assignment in enumerate(today_assignments, start=1):
            status = "[green]✓[/]" if assignment.get("completed") else "[grey70]○[/]"
            console.print(
                f"{index}. {status} [bold]{assignment['chore'].ljust(15)}[/] → [yellow]{assignment['user']}[/]"
            )

        console.print(
            "[grey70]\nUtilisation: python app.py complete <numéro ou nom de la corvée> [-p|--person <nom>] [--all][/]"
        )
        console.print(
            "[grey70]Par défaut: python app.py complete  ≡  talomi --all (3 personnes)[/]"
        )
        console.print("[grey70]Exemples:[/]")
        console.print("[grey70]  python app.py complete 1[/]")
        console.print("[grey70]  python app.py complete Vaisselle[/]")
        console.print("[grey70]  python app.py complete Vaisselle -p Alice[/]")
        console.print("[grey70]  python app.py complete Aspirateur --all\n[/]")
        return {"error": "missing_chore", "date": today}

    target_assignment = None
    assignment_index = -1

    try:
        chore_num = int(chore_name)
    except Exception:
        chore_num = -1

    if chore_num > 0 and chore_num <= len(today_assignments):
        target_assignment = today_assignments[chore_num - 1]
        assignment_index = next(
            (
                idx
                for idx, a in enumerate(assignments)
                if a.get("date") == target_assignment.get("date")
                and a.get("chore") == target_assignment.get("chore")
                and a.get("user") == target_assignment.get("user")
            ),
            -1,
        )
    else:
        matching_assignments = [
            a
            for a in today_assignments
            if chore_name.lower() in a.get("chore", "").lower()
        ]

        if not matching_assignments:
            console.print(f"\n[red]❌ Corvée \"{chore_name}\" non trouvée pour aujourd'hui.\n[/]")
            return {"error": "chore_not_found", "date": today}

        if all_mode:
            completed_count = 0
            for match in matching_assignments:
                if not match.get("completed"):
                    idx = next(
                        (
                            idx
                            for idx, a in enumerate(assignments)
                            if a.get("date") == match.get("date")
                            and a.get("chore") == match.get("chore")
                            and a.get("user") == match.get("user")
                        ),
                        -1,
                    )
                    if idx != -1:
                        assignments[idx]["completed"] = True
                        completed_count += 1

            save_json(ASSIGNMENTS_PATH, assignments)

            if completed_count == 0:
                console.print(
                    f"\n[yellow]⚠️  Toutes les corvées \"{chore_name}\" sont déjà marquées comme terminées.\n[/]"
                )
            else:
                console.print(
                    f"\n[green]✓ {completed_count} corvée(s) \"{chore_name}\" marquée(s) comme terminée(s) !\n[/]"
                )
                for assignment in matching_assignments:
                    console.print(
                        f"[grey70]  •[/] [bold]{assignment['chore']}[/] → [yellow]{assignment['user']}[/]"
                    )
                console.print("[grey70]\nBon travail ! 🎉\n[/]")

            show_today_status()
            return {"completed": completed_count, "date": today}

        if len(matching_assignments) > 1 and not user_name:
            console.print(f"\n[yellow]⚠️  Plusieurs corvées correspondent à \"{chore_name}\":\n[/]")
            for idx, assignment in enumerate(matching_assignments, start=1):
                status = "[green]✓[/]" if assignment.get("completed") else "[grey70]○[/]"
                console.print(
                    f"{idx}. {status} [bold]{assignment['chore']}[/] → [yellow]{assignment['user']}[/]"
                )
            console.print(
                f"[grey70]\nSpécifiez le nom d'utilisateur: python app.py complete {chore_name} -p <nom>[/]"
            )
            console.print(
                f"[grey70]Ou utilisez --all pour toutes les marquer: python app.py complete {chore_name} --all\n[/]"
            )
            return {"error": "ambiguous", "date": today}

        if user_name:
            target_assignment = next(
                (
                    a
                    for a in matching_assignments
                    if a.get("user", "").lower() == user_name.lower()
                ),
                None,
            )
            if not target_assignment:
                console.print(
                    f"\n[red]❌ Corvée \"{chore_name}\" non attribuée à \"{user_name}\" aujourd'hui.\n[/]"
                )
                return {"error": "user_mismatch", "date": today}
        else:
            target_assignment = matching_assignments[0]

        assignment_index = next(
            (
                idx
                for idx, a in enumerate(assignments)
                if a.get("date") == target_assignment.get("date")
                and a.get("chore") == target_assignment.get("chore")
                and a.get("user") == target_assignment.get("user")
            ),
            -1,
        )

    if not target_assignment or assignment_index == -1:
        console.print("\n[red]❌ Erreur interne lors de la sélection de la corvée.\n[/]")
        return {"error": "internal", "date": today}

    if target_assignment.get("completed"):
        console.print(
            f"\n[yellow]⚠️  La corvée \"{target_assignment['chore']}\" ({target_assignment['user']}) est déjà marquée comme terminée.\n[/]"
        )
        return {"error": "already_completed", "date": today}

    assignments[assignment_index]["completed"] = True
    save_json(ASSIGNMENTS_PATH, assignments)

    console.print("\n[green]✓ Corvée terminée ![/]")
    console.print(f"[bold]{target_assignment['chore']}[/] → [yellow]{target_assignment['user']}[/]")
    console.print("[grey70]Bon travail ! 🎉\n[/]")

    show_today_status()
    return {"completed": 1, "assignment": target_assignment, "date": today}
