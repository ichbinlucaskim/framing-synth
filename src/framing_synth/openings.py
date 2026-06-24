"""
Opening framing — header, king studs, jack studs, sill, cripple studs.

Encodes framing_rules.md §3 (header tiers + nonbearing flat 2x4) and §4
(opening anatomy). The opening's local centre along the panel is computed in
synthesizer.py and passed in as ``centre_x``.

IFC mapping (framing_rules.md §6): king/jack/cripple -> IfcMember(STUD),
header -> IfcMember(MEMBER), sill -> IfcMember(PLATE-like, type="sill").
"""
from __future__ import annotations

from ._geometry import make_member, stud_grid
from ._rules import (
    HEADER_TIERS,
    N_BOTTOM_PLATES,
    N_TOP_PLATES,
    NONBEARING_HEADER_JACKS,
    NONBEARING_HEADER_MAX_SPAN_MM,
    NONBEARING_HEADER_PLIES,
    NONBEARING_HEADER_SECTION,
    PLATE_THICKNESS_MM,
    SECTIONS_MM,
    SILL_HEIGHT_MM,
    SILL_SECTION,
    STUD_SPACING_MM,
)
from .plates import stud_section_for

_STUD_THICKNESS_MM = PLATE_THICKNESS_MM  # a stud presents its 38mm face along x


def header_for_span(width_mm: float, load_bearing: bool) -> tuple[str, int, int]:
    """Return (section, n_plies, n_jack_each_end) for an opening of given width.

    framing_rules.md §3:
      - nonbearing wall, width <= 2438mm -> single flat 2x4 (IRC R602.7.4)
      - else first HEADER_TIERS row whose span_max >= width
      - width beyond the largest tier (2970mm, ~9'9") is outside the
        prescriptive envelope -> ValueError("engineered design required")
    """
    if width_mm <= 0:
        raise ValueError(f"opening width must be positive, got {width_mm}")

    # Nonbearing wall, opening <= 8ft: single flat 2x4, no structural header
    # required (IRC R602.7.4). Wider nonbearing openings exceed the flat-2x4
    # allowance and fall through to the sized bearing tiers below.
    if not load_bearing and width_mm <= NONBEARING_HEADER_MAX_SPAN_MM:
        return (
            NONBEARING_HEADER_SECTION,
            NONBEARING_HEADER_PLIES,
            NONBEARING_HEADER_JACKS,
        )

    for span_max, section, n_plies, n_jack in HEADER_TIERS:
        if width_mm <= span_max:
            return section, n_plies, n_jack

    raise ValueError(
        f"opening width {width_mm:.0f}mm exceeds the largest prescriptive header "
        f"tier ({HEADER_TIERS[-1][0]:.0f}mm, single 2-2x12): engineered design "
        f"required (framing_rules.md §3, ADR-001)"
    )


