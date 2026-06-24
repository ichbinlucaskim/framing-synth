"""
Plate synthesis — bottom plate (1) + double top plate (2).

Encodes framing_rules.md §2: single bottom plate, double top plate, each a
horizontal 2x member running the full panel length. Plates match the wall stud
section so the wall has a consistent thickness.

IFC mapping (framing_rules.md §6): type="plate" -> IfcMember PredefinedType=PLATE.
"""
from __future__ import annotations

from ._geometry import make_member
from ._rules import (
    N_BOTTOM_PLATES,
    N_TOP_PLATES,
    PLATE_THICKNESS_MM,
    STUD_SECTION_EXTERIOR,
    STUD_SECTION_INTERIOR,
)


def stud_section_for(panel: dict) -> str:
    """Stud/plate nominal section for a panel (framing_rules.md §5).

    Exterior walls default to 2x6 (insulated cavity / energy code); interior and
    shear walls default to 2x4.
    """
    return STUD_SECTION_EXTERIOR if panel.get("panel_type") == "exterior" else STUD_SECTION_INTERIOR


def make_plates(panel: dict) -> list[dict]:
    """Generate bottom + top plates running the panel length.

    Bottom plate at z=0; the two top plates stacked at the head of the wall.
    Each plate spans x in [0, panel.length]. See framing_rules.md §2.
    """
    length = float(panel["length"])
    height = float(panel["height"])
    section = stud_section_for(panel)

    members: list[dict] = []

    # Bottom (sole) plate — single, at the base of the wall (framing_rules.md §2).
    for _ in range(N_BOTTOM_PLATES):
        z = 0.0
        members.append(
            make_member("plate", "bottom_plate", (0.0, 0.0, z), (length, 0.0, z), section)
        )

    # Double top plate — stacked just below the head of the wall (framing_rules.md §2).
    for i in range(N_TOP_PLATES):
        # lowest top plate first: height - 76, then height - 38
        z = height - (N_TOP_PLATES - i) * PLATE_THICKNESS_MM
        members.append(
            make_member("plate", "top_plate", (0.0, 0.0, z), (length, 0.0, z), section)
        )

    return members
