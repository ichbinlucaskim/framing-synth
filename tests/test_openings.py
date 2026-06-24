import pytest

from framing_synth.openings import frame_opening, header_for_span


def test_header_tier_selection():
    assert header_for_span(1000, load_bearing=True)[0] == "2x6"   # <=4ft
    assert header_for_span(1500, load_bearing=True)[0] == "2x8"   # <=6ft
    assert header_for_span(2400, load_bearing=True)[0] == "2x10"  # <=8ft


def test_nonbearing_uses_flat_2x4():
    section, plies, jacks = header_for_span(2000, load_bearing=False)
    assert section == "2x4"


def test_oversized_opening_raises():
    with pytest.raises(ValueError):
        header_for_span(5000, load_bearing=True)  # beyond largest tier (2970mm)


def test_window_has_header_king_jack_sill(window_panel):
    panel, openings = window_panel
    members = frame_opening(panel, openings["window_0"])
    types = {m["type"] for m in members}
    assert "header" in types
    assert "king" in types
    assert "jack" in types
    assert "sill" in types  # window -> sill present


def test_door_has_no_sill(window_panel):
    panel, openings = window_panel
    door = dict(openings["window_0"])
    door["type"] = "door"
    members = frame_opening(panel, door)
    types = {m["type"] for m in members}
    assert "sill" not in types  # doors have no sill
