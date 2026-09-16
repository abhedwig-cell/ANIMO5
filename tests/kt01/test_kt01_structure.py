#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE = ROOT / "prototype" / "kt01"
failures = []

def require(cond, label):
    if cond:
        print(f"PASS {label}")
    else:
        print(f"FAIL {label}")
        failures.append(label)

sources = list(PROTOTYPE.glob("*.f90"))
all_text = "\n".join(p.read_text(encoding="utf-8") for p in sources)
use_lines = "\n".join(line for line in all_text.splitlines() if re.match(r"\s*use\s+", line, re.I))
require(not re.search(r"\bswap\b|\bmod_.*swap", use_lines, re.I),
        "24 build/runtime source contains no dependency on SWAP5 modules")

base = "7a7d3a1f5a5c07bf36b7e6e2915338dabde20660"
try:
    changed = subprocess.check_output(["git", "diff", "--name-only", base, "HEAD"], cwd=ROOT, text=True).splitlines()
    production_changes = [p for p in changed if p.startswith("src/")]
    require(not production_changes, "25 no ANIMO scientific production source is modified")
except Exception as exc:
    print(f"FAIL 25 no ANIMO scientific production source is modified: {exc}")
    failures.append("25")

time_text = (PROTOTYPE / "mod_animo_time_coordinate.f90").read_text(encoding="utf-8")
require(not re.search(r"\breal\s*\(", time_text, re.I) and not re.search(r"\breal\b", time_text, re.I),
        "S01 canonical-time prototype module contains no REAL declaration or conversion")
require("epsilon" not in time_text.lower() and "ulp" not in time_text.lower(),
        "S02 time identity contains no epsilon or ULP policy")
require("a * d" not in time_text.lower() and "c * b" not in time_text.lower(),
        "S03 rational comparison does not use unchecked cross multiplication")

kernel_paths = [
    PROTOTYPE / "mod_animo_kernel_transactions.f90",
    PROTOTYPE / "mod_animo_committed_persistence.f90",
    PROTOTYPE / "mod_animo_interval_runtime.f90",
]
kernel_text = "\n".join(p.read_text(encoding="utf-8") for p in kernel_paths)
require(not re.search(r"\bopen\s*\(|\bclose\s*\(|\bread\s*\(|\bwrite\s*\(", kernel_text, re.I),
        "S04 kernel transaction, persistence and interval modules contain no file I/O")
require(not re.search(r"\bsave\b", all_text, re.I),
        "S05 prototype contains no hidden mutable SAVE state")

forbidden = ["headcalc", "richards", "modflow", "wofost", "rossfast"]
require(not any(term in all_text.lower() for term in forbidden),
        "S06 prototype source contains no excluded SWAP physics payload")

matrix = (ROOT / "docs" / "kt01" / "SWAP5_RUNTIME_REUSE_MATRIX.csv").read_text(encoding="utf-8")
required_blobs = [
    "d5a71a526efaebd82054580c3186f8e3545db331",
    "e4db4ede8162c8be877c8cad9f1babd57ba451b6",
    "ffd886c3401fc12739a456fe60a8741c12b9848b",
    "3962c270a7579b7403764674302445fe15ef5f72",
    "0b50dda5caf3b73a82561d7b0ba1e92386a08fee",
    "f96a66c0185d96ba48258f8560db275fa7fed58c",
]
require(all(blob in matrix for blob in required_blobs),
        "S07 provenance matrix pins all six exact SWAP5 source blobs")

contracts_text = (PROTOTYPE / "mod_animo_runtime_contracts.f90").read_text(encoding="utf-8")
persistence_text = (PROTOTYPE / "mod_animo_committed_persistence.f90").read_text(encoding="utf-8")
require("committed_journal" not in contracts_text.lower(),
        "S08 physical AcceptedState does not own committed event history")
require("transferjournal" not in persistence_text.lower() and "committedeventledger" not in persistence_text.lower(),
        "S09 physical checkpoint contains no event journal or committed event ledger")
require(re.search(r"type,\s*public\s*::\s*AcceptedCheckpoint\s*\n\s*private", persistence_text, re.I) is not None,
        "S10 checkpoint components are private outside persistence module")

if failures:
    print(f"KT01 STRUCTURAL TEST FAILURES: {len(failures)}")
    sys.exit(1)
print("KT01 STRUCTURAL TESTS 24-25 AND S01-S10: PASS")
