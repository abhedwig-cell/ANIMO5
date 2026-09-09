#!/usr/bin/env python3
"""Fail-closed validator for ANIMO-B3Q02 child-atom disposition carrier."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
BASE = "41e43c6a6888aac5b5b52041bcdd088c7afc68f1"
CARRIER_SCHEMA = ROOT / "integration/animo-b3/B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json"
BASE_SCHEMA = ROOT / "integration/animo-b3/B3_DISPOSITION_SCHEMA.json"
CURRENT = ROOT / "integration/animo-b3/TCD042_E1_CHILD_ATOM_CARRIER.json"
ATOMIZATION = ROOT / "integration/animo-b3/B3I05_TCD042_ATOMIZATION.json"
B3I05_STATUS = ROOT / "integration/animo-b3/ANIMO-B3I05_STATUS.json"
STATUS = ROOT / "integration/animo-b3/ANIMO-B3Q02_STATUS.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def changed_paths(base: str, head: str = "HEAD") -> list[str]:
    result = subprocess.run(["git", "diff", "--name-only", base, head], cwd=ROOT, text=True, capture_output=True, check=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def validate_cross_file(carrier: dict, base_validator: Draft202012Validator, atomization: dict) -> None:
    atoms = {item["atom_id"]: item for item in atomization["atoms"]}
    atom_id = carrier["atom_id"]
    parent = carrier["parent_tcd_id"]
    routing = carrier["canonical_routing"]

    require(atomization["parent_tcd"] == parent, "carrier parent does not match canonical atomization parent")
    require(atom_id in atoms, "carrier atom is not canonically routed under the cited parent")
    atom = atoms[atom_id]
    require(atom["class"].startswith(carrier["qualification_class"] + "_"), "carrier qualification class does not match canonical child class")
    require(routing["work_unit"] == "ANIMO-B3I05", "carrier cites unexpected canonical routing workunit")
    require(routing["status_ref"] == "integration/animo-b3/ANIMO-B3I05_STATUS.json", "carrier B3I05 status ref changed")
    require(routing["atomization_ref"] == "integration/animo-b3/B3I05_TCD042_ATOMIZATION.json", "carrier atomization ref changed")
    require(atomization["allocation_decision"]["child_atom_keys_are_top_level_register_rows"] is False, "child atom promoted to top-level TCD")
    require(atomization["allocation_decision"]["tcd_043_reserved"] is False, "TCD-043 unexpectedly reserved")

    if carrier["carrier_mode"] == "READINESS_ONLY":
        require(carrier["b3_disposition"] is None, "readiness carrier may not contain formal disposition")
        require(carrier["route_state"] == "NO_ADMISSION_ROUTE_CURRENTLY_AVAILABLE", "readiness route state changed")
        require(carrier["admission_effect"]["atom_admitted"] is False, "readiness carrier admits child")
        return

    disposition = carrier["b3_disposition"]
    base_validator.validate(disposition)
    require(disposition["tcd_ids"] == [parent], "embedded tcd_ids must contain lineage parent only")
    require(disposition["atomicity"] == "ATOMIC", "formal child disposition must be atomic")
    require(disposition["qualification_class"] == carrier["qualification_class"], "qualification class mismatch")
    require(disposition["admission_route"] == carrier["route_state"], "route mismatch")
    expected_scope = f"CANONICAL_CHILD_ATOM:{atom_id}"
    require(disposition["admission_decision"]["decision_scope"] == expected_scope, "decision_scope does not bind exact child atom")
    require(carrier["admission_effect"]["atom_admitted"] == disposition["admission_decision"]["admitted"], "child admission effect mismatch")
    require(carrier["admission_effect"]["parent_admitted"] is False, "child disposition may not admit parent")
    require(carrier["admission_effect"]["new_top_level_tcd_reserved"] is False, "child disposition may not reserve new TCD")
    require(carrier["admission_effect"]["canonical_register_append"] is False, "child disposition may not append canonical top-level register")
    require(carrier["admission_effect"]["production_migration_admitted"] is False, "child disposition may not imply production migration")


def formal_fixture() -> dict:
    import tools.validate_b3q01_governance as q1
    base = q1.normal_class_a_record()
    base["record_id"] = "SELFTEST-CHILD-TCD042-E1"
    base["tcd_ids"] = ["TCD-042"]
    base["qualification_class"] = "E"
    base["admission_decision"]["decision_scope"] = "CANONICAL_CHILD_ATOM:TCD-042-E1"
    return {
        "carrier_id": "SELFTEST-FORMAL-TCD042-E1",
        "carrier_version": 1,
        "carrier_mode": "FORMAL_DISPOSITION",
        "parent_tcd_id": "TCD-042",
        "atom_id": "TCD-042-E1",
        "qualification_class": "E",
        "canonical_routing": {
            "work_unit": "ANIMO-B3I05",
            "status_ref": "integration/animo-b3/ANIMO-B3I05_STATUS.json",
            "atomization_ref": "integration/animo-b3/B3I05_TCD042_ATOMIZATION.json",
            "parent_is_top_level_tcd": True,
            "atom_is_top_level_tcd": False,
        },
        "target_binding": {
            "target_kind": "CANONICAL_CHILD_ATOM",
            "parent_role": "TOP_LEVEL_LINEAGE_PARENT_ONLY",
            "atom_role": "ATOMIC_DISPOSITION_TARGET",
            "embedded_tcd_ids_role": "LINEAGE_PARENT_IDS_NOT_DISPOSITION_TARGET",
            "new_top_level_tcd_reserved": False,
        },
        "route_state": "NORMAL_B2_AVAILABLE",
        "b3_disposition": base,
        "admission_effect": {
            "atom_admitted": True,
            "parent_admitted": False,
            "new_top_level_tcd_reserved": False,
            "canonical_register_append": False,
            "production_migration_admitted": False,
        },
        "residual_blockers": [],
    }


def assert_schema_invalid(validator: Draft202012Validator, record: dict, label: str) -> None:
    if not list(validator.iter_errors(record)):
        raise AssertionError(f"Expected carrier schema rejection: {label}")


def assert_cross_invalid(record: dict, carrier_validator: Draft202012Validator, base_validator: Draft202012Validator, atomization: dict, label: str) -> None:
    try:
        carrier_validator.validate(record)
        validate_cross_file(record, base_validator, atomization)
    except Exception:
        return
    raise AssertionError(f"Expected cross-file rejection: {label}")


def main() -> None:
    carrier_schema = json.loads(CARRIER_SCHEMA.read_text(encoding="utf-8"))
    base_schema = json.loads(BASE_SCHEMA.read_text(encoding="utf-8"))
    current = json.loads(CURRENT.read_text(encoding="utf-8"))
    atomization = json.loads(ATOMIZATION.read_text(encoding="utf-8"))
    b3i05 = json.loads(B3I05_STATUS.read_text(encoding="utf-8"))
    status = json.loads(STATUS.read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(carrier_schema)
    Draft202012Validator.check_schema(base_schema)
    cv = Draft202012Validator(carrier_schema)
    bv = Draft202012Validator(base_schema)

    require(base_schema["properties"]["tcd_ids"]["items"]["pattern"] == "^TCD-[0-9]{3}$", "B3Q01 base schema identity contract changed")
    require(b3i05["status"] == "QUALIFIED_TCD042_CANONICAL_CHILD_ROUTING_NO_NEW_TCD_NO_ADMISSIONS", "B3I05 qualified routing lost")
    require(b3i05["work_status"]["qualified"] is True and b3i05["work_status"]["work_unit_complete"] is True, "B3I05 incomplete")

    cv.validate(current)
    validate_cross_file(current, bv, atomization)
    require(current["atom_id"] == "TCD-042-E1", "current carrier target changed")
    require(current["qualification_class"] == "E", "current carrier class changed")
    require(current["admission_effect"]["atom_admitted"] is False, "current readiness carrier admits E1")

    formal = formal_fixture()
    cv.validate(formal)
    validate_cross_file(formal, bv, atomization)

    bad = copy.deepcopy(current)
    bad["carrier_mode"] = "FORMAL_DISPOSITION"
    assert_schema_invalid(cv, bad, "formal carrier without disposition")

    bad = copy.deepcopy(formal)
    bad["admission_effect"]["parent_admitted"] = True
    assert_schema_invalid(cv, bad, "child carrier admitting parent")

    bad = copy.deepcopy(formal)
    bad["b3_disposition"]["tcd_ids"] = ["TCD-041"]
    assert_cross_invalid(bad, cv, bv, atomization, "embedded lineage parent mismatch")

    bad = copy.deepcopy(formal)
    bad["b3_disposition"]["admission_decision"]["decision_scope"] = "TCD-042"
    assert_cross_invalid(bad, cv, bv, atomization, "non-atomic parent decision scope")

    bad = copy.deepcopy(formal)
    bad["atom_id"] = "TCD-042-E9"
    bad["b3_disposition"]["admission_decision"]["decision_scope"] = "CANONICAL_CHILD_ATOM:TCD-042-E9"
    assert_cross_invalid(bad, cv, bv, atomization, "uncanonical child atom")

    bad = copy.deepcopy(formal)
    bad["b3_disposition"]["tcd_ids"] = ["TCD-042-E1"]
    assert_cross_invalid(bad, cv, bv, atomization, "child key inserted into legacy top-level tcd_ids")

    # Additive-only scope: do not mutate B3Q01 schema or canonical register.
    allowed = (
        ".github/workflows/animo-b3q02-",
        "docs/governance/B3_CHILD_ATOM_DISPOSITION_CARRIER.md",
        "integration/animo-b3/ANIMO-B3Q02_STATUS.json",
        "integration/animo-b3/B3_CHILD_ATOM_DISPOSITION_CARRIER_SCHEMA.json",
        "integration/animo-b3/TCD042_E1_CHILD_ATOM_CARRIER.json",
        "tools/b3q02/",
    )
    changed = changed_paths(BASE)
    require(changed, "B3Q02 contains no artifacts")
    for path in changed:
        require(path.startswith(allowed), f"B3Q02 scope widened by {path}")
        require(path != "integration/animo-b3/B3_DISPOSITION_SCHEMA.json", "B3Q02 modified B3Q01 base schema")
        require("THEORY_CODE_DISCREPANCY_REGISTER" not in path, "B3Q02 modified canonical TCD register")
        require(not path.startswith("src/"), "B3Q02 modified production source")

    require(status["work_unit"] == "ANIMO-B3Q02", "wrong B3Q02 status workunit")
    for key, value in status["scope_guards"].items():
        require(value is False, f"B3Q02 scope guard violated: {key}")

    print("B3Q02 PASS: additive canonical child-atom carrier preserves B3Q01 base schema, exact child identity, parent non-admission and no-new-TCD invariant")


if __name__ == "__main__":
    main()
