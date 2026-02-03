import random
from typing import Any, Dict, List, Optional

from ..animations.spinner import show_title, spin_wheel
from ..utils.console import get_console
from ..utils.date_helper import get_today_date
from ..utils.env import should_animate
from ..utils.file_manager import (
    ASSIGNMENTS_PATH,
    CONFIG_PATH,
    HISTORY_PATH,
    TOTEM_PATH,
    load_json,
    save_json,
)
from ..utils.gradient import pastel_text, rainbow_text
from ..utils.totem_manager import normalize_totem
from ..utils.user_selector import select_user_for_chore


def _has_assignment_today(assignments: List[Dict[str, Any]], today: str) -> bool:
    return any(assignment.get("date") == today for assignment in assignments)


def assign_chores(
    auto_mode: bool = False,
    count: Optional[Any] = None,
    specific_chore: Optional[str] = None,
    force_mode: bool = False,
    animate: Optional[bool] = None,
    no_anim: bool = False,
) -> Dict[str, Any]:
    console = get_console()
    config = load_json(CONFIG_PATH)
    history = load_json(HISTORY_PATH)
    assignments = load_json(ASSIGNMENTS_PATH)

    today = get_today_date()

    if auto_mode and _has_assignment_today(assignments, today) and not force_mode:
        console.print("[yellow]⚠️  Les corvées ont déjà été attribuées aujourd'hui (mode auto).[/]")
        return {"skipped": True, "reason": "already_assigned", "date": today}

    if animate is None:
        animate = should_animate(no_anim=no_anim)

    show_title()

    totem_raw = load_json(TOTEM_PATH)
    normalized = normalize_totem(totem_raw, list(history.keys()))
    immune = normalized["immune"]
    forced_queue = normalized["forcedQueue"]
    safe = normalized["safe"]
    safe_set = set(safe)

    chores_to_assign: List[str] = []

    if specific_chore and count is not None:
        matching = [
            chore
            for chore in config["chores"]
            if specific_chore.lower() in chore.lower()
        ]

        if not matching:
            console.print(f"\n[red]❌ Corvée \"{specific_chore}\" non trouvée dans la configuration.\n[/]")
            console.print("[grey70]Corvées disponibles:[/]")
            for chore in config["chores"]:
                console.print(f"[grey70]  • {chore}[/]")
            console.print("")
            return {"error": "chore_not_found", "date": today}

        chore_to_assign = matching[0]
        try:
            num_count = int(count)
        except Exception:
            num_count = -1

        if num_count < 1:
            console.print("\n[red]❌ Le nombre doit être un nombre positif.\n[/]")
            return {"error": "invalid_count", "date": today}

        chores_to_assign = [chore_to_assign] * num_count

        console.print(f"[grey70]📅 Date : {today}[/]")
        console.print(f"[grey70]🎯 Corvée : {chore_to_assign} x{num_count}[/]")
        console.print("")

    elif count is not None and not specific_chore:
        try:
            num_count = int(count)
        except Exception:
            num_count = -1
        if num_count < 1:
            console.print("\n[red]❌ Le nombre de corvées doit être un nombre positif.\n[/]")
            return {"error": "invalid_count", "date": today}

        if num_count > len(config["chores"]):
            console.print(
                f"\n[yellow]⚠️  Vous avez demandé {num_count} corvées mais il n'y en a que {len(config['chores'])} disponibles.[/]"
            )
            console.print(
                f"[grey70]Toutes les {len(config['chores'])} corvées seront attribuées.\n[/]"
            )
            chores_to_assign = list(config["chores"])
        else:
            chores_to_assign = random.sample(config["chores"], num_count)

        if not chores_to_assign:
            chores_to_assign = list(config["chores"])

        console.print(f"[grey70]📅 Date : {today}[/]")
        console.print(
            f"[grey70]🎯 Nombre de corvées : {len(chores_to_assign)}/{len(config['chores'])}[/]"
        )
        console.print("")

    else:
        chores_to_assign = list(config["chores"])
        console.print(f"[grey70]📅 Date : {today}[/]")
        console.print(f"[grey70]🎯 Toutes les corvées ({len(chores_to_assign)})[/]")
        console.print("")

    users = list(history.keys())
    non_safe_users = [user for user in users if user not in safe_set]
    if non_safe_users:
        total = sum(history[user] for user in non_safe_users)
        avg = round(total / len(non_safe_users))
        for user in safe:
            history[user] = avg

    eligible_users = [user for user in users if user not in safe_set]
    if not eligible_users:
        console.print("\n[red]❌ Aucun utilisateur disponible : tout le monde est \"à l'abri\".\n[/]")
        return {"error": "no_eligible_users", "date": today}

    def show_safe_art(user: str) -> None:
        console.print(
            "[cyan]   .-\"\"\"\"-.\n  /  _  _  \\\n |  (o)(o)  |\n |   .__.   |\n  \\  ----  /\n   `-.__.-`[/]"
        )
        console.print(f"[cyan]🛡️ {user} est à l'abri. Tour annulé, on relance.[/]")

    def select_user_for_run(
        run_history: Dict[str, int],
        run_immune: List[str],
        run_forced_queue: List[str],
        ignore_safe: bool,
    ) -> Dict[str, Any]:
        if run_forced_queue:
            forced_index = next(
                (idx for idx, user in enumerate(run_forced_queue) if user not in safe_set),
                -1,
            )
            if forced_index != -1:
                forced_user = run_forced_queue.pop(forced_index)
                return {"selected_user": forced_user, "restart_all": False}
            if not ignore_safe and run_forced_queue and run_forced_queue[0] in safe_set:
                return {
                    "selected_user": run_forced_queue[0],
                    "restart_all": True,
                    "safe_hit": True,
                }

        exclude_safe = safe if ignore_safe else []
        candidate_all = select_user_for_chore(run_history, exclude=exclude_safe)
        if not candidate_all:
            return {"selected_user": None, "restart_all": False}

        if not ignore_safe and candidate_all in safe_set:
            return {"selected_user": candidate_all, "restart_all": True, "safe_hit": True}

        if candidate_all in run_immune:
            exclude_list = list(set(run_immune + safe))
            alternative = select_user_for_chore(run_history, exclude=exclude_list)
            if alternative:
                if candidate_all in run_immune:
                    run_immune.remove(candidate_all)
                if candidate_all not in run_forced_queue:
                    run_forced_queue.append(candidate_all)
                console.print(f"[grey70]🛡️ Totem actif : {candidate_all} reporté au prochain tour.[/]")
                return {"selected_user": alternative, "restart_all": False}

        return {"selected_user": candidate_all, "restart_all": False}

    today_assignments: List[Dict[str, Any]] = []
    ignore_safe = False
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        attempts += 1
        run_history = dict(history)
        run_assignments: List[Dict[str, Any]] = []
        run_immune = list(immune)
        run_forced_queue = list(forced_queue)
        restart_all = False

        for chore in chores_to_assign:
            result = select_user_for_run(run_history, run_immune, run_forced_queue, ignore_safe)
            if result.get("restart_all"):
                if result.get("safe_hit") and result.get("selected_user"):
                    spin_wheel(users, result["selected_user"], chore, animate=animate)
                    show_safe_art(result["selected_user"])
                restart_all = True
                ignore_safe = True
                break

            selected_user = result.get("selected_user")
            if not selected_user:
                console.print("\n[red]❌ Impossible de sélectionner un utilisateur non protégé.\n[/]")
                return {"error": "no_candidate", "date": today}

            run_history[selected_user] += 1
            run_assignments.append(
                {
                    "date": today,
                    "chore": chore,
                    "user": selected_user,
                    "completed": False,
                }
            )

        if restart_all:
            continue

        for assignment in run_assignments:
            spin_wheel(users, assignment["user"], assignment["chore"], animate=animate)
            today_assignments.append(assignment)
            assignments.append(assignment)

        history.update(run_history)
        immune = run_immune
        forced_queue = run_forced_queue
        break

    if attempts >= max_attempts:
        console.print("\n[red]❌ Trop de relances dues aux utilisateurs \"à l'abri\".\n[/]")
        return {"error": "too_many_retries", "date": today}

    save_json(HISTORY_PATH, history)
    save_json(ASSIGNMENTS_PATH, assignments)
    save_json(TOTEM_PATH, {"immune": immune, "forcedQueue": forced_queue, "safe": safe})

    console.print("")
    console.print(rainbow_text("═" * 50))
    console.print(pastel_text("✨ Répartition terminée avec succès ! ✨"))
    console.print(rainbow_text("═" * 50))
    console.print("")

    return {
        "date": today,
        "assignments": today_assignments,
        "history": history,
        "totem": {"immune": immune, "forcedQueue": forced_queue, "safe": safe},
    }
