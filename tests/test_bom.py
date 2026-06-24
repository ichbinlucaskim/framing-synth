from framing_synth import compute_bom, synthesize_framing


def test_bom_counts_match_members(solid_panel):
    framing = synthesize_framing(solid_panel)
    bom = compute_bom(framing)
    total_from_bom = sum(item["count"] for item in bom["items"])
    assert total_from_bom == framing["member_count"]


def test_bom_groups_by_section(solid_panel):
    framing = synthesize_framing(solid_panel)
    bom = compute_bom(framing)
    sections = [item["section"] for item in bom["items"]]
    assert len(sections) == len(set(sections))  # no duplicate section rows


def test_bom_total_length_matches_members(window_panel):
    panel, openings = window_panel
    framing = synthesize_framing(panel, openings=openings)
    bom = compute_bom(framing)
    bom_total = sum(item["total_length_mm"] for item in bom["items"])
    member_total = sum(m["length"] for m in framing["members"])
    assert abs(bom_total - member_total) < 1.0
