from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "prototype" / "kt02" / "runtime"

runtime_files = sorted(RUNTIME.glob("*.f90"))
assert runtime_files, "no runtime files found"

for path in runtime_files:
    text = path.read_text(encoding="utf-8").lower()
    assert "use mod_animo" not in text, f"ANIMO dependency leaked into {path.name}"
    assert "use mod_swap" not in text, f"SWAP dependency leaked into {path.name}"
    assert "headcalc" not in text, f"hydraulic solver detail leaked into {path.name}"
    assert "richards" not in text, f"Richards physics leaked into {path.name}"
    assert "nh4" not in text and "no3" not in text and "po4" not in text, f"ANIMO science leaked into {path.name}"

contracts = (RUNTIME / "mod_transient_contracts.f90").read_text(encoding="utf-8").lower()
assert "abstract" in contracts and "transient_payload_t" in contracts

interval = (RUNTIME / "mod_transient_interval_runtime.f90").read_text(encoding="utf-8").lower()
assert "transient_client_t" in interval
assert "retry_permitted_after_reject" in interval
assert "external_accepted = working" in interval

print("KT02 structure checks: PASS")
