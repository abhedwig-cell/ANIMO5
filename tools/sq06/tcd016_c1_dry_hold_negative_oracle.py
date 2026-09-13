#!/usr/bin/env python3
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "integration/animo-science/SQ06_TCD016_C1_DRY_HOLD_PROCESS_QUALIFICATION.json"
FRAGMENT = ROOT / "integration/animo-testbank/fragments/ANIMO-SQ06_TCD016_C1_DRY_HOLD_NEGATIVE_FRAGMENT.json"


def no_process_step(mass: Decimal) -> Decimal:
    if mass < 0:
        raise ValueError("continuation mass must be nonnegative")
    return mass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    package = json.loads(PACKAGE.read_text())
    fragment = json.loads(FRAGMENT.read_text())

    require(package["decision"] == "NO_DRY_HOLD_PROCESS_LAW_SCIENTIFICALLY_QUALIFIED", "negative decision changed")
    require(package["final_qualification"] == "QUALIFIED_NEGATIVE_NO_DRY_HOLD_PROCESS_LAW_CURRENTLY_DEFENSIBLE", "qualification changed")
    require(package["positive_process_contract"] is None, "positive process contract silently introduced")
    require(package["parameters"] == [], "process parameter introduced")
    require(package["evidence_hierarchy_application"]["external_literature_invoked"] is False, "external literature usage must be explicit")
    require(package["hypotheses"]["H5"]["disposition"] == "SELECTED", "H5 must be selected")
    for hypothesis in ("H0", "H1", "H2", "H3", "H4"):
        require(package["hypotheses"][hypothesis]["disposition"].startswith("REJECTED"), f"{hypothesis} not rejected")

    inherited = package["inherited_contract"]
    require(inherited["continuation_owner"] == "M_surface_NH4_non_aqueous_continuation", "owner identity changed")
    require(inherited["unit"] == "kg N m-2", "unit changed")
    require(inherited["chemically_noncommittal"] is True, "chemical identity overcommitted")
    require(inherited["no_process_update_is_physical_inertness_claim"] is False, "persistence promoted to physics")
    require(inherited["observer_may_own_or_reconstruct_physical_state"] is False, "observer ownership inversion")

    # Exact Decimal no-process mass guard. This verifies state semantics only, not a physical rate law.
    samples = [
        Decimal("0"),
        Decimal("1E-30"),
        Decimal("0.000013880242022597072"),
        Decimal("0.125"),
        Decimal("999.999999999999999999"),
    ]
    for initial in samples:
        after = no_process_step(initial)
        require(after == initial, "no-process persistence lost exact mass")
        require(after - initial == Decimal("0"), "hidden creation or destruction")

    # Zero-mass limit.
    require(no_process_step(Decimal("0")) == Decimal("0"), "zero mass was created")

    # Timestep partition identity. No process operator means arbitrary partitioning cannot alter the state.
    initial = Decimal("0.000013880242022597072")
    one_step = no_process_step(initial)
    many_steps = initial
    for _ in range(97):
        many_steps = no_process_step(many_steps)
    require(one_step == many_steps == initial, "no-process guard depends on timestep partition")

    # Split-run/restart identity. Persisting the explicit owner is sufficient for the no-process guard.
    continuous = initial
    for _ in range(40):
        continuous = no_process_step(continuous)
    pre_restart = initial
    for _ in range(17):
        pre_restart = no_process_step(pre_restart)
    serialized = str(pre_restart)
    restored = Decimal(serialized)
    for _ in range(23):
        restored = no_process_step(restored)
    require(restored == continuous == initial, "restart did not exactly preserve continuation state")

    # Observer remains read-only and cannot reconstruct missing state from a residual.
    mass_contract = package["mass_state_restart_implications"]
    require(mass_contract["observer_can_reconstruct_missing_state_from_residual"] is False, "observer residual ownership allowed")
    require(package["dry_hold_operational_semantics_after_negative_qualification"]["observer_role"] == "READ_ONLY_ACCOUNTING_OBSERVER", "observer role changed")

    # A negative scientific qualification must not emit a dry-process event or boundary term.
    semantics = package["dry_hold_operational_semantics_after_negative_qualification"]
    require(semantics["process_rate"] is None, "unqualified dry rate introduced")
    require(semantics["process_transfer"] is None, "unqualified dry transfer introduced")
    require(semantics["boundary_term"] is None, "unqualified boundary term introduced")
    require(semantics["rewetting_semantics"] == "OUT_OF_SCOPE_AND_UNQUALIFIED", "rewetting leaked into SQ06")

    require(fragment["central_registry_modified"] is False, "central testbank registry mutation declared")
    require(fragment["whole_model_golden_baseline"] is False, "whole-model golden introduced")
    require(fragment["qualification"]["selected_hypothesis"] == "H5", "fragment hypothesis mismatch")
    require(fragment["qualification"]["positive_process_contract_qualified"] is False, "fragment promotes process law")

    print("PASS SQ06 negative qualification oracle")
    print("selected_hypothesis=H5")
    print("exact_mass_guard=PASS_NO_TOLERANCE")
    print("zero_mass_limit=PASS")
    print("timestep_partition=PASS")
    print("restart_state_sufficiency=PASS")
    print("observer_not_owner=PASS")
    print("rewetting_scope_guard=PASS")


if __name__ == "__main__":
    main()
