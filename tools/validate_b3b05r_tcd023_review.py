#!/usr/bin/env python3
import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = "e76345bf984c58ff0b30a24b39dc8e037a2f4fd6"
SOURCE_SHA = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
TESTBANK_SHA = "44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"
MEMBER_SHA = "938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV04_MATRIX_BLOB = "845db982f9a72e7cf271b74e948f46ce81dec028"


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(cond, msg):
    if not cond:
        raise SystemExit("FAIL: " + msg)


result = load("integration/animo-b3/TCD023_INDEPENDENT_SECOND_LINE_REVIEW.json")
prep04 = load("integration/animo-prep/PREP04_STABLE_DOM_P_PARTITION.json")
prep05 = load("integration/animo-prep/PREP05_CROSS_SPECIES_SYMMETRY_AUDIT.json")
recheck = load("integration/animo-b3/TCD023_INDEPENDENT_RECHECK.json")
expected = load("integration/animo-b3/TCD023_EXPECTED_DIFFERENCE.json")
upstream = load("integration/animo-b3/TCD023_UPSTREAM_EVIDENCE.json")
synq = load("integration/animo-synthetic/SYNTHETIC_ORACLE_REGISTER.json")

require(result["semantic_result"] == "PASS", "semantic result is not PASS")
require(result["reviewed_readiness"]["head"] == READINESS, "readiness pin changed")
require(result["reviewed_readiness"]["actions_conclusion_rechecked"] == "success", "readiness Actions not green")
require(result["live_authorities"]["GOV04"] == "ANIMO-GOV04@" + GOV04, "GOV04 review pin changed")
require(upstream["pinned_authorities"]["risk_tier_governance"]["head"] == GOV04, "readiness GOV04 pin changed")
require(upstream["pinned_authorities"]["risk_tier_governance"]["matrix_blob_sha"] == GOV04_MATRIX_BLOB, "GOV04 matrix blob pin changed")
require(result["frozen_B0"]["source_archive_sha256"] == SOURCE_SHA, "source archive pin mismatch")
require(result["frozen_B0"]["testbank_archive_sha256"] == TESTBANK_SHA, "testbank pin mismatch")
require(result["frozen_B0"]["source_member_sha256"] == MEMBER_SHA, "resp_miner pin mismatch")
require(result["frozen_B0"]["source_member_size_bytes"] == 62997, "resp_miner size mismatch")

source_hash = (ROOT / "reference/source/ANIMO_4.1.5.53.zip.sha256").read_text().split()[0]
testbank_hash = (ROOT / "reference/testcases/ANIMO_testbank.zip.sha256").read_text().split()[0]
require(source_hash == SOURCE_SHA, "repository source hash file mismatch")
require(testbank_hash == TESTBANK_SHA, "repository testbank hash file mismatch")

