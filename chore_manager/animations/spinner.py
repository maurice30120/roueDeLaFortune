import random
import time
from typing import List

from rich.text import Text

from ..utils.console import get_console
from ..utils.gradient import rainbow_text, pastel_text, cristal_text


FRAMES = ["🎰", "🎲", "🎯", "🎪", "🎨", "🎭", "🎬", "🎪"]
SPIN_DURATION = 2.0
FRAME_DELAY = 0.08


def show_title() -> None:
    console = get_console()
    lines = [
        "╔═══════════════════════════════════════════════╗",
        "║                                               ║",
        "║        🎰  ROUE DE LA FORTUNE  🎰           ║",
        "║          Répartition des corvées              ║",
        "║                                               ║",
        "╚═══════════════════════════════════════════════╝",
    ]
    console.print("")
    for line in lines:
        console.print(rainbow_text(line))
    console.print("")


def spin_wheel(
    users: List[str],
    selected_user: str,
    chore: str,
    animate: bool = True,
) -> None:
    console = get_console()

    if not animate:
        console.print(
            Text("✓ ", style="green")
            + Text(chore.ljust(15), style="bold")
            + Text(" → ")
            + rainbow_text(selected_user)
        )
        return

    iterations = int(SPIN_DURATION / FRAME_DELAY)
    console.print("")

    for i in range(iterations):
        random_user = random.choice(users)
        frame = FRAMES[i % len(FRAMES)]
        progress = i / iterations
        is_slowing = progress > 0.7

        line = f"{frame} {chore.ljust(15)} → {random_user}..."
        if progress < 0.3:
            text = rainbow_text(line)
        elif progress < 0.7:
            text = cristal_text(line)
        else:
            text = pastel_text(line)

        console.print(text, end="\r", soft_wrap=True)

        delay = FRAME_DELAY * (1 + progress * 2) if is_slowing else FRAME_DELAY
        time.sleep(delay)

    console.print(" " * 80, end="\r")

    for i in range(3):
        if i % 2 == 0:
            text = rainbow_text(f"✨ {chore.ljust(15)} → {selected_user} ✨")
        else:
            text = Text(f"✨ {chore.ljust(15)} → {selected_user} ✨", style="bold yellow")
        console.print(text, end="\r", soft_wrap=True)
        time.sleep(0.15)

    console.print(" " * 80, end="\r")
    console.print(
        Text("✓ ", style="green")
        + Text(chore.ljust(15), style="bold")
        + Text(" → ")
        + rainbow_text(selected_user)
    )
    time.sleep(0.3)
