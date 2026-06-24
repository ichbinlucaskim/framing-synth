"""
Demo: load panel(s) -> synthesise framing + BOM -> write JSON + elevation viz.

Run from framing-synth/ root:
    python scripts/demo.py

Source priority:
  1. ../panel-decompose/examples/demo_panels.json if present. Those panels carry
     opening *ids* only (no geometry — panel.schema.json stores ids), so any
     panel with openings is framed as solid here, with a note (ADR-004).
  2. The bundled examples/input_panel_*.json, which include an openings map so
     the flagship window elevation can be framed in full.

The flagship window example is always synthesised for the elevation image.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from aec_schema import validate_bom, validate_framing  # noqa: E402
from visualise import render_framing  # noqa: E402

from framing_synth import compute_bom, synthesize_framing  # noqa: E402

HERE = Path(__file__).parent.parent
EXAMPLES_DIR = HERE / "examples"


def _load_bundled(name: str) -> tuple[dict, dict]:
    data = json.loads((EXAMPLES_DIR / name).read_text())
    return data["panel"], data.get("openings", {})


def main() -> None:
    # (panel, openings, label) tuples to synthesise.
    jobs: list[tuple[dict, dict, str]] = []

    window_panel, window_openings = _load_bundled("input_panel_window.json")
    solid_panel, _ = _load_bundled("input_panel_solid.json")
    jobs.append((window_panel, window_openings, "bundled window"))
    jobs.append((solid_panel, {}, "bundled solid"))

    pd_dir = HERE.parent / "panel-decompose" / "examples"
    pd_output = pd_dir / "demo_panels.json"
    if pd_output.exists():
        panels = json.loads(pd_output.read_text()).get("panels", [])
        # panel-decompose now propagates opening geometry in panel-local coords
        # (ADR-004), so real openings can be framed instead of stripped.
        pd_openings_file = pd_dir / "demo_openings.json"
        pd_openings = (
            json.loads(pd_openings_file.read_text()) if pd_openings_file.exists() else {}
        )
        n_with = sum(1 for p in panels if p.get("openings"))
        print(
            f"Found panel-decompose output: {len(panels)} panels "
            f"({n_with} with openings), {len(pd_openings)} opening geometries"
        )
        for p in panels:
            jobs.append((p, pd_openings, f"panel-decompose {p['id']}"))

    all_framings: list[dict] = []
    all_boms: list[dict] = []
    n_framed_openings = 0
    for panel, openings, label in jobs:
        try:
            framing = synthesize_framing(panel, openings=openings or None)
        except ValueError as exc:
            # Out-of-envelope opening (e.g. too tall / wider than the prescriptive
            # header tiers). Skip rather than abort the whole demo over real data.
            print(f"  {label}: SKIPPED — {exc}")
            continue
        validate_framing(framing)
        bom = compute_bom(framing, panel)
        validate_bom(bom)
        all_framings.append(framing)
        all_boms.append(bom)
        if any(m["type"] in ("header", "sill") for m in framing["members"]):
            n_framed_openings += 1
        print(f"  {label}: {framing['member_count']} members, {len(bom['items'])} BOM rows")

    print(f"Panels with real framed openings (header/sill): {n_framed_openings}")

    (EXAMPLES_DIR / "demo_framing.json").write_text(
        json.dumps({"framings": all_framings}, indent=2)
    )
    (EXAMPLES_DIR / "demo_bom.json").write_text(json.dumps({"boms": all_boms}, indent=2))
    print(f"Wrote demo_framing.json + demo_bom.json -> {EXAMPLES_DIR}")

    # Flagship elevation: the window panel.
    render_framing(all_framings[0], window_panel, save_path=EXAMPLES_DIR / "demo_viz.png")


if __name__ == "__main__":
    main()
