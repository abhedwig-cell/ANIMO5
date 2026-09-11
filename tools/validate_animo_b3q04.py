#!/usr/bin/env python3
import json,subprocess
from pathlib import Path
BASE="7146612d5dfa8ad87a4660f0c50c68a5db1e3a29"
PREV="67a87c6a650d503c1b0968ada2cc5eaa5155aa42"
B3Q01="846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
ROOT=Path(__file__).resolve().parents[1]
RECOMP=ROOT/"integration/animo-b3/ANIMO-B3Q04_GLOBAL_QUEUE_RECOMPUTE.json"
PINS=ROOT/"integration/animo-b3/ANIMO-B3Q04_SOURCE_PINS.json"
FREEZE=ROOT/"integration/animo-b3/ANIMO-B3Q04_AUTHORING_FREEZE.json"
REVIEW=ROOT/"integration/animo-b3/ANIMO-B3Q04_INTERNAL_ADVERSARIAL_REVIEW.json"
STATUS=ROOT/"integration/animo-b3/ANIMO-B3Q04_STATUS.json"
ALLOWED={
 ".github/workflows/animo-b3q04-global-queue-recompute.yml",
 "integration/animo-b3/ANIMO-B3Q04_GLOBAL_QUEUE_RECOMPUTE.json",
 "integration/animo-b3/ANIMO-B3Q04_SOURCE_PINS.json",
 "integration/animo-b3/ANIMO-B3Q04_AUTHORING_FREEZE.json",
 "integration/animo-b3/ANIMO-B3Q04_INTERNAL_ADVERSARIAL_REVIEW.json",
 "integration/animo-b3/ANIMO-B3Q04_STATUS.json",
 "tools/validate_animo_b3q04.py",
}
def fail(m): raise SystemExit("ANIMO-B3Q04 validation failed: "+m)
def run(*a): return subprocess.run(a,cwd=ROOT,check=True,text=True,capture_output=True).stdout
def load(p): return json.loads(p.read_text())
def gj(c,p): return json.loads(run("git","show",f"{c}:{p}"))
def gt(c,p): return run("git","show",f"{c}:{p}")
def req(x,m):
    if not x: fail(m)