def frame_opening(panel: dict, opening: dict, *, centre_x: float | None = None) -> list[dict]:
    """Generate the framing members around a single opening.

    Members (framing_rules.md §4): header (n_plies), king studs (1 each side),
    jack studs (n_jack each side), sill + below-sill cripples for windows, and
    cripple studs above the header maintaining o.c. spacing.

    ``centre_x`` is the opening centre in panel-local x; if omitted, the
    opening's ``position`` is used directly (assumes panel start at wall origin).
    """
    height = float(panel["height"])
    load_bearing = bool(panel["load_bearing"])
    section = stud_section_for(panel)

    width = float(opening["width"])
    opening_height = float(opening["height"])
    is_window = opening.get("type") == "window"
    c = float(opening["position"]) if centre_x is None else float(centre_x)

    header_section, n_plies, n_jack = header_for_span(width, load_bearing)
    # Header depth in elevation: a built-up bearing header stands on edge (use
    # the nominal width); a nonbearing flat 2x4 lies flat (38mm). (§3, §5)
    flat_header = (not load_bearing) and header_section == NONBEARING_HEADER_SECTION
    header_depth = PLATE_THICKNESS_MM if flat_header else SECTIONS_MM[header_section][1]

    # Vertical reference planes (framing_rules.md §2, §4).
    z_base = N_BOTTOM_PLATES * PLATE_THICKNESS_MM          # top of bottom plate
    z_head = height - N_TOP_PLATES * PLATE_THICKNESS_MM    # underside of double top plate

    # Rough opening bottom: floor for doors, sill height for windows (§4).
    rough_bottom_z = z_base + (SILL_HEIGHT_MM if is_window else 0.0)
    header_bottom_z = rough_bottom_z + opening_height
    header_top_z = header_bottom_z + header_depth

    if header_top_z > z_head + 1e-6:
        raise ValueError(
            f"opening {opening.get('id', '?')} is too tall: header top "
            f"{header_top_z:.0f}mm exceeds wall head {z_head:.0f}mm "
            f"(framing_rules.md §4)"
        )

    # Rough opening edges and the king/jack columns either side (§4). When an
    # opening sits close to a panel joint the king/jack columns are clamped to
    # the panel bound — physically, the panel-edge stud doubles as the king
    # stud (framing_rules.md §4; orthogonal-panel limitation).
    length = float(panel["length"])

    def _clamp(x: float) -> float:
        return min(max(x, 0.0), length)

    x_left = c - width / 2.0
    x_right = c + width / 2.0
    king_left_x = _clamp(x_left - 19.0 - n_jack * _STUD_THICKNESS_MM)
    king_right_x = _clamp(x_right + 19.0 + n_jack * _STUD_THICKNESS_MM)

    members: list[dict] = []

    # --- King studs: full-height, one each side (framing_rules.md §4) ---
    for kx in (king_left_x, king_right_x):
        members.append(
            make_member("king", "king_stud", (kx, 0.0, z_base), (kx, 0.0, z_head), section)
        )

    # --- Jack (trimmer) studs: n_jack each side, plate -> header underside ---
    for i in range(n_jack):
        for sign, edge in ((-1.0, x_left), (1.0, x_right)):
            jx = _clamp(edge + sign * (19.0 + i * _STUD_THICKNESS_MM))
            members.append(
                make_member(
                    "jack", "jack_stud", (jx, 0.0, z_base), (jx, 0.0, header_bottom_z), section
                )
            )

    # --- Header: n_plies, spanning king-to-king on top of the jacks (§3) ---
    for ply in range(n_plies):
        y = ply * PLATE_THICKNESS_MM
        members.append(
            make_member(
                "header",
                "header",
                (king_left_x, y, header_bottom_z),
                (king_right_x, y, header_bottom_z),
                header_section,
            )
        )

    # --- Sill + below-sill cripples for windows (framing_rules.md §4) ---
    if is_window:
        members.append(
            make_member(
                "sill", "sill", (x_left, 0.0, rough_bottom_z), (x_right, 0.0, rough_bottom_z),
                SILL_SECTION,
            )
        )
        members += _cripples(
            panel, x_left, x_right, z_base, rough_bottom_z - PLATE_THICKNESS_MM, section
        )

    # --- Cripple studs above the header, maintaining o.c. spacing (§4) ---
    members += _cripples(panel, x_left, x_right, header_top_z, z_head, section)

    return members


def _cripples(
    panel: dict,
    x_left: float,
    x_right: float,
    z0: float,
    z1: float,
    section: str,
) -> list[dict]:
    """Short studs spanning z0->z1 at the panel's o.c. grid lines inside (x_left, x_right).

    Cripples sit on the same global stud grid so the sheathing nailing pattern is
    continuous (framing_rules.md §4). Skipped if the span is non-positive.
    """
    if z1 - z0 <= 1.0:
        return []
    length = float(panel["length"])
    out: list[dict] = []
    for x in stud_grid(length, STUD_SPACING_MM):
        if x_left + 1e-6 < x < x_right - 1e-6:
            out.append(
                make_member("cripple", "cripple_stud", (x, 0.0, z0), (x, 0.0, z1), section)
            )
    return out
