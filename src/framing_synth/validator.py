"""
Geometric validation for synthesised framing.

Beyond JSON Schema (handled by aec_schema.validate_framing), this checks Level-2
invariants that schema cannot express:

  - every member has positive length
  - all members lie within the panel bounding box (length × height), with a
    small float tolerance
  - standard studs do not intrude into an opening — derived from the x-extent of
    the header members, which span each opening's rough edges + bearing
  - member_count == len(members)

Industry precedent: BIM pipelines (e.g. IfcOpenShell) validate geometry
quantities at component boundaries before passing elements downstream; this
mirrors the ValidationResult pattern used in wall-extract / panel-decompose.
"""
from __future__ import annotations

from dataclasses import dataclass, field

_TOL_MM = 1.0


@dataclass
class ValidationResult:
    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.valid = False

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def __str__(self) -> str:
        lines = [f"  ERROR:   {e}" for e in self.errors]
        lines += [f"  WARNING: {w}" for w in self.warnings]
        return "\n".join(lines) if lines else "  OK"


def _z_range(member: dict) -> tuple[float, float]:
    z0, z1 = member["start"]["z"], member["end"]["z"]
    return (min(z0, z1), max(z0, z1))


def validate_framing_geometry(
    framing: dict,
    panel: dict,
    *,
    raise_on_error: bool = False,
) -> ValidationResult:
    """Geometric / containment checks for a synthesised framing assembly."""
    result = ValidationResult()
    members = framing.get("members", [])

    length = float(panel["length"])
    height = float(panel["height"])

    # member_count consistency (also enforced by aec_schema.validate_framing).
    declared = framing.get("member_count", -1)
    if declared != len(members):
        result.add_error(
            f"member_count ({declared}) != actual member count ({len(members)})"
        )

    # Header x-extents define the cleared opening zones (header spans rough
    # edges + bearing). A standard stud landing in that x-range overlaps the
    # opening (studs are full height, so z always overlaps the header).
    header_spans = [
        (min(m["start"]["x"], m["end"]["x"]), max(m["start"]["x"], m["end"]["x"]))
        for m in members
        if m["type"] == "header"
    ]

    for m in members:
        mid = m.get("id", "?")

        if m["length"] <= 0:
            result.add_error(f"{mid}: non-positive length {m['length']}")

        for pt_name in ("start", "end"):
            pt = m[pt_name]
            if not (-_TOL_MM <= pt["x"] <= length + _TOL_MM):
                result.add_error(
                    f"{mid}: {pt_name}.x {pt['x']:.1f} outside panel length [0, {length:.0f}]"
                )
            if not (-_TOL_MM <= pt["z"] <= height + _TOL_MM):
                result.add_error(
                    f"{mid}: {pt_name}.z {pt['z']:.1f} outside panel height [0, {height:.0f}]"
                )

        if m["type"] == "stud":
            sx = m["start"]["x"]
            for lo, hi in header_spans:
                if lo + _TOL_MM < sx < hi - _TOL_MM:
                    result.add_error(
                        f"{mid}: standard stud at x={sx:.0f} falls inside opening "
                        f"span ({lo:.0f}, {hi:.0f})"
                    )

    if not result.valid and raise_on_error:
        raise ValueError(
            f"Framing geometry validation failed ({len(result.errors)} errors):\n"
            + "\n".join(f"  {e}" for e in result.errors)
        )

    return result
