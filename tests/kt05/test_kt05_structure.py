from __future__ import annotations

import re
from pathlib import Path

from prototype.kt03.hydrology_step import HydrologyStep, SCHEMA_ID, UNIT_CONTRACT_ID

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "prototype" / "kt05" / "mod_animo_hydrology_adapter.f90"
text = SOURCE.read_text(encoding="utf-8")
lower = text.lower()


def type_fields(type_name: str) -> set[str]:
    match = re.search(
        rf"type\s*,\s*public\s*::\s*{re.escape(type_name)}\b(.*?)"
        rf"end\s+type\s+{re.escape(type_name)}",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    assert match, f"missing Fortran type {type_name}"
    fields: set[str] = set()
    for raw_line in match.group(1).splitlines():
        line = raw_line.split("!", 1)[0].strip()
        if "::" not in line:
            continue
        rhs = line.split("::", 1)[1]
        rhs = re.sub(r"\([^)]*\)", "", rhs)
        for part in rhs.split(","):
            name = part.split("=", 1)[0].strip().lower()
            if name:
                fields.add(name)
    return fields


assert SCHEMA_ID.lower() in lower
assert UNIT_CONTRACT_ID.lower() in lower

for forbidden in (
    "hlpimp",
    "powerstation",
    "source_record_sha256",
    "legacy_layout",
):
    assert forbidden not in lower, f"legacy/file-specific concept leaked into KT05: {forbidden}"

expected_step = set(HydrologyStep.__dataclass_fields__)
observed_step = type_fields("hydrology_step_t")
assert observed_step == expected_step, (
    f"Fortran HydrologyStep schema drift: "
    f"missing={sorted(expected_step-observed_step)}, "
    f"extra={sorted(observed_step-expected_step)}"
)

expected_projection = {
    "layer_count",
    "drainage_count",
    "evicirr",
    "evicpr",
    "evpn",
    "evsn",
    "evso",
    "evsoma",
    "evtrma",
    "flab",
    "fldr",
    "flev",
    "mofrt",
    "pnt",
    "prirr",
    "prr",
    "prsn",
    "ru",
    "runon",
    "sict",
    "snt",
    "st",
}
observed_projection = type_fields("hydro_detailed_external_t")
assert observed_projection == expected_projection, (
    f"Hydro_detailed external projection drift: "
    f"missing={sorted(expected_projection-observed_projection)}, "
    f"extra={sorted(observed_projection-expected_projection)}"
)

assert "mofrt(1:nl) = projection%mofrt" in lower
assert "flev(1:nl) = projection%flev" in lower
assert "flab(1:nl + 1) = projection%flab" in lower
assert "fldr(1:nudr, 1:nl) = projection%fldr" in lower

print("KT05 structural contract tests: PASS")
