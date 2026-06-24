from aec_schema import validate_bom, validate_framing

from framing_synth import compute_bom, synthesize_framing


def test_framing_passes_schema(window_panel):
    panel, openings = window_panel
    framing = synthesize_framing(panel, openings=openings)
    validate_framing(framing)


def test_bom_passes_schema(solid_panel):
    framing = synthesize_framing(solid_panel)
    bom = compute_bom(framing, solid_panel)
    validate_bom(bom)


def test_solid_framing_passes_schema(solid_panel):
    framing = synthesize_framing(solid_panel)
    validate_framing(framing)
