"""
framing-synth — synthesise light-wood-frame members from a wall panel.

Encodes IRC R602.7 + Canadian NBC/OBC prescriptive rules (see
docs/framing_rules.md). No public framing dataset exists; this is a rule-based
synthesis pipeline that turns a wall panel + its openings into fabrication-ready
studs, plates, and opening framing, plus a bill of materials.

Usage
-----
    from framing_synth import synthesize_framing, compute_bom
    from aec_schema import validate_framing, validate_bom

    framing = synthesize_framing(panel, openings=openings_map)
    validate_framing(framing)
    bom = compute_bom(framing, panel)
    validate_bom(bom)
"""
from __future__ import annotations

from .bom import compute_bom
from .synthesizer import synthesize_framing
from .validator import ValidationResult, validate_framing_geometry

__all__ = [
    "synthesize_framing",
    "compute_bom",
    "validate_framing_geometry",
    "ValidationResult",
]
__version__ = "0.1.0"
