#!/usr/bin/env python3
"""Independent exact-rational validator for ANIMO-SYNQ05 / TCD-037-A4."""
from __future__ import annotations
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "4da2dd067069944a5e3eeb5f532566a23402bd68"
RG05I = "94afe7d649a8c60758a41996f0059de0acddd2fc"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"

ORACLE = ROOT / "integration/animo-synthetic/SYNQ05_TCD037_A4_ORACLE.json"
STATUS = ROOT / "integration/animo-synthetic/ANIMO-SYNQ05_STATUS.json"

Z = Fraction(10000)
BASELINE = Fraction(100)
QD = Fraction(1, 16384)
QF = Fraction(1, 32768)
PD = Fraction(1, 4096)
PN = Fraction(1, 8192)
STATE = (Fraction(11), Fraction(22))
FLUX = Fraction(7)
N2OD = Fraction(51)
N2ON = Fraction(61)
QRD = Fraction(71)
A1, A2, A3, OTHER = map(Fraction, (31, 41, 46, 77))
CASES = {
    "EMISSION_NONZERO_PRODUCTION_ZERO": (True, QD, QF, Fraction(0), Fraction(0), Fraction(1, 4)),
    "PRODUCTION_NONZERO_EMISSION_ZERO": (True, Fraction(0), Fraction(0), PD, PN, Fraction(1, 4)),
    "COMPONENT_PERMUTED": (True, QF, QD, Fraction(0), Fraction(0), Fraction(1, 4)),
    "RATE_TIME_EQUIVALENT": (True, QD / 2, QF / 2, Fraction(0), Fraction(0), Fraction(1, 2)),
    "SIGNED_UPTAKE": (True, -QD, QF, Fraction(0), Fraction(0), Fraction(1, 4)),
    "INACTIVE": (False, QD, QF, PD, PN, Fraction(1, 4)),
}

ALLOWED = {
    ".github/workflows/animo-synq05-tcd037-a4.yml",
    "docs/synq05/WORK_UNIT_CONTRACT.md",
    "integration/animo-synthetic/ANIMO-SYNQ05_STATUS.json",
    "integration/animo-synthetic/SYNQ05_TCD037_A4_ORACLE.json",
    "tools/synq05/tcd037_a4_source_shaped_probe.f90",
    "tools/synq05/validate_tcd037_a4_synthetic.py",
}


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True).stdout


def show_json(commit, path):
    return json.loads(run("git", "show", f"{commit}:{path}"))


def exact(actual, expected, label):
    expected_float = float(expected)
    require(actual == expected_float, f"{label}: expected {expected_float.hex()}, got {actual.hex()}")


def expected_candidate(active, qdif, qflw, st):
    if not active:
        return BASELINE
    return BASELINE + Z * (qdif + qflw) * st


def expected_native_bad(active, pden, pnit, st):
    if not active:
        return BASELINE
    return BASELINE + Z * (pden + pnit) * st


def parse(path):
    rows = {}
    for raw in Path(path).read_text().splitlines():
        if not raw.strip():
            continue
        parts = raw.split()
        require(len(parts) == 18, f"bad row shape {len(parts)}: {raw}")
        case = parts[0]
        require(case in CASES and case not in rows, f"bad or duplicate case {case}")
        rows[case] = tuple(float(x.replace("D", "E")) for x in parts[1:])
    require(set(rows) == set(CASES), f"case set mismatch {rows.keys()}")
    return rows