member = None
with (ROOT / "reference/source/source_manifest.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["path"] == "ANIMO_4.1.5.53/resp_miner.for":
            member = row
            break
require(member is not None, "resp_miner missing from source manifest")
require(member["sha256"] == MEMBER_SHA, "source manifest resp_miner sha mismatch")
require(int(member["size_bytes"]) == 62997, "source manifest resp_miner size mismatch")

legacy = [
    "Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)",
    "Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)",
]
candidate = [
    "Transfop(19,Ln) = (1.0-AsfaSDO) * Transfop(17,Ln)",
    "Transfop(20,Ln) = AsfaSDO * Transfop(17,Ln)",
]
require(recheck["independent_source_recheck"]["legacy_P_daughter_19"] == legacy[0], "legacy line 19 mismatch")
require(recheck["independent_source_recheck"]["legacy_P_daughter_20"] == legacy[1], "legacy line 20 mismatch")
require(expected["candidate_change"]["candidate"] == candidate, "candidate seam mismatch")
require(recheck["independent_source_recheck"]["case2_selector"] == "Recfhu < 1e-12 AND RecfHUSDO < 1e-12 AND recfSDO >= 1e-12", "Case(2) selector mismatch")
require(recheck["independent_source_recheck"]["implicit_NP_conversion_factor_at_seam_found"] is False, "implicit N/P conversion remains unresolved")
require(recheck["species_identity"]["Transfon17_units"] == "kg N m-2 per interval", "N ownership/units mismatch")
require(recheck["species_identity"]["Transfop17_units"] == "kg P m-2 per interval", "P ownership/units mismatch")
require(recheck["species_identity"]["numeric_tolerance_needed_for_mathematical_identity"] is False, "identity unexpectedly needs tolerance")

hc = prep05["high_confidence_statements"]
require(len(hc) == 2 and all(x["mapped_discrepancy"] == "TCD-023" for x in hc), "PREP05 symmetry cross-check changed")
neg = prep05["tests"]["negative_controls"]
require("reciprocal N/P coupling is not promoted" in neg, "PREP05 reciprocal N/P negative control missing")
require("isolated N/P ratio relationship is not promoted" in neg, "PREP05 N/P ratio negative control missing")

oracles = {o["oracle_id"]: o for o in synq["oracles"]}
for oid in ("SYNQ-O004", "SYNQ-O005"):
    require(oid in oracles, f"{oid} missing")
    require(oracles[oid]["target_tcd"] == "TCD-023", f"{oid} target changed")
    require(oracles[oid]["pass_fail"] == "PASS", f"{oid} not PASS")
    require(oracles[oid]["independence_classification"] == "STRONGLY_INDEPENDENT", f"{oid} independence changed")
require(synq["evidence_boundary"]["B2_reference_created"] is False, "SYNQ improperly promoted to B2")

nat = recheck["natural_activation_independent_replay"]
require(nat["phosphorus_cycle_active"] is True, "natural case phosphorus not active")
require(nat["unique_time_layer_Case2_events"] == 9658, "natural activation count mismatch")
require(nat["affected_layers"] == [17,18,19,20,21,22,23], "affected layers mismatch")
require(prep04["reachability"]["actual_nonpotential_case2_events"] == 9658, "PREP04 cross-check count mismatch")
require(prep04["reachability"]["layers"] == nat["affected_layers"], "PREP04 layer cross-check mismatch")

require(nat["accumulated_legacy_local_P_identity_mismatch_kg_m_minus_2"] == 1.0806894643265774e-11, "accumulated mismatch changed")
require(nat["accumulated_legacy_local_P_identity_mismatch_kg_ha_minus_1"] == 1.0806894643265774e-7, "hectare mismatch changed")
require(nat["largest_single_event_identity_mismatch_kg_m_minus_2"] == 1.0228664519933875e-14, "single-event mismatch changed")

down = recheck["downstream_unrounded_effect_independent_replay"]
require(down["max_abs_delta_Tomnpo_kg_m_minus_2_per_step"] == 1.0228664519933892e-14, "Tomnpo delta changed")
require(down["max_abs_delta_Rekopo_kg_m_minus_3_d_minus_1"] == 9.327856586446364e-15, "Rekopo delta changed")
require(down["physical_or_process_effect_exactly_zero"] is False, "Tier A exclusion lost")

reg = recheck["eight_case_regression_replay"]
required_cases = ["CranGrass","CranMais","GrassPeat","LWKM_gras_1040.2021.2045","Puitmijn_Cranendonck_60","RuurloGrass","STONE_akk_0006.2001.2015","Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA"]
require(list(reg["cases"].keys()) == required_cases, "eight-case surface changed")
for c in required_cases:
    require(reg["cases"][c]["successful_completion"] is True, f"case failed: {c}")
    diffs = reg["cases"][c]["normalized_scientific_differences"]
    if c == "Puitmijn_Cranendonck_60":
        require(diffs == ["ani_pLO.Bal","ani_pTP.Bal","bapoLO.Out","bapoTP.Out","message.out"], "Puitmijn expected difference changed")
    else:
        require(diffs == [], f"unexpected difference in {c}")
require(reg["unexpected_changed_files"] == [], "unexpected changed outputs")
require(reg["missing_candidate_outputs"] == [], "missing candidate outputs")
require(reg["extra_candidate_outputs"] == [], "extra candidate outputs")
require(reg["comparison_has_scientific_numeric_tolerance"] is False, "scientific numeric tolerance introduced")
require(reg["volatile_metadata_normalization_only"] is True, "normalization scope widened")

require(result["risk"]["qualification_class"] == "B_LOCAL_ALGEBRA_INDEX_SPECIES", "review qualification class changed")
require(result["risk"]["GOV04_tier"] == "B", "review tier is not B")
require(result["risk"]["independent_review_required"] is True, "Tier-B independent review flag lost")
require(result["risk"]["tier_C_or_D_trigger_found"] is False, "higher-tier trigger unresolved")
require(result["downstream_effect"]["tier_A_available"] is False, "review incorrectly allows Tier A")
require(result["historical_behavior"]["revision_53_behavior"] == "UNKNOWN", "historical UNKNOWN not preserved")
require(result["historical_behavior"]["qualified_B2_found"] is False, "unexpected B2 claim")
require(result["independent_review_gate_satisfied"] is True, "independent gate not satisfied")
require(result["admission_performed"] is False, "admission performed in review")
require(result["production_modification_performed"] is False, "production modification performed in review")

allowed = {
    "docs/b3/TCD023_INDEPENDENT_SECOND_LINE_REVIEW_CONTRACT.md",
    "docs/b3/TCD023_INDEPENDENT_SECOND_LINE_REVIEW.md",
    "integration/animo-b3/TCD023_INDEPENDENT_SECOND_LINE_REVIEW.json",
    "tools/validate_b3b05r_tcd023_review.py",
    ".github/workflows/animo-b3b05r-tcd023-independent-review.yml",
}
changed = set(subprocess.check_output(["git", "diff", "--name-only", READINESS, "HEAD"], cwd=ROOT, text=True).splitlines())
require(changed <= allowed, "scope guard found unexpected changed paths: " + ", ".join(sorted(changed - allowed)))
for forbidden_prefix in ("reference/", "src/", "source/", "production/"):
    require(not any(p.startswith(forbidden_prefix) for p in changed), f"forbidden production/frozen path changed: {forbidden_prefix}")
require("docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" not in changed, "canonical TCD register changed")

print("ANIMO-B3B05R independent TCD-023 review validator: PASS")
print("semantic result: PASS")
print("reviewed readiness:", READINESS)
print("frozen B0/source member identity: PASS")
print("Case(2) species-local partition identity: PASS_EXACT_NO_TOLERANCE")
print("PREP05 legitimate N/P coupling negative controls: PASS")
print("SYNQ-O004/O005 boundary: PASS_NOT_B2")
print("natural activation: 9658 unique events, layers 17..23")
print("downstream nonzero Tomnpo/Rekopo effect: CONFIRMED_TIER_A_EXCLUDED")
print("eight-case regression surface: PASS")
print("GOV04 risk tier: B, live policy reviewed at pinned sibling authority")
print("historical revision-53 behaviour: UNKNOWN")
print("scope guard: PASS_REVIEW_ONLY_NO_ADMISSION_NO_PRODUCTION_CHANGE")
