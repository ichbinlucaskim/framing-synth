"""
Framing rule constants — encodes docs/framing_rules.md.

Each value cites its rule section. See framing_rules.md for full sources
(IRC R602.7, Canadian NBC/OBC, buildingSMART IFC4.3). This module is the single
point where domain numbers live; logic modules import from here so the rules
stay auditable against the documented source of truth.
"""
from __future__ import annotations

# --- Stud spacing (framing_rules.md §1) ---
STUD_SPACING_MM: float = 400.0      # Canada NBC/OBC default (Promise = Ontario). IRC = 406.
STUD_SPACING_US_MM: float = 406.0   # IRC 16" o.c. alternative (framing_rules.md §1)

# --- Plates (framing_rules.md §2) ---
PLATE_THICKNESS_MM: float = 38.0    # a 2x member laid flat = 1.5"
N_BOTTOM_PLATES: int = 1
N_TOP_PLATES: int = 2               # double top plate (default; framing_rules.md §2)

# --- Cross-sections (framing_rules.md §5), nominal -> (thickness_mm, width_mm) ---
# thickness is the 38mm face (along the wall / o.c. direction); width is the
# nominal depth (through-wall for studs, vertical for an on-edge header).
SECTIONS_MM: dict[str, tuple[float, float]] = {
    "2x3": (38.0, 64.0),
    "2x4": (38.0, 89.0),
    "2x6": (38.0, 140.0),
    "2x8": (38.0, 184.0),
    "2x10": (38.0, 235.0),
    "2x12": (38.0, 286.0),
}

# Default stud section by panel type (framing_rules.md §5):
# exterior walls default to 2x6 for the deeper insulated cavity (energy code).
STUD_SECTION_EXTERIOR: str = "2x6"
STUD_SECTION_INTERIOR: str = "2x4"

# --- Header sizing tiers (framing_rules.md §3) ---
# Simplified, code-grounded. Baseline load case (single storey, roof + ceiling,
# <=20ft building width, <=30psf snow, header top laterally braced) per §3.
# (span_max_mm, header_section, n_plies, n_jack_studs_each_end)
#
# ADR-001 / Option A: the top tier ends at 2970mm — the ACTUAL IRC Table
# R602.7(1) baseline maximum for a single 2-2x12 (~9'9"). The earlier 3658mm
# (12ft) row had no code basis for a single 2-2x12 and is intentionally dropped;
# spans beyond 2970mm raise ValueError (out of prescriptive envelope).
HEADER_TIERS: list[tuple[float, str, int, int]] = [
    (1219.0, "2x6", 2, 1),    # <= 4 ft
    (1829.0, "2x8", 2, 1),    # <= 6 ft
    (2438.0, "2x10", 2, 2),   # <= 8 ft
    (2970.0, "2x12", 2, 2),   # ~9'9" — IRC baseline single 2-2x12 maximum
]

# Nonbearing walls: single flat 2x4 for openings <= 8ft (IRC R602.7.4, §3).
NONBEARING_HEADER_SECTION: str = "2x4"
NONBEARING_HEADER_MAX_SPAN_MM: float = 2438.0
NONBEARING_HEADER_PLIES: int = 1
NONBEARING_HEADER_JACKS: int = 1

# --- Sill / window placement (framing_rules.md §4) ---
SILL_SECTION: str = "2x4"
# Typical residential window sill height above the subfloor (top of sill).
# Documented assumption — opening.schema.json carries no sill-height field.
SILL_HEIGHT_MM: float = 900.0

SCHEMA_VERSION: str = "0.1.0"
