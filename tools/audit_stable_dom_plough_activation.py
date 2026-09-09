#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

FROZEN_TESTBANK_SHA256 = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
MANAGEMENT_SUFFIX = "cranmais/input/management.inp"
INITIAL_SUFFIX = "cranmais/input/initial.inp"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def analyze_management(text: str) -> dict:
    lines = text.splitlines()
    pattern = re.compile(r"^\s*1\s+0\.00\s+0\s+2\s+0\.00\s*$")
    hits = [i for i, line in enumerate(lines, start=1) if pattern.match(line)]
    return {
        "plough_request_count": len(hits),
        "plough_request_lines": hits,
        "repeated_plough_requests_present": len(hits) >= 2,
    }


def analyze_initial(text: str) -> dict:
    lines = text.splitlines()
    marker = next((i for i, line in enumerate(lines) if line.strip().lower().startswith(">sdomin:")), None)
    if marker is None:
        return {"sdomin_marker_line": None, "value_count": 0, "all_values_zero": False}

    values = []
    value_lines = []
    for idx in range(marker + 1, min(marker + 4, len(lines))):
        toks = re.findall(r"[-+]?\d+(?:\.\d*)?(?:[EeDd][-+]?\d+)?", lines[idx])
        if toks:
            value_lines.append(idx + 1)
            values.extend(float(tok.replace("D", "E").replace("d", "e")) for tok in toks)
    return {
        "sdomin_marker_line": marker + 1,
        "value_lines": value_lines,
        "value_count": len(values),
        "all_values_zero": bool(values) and all(v == 0.0 for v in values),
    }


def audit_testbank(archive: Path) -> dict:
    raw = archive.read_bytes()
    archive_sha = sha256_bytes(raw)
    if archive_sha != FROZEN_TESTBANK_SHA256:
        raise ValueError(
            f"testbank SHA-256 mismatch: expected {FROZEN_TESTBANK_SHA256}, got {archive_sha}"
        )

    with zipfile.ZipFile(archive) as zf:
        files = [n for n in zf.namelist() if not n.endswith("/")]
        management = [n for n in files if n.replace("\\", "/").lower().endswith(MANAGEMENT_SUFFIX)]
        initial = [n for n in files if n.replace("\\", "/").lower().endswith(INITIAL_SUFFIX)]
        if len(management) != 1 or len(initial) != 1:
            raise ValueError(f"expected one CranMais management and initial file, got {management=} {initial=}")
        m_name, i_name = management[0], initial[0]
        m_data, i_data = zf.read(m_name), zf.read(i_name)

    m = analyze_management(m_data.decode("cp1252"))
    init = analyze_initial(i_data.decode("cp1252"))
    repeated = m["repeated_plough_requests_present"]
    initial_zero = init["all_values_zero"]
    return {
        "classification": (
            "FROZEN_CRANMAIS_REPEATED_PLOUGH_INPUT_PRESENT_INITIAL_STABLE_DOM_ZERO"
            if repeated and initial_zero
            else "FROZEN_CRANMAIS_ACTIVATION_SIGNATURE_NOT_CONFIRMED"
        ),
        "testbank_sha256": archive_sha,
        "management_member": m_name,
        "management_member_sha256": sha256_bytes(m_data),
        "initial_member": i_name,
        "initial_member_sha256": sha256_bytes(i_data),
        "management": m,
        "initial_stable_dom": init,
        "scope_note": (
            "This audit confirms frozen input requests and initial values only. It does not claim that a historical "
            "reference executable ran the case or quantify the numerical effect of the Addit.for undefined reads."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit frozen CranMais input activation for the PREP10 stable-DOM plough finding.")
    ap.add_argument("testbank", type=Path)
    ap.add_argument("--json", type=Path, dest="json_path")
    ns = ap.parse_args()
    result = audit_testbank(ns.testbank)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if ns.json_path:
        ns.json_path.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["classification"].startswith("FROZEN_CRANMAIS_REPEATED_PLOUGH_INPUT_PRESENT") else 2


if __name__ == "__main__":
    raise SystemExit(main())