def validate_probe(rows):
    for case, (active, qdif, qflw, pden, pnit, st) in CASES.items():
        values = rows[case]
        for idx, expected in enumerate((qdif, qflw, pden, pnit, st)):
            exact(values[idx], expected, f"{case}/input[{idx}]")
        exact(values[5], expected_candidate(active, qdif, qflw, st), f"{case}/candidate_N2Oe")
        exact(values[6], expected_native_bad(active, pden, pnit, st), f"{case}/native_bad_N2Oe")
        exact(values[7], N2OD, f"{case}/N2Od")
        exact(values[8], N2ON, f"{case}/N2On")
        exact(values[9], QRD, f"{case}/QRdN2O")
        exact(values[10], STATE[0], f"{case}/state1")
        exact(values[11], STATE[1], f"{case}/state2")
        exact(values[12], FLUX, f"{case}/process_flux")
        exact(values[13], A1, f"{case}/A1")
        exact(values[14], A2, f"{case}/A2")
        exact(values[15], A3, f"{case}/A3")
        exact(values[16], OTHER, f"{case}/other")

    emission = rows["EMISSION_NONZERO_PRODUCTION_ZERO"]
    production = rows["PRODUCTION_NONZERO_EMISSION_ZERO"]
    permuted = rows["COMPONENT_PERMUTED"]
    rate_time = rows["RATE_TIME_EQUIVALENT"]
    signed = rows["SIGNED_UPTAKE"]
    inactive = rows["INACTIVE"]

    require(emission[5] != 100.0 and emission[6] == 100.0,
            "emission-only case must activate candidate and reject production-total native-bad owner")
    require(production[5] == 100.0 and production[6] != 100.0,
            "production-only case must leave candidate unchanged and activate native-bad mismatch")
    require(permuted[5] == emission[5], "component permutation changed total-emission ownership")
    require(rate_time[5] == emission[5], "rate-time equivalent atmosphere-emission amount changed observer")
    require(signed[5] < 100.0, "signed negative atmosphere exchange must decrease N2Oe observer")
    require(inactive[5] == 100.0 and inactive[6] == 100.0, "inactive seam changed observer")


