#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="bc9e6ed997a078336645210ebb4d99ae976893fe"
PREV="997d867a2b107ec8e28efce530c82a204719de46"
B3Q01="846e0f4d02a38b9e02cc1419b1ca87e63aaedb54"
B3I10="942f26fe32eaf91679e59a1968ae173a3703e22d"
ASSURANCE="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT_LOWER_THAN_GOV04_SEPARATE_CONTEXT"
RECOMP=R/"integration/animo-b3/ANIMO-B3Q06_GLOBAL_QUEUE_RECOMPUTE.json"
PINS=R/"integration/animo-b3/ANIMO-B3Q06_SOURCE_PINS.json"
FREEZE=R/"integration/animo-b3/ANIMO-B3Q06_AUTHORING_FREEZE.json"
REVIEW=R/"integration/animo-b3/ANIMO-B3Q06_INTERNAL_ADVERSARIAL_REVIEW.json"
STATUS=R/"integration/animo-b3/ANIMO-B3Q06_STATUS.json"
ALLOWED={".github/workflows/animo-b3q06-global-queue-recompute.yml","integration/animo-b3/ANIMO-B3Q06_GLOBAL_QUEUE_RECOMPUTE.json","integration/animo-b3/ANIMO-B3Q06_SOURCE_PINS.json","integration/animo-b3/ANIMO-B3Q06_AUTHORING_FREEZE.json","integration/animo-b3/ANIMO-B3Q06_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3Q06_STATUS.json","tools/validate_animo_b3q06.py"}
def fail(m): raise SystemExit("ANIMO-B3Q06 validation failed: "+m)
def run(*a): return subprocess.run(a,cwd=R,check=True,text=True,capture_output=True).stdout
def load(p): return json.loads(p.read_text())
def gj(c,p): return json.loads(run("git","show",f"{c}:{p}"))
def gt(c,p): return run("git","show",f"{c}:{p}")
def req(x,m):
    if not x: fail(m)
