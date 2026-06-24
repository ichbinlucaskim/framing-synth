"""
Bill of materials — roll up framing members by nominal section.

Produces a bom.schema.json object: one row per section with member count and
summed length, suitable for a cutting list / procurement. Optional sheathing
area is the panel face area (length × height).
"""
from __future__ import annotations

from ._rules import SCHEMA_VERSION


def compute_bom(framing: dict, panel: dict | None = None) -> dict:
    """Roll framing members up into a bill of materials.

    Members are grouped by ``section``; each row carries the count and the
    summed ``length`` in mm. If ``panel`` is given, the exterior sheathing area
    (panel face, m²) is included.
    """
    counts: dict[str, int] = {}
    totals: dict[str, float] = {}
    for m in framing["members"]:
        section = m["section"]
        counts[section] = counts.get(section, 0) + 1
        totals[section] = totals.get(section, 0.0) + float(m["length"])

    # Stable ordering by section for deterministic output.
    items = [
        {
            "section": section,
            "count": counts[section],
            "total_length_mm": round(totals[section], 3),
        }
        for section in sorted(counts)
    ]

    bom = {
        "schema_version": SCHEMA_VERSION,
        "panel_id": framing["panel_id"],
        "items": items,
    }

    if panel is not None:
        bom["sheathing_area_m2"] = round(
            float(panel["length"]) * float(panel["height"]) / 1_000_000.0, 4
        )

    return bom
