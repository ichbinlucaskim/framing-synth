from framing_synth import synthesize_framing, validate_framing_geometry


def test_no_member_outside_panel(solid_panel):
    framing = synthesize_framing(solid_panel)
    result = validate_framing_geometry(framing, solid_panel)
    assert result.valid, str(result)


def test_member_count_matches(solid_panel):
    framing = synthesize_framing(solid_panel)
    assert framing["member_count"] == len(framing["members"])


def test_studs_clear_of_opening(window_panel):
    panel, openings = window_panel
    framing = synthesize_framing(panel, openings=openings)
    result = validate_framing_geometry(framing, panel)
    assert result.valid, str(result)
