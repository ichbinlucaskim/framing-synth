from framing_synth.studs import make_studs


def test_studs_at_spacing(solid_panel):
    studs = make_studs(solid_panel, [])
    # 3000mm / 400mm o.c. -> studs at 0,400,...,2800,3000 -> 9 studs (ends guaranteed)
    assert len(studs) >= 8


def test_end_studs_present(solid_panel):
    studs = make_studs(solid_panel, [])
    xs = sorted(s["start"]["x"] for s in studs)
    assert xs[0] == 0
    assert abs(xs[-1] - 3000) < 1.0


def test_stud_length(solid_panel):
    studs = make_studs(solid_panel, [])
    # 2438 - 38 (bottom) - 76 (double top) = 2324mm
    for s in studs:
        assert abs(s["length"] - 2324) < 1.0


def test_studs_skip_opening(window_panel):
    panel, _ = window_panel
    # window 1200 wide centred at 1500 -> span 900-2100mm
    studs = make_studs(panel, [(900, 2100)])
    for s in studs:
        assert not (900 < s["start"]["x"] < 2100), (
            f"Standard stud at {s['start']['x']} falls inside opening"
        )
