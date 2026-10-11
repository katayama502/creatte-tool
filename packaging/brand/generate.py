#!/usr/bin/env python3
"""Generates Creatte Tool's brand artwork as SVG: the app mark, the menu-bar template mark,
the header wordmarks and the twelve app icons. Glyphs are converted to outlines from
M PLUS Rounded 1c Black (SIL OFL 1.1), so the SVGs need no fonts to render.

Usage: python3 packaging/brand/generate.py <repo root>
Then packaging/icons.sh renders the PNG / ICO / ICNS files from them.
"""
import os
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..")
FONT = TTFont(os.path.join(os.path.dirname(__file__), "MPLUSRounded1c-Black.ttf"))
GS = FONT.getGlyphSet()
CMAP = FONT.getBestCmap()
UPM = FONT["head"].unitsPerEm

ORANGE, ORANGE_DARK, CREAM, WHITE, INK = "#F39A28", "#FF9100", "#FFF3E0", "#FEFEFE", "#1A1A1A"
BROWN = "#3D2014"
LETTERS = [("C", BROWN), ("r", "#E84C4C"), ("e", "#3B82C4"), ("a", "#2BAE6B"), ("t", "#F0B429"), ("t", "#F0B429"), ("e", "#E84C7A")]


def glyph(ch, x, baseline, size):
    """SVG path data for `ch` with its origin at (x, baseline), `size` px per em; and its advance."""
    name = CMAP[ord(ch)]
    pen = SVGPathPen(GS)
    s = size / UPM
    GS[name].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
    return pen.getCommands(), GS[name].width * s


def text_width(text, size, tracking=0.0):
    return sum(GS[CMAP[ord(c)]].width for c in text) * size / UPM + tracking * (len(text) - 1)


def run(text_colors, x, baseline, size, tracking=0.0):
    out = []
    for ch, color in text_colors:
        d, adv = glyph(ch, x, baseline, size)
        if d:
            out.append(f'<path fill="{color}" d="{d}"/>')
        x += adv + tracking
    return "".join(out), x


def write(rel, svg):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


def mark(card=WHITE):
    """The app mark: an orange rounded square holding a white card, a brown "C" and the five
    wordmark colours as dots: Creatte's orange-background-and-white-card signature."""
    c, adv = glyph("C", 0, 0, 560)
    cx = 512 - adv / 2
    c, _ = glyph("C", cx, 650, 560)
    dots = "".join(
        f'<circle cx="{332 + i * 90}" cy="780" r="30" fill="{col}"/>'
        for i, col in enumerate(["#E84C4C", "#3B82C4", "#2BAE6B", "#F0B429", "#E84C7A"])
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img" aria-label="Creatte Tool">'
        "<title>Creatte Tool</title>"
        f'<rect x="0" y="0" width="1024" height="1024" rx="228" fill="{ORANGE}"/>'
        f'<rect x="132" y="132" width="760" height="760" rx="150" fill="{card}"/>'
        f'<path fill="{BROWN}" d="{c}"/>{dots}</svg>'
    )


def mark_template():
    """Black on transparent for the macOS menu bar (macOS tints it): the "C" and one dot row."""
    c, adv = glyph("C", 0, 0, 780)
    c, _ = glyph("C", 512 - adv / 2, 760, 780)
    dots = "".join(f'<circle cx="{332 + i * 90}" cy="900" r="38" fill="#000"/>' for i in range(5))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><path fill="#000" d="{c}"/>{dots}</svg>'


def wordmark(dark):
    """'Creatte Tool': each letter of Creatte in its brand colour, then 'Tool' in ink."""
    size, base = 100, 100
    first = BROWN if not dark else "#FFF3E0"
    letters = [(LETTERS[0][0], first)] + LETTERS[1:]
    a, x = run(letters, 0, base, size, -2)
    tool_col = "#FFFFFF" if dark else INK
    b, x = run([(c, tool_col) for c in "Tool"], x + 28, base, size, -2)
    w = round(x + 4)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -8 {w} 136" width="{w}" height="136">{a}{b}</svg>', w / 136


APPS = [
    ("photocraft", "Ph", "#2F7BF5"), ("vectorcraft", "Ve", "#E8573F"), ("filmcraft", "Fi", "#8B5CF6"),
    ("lightcraft", "Li", "#F2A516"), ("pdfcraft", "Pd", "#12A58A"), ("effectcraft", "Ef", "#E0368F"),
    ("designcraft", "La", "#7BB51C"), ("wordcraft", "Wr", "#3F5FE0"), ("deckcraft", "De", "#F07A1E"),
    ("gridcraft", "Sh", "#1F9D55"), ("cadcraft", "Ca", "#3EA6E8"), ("soundcraft", "So", "#1FA5C9"),
]


def app_icon(abbr, color):
    size = 330
    w = text_width(abbr, size, -10)
    t, _ = run([(c, color) for c in abbr], 512 - w / 2, 640, size, -10)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'
        f'<rect width="1024" height="1024" rx="228" fill="{color}"/>'
        f'<rect x="120" y="120" width="784" height="784" rx="160" fill="{WHITE}"/>'
        f'{t}<rect x="372" y="720" width="280" height="36" rx="18" fill="{ORANGE_DARK}"/></svg>'
    )


if __name__ == "__main__":
    write("assets/brand/creatte-mark.svg", mark())
    write("assets/brand/creatte-mark-black.svg", mark_template())
    light, aspect = wordmark(False)
    dark, _ = wordmark(True)
    write("assets/brand/creatte-tool-wordmark.svg", light)
    write("assets/brand/creatte-tool-wordmark-white.svg", dark)
    with open(os.path.join(ROOT, "assets/brand/wordmark-aspect.txt"), "w") as f:
        f.write(f"{aspect:.4f}\n")
    for app_id, abbr, color in APPS:
        write(f"assets/brand/app-icons/{app_id}.svg", app_icon(abbr, color))
    print("brand SVGs written; wordmark aspect", round(aspect, 4))
