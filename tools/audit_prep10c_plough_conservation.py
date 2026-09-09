#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_ADDIT_SHA256 = "e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d"
EXPECTED_INICALC_SHA256 = "306dd3be262a9eaa293520c754190931bc54e76e7d84b3145efe5663a3e523e1"
ADDIT_MEMBER = "ANIMO_4.1.5.53/Addit.for"
INICALC_MEMBER = "ANIMO_4.1.5.53/Inicalc.for"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_lines(data: bytes) -> list[str]:
    return [re.sub(r"\s+", " ", line.strip()).lower() for line in data.decode("latin1").splitlines()]


def require_once(lines: list[str], needle: str) -> int:
    needle = re.sub(r"\s+", " ", needle.strip()).lower()
    hits = [i + 1 for i, line in enumerate(lines) if line == needle]
    if len(hits) != 1:
        raise ValueError(f"expected exactly one line {needle!r}, found {hits}")
    return hits[0]


def audit(source_zip: Path) -> dict:
    archive_bytes = source_zip.read_bytes()
    actual_archive = sha256_bytes(archive_bytes)
    if actual_archive != EXPECTED_SOURCE_SHA256:
        raise ValueError(
            f"source archive SHA-256 mismatch: expected {EXPECTED_SOURCE_SHA256}, got {actual_archive}"
        )

    with zipfile.ZipFile(source_zip) as zf:
        addit = zf.read(ADDIT_MEMBER)
        inicalc = zf.read(INICALC_MEMBER)

    if sha256_bytes(addit) != EXPECTED_ADDIT_SHA256:
        raise ValueError("Addit.for member SHA-256 mismatch")
    if sha256_bytes(inicalc) != EXPECTED_INICALC_SHA256:
        raise ValueError("Inicalc.for member SHA-256 mismatch")

    a = normalized_lines(addit)
    i = normalized_lines(inicalc)

    facts = {
        "bo_zero_line": require_once(i, "Bo(0) = 0.0"),
        "bo_cumulative_line": require_once(i, "Bo(Ln) = Bo(Ln-1) + He(Ln)"),
        "plough_branch_line": require_once(a, "If (Pl(I) .Gt. 0) Then"),
        "current_mass_loop_line": require_once(a, "Do Ln = 0,Pl(I)"),
        "stable_dom_accumulation_line": require_once(
            a, "SuStdiorma = SuStdiorma + CoStdiorma(Ln)*He(Ln)* &"
        ),
        "stable_don_accumulation_line": require_once(
            a, "SuStdiorni = SuStdiorni + CoStdiorni(Ln)*He(Ln)* &"
        ),
        "stable_dop_accumulation_line": require_once(
            a, "If(Ipo.Eq.1) SuStdiorpo = SuStdiorpo + CoStdiorpo(Ln) &"
        ),
        "redistribution_loop_line": require_once(a, "Do Ln = 1,Pl(I)"),
        "stable_help_line": require_once(a, "Help = He(Ln)/bo(Pl(I)) / &"),
        "stable_dom_redistribution_line": require_once(a, "CoStdiorma(Ln) = Help * SuStdiorma"),
        "stable_don_redistribution_line": require_once(a, "CoStdiorni(Ln) = Help * SuStdiorni"),
        "stable_dop_redistribution_line": require_once(
            a, "If (Ipo.Eq.1) CoStdiorpo(Ln) = Help * SuStdiorpo"
        )
    }

    for variable in ("sustdiorma", "sustdiorni", "sustdiorpo"):
        zero_hits = [n + 1 for n, line in enumerate(a) if re.search(rf"\b{variable}\s*=\s*0(?:\.0*)?\b", line)]
        if zero_hits:
            raise ValueError(f"frozen Addit.for unexpectedly contains explicit zero reset for {variable}: {zero_hits}")

    return {
        "work_unit": "ANIMO-PREP10C",
        "evidence_class": "SOURCE_BOUND_CONSERVATION_RECONCILIATION",
        "source_archive_sha256": actual_archive,
        "members": {
            ADDIT_MEMBER: {"sha256": sha256_bytes(addit), "size_bytes": len(addit)},
            INICALC_MEMBER: {"sha256": sha256_bytes(inicalc), "size_bytes": len(inicalc)}
        },
        "source_facts": facts,
        "derived_identity": {
            "bo_definition": "Bo(Pl)=sum(He(Ln), Ln=1..Pl)",
            "current_event_accumulator": "S_current=sum(current stable-pool mass, Ln=0..Pl)",
            "redistributed_layer_mass": "M_new(Ln)=He(Ln)/Bo(Pl)*S_event",
            "redistributed_total": "sum(M_new(Ln), Ln=1..Pl)=S_event",
            "defective_persistent_case": "S_event=S_prior+S_current, so prior-event mass is redistributed again",
            "candidate_reset_case": "S_prior=0 before summation, so redistributed total equals current-event mass only"
        },
        "classification": "EVENT_RESET_RESTORES_CLOSED_CURRENT_EVENT_REDISTRIBUTION_IDENTITY",
        "physics_model_changed_by_identity": false,
        "numerical_policy_changed_by_identity": false
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source_zip", type=Path)
    ap.add_argument("--json", type=Path)
    ns = ap.parse_args()
    report = audit(ns.source_zip)
    encoded = json.dumps(report, indent=2) + "\n"
    if ns.json:
        ns.json.parent.mkdir(parents=True, exist_ok=True)
        ns.json.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