for c in (BASE,PREV,B3Q01,B3I10): subprocess.run(["git","cat-file","-e",f"{c}^{{commit}}"],cwd=R,check=True)
changed={p for p in run("git","diff","--name-only",BASE+"..HEAD").splitlines() if p}
req(changed<=ALLOWED,"scope escape "+str(sorted(changed-ALLOWED)))
req(not any(p.startswith("src/") or p.startswith("reference/") or p.startswith("integration/animo-reg/") for p in changed),"source/reference/regie modified")
req("docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv" not in changed,"canonical TCD register modified")
pins=load(PINS); rec=load(RECOMP); fr=load(FREEZE); st=load(STATUS)
req(pins["base_authority"]["head"]==BASE and pins["base_authority"]["exact_final_ci_run"]==34687736122 and pins["base_authority"]["exact_final_ci_conclusion"]=="success","RG05O pin")
req(pins["previous_queue_authority"]["head"]==PREV and pins["previous_queue_authority"]["exact_final_ci_run"]==34654186685 and pins["previous_queue_authority"]["exact_final_ci_conclusion"]=="success","B3Q05 pin")
req(pins["assurance"]==ASSURANCE,"pin assurance")
live=pins["live_recheck"]
req(live["rg05o_b3_complete"] is False and live["rg05o_b4_open"] is False and live["rg05o_production_open"] is False,"live project gate")
req(live["rg05o_scientific_admissions"]==32 and live["rg05o_top_level_admitted"]==22 and live["rg05o_admitted_child_atoms"]==10,"live RG05O counts")
req(live["canonical_top_level_count"]==25 and live["canonical_tail"]=="TCD-042" and live["newer_top_level_tcd_reservation_found"] is False,"canonical live pins")
req(fr["base_head"]==BASE and fr["review_must_pin_exact_commit"] is True and fr["substantive_change_resets_GOV05_review"] is True,"freeze contract")
rg=gj(BASE,"integration/animo-reg/ANIMO-RG05O_STATUS.json")
req(rg["state"]=="QUALIFIED_NINTH_BATCHED_B3_ADMISSION_INTEGRATION_TCD033_TCD032_TCD019_NO_PRODUCTION","RG05O state")
req(rg["scientific_admission_count"]==32 and rg["historical_uncertainty_admission_count"]==32 and rg["top_level_admitted_tcd_count"]==22 and rg["admitted_child_atom_count"]==10,"RG05O counts")
req(rg["current_queue_authority"]=="ANIMO-B3Q05@"+PREV,"RG05O prior queue pin")
req(rg["tcd033_state"]["top_level_admitted"] is True and rg["tcd032_state"]["top_level_admitted"] is True and rg["tcd019_state"]["top_level_admitted"] is True,"RG05O integrated admissions")
req(rg["tcd019_state"]["legacy_fallback_admitted"] is False,"TCD019 fallback boundary")
req(rg["b3_complete"] is False and rg["b4_open"] is False and rg["production_open"] is False,"RG05O downstream gate")
prev=gj(PREV,"integration/animo-b3/ANIMO-B3Q05_GLOBAL_QUEUE_RECOMPUTE.json")
req(prev["counts"]=={"canonical_top_level_queue":25,"admitted_top_level":19,"unadmitted_top_level":6,"admitted_child_atoms":10,"scientific_admission_objects":29},"B3Q05 counts")
req(prev["closure_result"]["global_canonical_b3_queue_closed"] is False,"B3Q05 closure state")
queue=gj(BASE,"integration/animo-reg/RG05_B3_QUEUE.json")
ids=[x["tcd"] for x in queue["entries"]]
req(len(ids)==25 and len(set(ids))==25,"canonical queue membership")
req(queue["canonical_register"]["tail"]=="TCD-042" and queue["canonical_register"]["tcd_043_reserved"] is False,"canonical queue tail")
expected_admitted=set(prev["admitted_top_level_at_RG05N"])|{"TCD-019","TCD-032","TCD-033"}
expected_unadmitted=set(ids)-expected_admitted
req(len(expected_admitted)==22 and len(expected_unadmitted)==3,"derived queue counts")
req(expected_unadmitted=={"TCD-016","TCD-034","TCD-040"},"derived remaining set")
req(set(rec["canonical_top_level_queue"])==set(ids),"recomputed canonical membership")
req(set(rec["admitted_top_level_at_RG05O"])==expected_admitted,"admitted set")
req({x["tcd"] for x in rec["unadmitted_top_level_at_RG05O"]}==expected_unadmitted,"unadmitted set")
req(set(rec["newly_admitted_top_level_since_B3Q05"])=={"TCD-019","TCD-032","TCD-033"},"new top-level delta")
req(rec["newly_admitted_child_atoms_since_B3Q05"]==[],"unexpected child delta")
req(rec["counts"]=={"canonical_top_level_queue":25,"admitted_top_level":22,"unadmitted_top_level":3,"admitted_child_atoms":10,"scientific_admission_objects":32},"recompute counts")
req(all(x["last_queue_state_revalidated_here"] is False for x in rec["unadmitted_top_level_at_RG05O"]),"remaining states requalified here")
rules=gt(B3Q01,"docs/governance/B3_COMPOSITION_RULES.md")
req("If one required component is not admitted, the composition is not admitted." in rules,"B3Q01 component rule")
req("all component records are admitted and immutable by identity" in rules,"B3Q01 composition rule")
route=gj(B3I10,"integration/animo-b3/ANIMO-B3I10_STATUS.json")
req(route.get("qualified") is True and route.get("scientific_admission") is False,"B3I10 state")
cl=rec["closure_result"]
req(cl["global_canonical_b3_queue_closed"] is False and cl["whole_b3_composition_precondition_met"] is False and cl["positive_b3_composition_completeness_authority_allowed"] is False,"negative closure")
req(cl["tb7_allowed"] is False and cl["b4_allowed"] is False and cl["production_allowed"] is False,"downstream forbidden")
req(cl["blocker"]=="THREE_CANONICAL_TOP_LEVEL_B3_QUEUE_OBJECTS_REMAIN_UNADMITTED_AT_RG05O","blocker")
req(all(v is False for v in rec["hard_boundaries"].values()),"recompute hard boundary")
req(st["current_aggregate_authority"]=="ANIMO-RG05O@"+BASE,"status aggregate")
req(st["canonical_queue"]=={"top_level_objects":25,"tail":"TCD-042","tcd043_reserved":False,"admitted_top_level":22,"unadmitted_top_level":3,"admitted_child_atoms":10,"scientific_admission_objects":32},"status queue")
req(set(st["unadmitted_top_level"])==expected_unadmitted,"status unadmitted")
req(st["global_canonical_b3_queue_closed"] is False and st["whole_b3_composition_complete"] is False and st["tb7_allowed"] is False and st["b4_allowed"] is False and st["production_allowed"] is False,"status negative gate")
req(st["registry_or_queue_modified"] is False and all(v is False for v in st["hard_boundaries"].values()),"status boundaries")
req(st["assurance"]==ASSURANCE and st["review"]["assurance"]==ASSURANCE,"status assurance")
if REVIEW.exists():
    rv=load(REVIEW); h=rv.get("reviewed_head")
    req(rv.get("model")=="MANDATORY_SINGLE_AGENT_ADVERSARIAL_REVIEW" and rv.get("same_agent") is True and rv.get("genuinely_independent") is False and rv.get("independence_claimed") is False,"review model")
    req(rv.get("assurance")==ASSURANCE and rv.get("outcome")=="SELF_REVIEW_PASS_NEGATIVE_B3_CLOSURE_GATE_THREE_TOP_LEVEL_UNADMITTED","review outcome")
    req(bool(h) and rv.get("reviewed_head_ci_conclusion")=="success" and rv.get("reviewed_head_ci_run") and rv.get("reviewed_head_ci_job"),"reviewed-head CI")
    post=set(run("git","diff","--name-only",h+"..HEAD").splitlines())
    req(post<={"integration/animo-b3/ANIMO-B3Q06_INTERNAL_ADVERSARIAL_REVIEW.json","integration/animo-b3/ANIMO-B3Q06_STATUS.json"},"post-review substantive change")
    req(st["state"]=="QUALIFIED_ANIMO_B3Q06_GLOBAL_QUEUE_RECOMPUTE_BLOCKED_THREE_TOP_LEVEL_UNADMITTED","final state")
    req(st["decision"]=="B3_COMPOSITION_INCOMPLETE_DO_NOT_OPEN_TB7_B4_OR_PRODUCTION","final decision")
    req(st["work_status"]=={"realized":True,"persisted":True,"tested":True,"reviewed":True,"qualified":True,"work_unit_complete":True},"final work status")
    req(st["review"]["completed"] is True and st["review"]["genuinely_independent"] is False,"final review status")
    print("ANIMO-B3Q06 PASS final negative closure gate; three top-level objects remain")
else:
    req(st["phase"]=="AUTHORING_FROZEN_PENDING_GOV05_ADVERSARIAL_REVIEW" and st["state"]=="CANDIDATE_NEGATIVE_CLOSURE_GATE_PENDING_REVIEW","candidate state")
    req(st["work_status"]["qualified"] is False and st["review"]["completed"] is False,"candidate not prematurely qualified")
    print("ANIMO-B3Q06 PASS frozen candidate pending GOV05 adversarial review")
