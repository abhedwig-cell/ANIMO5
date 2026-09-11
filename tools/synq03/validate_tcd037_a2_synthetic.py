#!/usr/bin/env python3
"""Independent exact-rational validator for ANIMO-SYNQ03 / TCD-037-A2."""
from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "331f6ed91d4a1c15a23ae0c1ad75d1b540f61858"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"

ORACLE_PATH = ROOT / "integration/animo-synthetic/SYNQ03_TCD037_A2_ORACLE.json"
STATUS_PATH = ROOT / "integration/animo-synthetic/ANIMO-SYNQ03_STATUS.json"
DOC_PATH = ROOT / "docs/synthetic/TCD037_A2_INDEPENDENT_SYNTHETIC_ACTIVATION.md"

Z = Fraction(10000)
CFRAC = Fraction(1, 2)
D_OM = Fraction(16)
BASE_CH4E = Fraction(100)
BASE_CO2E = Fraction(200)
STATE = (Fraction(11), Fraction(22), Fraction(33))
FLUX = (Fraction(7), Fraction(13))
A1 = Fraction(31)
A3 = Fraction(41)
A4 = Fraction(51)
OTHER = Fraction(77)

QPR_ACTIVE = (
    Fraction(1, 16384),
    Fraction(1, 8192),
    Fraction(3, 16384),
)
QEM_ACTIVE = (
    Fraction(1, 32768),
    Fraction(1, 16384),
    Fraction(1, 32768),
    Fraction(0),
)
QEM_EQUAL = (
    Fraction(1, 8192),
    Fraction(1, 8192),
    Fraction(1, 8192),
    Fraction(0),
)
ZERO_PR = (Fraction(0),) * 3
ZERO_EM = (Fraction(0),) * 4

CASES = {
    "DIVERGENT_ACTIVE": (True, QPR_ACTIVE, QEM_ACTIVE, Fraction(1, 4)),
    "FORMATION_ONLY": (True, QPR_ACTIVE, ZERO_EM, Fraction(1, 4)),
    "EMISSION_ONLY": (True, ZERO_PR, QEM_ACTIVE, Fraction(1, 4)),
    "EQUAL_TOTALS_CONTROL": (True, QPR_ACTIVE, QEM_EQUAL, Fraction(1, 4)),
    "RATE_TIME_EQUIVALENT": (
        True,
        tuple(q / 2 for q in QPR_ACTIVE),
        tuple(q / 2 for q in QEM_ACTIVE),
        Fraction(1, 2),
    ),
    "INACTIVE": (False, QPR_ACTIVE, QEM_ACTIVE, Fraction(1, 4)),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(*args: str) -> str:
    proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=True)
    return proc.stdout


def show_json(commit: str, path: str) -> dict:
    return json.loads(run("git", "show", f"{commit}:{path}"))


def expected(active: bool, qpr: tuple[Fraction, ...], qem: tuple[Fraction, ...], st: Fraction):
    if not active:
        return BASE_CH4E, BASE_CO2E, Fraction(0), Fraction(0)
    formation = sum(qpr, Fraction(0)) * st
    emission = sum(qem, Fraction(0)) * st
    ch4e = BASE_CH4E + Z * emission / CFRAC
    co2e = BASE_CO2E + D_OM - Z * formation / CFRAC
    return ch4e, co2e, formation, emission


def exact_float(actual: float, expected_value: Fraction, label: str) -> None:
    expected_float = float(expected_value)
    require(
        actual == expected_float,
        f"{label}: expected exact binary64 {expected_float.hex()}, got {actual.hex()}",
    )


def parse_output(path: Path):
    rows: dict[str, tuple[float, ...]] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        parts = raw.split()
        require(len(parts) == 22, f"unexpected probe row shape ({len(parts)} fields): {raw}")
        case = parts[0]
        require(case in CASES, f"unexpected case {case}")
        require(case not in rows, f"duplicate case {case}")
        rows[case] = tuple(float(x.replace("D", "E")) for x in parts[1:])
    require(set(rows) == set(CASES), f"case set mismatch: {sorted(rows)}")
    return rows


