#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_PATH = ROOT / "integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json"
MATRIX_PATH = ROOT / "integration/animo-runtime/TCD037_ACCOUNTING_SEMANTICS_MATRIX.json"

EXPECTED_STATUS = "QUALIFIED_ACCOUNTING_SEMANTIC_SPLIT_PARENT_ATOMIZATION_REQUIRED"
EXPECTED_BASE = "ANIMO-RUNTIMEQ02@45e8073fa95035b3565bd8b373ac327915cf1af5"
EXPECTED_AGGREGATE = "ANIMO-RG05G@4551b6b4c3f987b1247571d59f8489b2f1a71ba6"
EXPECTED_ROUTE = "ANIMO-B3I06@8f01f0cb366dfa8cc63a184d6f885100899a8cd9"
EXPECTED_GOV04 = "ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc"
EXPECTED_B3Q01 = "ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
EXPECTED_NEXT = "ANIMO-B3I07 — TCD-037 GHG Balance Observer Child-Atom Routing & Tier-A Readiness Partition"
EXPECTED_ARCHIVE = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"
EXPECTED_FILES = {
    "Outbal_calc.for": "4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981",
    "Outbal_write.for": "cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea",
    "Outsel.for": "b058b88aef464183aa35bdb0377315e3755192e5ee70bb88db6522cf1311ec9d",
    "ghg_ch4.for": "00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98",
    "ghg_n2o.for": "493bf88d4b321df64817a7c0eaa2725ad614a45df0a0f16cefa96ac348254175",
    "outbal2.inc": "dcf8458f3609af685f1058a378df4c4fab5a23406c573913cbd882a0a06921aa",
    "Animo.for": "352854c2ccd94b55731590fe2a2377012a302a041397fc51379c7b449b2821f7",
    "Animo.inc": "0f8b58e522ac2cdae95e8ae727dbf3ecea942e39c4d117b6bcae955d80fb69a2",
}
EXPECTED_OWNERS = {
    "CH4_FORM_LAYER": "QPrCH4(Ln)*St",
    "CH4_FORM_TOTAL": "sum(QPrCH4(1:Nl)*St)",
    "CH4_EMIT_TOTAL": "(QEmCH4Dif+QEmCH4Ebl+QEmCH4Flw+QEmCH4Plt)*St",
    "N2O_DENI_FORM_LAYER": "QPrN2Oden(Ln)*St",
    "N2O_NITR_FORM_LAYER": "QPrN2Onit(Ln)*St before existing Outbal_calc reporting threshold",
    "N2O_EMIT_TOTAL": "(QEmN2ODif+QEmN2OFlw)*St",
    "QRdN2O": "SEPARATE_N2O_REDUCTION_SINK_NOT_TCD037_OBSERVER_PRODUCER",
}
EXPECTED_CHILDREN = {
    "TCD-037-A1": ["Bfom(CH4f)", "Bahu(CH4f)", "Bdom(CH4f)", "Bfom(CO2f)", "Bahu(CO2f)", "Bdom(CO2f)"],
    "TCD-037-A2": ["Btom(CH4e)", "Btom(CO2e)"],
    "TCD-037-A3": ["Bani(N2Od)"],
    "TCD-037-A4": ["Bani(N2Oe)"],
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"RUNTIMEQ03 validation FAIL: {message}")


def load_json(path):
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


status = load_json(STATUS_PATH)
matrix = load_json(MATRIX_PATH)

