import sys


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


def should_animate(no_anim: bool = False) -> bool:
    if no_anim:
        return False
    if is_notebook():
        return False
    return is_tty()
