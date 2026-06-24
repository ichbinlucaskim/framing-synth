# Architecture Decision Records — framing-synth

Short, dated records of non-obvious design decisions. See `framing_rules.md` for
the source-cited domain rules these encode.

---

## ADR-001 — Prescriptive synthesis, not structural design

**Status:** accepted (2026-06-16)

**Context.** framing-synth sizes headers and lays out studs from panel geometry
without performing structural analysis. Real header sizing depends on span,
tributary width, snow/floor loads, species, and storey count.

**Decision.** Encode the *prescriptive* (table-lookup) provisions that IRC/NBC
permit in lieu of engineered design. Header sizes come from a simplified tier
table (`_rules.HEADER_TIERS`) pinned to one baseline load case — single storey,
roof + ceiling only, ≤20 ft building width, ≤30 psf snow, laterally braced
header top (see `framing_rules.md §3`).

**Option A — hard stop at 2970 mm.** The top tier ends at **2970 mm** (~9′9″),
the *actual* IRC Table R602.7(1) baseline maximum for a single 2‑2×12. The
earlier 3658 mm (12 ft) placeholder had **no code basis** for a single 2‑2×12
and was dropped. Openings wider than 2970 mm raise
`ValueError("…engineered design required…")` rather than fabricating an unbacked
size. This was a deliberate Stage-A finding carried into the implementation.

**Consequences.** Output is correct for the documented envelope and *fails loud*
outside it. Multi-storey loads, heavy snow, wide spans, and engineered (LVL)
headers are out of scope and must be handled upstream.

---

## ADR-002 — Stud spacing 400 mm (NBC/OBC) default

**Status:** accepted (2026-06-16)

**Context.** IRC uses 16″ o.c. = 406 mm; the Canadian NBC/OBC expresses o.c.
spacing as a true metric **400 mm**, not a soft-converted 406 mm
(`framing_rules.md §1`).

**Decision.** Default `STUD_SPACING_MM = 400.0`. The IRC value is retained as
`STUD_SPACING_US_MM = 406.0` for callers targeting US jurisdictions.

**Consequences.** The pipeline is Canada-first (the target deployment context).
Switching jurisdictions is a one-constant change, not a code change.

---

## ADR-003 — Member type/role tags align with the IFC4 mapping

**Status:** accepted (2026-06-16)

**Context.** Framing members are consumed downstream by `aec-ifc-export`, which
maps them to `IfcMember` + `IfcElementAssembly` (`framing_rules.md §6`).

**Decision.** Emit `type`/`role` tags that map 1:1 onto IFC predefined types so
no remapping is needed downstream:

| `type` | `role` | IFC4 mapping |
|---|---|---|
| `stud` / `king` / `jack` / `cripple` | `*_stud` | `IfcMember` PredefinedType `STUD` |
| `plate` / `sill` | `bottom_plate` / `top_plate` / `sill` | `IfcMember` PredefinedType `PLATE` |
| `header` | `header` | `IfcMember` PredefinedType `MEMBER` |

Panel → `IfcElementAssembly` (premanufactured), members aggregated via
`IfcRelAggregates`. Source: buildingSMART IFC4.3.

**Consequences.** `aec-ifc-export` is a thin mapping layer. The tag vocabulary
is fixed by `framing.schema.json`'s enums, so drift is caught by schema
validation.

---

## ADR-004 — Openings map required for opening framing

**Status:** accepted (2026-06-16)

**Context.** `panel.schema.json` stores `openings` as a list of **ids only** —
no width/height/position geometry. Framing an opening needs that geometry.

**Decision.** `synthesize_framing(panel, openings=None)` accepts an optional
`{id: opening_dict}` map. If a panel lists opening ids but no matching geometry
is supplied, raise a clear `ValueError` naming the missing id.

**Coordinate convention (updated 2026-06-16).** `opening.position` in the map is
**panel-local** — the distance from the panel start to the opening centre along
the panel. The *producer* performs the wall→panel conversion:
`panel-decompose`'s `decompose_walls(return_openings=True)` emits the map already
in panel-local coordinates (panel-decompose ADR-004). framing-synth therefore
consumes `position` directly, with **no** `panel.start.x` subtraction and no
orthogonal-panel assumption on the consumer side. This replaces the earlier
`position − panel.start.x` derivation, which double-subtracted the offset once
panel-decompose started producing panel-local positions.

**Consequences.** Standalone synthesis is explicit about its inputs; callers
feeding raw panel ids (no geometry) get an actionable error instead of silently
dropping opening framing. The wall→panel coordinate conversion lives in one place
(the producer), so the two repos cannot disagree about the origin.