require(status["work_unit"] == "ANIMO-RUNTIMEQ03", "wrong work unit")
require(status["tcd"] == "TCD-037", "wrong TCD")
require(status["status"] == EXPECTED_STATUS, "wrong status")
require(status["authoring_base"] == EXPECTED_BASE, "wrong authoring base")
require(status["aggregate_authority"] == EXPECTED_AGGREGATE, "wrong aggregate authority")
require(status["canonical_routing_authority"] == EXPECTED_ROUTE, "wrong routing authority")
require(status["gov04_authority"] == EXPECTED_GOV04, "wrong GOV04 authority")
require(status["b3q01_authority"] == EXPECTED_B3Q01, "wrong B3Q01 authority")
require(status["next_work_unit"] == EXPECTED_NEXT, "wrong next work unit")
require(status["parent_atomic"] is False, "parent must be non-atomic")
require(status["parent_atomization_required"] is True, "parent atomization must be required")
require(status["canonical_child_atoms_allocated"] is False, "RUNTIMEQ03 may not allocate canonical children")
require(status["new_top_level_tcd"] is False, "RUNTIMEQ03 may not allocate a top-level TCD")
require(status["proposed_child_count"] == 4, "expected four proposed children")
require(status["proposed_child_ids"] == list(EXPECTED_CHILDREN), "proposed child ids changed")
require(status["proposed_child_risk_tier"] == "TIER_A_CANDIDATE", "child risk classification changed")
require(status["parent_tier_a_waiver"] == "NOT_AVAILABLE_AT_PARENT_SCOPE_ATOMIZATION_REQUIRED", "parent waiver must remain unavailable")
require(status["natural_active_ghg_case"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural GHG evidence overstated")
require(status["synthetic_evidence"] == "B1_ONLY_NOT_INDEPENDENT_B2", "synthetic evidence strength overstated")
require(status["historical_intel_behavior"] == "UNKNOWN", "historical Intel behavior must remain unknown")
require(status["scientific_admission"] is False, "scientific admission forbidden")
require(status["production_patch"] is False, "production patch forbidden")
require(status["b4"] is False, "B4 forbidden")
require(status["rg05h_update"] is False, "RG05H forbidden")
require(status["composition"] == [], "TCD composition forbidden")
for key in ("physical_state", "process_flux", "restart_state", "solver_or_numerical_policy"):
    require(status["expected_difference"][key] == "NONE", f"unexpected {key} difference")
require(status["expected_difference"]["observer_only"] is True, "expected difference must be observer-only")

require(matrix["work_unit"] == "ANIMO-RUNTIMEQ03", "matrix work unit mismatch")
require(matrix["tcd"] == "TCD-037", "matrix TCD mismatch")
require(matrix["source_identity"]["archive_sha256"] == EXPECTED_ARCHIVE, "frozen archive pin changed")
require(matrix["source_identity"]["files"] == EXPECTED_FILES, "frozen file pins changed")
require(matrix["semantic_owners"] == EXPECTED_OWNERS, "semantic owner map changed")
require(matrix["semantic_collisions"]["CH4_INDEX0_FORMATION_VS_EMISSION_OVERLOAD"] is True, "CH4 index-0 collision missing")
require(matrix["semantic_collisions"]["N2O_INDEX0_PRODUCTION_VS_EMISSION_CONSUMER_MISMATCH"] is True, "N2O index-0 mismatch missing")
require(matrix["semantic_collisions"]["single_array_single_owner_contract_valid"] is False, "single-array ownership must remain rejected")

children = matrix["proposed_children"]
require(len(children) == 4, "matrix must contain four proposed children")
require([c["atom_id"] for c in children] == list(EXPECTED_CHILDREN), "matrix child order/identity changed")
for child in children:
    atom = child["atom_id"]
    require(child["parent_tcd"] == "TCD-037", f"{atom} wrong parent")
    require(child["canonical"] is False, f"{atom} must remain provisional")
    require(child["qualification_class"] == "A_ACCOUNTING_REPORTING_ONLY", f"{atom} class changed")
    require(child["gov04_risk"] == "TIER_A_CANDIDATE", f"{atom} GOV04 risk changed")
    require(child["allowed_observer_differences"] == EXPECTED_CHILDREN[atom], f"{atom} expected-difference whitelist changed")

contract = matrix["expected_difference_contract"]
require(contract == {
    "physical_state": "NONE",
    "process_flux": "NONE",
    "restart_state": "NONE",
    "solver_or_numerical_policy": "NONE",
    "scope": "OBSERVER_ACCOUNTING_FIELDS_ONLY",
}, "matrix expected-difference contract changed")
activation = matrix["activation_evidence"]
require(activation["natural_active_ghg"] == "BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH", "natural activation overstated")
require(activation["synthetic_probe"] == "PASS_B1_CAUSAL_ONLY", "probe evidence strength changed")
require(activation["synthetic_probe_sha256"] == "e0da47422092896c7f3b2ab6b81070fb25e9907424ca51808b6a906ae76c0a47", "probe source hash changed")
require(activation["expected_output_sha256"] == "e734b3f90a7a86e7708a34ee309a71f2cd6d677f360e6cb87b0d394e44e2114b", "probe output hash changed")
require(activation["historical_intel_behavior"] == "UNKNOWN", "historical behavior overstated")
routing = matrix["routing"]
require(routing["parent_atomic"] is False, "routing parent must remain non-atomic")
require(routing["parent_atomization_required"] is True, "routing atomization flag missing")
require(routing["canonical_child_atoms_allocated"] is False, "routing may not allocate children")
require(routing["new_top_level_tcd"] is False, "routing may not allocate top-level TCD")
require(routing["parent_tier_a_waiver"] == "NOT_AVAILABLE_AT_PARENT_SCOPE_ATOMIZATION_REQUIRED", "routing parent waiver changed")
require(routing["next_work_unit"] == EXPECTED_NEXT, "routing next work unit changed")

print("RUNTIMEQ03 validation PASS")
