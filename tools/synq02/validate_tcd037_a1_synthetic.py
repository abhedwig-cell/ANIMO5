#!/usr/bin/env python3
"""Independent exact-rational validator for ANIMO-SYNQ02 / TCD-037-A1."""
from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "3e4247928bb43f30def951fa8804560636affbef"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"

ORACLE_PATH = ROOT / "integration/animo-synthetic/SYNQ02_TCD037_A1_ORACLE.json"
STATUS_PATH = ROOT / "integration/animo-synthetic/ANIMO-SYNQ02_STATUS.json"
DOC_PATH = ROOT / "docs/synthetic/TCD037_A1_INDEPENDENT_SYNTHETIC_ACTIVATION.md"

BASE_CH4 = (Fraction(10), Fraction(20), Fraction(30))
BASE_CO2 = (Fraction(40), Fraction(50), Fraction(60))
STATE = (Fraction(11), Fraction(22), Fraction(33))
FLUX = (Fraction(7), Fraction(13))
OTHER = Fraction(77)
Z = Fraction(10000)
CFRAC = Fraction(1, 2)

F_ACTIVE = (
    (Fraction(8), Fraction(4), Fraction(4)),
    (Fraction(4), Fraction(8), Fraction(4)),
    (Fraction(4), Fraction(4), Fraction(8)),
)
Q_ACTIVE = (
    Fraction(1, 16384),
    Fraction(1, 8192),
    Fraction(3, 16384),
)

CASES = {
    "ACTIVE": (True, F_ACTIVE, Q_ACTIVE, Fraction(1, 4)),
    "ZERO_CH4": (True, F_ACTIVE, (Fraction(0),) * 3, Fraction(1, 4)),
    "PERMUTED": (
        True,
        (F_ACTIVE[2], F_ACTIVE[0], F_ACTIVE[1]),
        (Q_ACTIVE[2], Q_ACTIVE[0], Q_ACTIVE[1]),
        Fraction(1, 4),
    ),
    "RATE_TIME_EQUIVALENT": (
        True,
        F_ACTIVE,
        tuple(q / 2 for q in Q_ACTIVE),
        Fraction(1, 2),
    ),
    "INACTIVE": (False, F_ACTIVE, Q_ACTIVE, Fraction(1, 4)),
}
EXPECTED_CASE_ORDER = list(CASES)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(*args: str) -> str:
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)
    return p.stdout


def show_json(commit: str, path: str) -> dict:
    return json.loads(run("git", "show", f"{commit}:{path}"))


def expected_layer(active: bool, f: tuple[Fraction, Fraction, Fraction], q: Fraction, st: Fraction):
    if not active:
        return BASE_CH4, BASE_CO2
    btot = sum(f, Fraction(0))
    require(btot > Fraction(1, 10**9), "synthetic oracle entered unqualified Btot branch")
    m_ch4 = Z * q * st / CFRAC
    ch4_inc = tuple(fi * m_ch4 / btot for fi in f)
    co2_inc = tuple(fi - ci for fi, ci in zip(f, ch4_inc))
    require(sum(ch4_inc, Fraction(0)) == m_ch4, "exact CH4 partition identity failed in oracle")
    require(sum((ci + oi for ci, oi in zip(ch4_inc, co2_inc)), Fraction(0)) == btot, "exact CH4+CO2 identity failed in oracle")
    return (
        tuple(b + inc for b, inc in zip(BASE_CH4, ch4_inc)),
        tuple(b + inc for b, inc in zip(BASE_CO2, co2_inc)),
    )


def parse_output(path: Path):
    rows = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split()
        require(len(parts) == 20, f"unexpected probe row shape ({len(parts)} fields): {raw}")
        case = parts[0]
        layer = int(parts[1])
        vals = tuple(float(x.replace("D", "E")) for x in parts[2:])
        rows.append((case, layer, vals))
    return rows


def exact_float(actual: float, expected: Fraction, label: str) -> None:
    expected_float = float(expected)
    require(actual == expected_float, f"{label}: expected exact binary64 {expected_float.hex()}, got {actual.hex()}")


