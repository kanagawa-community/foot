#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.ini from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# The 16 ANSI colors, normal then bright.
COLORS = [f"term.{c}" for c in ANSI] + [f"term.bright_{c}" for c in ANSI]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

def theme(variant, appearance, c):
    h = lambda r: c[r].lstrip("#")  # noqa: E731
    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/foot", ""]
    out += ["[main]", f"initial-color-theme={appearance}", ""]
    out += [f"[colors-{appearance}]", f"cursor={h('ui.bg')} {h('ui.fg_dim')}"]
    out += [f"foreground={h('ui.fg')}", f"background={h('ui.bg')}"]
    out += [f"selection-foreground={h('ui.fg')}", f"selection-background={h('ui.bg_visual')}"]
    out += [f"regular{i}={h(r)}" for i, r in enumerate(COLORS[:8])]
    out += [f"bright{i}={h(r)}" for i, r in enumerate(COLORS[8:])]
    out += [f"16={h('term.extended_1')}", f"17={h('term.extended_2')}"]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.ini"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(theme(v, variants[v]["appearance"], roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
