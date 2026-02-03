import json
import sys
from pathlib import Path

from .console import get_console

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config.json"
HISTORY_PATH = ROOT_DIR / "data" / "history.json"
ASSIGNMENTS_PATH = ROOT_DIR / "data" / "assignments.json"
TOTEM_PATH = ROOT_DIR / "data" / "totem.json"


def load_json(file_path: Path):
    console = get_console()
    try:
        data = file_path.read_text(encoding="utf-8")
        return json.loads(data)
    except Exception as exc:
        console.print(f"[red]❌ Erreur lors de la lecture de {file_path}:[/] {exc}")
        sys.exit(1)


def save_json(file_path: Path, data) -> None:
    console = get_console()
    try:
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        console.print(f"[red]❌ Erreur lors de l'écriture de {file_path}:[/] {exc}")
        sys.exit(1)
