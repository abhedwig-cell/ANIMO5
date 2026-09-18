#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="2279a961459211e03550dfda4af09ab4f7f6b9a3"
RG06="8efdd151d89e1cff131d4b21e2acf559ca1828d6"
KT15A="2279a961459211e03550dfda4af09ab4f7f6b9a3"
ARCH02="a079d93c965f6073586c55ee4b3544dd8873b723"
GOV04="1bbe4c211197590f346803106e45dca5faae79fc"

def fail(msg):
    print("KT16 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())
def show_json(sha,path):
    return json.loads(subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R,text=True))

st=load("integration/animo-kt16/ANIMO-KT16_STATUS.json")

rg=show_json(RG06,"integration/animo-reg/ANIMO-RG06_STATUS.json")
if rg.get("state")!="QUALIFIED_POST_KT11_CURRENT_PROGRAM_REBASELINE_AND_NEXT_WAVE_ROUTING_NO_SCIENTIFIC_OR_PRODUCTION_ADVANCE":
    fail("RG06 state")
if rg.get("b4_open") is not False or rg.get("production_open") is not False:
    fail("RG06 gates")

kt=show_json(KT15A,"integration/animo-kt15a/ANIMO-KT15A_STATUS.json")
if kt.get("state")!="QUALIFIED_IMMUTABLE_APPLICATION_CONFIGURATION_BINDING_TIER_D_REVIEW_REQUIRED":
    fail("KT15A state")
for field in [
    "immutable_application_config_qualified",
    "accepted_state_config_binding_qualified",
    "exact_config_equality_qualified",
    "multi_interval_config_stability_qualified"
]:
    if kt.get(field) is not True:
        fail("KT15A qualification flag "+field)
if kt.get("checkpoint_schema_admitted") is not False or kt.get("canonical_state_admitted") is not False:
    fail("KT15A state/checkpoint boundary")
if kt.get("production_authorized") is not False:
    fail("KT15A production boundary")

arch=show_json(ARCH02,"integration/animo-architecture/ANIMO-ARCH02_STATUS.json")
if arch.get("decision")!="QUALIFIED_CANDIDATE_RESTART_AND_CHECKPOINT_SUFFICIENCY_ARCHITECTURE":
    fail("ARCH02 design state")
if arch.get("candidate_design_only") is not True:
    fail("ARCH02 must remain design-only")
if arch.get("canonical_state_gate_admitted") is not False or arch.get("production_implemented") is not False:
    fail("ARCH02 authority overclaim")
decisions=arch.get("architecture_decisions",[])
if "portable checkpoints are created only at accepted transaction boundaries" not in decisions:
    fail("ARCH02 accepted-boundary rule missing")

gov=show_json(GOV04,"integration/animo-governance/ANIMO-GOV04_STATUS.json")
if "D" not in gov.get("policy",{}).get("risk_tiers",[]):
    fail("Tier D missing")

mod=(R/"prototype/kt16/mod_animo_accepted_application_checkpoint.f90").read_text()
for required in [
    "ANIMO_KT16_ACCEPTED_APPLICATION_CHECKPOINT_V1",
    "ACCEPTED_BOUNDARY_ONLY",
    "ANIMO_TCD042_TOP_STATE_V1",
    "type(kt15_application_config_t) :: config",
    "type(composite_accepted_continuation_t) :: continuation",
    "integer(int64) :: generation",
    "type(TimeCoordinate) :: accepted_time",
    "integer :: layer_count",
    "real(real64) :: tcd042_concentration",
    "call validate_kt15_application_state(state",
    "call snapshot_kt15_application_config(state",
    "call snapshot_kt15_continuation(state",
    "call snapshot_kt15_science_payload(state",
    "call validate_kt16_application_checkpoint(checkpoint",
    "same_kt15_application_config(checkpoint%config, expected_config)",
    "call reconstruct_accepted_store_trusted(checkpoint%lineage_id, checkpoint%generation",
    "call initialize_kt15_application_state(store, checkpoint%continuation, checkpoint%config"
]:
    if required not in mod:
        fail("checkpoint implementation drift "+required)

for forbidden in [
    "open(unit",
    "open(",
    "write(unit",
    "read(unit",
    "sha256sum",
    "hashlib",
    "openssl",
    "trial_state",
    "trial_scratch",
    "transfer_journal"
]:
    if forbidden.lower() in mod.lower():
        fail("forbidden checkpoint scope "+forbidden)

# Internal manifest/continuation coherence must be checked before trusted reconstruction.
for required in [
    "KT16_LINEAGE_CONTINUATION_MISMATCH",
    "KT16_GENERATION_CONTINUATION_MISMATCH",
    "KT16_TIME_CONTINUATION_MISMATCH",
    "KT16_LAYER_COUNT_CONTINUATION_MISMATCH",
    "KT16_EXPECTED_CONFIG_MISMATCH"
]:
    if required not in mod:
        fail("fail-closed checkpoint coherence missing "+required)

test=(R/"tests/kt16/test_kt16_accepted_application_checkpoint.f90").read_text()
for required in [
    "test_split_run_matches_uninterrupted_exactly",
    "test_corrupt_checkpoint_rejected",
    "test_wrong_expected_config_rejected",
    "encode_kt16_application_checkpoint",
    "restore_kt16_application_checkpoint",
    "final science exact split-run",
    "continuation generation exact",
    "Runinu exact",
    "cursor slot exact",
    "final config exact split-run",
    "trial-like checkpoint rejected",
    "generation corruption rejected",
    "lineage corruption rejected",
    "accepted-time corruption rejected",
    "geometry extent corruption rejected",
    "wrong expected config rejected"
]:
    if required not in test:
        fail("checkpoint test coverage drift "+required)

allowed_prefixes=("prototype/kt16/","tests/kt16/","docs/kt16/","integration/animo-kt16/")
allowed_exact={
    ".github/workflows/animo-kt16-accepted-application-checkpoint.yml",
    "tools/validate_kt16_accepted_application_checkpoint.py"
}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("scope escape "+path)

for k,v in st.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard boundary "+k)

if st.get("state")=="NOT_YET_QUALIFIED":
    if st.get("work_status",{}).get("qualified") is not False:
        fail("qualified too early")
    print("PASS_KT16_AUTHORING")
elif st.get("state")=="QUALIFIED_ACCEPTED_APPLICATION_CHECKPOINT_SPLIT_RUN_RESTART_TIER_D_REVIEW_REQUIRED":
    rv=load("integration/animo-kt16/ANIMO-KT16_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" or rv.get("genuinely_independent") is not False:
        fail("review assurance")
    for field in [
        "accepted_boundary_checkpoint_qualified",
        "typed_checkpoint_record_qualified",
        "trusted_restore_path_qualified",
        "exact_split_run_equivalence_qualified",
        "corrupt_checkpoint_rejection_qualified",
        "expected_config_restore_binding_qualified"
    ]:
        if st.get(field) is not True:
            fail("qualification flag "+field)
    for field in [
        "file_format_qualified","integrity_hash_qualified","canonical_checkpoint_admitted",
        "canonical_state_admitted","historical_b2_restart_equivalence_claimed",
        "independent_review_completed","production_authorized"
    ]:
        if st.get(field) is not False:
            fail("overclaim "+field)
    print("PASS_KT16_QUALIFIED_ACCEPTED_APPLICATION_RESTART")
else:
    fail("unexpected state")