def validate_probe(rows) -> None:
    require(len(rows) == 15, f"expected 15 rows, got {len(rows)}")
    by_case: dict[str, list[tuple[int, tuple[float, ...]]]] = {k: [] for k in CASES}
    for case, layer, vals in rows:
        require(case in CASES, f"unexpected case {case}")
        by_case[case].append((layer, vals))

    for case in EXPECTED_CASE_ORDER:
        active, fset, qset, st = CASES[case]
        records = sorted(by_case[case])
        require([layer for layer, _ in records] == [1, 2, 3], f"{case}: layer set mismatch")
        for layer, vals in records:
            idx = layer - 1
            f = fset[idx]
            q = qset[idx]
            expected_ch4, expected_co2 = expected_layer(active, f, q, st)

            echoed_f = vals[0:3]
            echoed_q, echoed_st, echoed_cfrac = vals[3:6]
            out_ch4 = vals[6:9]
            out_co2 = vals[9:12]
            state = vals[12:15]
            flux = vals[15:17]
            other = vals[17]

            for j in range(3):
                exact_float(echoed_f[j], f[j], f"{case}/L{layer}/F{j+1}")
            exact_float(echoed_q, q, f"{case}/L{layer}/QPrCH4")
            exact_float(echoed_st, st, f"{case}/L{layer}/St")
            exact_float(echoed_cfrac, CFRAC, f"{case}/L{layer}/Cfracom")
            for j in range(3):
                exact_float(out_ch4[j], expected_ch4[j], f"{case}/L{layer}/CH4_{j+1}")
                exact_float(out_co2[j], expected_co2[j], f"{case}/L{layer}/CO2_{j+1}")
                exact_float(state[j], STATE[j], f"{case}/L{layer}/state_sentinel_{j+1}")
            for j in range(2):
                exact_float(flux[j], FLUX[j], f"{case}/L{layer}/flux_sentinel_{j+1}")
            exact_float(other, OTHER, f"{case}/L{layer}/unrelated_observer")

    active = [vals for _, vals in sorted(by_case["ACTIVE"])]
    perm = [vals for _, vals in sorted(by_case["PERMUTED"])]
    rate_time = [vals for _, vals in sorted(by_case["RATE_TIME_EQUIVALENT"])]
    inactive = [vals for _, vals in sorted(by_case["INACTIVE"])]
    zero = [vals for _, vals in sorted(by_case["ZERO_CH4"])]

    out_slice = slice(6, 12)
    require(tuple(active[2][out_slice]) == tuple(perm[0][out_slice]), "PERMUTED L1 must equal ACTIVE L3 observer result")
    require(tuple(active[0][out_slice]) == tuple(perm[1][out_slice]), "PERMUTED L2 must equal ACTIVE L1 observer result")
    require(tuple(active[1][out_slice]) == tuple(perm[2][out_slice]), "PERMUTED L3 must equal ACTIVE L2 observer result")
    for i in range(3):
        require(tuple(active[i][out_slice]) == tuple(rate_time[i][out_slice]), f"rate-time amount identity failed at layer {i+1}")
        require(tuple(inactive[i][6:9]) == tuple(float(x) for x in BASE_CH4), f"inactive CH4 baseline changed at layer {i+1}")
        require(tuple(inactive[i][9:12]) == tuple(float(x) for x in BASE_CO2), f"inactive CO2 baseline changed at layer {i+1}")
        require(tuple(zero[i][6:9]) == tuple(float(x) for x in BASE_CH4), f"zero-CH4 branch has CH4 increment at layer {i+1}")


