"""Tests manuels pour la CLI Python (à lancer à la main).

Usage:
  python3 test_manual.py           # affiche la liste des tests
  python3 test_manual.py assign    # lance le test assign
  python3 test_manual.py all       # lance tous les tests (avec sauvegarde/restauration)
"""

import json
import shutil
import sys
import tempfile
from pathlib import Path

from chore_manager import (
    add_safe_user,
    add_totem_user,
    assign_chores,
    clear_safe,
    clear_totem,
    complete_chore,
    remove_safe_user,
    remove_totem_user,
    reset,
    show_status,
    show_totem_status,
)
from chore_manager.utils.file_manager import ASSIGNMENTS_PATH, HISTORY_PATH, TOTEM_PATH

ROOT = Path(__file__).resolve().parent


def _backup_data() -> Path:
    tmp_dir = Path(tempfile.mkdtemp(prefix="chore_manager_test_"))
    data_dir = tmp_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(HISTORY_PATH, data_dir / "history.json")
    shutil.copy2(ASSIGNMENTS_PATH, data_dir / "assignments.json")
    shutil.copy2(TOTEM_PATH, data_dir / "totem.json")
    return tmp_dir


def _restore_data(tmp_dir: Path) -> None:
    data_dir = tmp_dir / "data"
    shutil.copy2(data_dir / "history.json", HISTORY_PATH)
    shutil.copy2(data_dir / "assignments.json", ASSIGNMENTS_PATH)
    shutil.copy2(data_dir / "totem.json", TOTEM_PATH)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_assign_basic():
    print("\n[TEST] assign (par défaut, sans animation)")
    result = assign_chores(auto_mode=True, count=3, specific_chore="talomi", force_mode=True, animate=False)
    print("Résultat:", result)


def test_assign_specific():
    print("\n[TEST] assign (corvée spécifique)")
    result = assign_chores(auto_mode=True, count=2, specific_chore="Vaisselle", force_mode=True, animate=False)
    print("Résultat:", result)


def test_status():
    print("\n[TEST] status")
    result = show_status()
    print("Résumé:", {
        "history_keys": list(result.get("history", {}).keys()),
        "today_count": len(result.get("today_assignments", [])),
    })


def test_complete_by_name():
    print("\n[TEST] complete (par nom, --all)")
    result = complete_chore("talomi", all_mode=True)
    print("Résultat:", result)


def test_complete_by_number():
    print("\n[TEST] complete (par numéro)")
    result = complete_chore("1", all_mode=False)
    print("Résultat:", result)


def test_totem():
    print("\n[TEST] totem add/remove/safe")
    show_totem_status()

    # Choisir un utilisateur existant dans config.json via history.json
    history = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    users = list(history.keys())
    if not users:
        print("Aucun utilisateur trouvé dans history.json")
        return

    user = users[0]
    add_totem_user(user)
    add_safe_user(user)
    show_totem_status()
    remove_totem_user(user)
    remove_safe_user(user)
    clear_safe()
    clear_totem()
    show_totem_status()


def test_reset():
    print("\n[TEST] reset (confirm=False)")
    result = reset(confirm=False)
    print("Résultat:", result)


def run_all():
    backup_dir = _backup_data()
    try:
        test_assign_basic()
        test_assign_specific()
        test_status()
        test_complete_by_name()
        test_complete_by_number()
        test_totem()
        test_reset()
    finally:
        _restore_data(backup_dir)
        print("\nDonnées restaurées après tests.")


def main():
    tests = {
        "assign": test_assign_basic,
        "assign_specific": test_assign_specific,
        "status": test_status,
        "complete_name": test_complete_by_name,
        "complete_number": test_complete_by_number,
        "totem": test_totem,
        "reset": test_reset,
        "all": run_all,
    }

    if len(sys.argv) == 1:
        print("Tests manuels disponibles:")
        for name in tests:
            print(f"  - {name}")
        print("\nExemples:")
        print("  python3 test_manual.py assign")
        print("  python3 test_manual.py all")
        return

    name = sys.argv[1]
    test_fn = tests.get(name)
    if not test_fn:
        print(f"Test inconnu: {name}")
        sys.exit(1)

    if name == "all":
        test_fn()
    else:
        backup_dir = _backup_data()
        try:
            test_fn()
        finally:
            _restore_data(backup_dir)
            print("\nDonnées restaurées après test.")


if __name__ == "__main__":
    main()
