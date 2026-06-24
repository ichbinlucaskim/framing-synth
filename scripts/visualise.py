"""
2D elevation view of a synthesised panel: plates, studs, header, king/jack
studs, sill, and cripples, colour-coded by role with a legend.

This is the flagship demo image for framing-synth.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

# Role -> colour. Keys are member "type" tags (framing.schema.json).
_COLOURS: dict[str, str] = {
    "plate": "#8c564b",    # brown
    "stud": "#1f77b4",     # blue
    "header": "#d62728",   # red
    "king": "#2ca02c",     # green
    "jack": "#ff7f0e",     # orange
    "sill": "#9467bd",     # purple
    "cripple": "#17becf",  # cyan
}
_LABELS = {
    "plate": "plate (bottom/top)",
    "stud": "stud (standard)",
    "header": "header",
    "king": "king stud",
    "jack": "jack stud",
    "sill": "sill",
    "cripple": "cripple stud",
}

# Nominal section -> elevation thickness (mm) for horizontal members.
_SECTION_DEPTH = {"2x3": 64, "2x4": 89, "2x6": 140, "2x8": 184, "2x10": 235, "2x12": 286}
_FACE_MM = 38.0  # 2x face thickness drawn for vertical members


def _patch_bounds(m: dict[str, Any]) -> tuple[float, float, float, float]:
    """Return (x, z, width, height) of the rectangle to draw for a member."""
    x0, x1 = m["start"]["x"], m["end"]["x"]
    z0, z1 = m["start"]["z"], m["end"]["z"]
    if abs(x1 - x0) < 1e-6:  # vertical member (stud/king/jack/cripple)
        return x0 - _FACE_MM / 2, min(z0, z1), _FACE_MM, abs(z1 - z0)
    # horizontal member (plate/header/sill): draw upward from the line
    if m["type"] == "header":
        thickness = _SECTION_DEPTH.get(m["section"], _FACE_MM)
        thickness = _FACE_MM if m["section"] == "2x4" else thickness  # flat 2x4 header
    else:
        thickness = _FACE_MM
    return min(x0, x1), z0, abs(x1 - x0), thickness


def render_framing(
    framing: dict[str, Any],
    panel: dict[str, Any],
    save_path: Path | None = None,
) -> None:
    """Render a framing assembly as a labelled 2D elevation."""
    fig, ax = plt.subplots(figsize=(12, 7))

    for m in framing["members"]:
        x, z, w, h = _patch_bounds(m)
        colour = _COLOURS.get(m["type"], "#888888")
        ax.add_patch(
            Rectangle((x, z), w, h, facecolor=colour, edgecolor="black", linewidth=0.4, alpha=0.9)
        )

    length = float(panel["length"])
    height = float(panel["height"])
    ax.add_patch(
        Rectangle((0, 0), length, height, fill=False, edgecolor="black", linewidth=1.2)
    )

    ax.set_xlim(-100, length + 100)
    ax.set_ylim(-100, height + 100)
    ax.set_aspect("equal")
    ax.set_xlabel("x — along panel (mm)")
    ax.set_ylabel("z — height above subfloor (mm)")
    ax.set_title(
        f"framing-synth — panel {panel['id']} "
        f"({panel['panel_type']}, {'load-bearing' if panel['load_bearing'] else 'nonbearing'})"
    )

    present = [t for t in _COLOURS if any(m["type"] == t for m in framing["members"])]
    handles = [
        Patch(facecolor=_COLOURS[t], edgecolor="black", label=_LABELS[t]) for t in present
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.12),
        ncol=4,
        frameon=False,
    )

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close(fig)