def validate_authorities_and_scope() -> None:
    rg05h = show_json(BASE, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    require(rg05h["work_unit"] == "ANIMO-RG05H", "wrong aggregate base")
    require(rg05h["state"] == "QUALIFIED_EARLY_AGGREGATE_ROUTING_REFRESH_PLUS_ONE_POST_RG05G_ATOMIC_ADMISSION_NO_PRODUCTION", "RG05H is not qualified")
    require(rg05h["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "RG05H does not point to B3I07")
    require(rg05h["b4_open"] is False and rg05h["production_open"] is False, "later project gate unexpectedly open")

    b3i07 = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    require(b3i07["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 not qualified")
    require("TCD-037-A1" in b3i07["intake"]["child_atoms"], "A1 is not canonical")
    require(b3i07["intake"]["child_class"] == "A_ACCOUNTING_REPORTING_ONLY", "A1 class changed")
    require(b3i07["intake"]["child_risk_state"] == "TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE", "A1 waiver state changed")
    require(b3i07["tier_a_waiver"]["granted"] is False, "A1 already waived unexpectedly")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    require(rq["status"] == "QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED", "RUNTIMEQ03 status changed")
    require(rq["semantic_qualification"]["ch4_layer_formation_owner"] == "QPrCH4(Ln)*St", "A1 source owner changed")
    require(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural active GHG case state changed")
    require(rq["historical_intel_behavior"] == "UNKNOWN", "historical behavior promoted")

    synq01 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq01["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM", "SYNQ01 policy authority not qualified")

    gov04 = run("git", "show", f"{GOV04}:docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    require("purpose-built synthetic activation" in gov04, "GOV04 synthetic activation alternative not found")
    require("independently qualified for causality and scope" in gov04, "GOV04 independence predicate not found")

    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    require(oracle["work_unit"] == "ANIMO-SYNQ02" and oracle["target"] == "TCD-037-A1", "wrong oracle target")
    require(oracle["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "synthetic evidence promoted")
    require(oracle["independence"]["historical_reference_claim"] is False, "synthetic evidence claims historical reference")
    require(oracle["accounting_contract"]["layer_amount"] == "QPrCH4(Ln) * St", "oracle layer amount contract changed")
    require(oracle["accounting_contract"]["numerical_acceptance"] == "EXACT_BINARY64_FOR_CHOSEN_DYADIC_SYNTHETIC_VALUES_NO_EMPIRICAL_TOLERANCE", "oracle numerical acceptance changed")
    require(oracle["natural_case"]["state"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "oracle fabricates natural case")
    require(oracle["historical_behavior"] == "UNKNOWN", "oracle promotes historical behavior")
    require(oracle["gov04_activation_predicate"]["tier_a_waiver_granted"] is False, "oracle grants waiver")
    require(oracle["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"] in {"PENDING_CI", "PASS"}, "invalid activation lifecycle")
    for value in oracle["scope"].values():
        require(value is False, "oracle scope exceeds evidence-only workunit")

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    require(status["work_unit"] == "ANIMO-SYNQ02" and status["target"] == "TCD-037-A1", "wrong status target")
    require(status["aggregate_authority"] == f"ANIMO-RG05H@{BASE}", "wrong aggregate authority")
    require(status["routing_authority"] == f"ANIMO-B3I07@{B3I07}", "wrong routing authority")
    require(status["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "status promotes evidence")
    require(status["historical_behavior"] == "UNKNOWN", "status promotes history")
    require(status["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "status fabricates natural case")
    require(status["tier_a_waiver_granted"] is False and status["scientific_admission"] is False, "status grants waiver/admission")
    require(status["state"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_TCD037_A1_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2"}, "unexpected status lifecycle")

    doc = DOC_PATH.read_text(encoding="utf-8")
    require("INDEPENDENT_IMPLEMENTATION_AND_ALGEBRAIC_ORACLE_FOR_CAUSALITY_AND_SCOPE" in doc, "document lacks bounded independence claim")
    require("does **not** itself grant the Tier-A waiver" in doc, "document must reject self-waiver")
    require("UNKNOWN" in doc and "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH" in doc, "document loses evidence boundaries")

    allowed = {
        ".github/workflows/animo-synq02-tcd037-a1.yml",
        "docs/synthetic/TCD037_A1_INDEPENDENT_SYNTHETIC_ACTIVATION.md",
        "integration/animo-synthetic/ANIMO-SYNQ02_STATUS.json",
        "integration/animo-synthetic/SYNQ02_TCD037_A1_ORACLE.json",
        "tools/synq02/tcd037_a1_source_shaped_probe.f90",
        "tools/synq02/validate_tcd037_a1_synthetic.py",
    }
    changed = [x.strip() for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x.strip()]
    require(changed, "no SYNQ02 artifacts")
    for path in changed:
        require(path in allowed, f"SYNQ02 scope widened by {path}")
        require(not path.startswith("src/"), "production source modified")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "canonical TCD register modified")
        require(not path.startswith("integration/animo-reg/"), "aggregate snapshot modified")


def main() -> None:
    require(len(sys.argv) == 2, "usage: validate_tcd037_a1_synthetic.py PROBE_OUTPUT")
    output = Path(sys.argv[1])
    require(output.is_file(), f"probe output not found: {output}")
    validate_authorities_and_scope()
    validate_probe(parse_output(output))
    print("SYNQ02 PASS: TCD-037-A1 independent synthetic causality/scope activation qualified; exact oracle; B1 only; no waiver or admission")


if __name__ == "__main__":
    main()
