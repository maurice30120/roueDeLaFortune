from rich.console import Console

from .env import force_animate_from_env

_console = None


def _build_console() -> Console:
    if force_animate_from_env():
        return Console(force_terminal=True, color_system="truecolor")
    return Console()


def get_console() -> Console:
    global _console
    if _console is None:
        _console = _build_console()
    return _console
