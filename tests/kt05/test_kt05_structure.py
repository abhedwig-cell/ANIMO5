from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "prototype" / "kt05" / "mod_animo_hydrology_adapter.f90"

text = SOURCE.read_text(encoding="utf-8").lower()

for forbidden in (
    "hlpimp",
    "powerstation",
    "source_record_sha256",
    "legacy_layout",
    "swap solver",
):
    assert forbidden not in text, f"legacy/file-specific concept leaked into KT05: {forbidden}"

for identity in (
    "animo_hydrology_step_v1",
    "animo_hydrology_units_v1",
):
    assert identity in text, f"missing frozen KT03 identity: {identity}"

for field in (
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
):
    assert field in text, f"missing explicit Hydro_detailed projection field: {field}"

print("KT05 structural contract tests: PASS")
