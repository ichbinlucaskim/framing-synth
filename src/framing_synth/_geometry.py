"""
Geometry primitives shared across the framing modules.

Coordinate model (framing.schema.json point3d), elevation view of one panel:
  x — mm along the panel length (the o.c. / spacing direction)
  y — mm through the wall depth (single plane here; plies offset in y)
  z — mm height above the subfloor

Members are stored as line segments (start/end points) plus a nominal section;
the schema carries the cross-section separately, so geometry here is 1-D lines.
"""
from __future__ import annotations

import math


def make_member(
    type_: str,
    role: str,
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    section: str,
    *,
    mid: str = "",
) -> dict:
    """Build a framing.schema.json member dict.

    ``length`` is the Euclidean length of the segment in mm. ``mid`` is a
    placeholder id; synthesizer.py assigns final sequential ids.
    """
    length = math.dist(start, end)
    return {
        "id": mid,
        "type": type_,
        "role": role,
        "start": {"x": round(start[0], 3), "y": round(start[1], 3), "z": round(start[2], 3)},
        "end": {"x": round(end[0], 3), "y": round(end[1], 3), "z": round(end[2], 3)},
        "section": section,
        "length": round(length, 3),
    }


def stud_grid(length: float, spacing: float) -> list[float]:
    """On-centre stud x-positions across a panel of the given length.

    Guarantees a stud at each panel end (x=0 and x=length); interior studs at
    ``spacing`` o.c. (framing_rules.md §1). Positions are de-duplicated so a
    panel whose length is an exact multiple of the spacing does not double the
    end stud.
    """
    positions: list[float] = []
    x = 0.0
    while x < length - 1e-6:
        positions.append(round(x, 3))
        x += spacing
    positions.append(round(length, 3))  # guaranteed end stud
    # de-dup (handles length being an exact multiple of spacing)
    seen: set[float] = set()
    unique: list[float] = []
    for p in positions:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def in_any_span(x: float, spans: list[tuple[float, float]], *, tol: float = 1e-6) -> bool:
    """True if x lies strictly inside any (lo, hi) opening span."""
    return any(lo + tol < x < hi - tol for lo, hi in spans)
