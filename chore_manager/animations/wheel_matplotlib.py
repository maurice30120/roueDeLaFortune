from __future__ import annotations

import math
import random
from typing import List, Optional


def _ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def spin_wheel_matplotlib(
    users: List[str],
    selected_user: str,
    chore: str,
    *,
    duration_s: float = 2.5,
    fps: int = 30,
    seed: Optional[int] = None,
):
    """
    Notebook-friendly wheel animation (matplotlib) that stops on `selected_user`.

    Returns an IPython display object when available, otherwise returns None.
    """
    try:
        import matplotlib.pyplot as plt  # type: ignore
        from matplotlib.animation import FuncAnimation  # type: ignore
    except Exception:
        return None

    try:
        from IPython.display import HTML  # type: ignore
    except Exception:
        HTML = None  # type: ignore

    if not users or selected_user not in users:
        return None

    n = len(users)
    slice_deg = 360.0 / n
    selected_idx = users.index(selected_user)

    # Pick a random starting angle, then spin multiple turns and land on the selected slice.
    rng = random.Random(seed)
    start_angle = rng.uniform(0.0, 360.0)
    final_angle = 90.0 - (selected_idx + 0.5) * slice_deg  # selected slice center at top
    extra_turns = rng.randint(3, 6)
    end_angle = final_angle + 360.0 * extra_turns

    frames = max(2, int(math.ceil(duration_s * fps)))

    fig, ax = plt.subplots(figsize=(6.5, 6.5), subplot_kw={"aspect": "equal"})
    ax.set_axis_off()

    palette = [
        "#FF6B6B",
        "#FFD93D",
        "#6BCB77",
        "#4D96FF",
        "#9D4EDD",
        "#FF8FAB",
        "#06D6A0",
        "#F77F00",
        "#118AB2",
    ]
    colors = [palette[i % len(palette)] for i in range(n)]

    def draw(angle: float) -> None:
        ax.clear()
        ax.set_axis_off()

        # Wheel
        ax.pie(
            [1] * n,
            labels=users,
            colors=colors,
            startangle=angle,
            counterclock=True,
            labeldistance=0.78,
            textprops={"fontsize": 10, "color": "#111"},
            wedgeprops={"linewidth": 1.5, "edgecolor": "white"},
        )

        # Pointer (triangle) at the top
        ax.plot([0.0], [1.06], marker="v", markersize=18, color="#111")

        ax.text(
            0.0,
            1.22,
            chore,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="#111",
        )

    def update(i: int):
        t = i / (frames - 1)
        eased = _ease_out_cubic(t)
        angle = start_angle + (end_angle - start_angle) * eased
        draw(angle)
        return []

    anim = FuncAnimation(fig, update, frames=frames, interval=1000 / fps, blit=False)

    # Convert to HTML/JS for notebooks.
    if HTML is not None:
        html = anim.to_jshtml()
        plt.close(fig)
        return HTML(html)

    # Fallback: show the final frame only.
    draw(end_angle)
    return None

