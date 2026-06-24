"""
Main synthesis pipeline: panel -> framing members.

Orchestrates plates + studs + opening framing into a framing.schema.json object.
See docs/framing_rules.md for the rules each step encodes and docs/decisions.md
(ADR-004) for why an openings map is required to frame openings.
"""
from __future__ import annotations

from ._rules import SCHEMA_VERSION
from .openings import frame_opening
from .plates import make_plates
from .studs import make_studs
from .validator import validate_framing_geometry


def _opening_span(panel: dict, opening: dict) -> tuple[float, float, float]:
    """(centre_x, lo, hi) of an opening in panel-local x.

    opening.position is **panel-local**: the distance from the panel start to the
    opening centre, measured along the panel. The producer (panel-decompose,
    decompose_walls(return_openings=True)) performs the wall->panel coordinate
    conversion, so framing-synth consumes the position directly — no offset
    subtraction, and no orthogonal-panel assumption here. See ADR-004.
    """
    centre = float(opening["position"])
    half = float(opening["width"]) / 2.0
    return centre, centre - half, centre + half


def synthesize_framing(panel: dict, openings: dict[str, dict] | None = None) -> dict:
    """Synthesise framing members for a single panel.

    Parameters
    ----------
    panel:
        Panel dict (panel.schema.json).
    openings:
        Map of opening id -> opening dict (opening.schema.json). Required when
        the panel lists opening ids, because panel.schema.json stores ids only,
        not geometry (ADR-004).

    Returns
    -------
    Framing dict (framing.schema.json) with sequential member ids.
    """
    openings = openings or {}
    opening_ids = panel.get("openings", []) or []

    resolved: list[dict] = []
    for oid in opening_ids:
        if oid not in openings:
            raise ValueError(
                f"panel {panel['id']!r} references opening {oid!r} but no geometry "
                f"was supplied; pass openings={{id: opening_dict}} "
                f"(see docs/decisions.md ADR-004)"
            )
        centre, _, _ = _opening_span(panel, openings[oid])
        resolved.append({**openings[oid], "_centre_x": centre})

    # Frame openings first, then derive the stud-skip spans from each opening's
    # actual header extent (king-to-king, post-clamping). This keeps the studs
    # cleared exactly where the validator expects — the two cannot disagree.
    opening_members: list[dict] = []
    skip_spans: list[tuple[float, float]] = []
    for opening in resolved:
        oms = frame_opening(panel, opening, centre_x=opening["_centre_x"])
        opening_members += oms
        header_xs = [
            x for m in oms if m["type"] == "header" for x in (m["start"]["x"], m["end"]["x"])
        ]
        if header_xs:
            skip_spans.append((min(header_xs), max(header_xs)))

    members: list[dict] = []
    members += make_plates(panel)
    members += make_studs(panel, skip_spans)
    members += opening_members

    # Sequential, stable member ids.
    for i, m in enumerate(members, start=1):
        m["id"] = f"{panel['id']}-m{i:03d}"

    framing = {
        "schema_version": SCHEMA_VERSION,
        "panel_id": panel["id"],
        "members": members,
        "member_count": len(members),
    }

    # Level-2 geometric validation (raises on hard geometric errors).
    validate_framing_geometry(framing, panel, raise_on_error=True)
    return framing
