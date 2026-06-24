# Framing Rules — Light Wood Frame Synthesis

> Source-cited rule set for synthesising stud/plate/header framing from wall
> panels. This is a prescriptive simplification grounded in **IRC R602.7** and
> the **Canadian NBC / OBC (Part 9)**, **NOT** a structural engineering design.
> Loads are assumed, not calculated. Every numeric rule below cites a primary
> source in §7.

---

## Scope and assumptions

This document governs synthesis of light wood-frame framing members (studs,
plates, headers, and opening framing) for a single wall panel.

| Assumption | Value | Rationale |
|---|---|---|
| Building system | Light wood frame, platform construction | Panelized walls |
| Load case (baseline) | **Single storey — roof + ceiling only** | Simplest prescriptive case in IRC Table R602.7(1); see §3 |
| Lumber grade | **No. 2** Spruce-Pine-Fir (SPF) | Default species group for the IRC/NBC prescriptive tables; SPF is the dominant Canadian framing species |
| Lateral bracing | Header top **is** laterally braced by perpendicular framing | Required for the un-reduced spans in IRC Table R602.7(1); see §3 footnote |
| Jurisdiction default | **Canadian NBC / OBC**  | Drives 400 mm o.c. default and metric member sizes |
| Wall height (default) | 2438 mm (8 ft) | Standard residential storey height |

**Why prescriptive, not engineered:** the framing-synth tool generates framing
geometry from panel + opening inputs without performing structural analysis. It
follows the *prescriptive* (table-lookup) provisions that codes permit in lieu
of engineered design. Where a real project exceeds the prescriptive envelope
(multi-storey loads, snow loads > 30 psf / ~1.4 kPa, building width > 6 m,
spans beyond the tiers in §3), an engineered design is required and this rule
set **does not apply**. The tier table in §3 is deliberately **conservative**
relative to the published maxima (see §3) to keep a safety margin.

---

## 1. Stud spacing