def validate_probe(rows: dict[str, tuple[float, ...]]) -> None:
    for case, (active, qpr, qem, st) in CASES.items():
        vals = rows[case]
        require(len(vals) == 21, f"{case}: expected 21 numeric columns")
        echoed_qpr = vals[0:3]
        echoed_qem = vals[3:7]
        echoed_st = vals[7]
        echoed_dom = vals[8]
        echoed_cfrac = vals[9]
        out_ch4e = vals[10]
        out_co2e = vals[11]
        state = vals[12:15]
        flux = vals[15:17]
        a1, a3, a4, other = vals[17:21]

        for i in range(3):
            exact_float(echoed_qpr[i], qpr[i], f"{case}/QPrCH4[{i+1}]")
        for i in range(4):
            exact_float(echoed_qem[i], qem[i], f"{case}/QEmCH4[{i+1}]")
        exact_float(echoed_st, st, f"{case}/St")
        exact_float(echoed_dom, D_OM, f"{case}/D_OM")
        exact_float(echoed_cfrac, CFRAC, f"{case}/Cfracom")

        exp_ch4e, exp_co2e, _, _ = expected(active, qpr, qem, st)
        exact_float(out_ch4e, exp_ch4e, f"{case}/Btom(CH4e)")
        exact_float(out_co2e, exp_co2e, f"{case}/Btom(CO2e)")

        for i in range(3):
            exact_float(state[i], STATE[i], f"{case}/physical_state[{i+1}]")
        for i in range(2):
            exact_float(flux[i], FLUX[i], f"{case}/process_flux[{i+1}]")
        exact_float(a1, A1, f"{case}/A1_sentinel")
        exact_float(a3, A3, f"{case}/A3_sentinel")
        exact_float(a4, A4, f"{case}/A4_sentinel")
        exact_float(other, OTHER, f"{case}/unrelated_observer")

    divergent = rows["DIVERGENT_ACTIVE"]
    formation_only = rows["FORMATION_ONLY"]
    emission_only = rows["EMISSION_ONLY"]
    rate_time = rows["RATE_TIME_EQUIVALENT"]
    inactive = rows["INACTIVE"]

    # Independent causal discrimination of the two semantic owners.
    require(divergent[11] == formation_only[11], "same formation must preserve Btom(CO2e)")
    require(divergent[10] != formation_only[10], "changed emission must change Btom(CH4e)")
    require(divergent[10] == emission_only[10], "same emission must preserve Btom(CH4e)")
    require(divergent[11] != emission_only[11], "changed formation must change Btom(CO2e)")
    require(divergent[10:12] == rate_time[10:12], "rate-time amount equivalence failed")
    require(inactive[10] == float(BASE_CH4E) and inactive[11] == float(BASE_CO2E), "inactive observer branch changed target fields")

    _, _, div_form, div_emit = expected(True, QPR_ACTIVE, QEM_ACTIVE, Fraction(1, 4))
    require(div_form != div_emit, "divergent case failed to discriminate formation from emission")
    require(div_form == Fraction(3, 32768), "unexpected divergent formation amount")
    require(div_emit == Fraction(1, 32768), "unexpected divergent emission amount")
    _, _, eq_form, eq_emit = expected(True, QPR_ACTIVE, QEM_EQUAL, Fraction(1, 4))
    require(eq_form == eq_emit, "equal-totals control does not actually have equal source-owned amounts")