def validate_authorities_and_scope():
    base = show_json(BASE, "integration/animo-b3/ANIMO-B3D25_STATUS.json")
    require(base["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "B3D25 base not admitted")
    require(base["target_child_atom"] == "TCD-037-A3", "wrong B3D25 target")
    require(base["candidate_admission_effect"]["a4_admitted"] is False, "A4 already admitted at base")
    require(base["candidate_admission_effect"]["parent_tcd_admitted"] is False, "parent TCD-037 admitted at base")
    require(base["aggregate_policy"]["pending_atomic_admissions_after_rg05i_if_qualified"] == 1,
            "post-RG05I admission cadence drift")

    aggregate = show_json(RG05I, "integration/animo-reg/ANIMO-RG05I_STATUS.json")
    require(aggregate["state"] == "QUALIFIED_THIRD_BATCHED_ATOMIC_ADMISSION_INTEGRATION_THREE_POST_RG05H_ADMISSIONS_NO_PRODUCTION",
            "RG05I not qualified")
    require(aggregate["tcd037_state"]["parent_admitted"] is False, "RG05I parent admission drift")
    require(aggregate["tcd037_state"]["unadmitted_children"] == ["TCD-037-A3", "TCD-037-A4"],
            "RG05I historical child state drift")
    require(aggregate["b4_open"] is False and aggregate["production_open"] is False, "RG05I downstream gate opened")

    atomization = show_json(B3I07, "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms = {item["atom_id"]: item for item in atomization["atoms"]}
    a4 = atoms["TCD-037-A4"]
    require(a4["class"] == "A_ACCOUNTING_REPORTING_ONLY", "A4 class drift")
    require(a4["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St", "A4 source owner drift")
    require(a4["allowed_observer_fields"] == ["Bani(N2Oe)"], "A4 difference surface drift")
    require(a4["explicit_exclusions"] == [
        "Banh(N2On) per-layer production accounting",
        "existing nitrification reporting threshold",
        "QRdN2O reduction sink",
    ], "A4 exclusions drift")
    require(a4["natural_activation"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "A4 natural-case state drift")
    require(a4["historical_behavior"] == "UNKNOWN", "A4 historical behavior promoted")

    runtime = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    sem = runtime["semantic_qualification"]
    require(sem["n2o_atmosphere_emission_owner"] == "(QEmN2ODif+QEmN2OFlw)*St", "runtime A4 owner drift")
    require(sem["n2o_index0_consumer_mismatch"] is True, "runtime N2O index-0 mismatch no longer established")
    require(sem["n2o_reduction_role"] == "SEPARATE_N2O_REDUCTION_SINK_NOT_TCD037_OBSERVER_PRODUCER",
            "QRdN2O role drift")
    require(runtime["expected_difference"]["physical_state"] == "NONE" and
            runtime["expected_difference"]["process_flux"] == "NONE" and
            runtime["expected_difference"]["restart_state"] == "NONE" and
            runtime["expected_difference"]["solver_or_numerical_policy"] == "NONE",
            "runtime non-interference basis drift")
    require(runtime["historical_intel_behavior"] == "UNKNOWN", "runtime historical behavior promoted")

    synq = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM",
            "SYNQ01 policy authority drift")

    gov05 = show_json(GOV05, "integration/animo-governance/ANIMO-GOV05_STATUS.json")
    require(gov05["work_status"]["qualified"] is True and
            gov05["assurance_change"]["scientific_gate_reduction"] is False,
            "GOV05 not qualified or scientific gates weakened")

    gov03 = show_json(GOV03, "integration/animo-governance/ANIMO-GOV03_STATUS.json")
    require(gov03["qualified_closure_state"] == "B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT",
            "GOV03 B2 closure drift")

    oracle = json.loads(ORACLE.read_text())
    require(oracle["work_unit"] == "ANIMO-SYNQ05" and oracle["target"] == "TCD-037-A4", "wrong oracle identity")
    require(oracle["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "synthetic evidence promoted")
    require(oracle["accounting_contract"]["source_owner"] == "(QEmN2ODif+QEmN2OFlw)*St", "oracle owner drift")
    require(oracle["accounting_contract"]["observer_increment"] == "10000*(QEmN2ODif+QEmN2OFlw)*St", "oracle identity drift")
    require(oracle["allowed_difference_surface"] == ["Bani(N2Oe)"], "oracle scope widened")
    require(oracle["historical_behavior"] == "UNKNOWN" and oracle["historical_fidelity_claimed"] is False,
            "oracle historical behavior overclaimed")
    require(oracle["natural_case"]["translation_performed"] is False, "testcase translated")
    require(oracle["frozen_source_provenance"]["archive_sha256"] == SOURCE_SHA, "source identity drift")
    require(oracle["frozen_source_provenance"]["raw_source_redistributed"] is False,
            "licensed source redistributed")

    status = json.loads(STATUS.read_text())
    require(status["state"] in {
        "PERSISTED_VALIDATION_PENDING",
        "QUALIFIED_TCD037_A4_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2",
    }, "status lifecycle invalid")
    require(status["scientific_admission"] is False and status["tier_a_waiver_granted"] is False,
            "SYNQ05 overclaims admission or waiver")
    require(status["historical_behavior"] == "UNKNOWN" and status["historical_fidelity_claimed"] is False,
            "status historical behavior overclaimed")
    require(status["global_Ly_equals_Ln_theorem_claimed"] is False, "unsupported global index theorem claimed")
    require(status["production_source_modified"] is False and status["canonical_register_modified"] is False and
            status["testcase_translation_performed"] is False and status["b4_opened"] is False and
            status["aggregate_update_performed"] is False,
            "SYNQ05 scope boundary violated")

    manifest = (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text()
    require(SOURCE_SHA in manifest, "frozen source manifest drift")

    changed = {p.strip() for p in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if p.strip()}
    require(changed == ALLOWED, "scope differs from exact six-file SYNQ05 package: " + repr(sorted(changed)))
    for path in changed:
        require(not path.startswith(("src/", "reference/", "production/")), "protected production/B0 path modified: " + path)
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")


def main():
    require(len(sys.argv) == 2, "usage: validate_tcd037_a4_synthetic.py <probe-output>")
    rows = parse(sys.argv[1])
    validate_probe(rows)
    validate_authorities_and_scope()
    print("SYNQ05 PASS: exact A4 atmosphere-emission ownership, production-total discriminator, signed exchange and scope qualified at B1 synthetic strength; not B2")


if __name__ == "__main__":
    main()
