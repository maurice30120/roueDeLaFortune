import colorsys
from typing import Iterable, Sequence, Tuple

from rich.text import Text

RGB = Tuple[int, int, int]


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _blend(c1: RGB, c2: RGB, t: float) -> RGB:
    return (
        int(_lerp(c1[0], c2[0], t)),
        int(_lerp(c1[1], c2[1], t)),
        int(_lerp(c1[2], c2[2], t)),
    )


def _gradient_color(colors: Sequence[RGB], position: float) -> RGB:
    if len(colors) == 1:
        return colors[0]
    position = max(0.0, min(1.0, position))
    segments = len(colors) - 1
    scaled = position * segments
    index = min(int(scaled), segments - 1)
    local_t = scaled - index
    return _blend(colors[index], colors[index + 1], local_t)


def _apply_gradient(text: str, colors: Sequence[RGB]) -> Text:
    result = Text()
    if not text:
        return result
    length = len(text)
    denom = max(length - 1, 1)
    for i, ch in enumerate(text):
        t = i / denom
        r, g, b = _gradient_color(colors, t)
        result.append(ch, style=f"rgb({r},{g},{b})")
    return result


def rainbow_text(text: str) -> Text:
    result = Text()
    if not text:
        return result
    length = len(text)
    denom = max(length - 1, 1)
    for i, ch in enumerate(text):
        hue = i / denom
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        result.append(ch, style=f"rgb({int(r*255)},{int(g*255)},{int(b*255)})")
    return result


def pastel_text(text: str) -> Text:
    result = Text()
    if not text:
        return result
    length = len(text)
    denom = max(length - 1, 1)
    for i, ch in enumerate(text):
        hue = i / denom
        r, g, b = colorsys.hsv_to_rgb(hue, 0.4, 0.95)
        result.append(ch, style=f"rgb({int(r*255)},{int(g*255)},{int(b*255)})")
    return result


def cristal_text(text: str) -> Text:
    colors = [
        (161, 196, 253),
        (194, 233, 251),
    ]
    return _apply_gradient(text, colors)


def gradient_lines(lines: Iterable[str], palette: str = "rainbow") -> Text:
    items = list(lines)
    result = Text()
    for idx, line in enumerate(items):
        if palette == "pastel":
            text = pastel_text(line)
        elif palette == "cristal":
            text = cristal_text(line)
        else:
            text = rainbow_text(line)
        result.append_text(text)
        if idx < len(items) - 1:
            result.append("\n")
    return result
