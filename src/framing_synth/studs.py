"""
Stud layout at on-centre spacing.

Encodes framing_rules.md §1 (400mm o.c. default) and §2 (stud length formula).
Studs whose grid position falls inside an opening are omitted here — they are
replaced by king/jack/cripple members in openings.py.

IFC mapping (framing_rules.md §6): type="stud" -> IfcMember PredefinedType=STUD.
"""
from __future__ import annotations

from ._geometry import in_any_span, make_member, stud_grid
from ._rules import (
    N_BOTTOM_PLATES,
    N_TOP_PLATES,
    PLATE_THICKNESS_MM,
    STUD_SPACING_MM,
)
from .plates import stud_section_for


def stud_length(height: float) -> float:
    """Stud length = wall height − bottom plate − double top plate.

    framing_rules.md §2: height − 1·38 − 2·38 = height − 114 mm.
    """
    return height - (N_BOTTOM_PLATES + N_TOP_PLATES) * PLATE_THICKNESS_MM


def make_studs(panel: dict, opening_spans: list[tuple[float, float]]) -> list[dict]:
    """Place standard studs at STUD_SPACING_MM o.c. along the panel.

    - guarantees a stud at each panel end (framing_rules.md §1)
    - stud runs from the top of the bottom plate to the underside of the double
      top plate (framing_rules.md §2)
    - SKIPS any grid position inside an opening span (those become king/jack/
      cripple in openings.py)
    """
    length = float(panel["length"])
    height = float(panel["height"])
    section = stud_section_for(panel)

    z0 = N_BOTTOM_PLATES * PLATE_THICKNESS_MM          # top of bottom plate
    z1 = height - N_TOP_PLATES * PLATE_THICKNESS_MM    # underside of double top plate

    members: list[dict] = []
    for x in stud_grid(length, STUD_SPACING_MM):
        if in_any_span(x, opening_spans):
            continue  # replaced by opening framing (openings.py)
        members.append(
            make_member("stud", "standard_stud", (x, 0.0, z0), (x, 0.0, z1), section)
        )
    return members