for c in (BASE,PREV,B3Q01,B3I10): subprocess.run(["git","cat-file","-e",f"{c}^{{commit}}"],cwd=ROOT,check=True)
changed={p for p in run("git","diff","--name-only",BASE+"..HEAD").splitlines() if p}
req(changed<=ALLOWED,"scope escape "+str(sorted(changed-ALLOWED)))
req(not any(p.startswith("src/") or p.startswith("reference/") for p in changed),"source/reference modified")
req("integration/animo-reg/RG05_B3_QUEUE.json" not in changed,"canonical queue source modified")
req("docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" not in changed,"canonical TCD register modified")
pins=load(PINS); rec=load(RECOMP); fr=load(FREEZE); st=load(STATUS)
req(pins["base_authority"]["head"]==BASE and pins["base_authority"]["exact_final_ci_run"]==34610132079 and pins["base_authority"]["exact_final_ci_conclusion"]=="success","RG05M pin")
req(pins["previous_queue_authority"]["head"]==PREV and pins["previous_queue_authority"]["exact_final_ci_run"]==34590598874 and pins["previous_queue_authority"]["exact_final_ci_conclusion"]=="success","B3Q03 pin")
req(pins["assurance"]=="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT","pin assurance")
req(pins["live_recheck"]["rg05m_b3_complete"] is False and pins["live_recheck"]["rg05m_b4_open"] is False and pins["live_recheck"]["rg05m_production_open"] is False,"live project gate")
req(pins["live_recheck"]["newer_top_level_tcd_reservation_found"] is False,"later top-level reservation")
req(fr["base_head"]==BASE and fr["review_must_pin_exact_commit"] is True and fr["substantive_change_resets_GOV05_review"] is True,"freeze contract")
rg=gj(BASE,"integration/animo-reg/ANIMO-RG05M_STATUS.json")
req(rg["state"]=="QUALIFIED_SEVENTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD042_E1_PARENT_AND_TCD029_NO_PRODUCTION","RG05M state")
req(rg["scientific_admission_count"]==26 and rg["historical_uncertainty_admission_count"]==26 and rg["top_level_admitted_tcd_count"]==16 and rg["admitted_child_atom_count"]==10,"RG05M counts")
req(rg["tcd042_state"]["parent_admitted"] is True and rg["tcd042_state"]["Hetop_zero_admitted"] is False and rg["tcd042_state"]["outside_NQ03_envelope_admitted"] is False,"RG05M TCD042")
req(rg["tcd029_state"]["top_level_admitted"] is True and rg["tcd029_state"]["tcd019_modified_or_admitted"] is False,"RG05M TCD029")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False,"RG05M downstream gate")
prev=gj(PREV,"integration/animo-b3/ANIMO-B3Q03_GLOBAL_QUEUE_RECOMPUTE.json")
req(prev["counts"]=={"canonical_top_level_queue":25,"admitted_top_level":14,"unadmitted_top_level":11,"admitted_child_atoms":9,"scientific_admission_objects":23},"B3Q03 counts")
queue=gj(BASE,"integration/animo-reg/RG05_B3_QUEUE.json")
ids=[x["tcd"] for x in queue["entries"]]
req(len(ids)==25 and len(set(ids))==25,"canonical queue membership")
req(queue["canonical_register"]["tail"]=="TCD-042" and queue["canonical_register"]["tcd_043_reserved"] is False,"canonical queue tail")
expected_admitted=set(prev["admitted_top_level_at_RG05L"])|{"TCD-029","TCD-042"}
expected_unadmitted=set(ids)-expected_admitted
req(len(expected_admitted)==16 and len(expected_unadmitted)==9,"derived queue counts")
req(set(rec["canonical_top_level_queue"])==set(ids),"recomputed canonical membership")
req(set(rec["admitted_top_level_at_RG05M"])==expected_admitted,"admitted set")
req({x["tcd"] for x in rec["unadmitted_top_level_at_RG05M"]}==expected_unadmitted,"unadmitted set")
req(set(rec["newly_admitted_top_level_since_B3Q03"])=={"TCD-029","TCD-042"},"new top-level delta")
req(rec["newly_admitted_child_atoms_since_B3Q03"]==["TCD-042-E1"],"child delta")
req(rec["counts"]=={"canonical_top_level_queue":25,"admitted_top_level":16,"unadmitted_top_level":9,"admitted_child_atoms":10,"scientific_admission_objects":26},"recompute counts")
rules=gt(B3Q01,"docs/governance/B3_COMPOSITION_RULES.md")
req("If one required component is not admitted, the composition is not admitted." in rules,"B3Q01 component rule")
req("all component records are admitted and immutable by identity" in rules,"B3Q01 composition rule")
route=gj(B3I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
req(route.get("qualified") is True and route.get("scientific_admission") is False,"B3I10 state")
cl=rec["closure_result"]
req(cl["global_canonical_b3_queue_closed"] is False and cl["whole_b3_composition_precondition_met"] is False and cl["positive_b3_composition_completeness_authority_allowed"] is False,"negative closure")
req(cl["tb7_allowed"] is False and cl["b4_allowed"] is False and cl["production_allowed"] is False,"downstream forbidden")
req(cl["blocker"]=="NINE_CANONICAL_TOP_LEVEL_B3_QUEUE_OBJECTS_REMAIN_UNADMITTED_AT_RG05M","blocker")
req(all(v is False for v in rec["hard_boundaries"].values()),"recompute hard boundary")
req(st["current_aggregate_authority"]=="ANIMO-RG05M@"+BASE,"status aggregate")
req(st["canonical_queue"]["top_level_objects"]==25 and st["canonical_queue"]["admitted_top_level"]==16 and st["canonical_queue"]["unadmitted_top_level"]==9 and st["canonical_queue"]["admitted_child_atoms"]==10 and st["canonical_queue"]["scientific_admission_objects"]==26,"status counts")
req(set(st["unadmitted_top_level"])==expected_unadmitted,"status unadmitted")
req(st["global_canonical_b3_queue_closed"] is False and st["whole_b3_composition_complete"] is False and st["tb7_allowed"] is False and st["b4_allowed"] is False and st["production_allowed"] is False,"status negative gate")
req(st["registry_or_queue_modified"] is False and all(v is False for v in st["hard_boundaries"].values()),"status boundaries")
if REVIEW.exists():
    rv=load(REVIEW); h=rv.get("reviewed_head")
    req(rv.get("model")=="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" and rv.get("same_agent") is True and rv.get("genuinely_independent") is False and rv.get("independence_claimed") is False,"review model")
    req(rv.get("assurance")=="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT" and rv.get("outcome")=="SELF_REVIEW_PASS_NEGATIVE_B3_CLOSURE_GATE_NINE_TOP_LEVEL_UNADMITTED","review outcome")
    req(bool(h) and rv.get("reviewed_head_ci_conclusion")=="success" and rv.get("reviewed_head_ci_run"),"reviewed-head CI")
    post=run("git","diff","--name-only",h+"..HEAD").splitlines()
    req(not (set(post)-{"integration/animo-b3/ANIMO-B3Q04_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3Q04_STATUS.json"}),"post-review substantive change")
    req(st["state"]=="QUALIFIED_ANIMO_B3Q04_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_NINE_TOP_LEVEL_UNADMITTED","final state")
    req(st["decision"]=="B3_COMPOSITION_INCOMPLETE_DO_NOT_OPEN_TB7_B4_OR_PRODUCTION","final decision")
    req(st["work_status"]["tested"] is True and st["work_status"]["reviewed"] is True and st["work_status"]["qualified"] is True and st["work_status"]["work_unit_complete"] is True,"final work status")
    req(st["review"]["completed"] is True and st["review"]["genuinely_independent"] is False,"final review status")
    print("ANIMO-B3Q04 PASS final negative closure gate; nine top-level objects remain")
else:
    req(st["phase"]=="AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" and st["state"]=="CANDIDATE_NEGATIVE_CLOSURE_GATE_PENDING_REVIEW","candidate state")
    req(st["work_status"]["qualified"] is False and st["review"]["completed"] is False,"candidate not prematurely qualified")
    print("ANIMO-B3Q04 PASS frozen candidate pending GOV05 adversarial review")