def validate_authorities_and_scope() -> None:
    b3d21 = show_json(BASE, "integration/animo-b3/ANIMO-B3D21_STATUS.json")
    require(b3d21["work_unit"] == "ANIMO-B3D21", "wrong exact base workunit")
    require(b3d21["state"] == "ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY", "B3D21 base is not admitted")
    require(b3d21["target_child_atom"] == "TCD-037-A1", "B3D21 target changed")
    require(b3d21["admission_effect"]["child_atom_admitted"] is True, "A1 admission missing at base")
    require(b3d21["admission_effect"]["parent_tcd_admitted"] is False, "parent TCD unexpectedly admitted")
    require(b3d21["admission_effect"]["sibling_atoms_admitted"] == [], "sibling admission already present at base")
    require(b3d21["aggregate_policy"]["rg05i_created"] is False, "RG05I unexpectedly existed at SYNQ03 base")
    require(b3d21["work_status"]["qualified"] is True and b3d21["work_status"]["work_unit_complete"] is True, "B3D21 base incomplete")

    rg05h = show_json(RG05H, "integration/animo-reg/ANIMO-RG05H_STATUS.json")
    require(rg05h["work_unit"] == "ANIMO-RG05H", "wrong aggregate authority")
    require(rg05h["work_status"]["qualified"] is True, "RG05H not qualified")
    require(rg05h["current_routing_authority"] == f"ANIMO-B3I07@{B3I07}", "RG05H routing authority changed")
    require(rg05h["b4_open"] is False and rg05h["production_open"] is False, "later project gate unexpectedly open")

    b3i07 = show_json(B3I07, "integration/animo-b3/ANIMO-B3I07_STATUS.json")
    require(b3i07["status"] == "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION", "B3I07 not qualified")
    require("TCD-037-A2" in b3i07["intake"]["child_atoms"], "A2 is not canonical")
    require(b3i07["intake"]["child_class"] == "A_ACCOUNTING_REPORTING_ONLY", "A2 class changed")
    require(b3i07["readiness_routes"]["TCD-037-A2"] == "ANIMO-B3A06", "A2 readiness route changed")

    atomization = show_json(B3I07, "integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms = {a["atom_id"]: a for a in atomization["atoms"]}
    require("TCD-037-A2" in atoms, "A2 absent from canonical atomization")
    a2 = atoms["TCD-037-A2"]
    require(a2["class"] == "A_ACCOUNTING_REPORTING_ONLY", "A2 atom class changed")
    require(a2["source_owners"]["formation_total"] == "sum(QPrCH4(1:Nl)*St)", "A2 formation owner changed")
    require(a2["source_owners"]["atmosphere_emission"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "A2 emission owner changed")
    require(a2["allowed_observer_fields"] == ["Btom(CH4e)", "Btom(CO2e) formation-side dissimilation complement only"], "A2 difference surface changed")
    require(a2["wider_ghg_carbon_ledger_claim"] is False, "A2 widened into full carbon ledger")

    rq = show_json(RUNTIMEQ03, "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    require(rq["status"] == "QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED", "RUNTIMEQ03 status changed")
    sq = rq["semantic_qualification"]
    require(sq["ch4_total_formation_owner"] == "sum(QPrCH4(1:Nl)*St)", "RUNTIMEQ03 formation owner changed")
    require(sq["ch4_atmosphere_emission_owner"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "RUNTIMEQ03 emission owner changed")
    require(sq["ch4_index0_overloaded"] is True, "RUNTIMEQ03 no longer qualifies CH4 index-0 overload")
    require(rq["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural active GHG case state changed")
    require(rq["historical_intel_behavior"] == "UNKNOWN", "historical behavior promoted")
    require(rq["expected_difference"]["physical_state"] == "NONE" and rq["expected_difference"]["process_flux"] == "NONE", "A2 non-interference basis changed")

    synq01 = show_json(SYNQ01, "integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq01["status"] == "QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM", "SYNQ01 policy authority not qualified")
    require(synq01["evidence_boundary"]["B2_reference_created"] is False, "SYNQ01 unexpectedly creates B2")

    gov04 = run("git", "show", f"{GOV04}:docs/governance/ANIMO_GOV04_RISK_TIERED_REVIEW_POLICY.md")
    require("purpose-built synthetic activation is independently qualified for causality and scope" in gov04, "GOV04 synthetic activation alternative missing")
    require("historical behaviour remains exactly `UNKNOWN`" in gov04, "GOV04 historical-uncertainty predicate missing")

    oracle = json.loads(ORACLE_PATH.read_text(encoding="utf-8"))
    require(oracle["work_unit"] == "ANIMO-SYNQ03" and oracle["target"] == "TCD-037-A2", "wrong oracle target")
    require(oracle["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "synthetic evidence promoted")
    require(oracle["independence"]["historical_reference_claim"] is False, "synthetic oracle claims historical reference")
    require(oracle["accounting_contract"]["ch4_formation_total"] == "sum(QPrCH4(1:Nl)*St)", "oracle formation owner changed")
    require(oracle["accounting_contract"]["ch4_atmosphere_emission_total"] == "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St", "oracle emission owner changed")
    require(oracle["accounting_contract"]["full_model_co2_ledger_claim"] is False, "oracle widens CO2 claim")
    require(oracle["natural_case"]["state"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "oracle fabricates natural case")
    require(oracle["natural_case"]["translation_performed"] is False, "oracle translates incompatible testcase")
    require(oracle["historical_behavior"] == "UNKNOWN", "oracle promotes history")
    require(oracle["gov04_activation_predicate"]["tier_a_waiver_granted"] is False, "oracle grants Tier-A waiver")
    require(oracle["gov04_activation_predicate"]["independently_qualified_for_causality_and_scope"] in {"PENDING_CI", "PASS"}, "invalid oracle qualification lifecycle")
    for key, value in oracle["scope"].items():
        require(value is False, f"oracle scope exceeds evidence-only workunit: {key}")

    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    require(status["work_unit"] == "ANIMO-SYNQ03" and status["target"] == "TCD-037-A2", "wrong status target")
    require(status["base_authority"] == f"ANIMO-B3D21@{BASE}", "wrong SYNQ03 base authority")
    require(status["aggregate_authority"] == f"ANIMO-RG05H@{RG05H}", "wrong aggregate authority in status")
    require(status["routing_authority"] == f"ANIMO-B3I07@{B3I07}", "wrong routing authority in status")
    require(status["evidence_strength"] == "B1_SYNTHETIC_NOT_B2", "status promotes evidence")
    require(status["historical_behavior"] == "UNKNOWN", "status promotes history")
    require(status["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "status fabricates natural case")
    require(status["testcase_translation_performed"] is False, "status translates incompatible testcase")
    require(status["tier_a_waiver_granted"] is False and status["scientific_admission"] is False, "status grants waiver/admission")
    require(status["parent_or_sibling_admission"] is False, "status implies parent/sibling admission")
    require(status["full_carbon_ledger_closure_claimed"] is False and status["tcd032_036_composition"] is False, "status widens A2 scope")
    require(status["state"] in {"PERSISTED_VALIDATION_PENDING", "QUALIFIED_TCD037_A2_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2"}, "unexpected status lifecycle")

    doc = DOC_PATH.read_text(encoding="utf-8")
    require("INDEPENDENT_IMPLEMENTATION_AND_ALGEBRAIC_ORACLE_FOR_CAUSALITY_AND_SCOPE" in doc, "document lacks bounded independence claim")
    require("does **not** grant the GOV04 Tier-A waiver" in doc, "document must reject self-waiver")
    require("B1_SYNTHETIC_NOT_B2" in doc and "UNKNOWN" in doc, "document loses evidence boundary")
    require("not a model-wide CO2 ledger" in doc, "document must preserve bounded CO2e semantics")

    allowed = {
        ".github/workflows/animo-synq03-tcd037-a2.yml",
        "docs/synthetic/TCD037_A2_INDEPENDENT_SYNTHETIC_ACTIVATION.md",
        "integration/animo-synthetic/ANIMO-SYNQ03_STATUS.json",
        "integration/animo-synthetic/SYNQ03_TCD037_A2_ORACLE.json",
        "tools/synq03/tcd037_a2_source_shaped_probe.f90",
        "tools/synq03/validate_tcd037_a2_synthetic.py",
    }
    changed = {x.strip() for x in run("git", "diff", "--name-only", BASE, "HEAD").splitlines() if x.strip()}
    require(changed == allowed, f"SYNQ03 exact scope mismatch: {sorted(changed ^ allowed)}")
    require(not any(p.startswith("src/") for p in changed), "production source modified")
    require(not any(p.startswith("docs/governance/") for p in changed), "governance policy modified")
    require(not any("THEORY_CODE_DISCREPANCY_REGISTER" in p for p in changed), "canonical TCD register modified")
    require(not any("B3D21" in p or "B3A05" in p for p in changed), "prior admission/readiness authority modified")


def main() -> None:
    require(len(sys.argv) == 2, "usage: validate_tcd037_a2_synthetic.py <probe-output>")
    output = Path(sys.argv[1])
    require(output.is_file(), f"probe output missing: {output}")
    validate_authorities_and_scope()
    rows = parse_output(output)
    validate_probe(rows)
    print("SYNQ03 PASS: TCD-037-A2 formation/emission ownership is independently discriminated at B1 synthetic evidence level with exact scope and no admission")


if __name__ == "__main__":
    main()
