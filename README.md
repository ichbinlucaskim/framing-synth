# framing-synth

**Synthesise fabrication-ready light-wood-frame members — studs, plates,
headers, and full opening framing — from a single wall panel.**

This is the flagship repo of the AEC pipeline. There is **no public dataset** of
framed walls to learn from, so framing is generated from *rules*, not a model:
a source-cited encoding of the IRC R602.7 and Canadian NBC/OBC prescriptive
provisions (see [`docs/framing_rules.md`](docs/framing_rules.md)). It maps
directly onto the core problem of panelized off-site construction — turning a
wall panel into a cut list and an assembly the shop floor can build.

![framing elevation](examples/demo_viz.png)

*Elevation of a 3000 mm exterior load-bearing panel with a 1200 mm window:
single bottom plate + double top plate, studs at 400 mm o.c., a 2‑2×6 header on
jack studs between full-height king studs, a window sill, and cripple studs
maintaining the o.c. grid above the header and below the sill.*

## Pipeline position

```
panel-decompose (done)  →  framing-synth (THIS)  →  aec-ifc-export (later)
   panel JSON               framing members + BOM      IFC ElementAssembly
```

- **Input:** a panel (`panel.schema.json`) + its openings (`opening.schema.json`).
- **Output:** framing (`framing.schema.json`) + a bill of materials (`bom.schema.json`).

## Quick start

```bash
make setup     # sync LICENSE, install aec-schema + this package (dev extras)
make test      # pytest
make lint      # ruff
make demo      # synthesise examples -> JSON + elevation PNG
```

```python
from framing_synth import synthesize_framing, compute_bom
from aec_schema import validate_framing, validate_bom

framing = synthesize_framing(panel, openings={"window_0": window})
validate_framing(framing)          # JSON Schema + member_count check

bom = compute_bom(framing, panel)  # roll-up by section + sheathing area
validate_bom(bom)
```

`synthesize_framing` runs Level-2 geometric validation internally (containment +
studs clear of openings + member-count) and raises on hard errors; call
`validate_framing_geometry(framing, panel)` directly for a non-raising
`ValidationResult`.

## What it encodes

All values are documented and source-cited in
[`docs/framing_rules.md`](docs/framing_rules.md):

| Area | Rule (default) | Source |
|---|---|---|
| Stud spacing | 400 mm o.c. (NBC/OBC); 406 mm IRC available | IRC R602.3 / NBC 9.23.10.1 |
| Plates | 1 bottom + 2 top (double top plate), 38 mm each | IRC R602.3.1/.2 |
| Stud length | `height − 114 mm` | framing_rules.md §2 |
| Header sizing | tiered 2‑2×6 … 2‑2×12, jack count from table | IRC Table R602.7(1) |
| Nonbearing header | single flat 2×4, ≤ 8 ft | IRC R602.7.4 |
| Sections | 2×4 = 38×89 mm, 2×6 = 38×140 mm, … | CSA / CWC |
| Member type tags | align to `IfcMember` + `IfcElementAssembly` | buildingSMART IFC4.3 |

See [`docs/decisions.md`](docs/decisions.md) for the ADRs (including the
**2970 mm header hard-stop**, ADR-001).

## Limitations

- **Prescriptive, not engineered.** One baseline load case (single storey, roof
  + ceiling, ≤30 psf snow, ≤20 ft width). Openings wider than **2970 mm** are
  rejected — engineered (e.g. LVL) headers are out of scope (ADR-001).
- **Orthogonal panels.** Opening-local x assumes axis-aligned walls (ADR-004).
- **Openings carry ids only** in `panel.schema.json`; pass an `openings` map to
  frame them (ADR-004).
- 2D elevation model (x along panel, z height); ply offset in y is nominal.

## Layout

```
src/framing_synth/   _rules.py (constants) · plates · studs · openings ·
                     synthesizer · bom · validator
docs/                framing_rules.md (source of truth) · decisions.md (ADRs)
examples/            input_panel_*.json · expected_framing.json · expected_bom.json
scripts/             demo.py · visualise.py
tests/               plates · studs · openings · collision · bom · schema
```

Imports only [`aec-schema`](../aec-schema). Licensed under the repo template
LICENSE.