| Jurisdiction | Standard spacing | Permitted wider spacing | Source |
|---|---|---|---|
| US — IRC | **406 mm** (16″ o.c.) | 610 mm (24″ o.c.) | IRC R602.3, Table R602.3(5) [[1]](#7-sources) |
| Canada — NBC / OBC | **400 mm** (metric o.c.) | 600 mm; 300 mm for heavier loads | NBC/OBC Table 9.23.10.1 [[2]](#7-sources)[[3]](#7-sources) |

- **Default for framing-synth: 400 mm o.c.** (Canadian metric value; Promise
  Robotics = Ontario). The NBC expresses on-centre spacing in true metric
  (400 / 600 mm), **not** as a soft-converted 406 mm. [[2]](#7-sources)
- NBC/OBC Table 9.23.10.1 allows **38 × 140 mm (2×6)** exterior-wall studs at
  **400 mm o.c.** up to **3.6 m** unsupported height supporting *roof + 2
  floors*; **38 × 89 mm (2×4)** exterior studs at 400 mm o.c. reach 3.0 m for
  *roof ± attic + 1 floor*. Closer spacing (300 mm) or larger members are
  required as floor count or height increases. [[3]](#7-sources)
- **24″ o.c. small-window note (IRC):** where studs are spaced at 610 mm
  (24″ o.c.) and a window opening is narrower than the stud spacing, no header
  is required for the opening (the opening fits between existing studs).
  [[4]](#7-sources)

---

## 2. Plate configuration

| Element | Count | Notes | Source |
|---|---|---|---|
| Bottom plate (sole plate) | **1** (single) | Single 2× member | IRC R602.3.1 / NBC 9.23.10 [[1]](#7-sources) |
| Top plate | **2** (double top plate) | Default. Single top plate permitted only under stacked-framing conditions; default to double | IRC R602.3.2 [[1]](#7-sources) |
| Plate thickness (flat) | **38 mm** (1.5″) | A 2× member laid flat | §5 / [[5]](#7-sources) |

**Stud length formula** (platform framing):

```
stud_length = wall_height − bottom_plate_thickness − (2 × top_plate_thickness)
            = wall_height − 38 − 76
            = wall_height − 114 mm
```

- For an 8 ft (2438 mm) wall: `2438 − 114 = 2324 mm`.
- **Relationship to the precut stud (92‑5/8″ = 2353 mm):** a standard
  US precut stud (2353 mm) + single bottom plate (38 mm) + **double** top plate
  (76 mm) = 2467 mm ≈ 97‑1/8″, which yields a finished wall just over 8 ft to
  accommodate 8 ft (2438 mm) wallboard with clearance. Precut stud length is
  therefore a function of the assumed plate count; framing-synth derives stud
  length from the formula above for the actual configured plate count rather
  than hard-coding a precut length. [[6]](#7-sources)

---

## 3. Header sizing

**Simplified, code-grounded tier table.** This is a *simplification* of IRC
Table R602.7(1), pinned to the baseline load case (**single storey, roof +
ceiling only, ≤ 6 m / 20 ft building width, ground snow load ≤ 30 psf ≈
1.4 kPa, header top laterally braced**). Spans are **rounded down** to round
metric tiers, so each tier is **conservative** relative to the published
maxima. [[7]](#7-sources)

| Opening span | Bearing-wall header | Jack studs (NJ) each end |
|---|---|---|
| ≤ 1219 mm (4 ft) | 2‑2×6 | 1 |
| ≤ 1829 mm (6 ft) | 2‑2×8 | 1 |
| ≤ 2438 mm (8 ft) | 2‑2×10 | 2 |
| ≤ **2970 mm** (~9′9″) | 2‑2×12 | 2 |
| Nonbearing, ≤ 2438 mm (8 ft) | single flat 2×4 | 1 |

> **Hard stop (ADR-001, Option A):** the top tier ends at **2970 mm**, the
> *actual* IRC Table R602.7(1) baseline maximum for a single 2‑2×12 (≈9′9″).
> Openings wider than 2970 mm fall **outside** the prescriptive envelope and the
> synthesiser raises `ValueError("engineered design required")` rather than
> inventing an unbacked tier. This replaces the earlier 3658 mm (12 ft)
> placeholder, which had no code basis for a single 2‑2×12.

**Verification against IRC Table R602.7(1)** (exterior bearing wall, 20 ft
building width, 30 psf snow, roof + ceiling, 1 storey) — published maxima are
*larger* than our tiers, confirming the tiers are conservative: [[7]](#7-sources)

| Header | Published max span (roof+ceiling) | NJ | Our tier threshold |
|---|---|---|---|
| 2‑2×6 | ~4′7″–5′5″ (1397–1651 mm) | 1 | 1219 mm ✓ |
| 2‑2×8 | ~5′9″–6′10″ (1753–2083 mm) | 1 | 1829 mm ✓ |
| 2‑2×10 | ~6′10″–8′5″ (2083–2565 mm) | 2 | 2438 mm ✓ |
| 2‑2×12 | ~8′1″–9′9″ (2464–2972 mm) | 2 | 2970 mm ✓ |

> The top tier is pinned to the single-2‑2×12 baseline maximum (~9′9″ ≈
> 2970 mm). Openings beyond 2970 mm require a deeper/built-up header or
> engineered beam and are **rejected** by the synthesiser (out of prescriptive
> envelope) — see the hard-stop note above and ADR-001.

**Jack studs (NJ):** *NJ* is read directly from Table R602.7(1) and given
alongside each span. Where NJ = 1, the header may alternatively be supported by
an approved framing anchor fastened to the full-height king stud instead of a
jack stud. [[7]](#7-sources)

**Lateral bracing footnote (f):** tabulated spans assume the header top is
laterally braced by perpendicular framing. Where the top is **not** braced,
tabulated spans for **2×8 / 2×10 / 2×12** headers are multiplied by **0.70**
(or the header must be engineered). framing-synth assumes braced tops per the
baseline assumptions (§Scope). [[7]](#7-sources)

**Nonbearing walls (R602.7.4):** load-bearing headers are **not required** in
interior or exterior nonbearing walls. A single **flat 2×4** member is permitted
as a header for openings **up to 8 ft (2438 mm)** wide, provided the vertical
distance to the parallel nailing surface above is not more than 24″ (610 mm);
cripples/blocking above are not required in that case. [[8]](#7-sources)

---

## 4. Opening framing anatomy

Standard light-frame anatomy around a wall opening (door or window). All members
below map to `IfcMember` (see §6).

| Member | Description | Count / rule | Source |
|---|---|---|---|
| **King stud** | Full-height stud each side of the opening, plate-to-plate, nailed to the header ends | 1 per side (min.) | [[8]](#7-sources) |
| **Jack stud** (trimmer) | Runs bottom plate → underside of header; carries the header | **NJ per side** (from §3 table) | [[7]](#7-sources)[[8]](#7-sources) |
| **Header** | Spans the opening, bears on the jack studs | per §3 | [[7]](#7-sources) |
| **Sill** (window only) | Horizontal member at the bottom of a window opening; defines the rough-opening bottom | 1 (single; double for wide openings) | [[1]](#7-sources) |
| **Cripple stud** | Short studs **above** the header and **below** the sill, transferring load and continuing the wall sheathing nailing pattern | maintain o.c. spacing | [[1]](#7-sources) |

**ASCII elevation (window opening):**

```
 ___________________________________________   ← double top plate
|   |   |   |   |   |   |   |   |   |   |   |
|   | cripple studs (above header)  |   |   |    ← cripples keep o.c. spacing
|   |___|___________________________|___|   |
|   | K | J |     HEADER        | J | K |   |  K = king stud
|   |   |   |__________________ |   |   |   |  J = jack stud (NJ deep)
|   |   |   |                   |   |   |   |
|   |   |   |   ROUGH OPENING   |   |   |   |
|   |   |   |   (window)        |   |   |   |
|   |   |   |___________________|   |   |   |
|   |   |   |     SILL          |   |   |   |
|   |   |   |___|___________|___|   |   |   |   
|   |   | cripple studs (below sill)|   |   |    ← cripples keep o.c. spacing
|___|___|___|___|___|___|___|___|___|___|___|   ← single bottom plate
```

*(A door opening is identical but omits the sill and the below-sill cripples;
the rough opening runs to the bottom plate.)*

**How cripples maintain o.c. spacing:** the regular stud grid is laid out at the
configured o.c. spacing (§1) across the whole panel **first**. Where a full-
height stud would intersect the opening it is replaced by king/jack studs at the
opening edges, and the would-be studs above the header and below the sill become
**cripple studs** on the *same grid lines*. This preserves a continuous nailing
surface for sheathing/drywall at the panel's o.c. module. [[1]](#7-sources)

---

## 5. Member cross-sections

Nominal "2×n" framing → actual planed dry dimensions (metric per CSA O141 /
Canadian dimension-lumber convention; thickness 38 mm for all 2× members).
[[5]](#7-sources)[[9]](#7-sources)

| Nominal | Actual (imperial) | Actual (metric) | Typical framing use |
|---|---|---|---|
| 2×4 | 1½″ × 3½″ | **38 × 89 mm** | Interior walls, nonbearing partitions, flat nonbearing headers |
| 2×6 | 1½″ × 5½″ | **38 × 140 mm** | Exterior walls (deeper cavity for insulation / energy code) |
| 2×8 | 1½″ × 7¼″ | **38 × 184 mm** | Headers (≤ 6 ft tier) |
| 2×10 | 1½″ × 9¼″ | **38 × 235 mm** | Headers (≤ 8 ft tier) |
| 2×12 | 1½″ × 11¼″ | **38 × 286 mm** | Headers (≤ 12 ft tier) |

- **2×4 (38×89) vs 2×6 (38×140) selection:** interior/nonbearing walls default
  to 2×4; **exterior walls default to 2×6** because the deeper cavity is needed
  to meet thermal-resistance (effective-R) requirements of the energy code and
  NBC Part 9 / Ontario SB-12. [[3]](#7-sources)
- A header is built up from two 2× members of the depth given in §3 (e.g.
  "2‑2×8" = two 38×184 mm members), typically with a flat spacer to match wall
  thickness. [[7]](#7-sources)

---

## 6. IFC4 mapping (intended — implemented later in `aec-ifc-export`)

This section documents the **intended** IFC4.3 mapping so synthesized framing
members carry the correct type tags downstream. It is **not** implemented here.

### Members → `IfcMember`

All linear framing members map to **`IfcMember`** (subtype of `IfcBuiltElement`,
a linear structural element; load-bearing function is not required by the
entity). `PredefinedType` is drawn from **`IfcMemberTypeEnum`**. [[10]](#7-sources)[[11]](#7-sources)

| Framing member | `IfcMember.PredefinedType` | Notes |
|---|---|---|
| Stud / king stud / jack stud / cripple | **`STUD`** | `STUD` = "Vertical element in wall framing" (added IFC2x2) [[11]](#7-sources) |
| Top plate / bottom plate / sill | **`PLATE`** | `PLATE` = "A linear continuous horizontal element in wall framing, such as a head piece or a sole plate" (IFC2x2) [[11]](#7-sources) |
| Header | **`MEMBER`** (or `USERDEFINED`, `ObjectType="HEADER"`) | No dedicated header enum; `MEMBER` is the generic linear element. If finer typing is needed, use `USERDEFINED` + `ObjectType` [[11]](#7-sources) |

- **Why `IfcMember` over `IfcPlate` for plates:** the IFC `STUD`/`PLATE` *enum
  values* are explicitly defined on **`IfcMemberTypeEnum`** as wall-framing
  members; `IfcPlate` is intended for planar (sheet) elements, not linear flat
  2× lumber. For consistency, **all** linear 2× framing members use
  `IfcMember`, with `PredefinedType=PLATE` carrying the plate semantics.
  [[10]](#7-sources)[[11]](#7-sources)
- **`USERDEFINED` constraint:** `PredefinedType` may only be `USERDEFINED` when
  an `ObjectType` attribute is supplied; type assignment via `IsTypedBy` must
  reference an `IfcMemberType`. [[10]](#7-sources)

### Panel assembly → `IfcElementAssembly`

The complete wall panel maps to **`IfcElementAssembly`** (subtype of
`IfcElement`). buildingSMART states: *"Premanufactured or precast elements are
examples of the general IfcElementAssembly entity"* — a panelized wall is
exactly such a premanufactured assembly. [[12]](#7-sources)

- Individual `IfcMember` components aggregate into the assembly via
  **`IfcRelAggregates`** (exposed on the assembly's inverse `IsDecomposedBy`).
  Aggregated components are **not** additionally placed in the project spatial
  hierarchy. [[12]](#7-sources)
- `PredefinedType` from `IfcElementAssemblyTypeEnum` — closest fit is
  **`USERDEFINED`** (e.g. `ObjectType="WALL_PANEL"`); none of the enum values
  (RIGID_FRAME, SUPPORTINGASSEMBLY, …) specifically names a stud-wall panel.
  [[12]](#7-sources)

This mapping (`IfcMember` + `IfcElementAssembly` + `IfcRelAggregates`) is
implemented in **`aec-ifc-export`**; `framing-synth` only attaches the intended
type tags to its member data.

---

## 7. Sources

1. **IRC 2021 §R602.3 — Design and Construction (wood wall framing), Tables
   R602.3(5) / R602.3.2 (stud spacing, top/bottom plates).** International Code
   Council. https://codes.iccsafe.org/s/IRC2021P2/chapter-6-wall-construction/IRC2021P2-Pt03-Ch06-SecR602.3
2. **National Building Code of Canada 2020 — Part 9.23 Wood-Frame
   Construction (on-centre stud spacing 400/600 mm).** National Research
   Council Canada. https://nrc.canada.ca/en/certifications-evaluations-standards/codes-canada
   (see Proposed Change / Table 9.23.10.1 review:
   https://nrc.canada.ca/en/certifications-evaluations-standards/codes-canada/codes-development-process/public-review/2022/pcfs/nbc20_divb_09.23.10.01._table_001677.html)
3. **Ontario Building Code — Table 9.23.10.1, Stud Size and Spacing**
   (38×89 / 38×140 mm; 300/400/600 mm o.c.; max heights vs floors supported).
   https://www.buildingcode.online/1848.html
4. **IRC 2021 §R602.7 — Headers (24″ o.c. small-opening note).**
   https://codes.iccsafe.org/s/IRC2021P2/chapter-6-wall-construction/IRC2021P2-Pt03-Ch06-SecR602.7
5. **2×4 Actual & Nominal Measurements (38 × 89 mm).**
   https://2x4actualsize.com/2x4-size-actual-nominal-measurements/
6. **Dimension lumber / precut studs — Canadian convention.** Natural
   Resources Canada. https://natural-resources.canada.ca/forests-forestry/forest-industry-trade/dimension-lumber
7. **IRC 2021 §R602.7 & Table R602.7(1) — Girder/Header Spans for Exterior
   Bearing Walls (spans, NJ jack studs, lateral-bracing footnote f, ×0.70
   reduction).** https://codes.iccsafe.org/s/IRC2021P2/chapter-6-wall-construction/IRC2021P2-Pt03-Ch06-SecR602.7
   ; representative span values cross-checked at UpCodes
   https://up.codes/viewer/connecticut/irc-2021/chapter/6/wall-construction
   and Republic, MO span tables
   https://www.republicmo.com/DocumentCenter/View/139/Girder-and-Header-Spans---Exterior-Walls
8. **IRC 2021 §R602.7.4 — Nonbearing wall headers (single flat 2×4, ≤ 8 ft).**
   https://codes.iccsafe.org/s/IRC2021P2/chapter-6-wall-construction/IRC2021P2-Pt03-Ch06-SecR602.7
9. **The Canadian Wood Council — Lumber (dimension-lumber sizes).**
   https://cwc.ca/articles/lumber/
10. **buildingSMART IFC4.3 — `IfcMember` entity.**
    https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcMember.htm
11. **buildingSMART IFC4.3 — `IfcMemberTypeEnum` (STUD, PLATE, MEMBER, …).**
    https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcMemberTypeEnum.htm
12. **buildingSMART IFC4.3 — `IfcElementAssembly` (premanufactured/precast
    assemblies; `IfcRelAggregates`).**
    https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/IfcElementAssembly.htm
