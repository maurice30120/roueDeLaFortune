import os
import sys

_TRUTHY = {"1", "true", "yes", "y", "on"}


def _is_truthy(value: str) -> bool:
    return value.strip().lower() in _TRUTHY


def force_animate_from_env() -> bool:
    return _is_truthy(os.getenv("RDLF_FORCE_ANIM", ""))


def is_notebook() -> bool:
    try:
        from IPython import get_ipython  # type: ignore

        shell = get_ipython()
        if shell is None:
            return False
        return shell.__class__.__name__ == "ZMQInteractiveShell"
    except Exception:
        return False


def is_tty() -> bool:
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def should_animate(no_anim: bool = False, force_anim: bool = False) -> bool:
    if no_anim:
        return False
    if force_anim or force_animate_from_env():
        return True
    if is_notebook():
        return False
    return is_tty()
