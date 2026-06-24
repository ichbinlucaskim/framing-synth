from framing_synth._rules import N_BOTTOM_PLATES, N_TOP_PLATES
from framing_synth.plates import make_plates


def test_plate_count(solid_panel):
    plates = make_plates(solid_panel)
    assert len(plates) == N_BOTTOM_PLATES + N_TOP_PLATES  # 1 + 2 = 3


def test_plate_roles(solid_panel):
    plates = make_plates(solid_panel)
    roles = [p["role"] for p in plates]
    assert roles.count("bottom_plate") == 1
    assert roles.count("top_plate") == 2


def test_plate_length_matches_panel(solid_panel):
    plates = make_plates(solid_panel)
    for p in plates:
        length = abs(p["end"]["x"] - p["start"]["x"])
        assert abs(length - 3000) < 1.0


def test_exterior_plates_are_2x6(solid_panel):
    # Exterior wall -> 2x6 studs/plates (framing_rules.md §5).
    plates = make_plates(solid_panel)
    assert all(p["section"] == "2x6" for p in plates)
