#!/usr/bin/env python3
import json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE="872c78b6c020086280e31e1d9a7408e8b5a1afc7"
RG05J="624bbad35add93de29ac89649155d9fa086a73af"
B3I07="54679c7555a963133dfd686648af334f479c5808"
PRED="for every active D: (I intersection S_D is empty) OR (S_D subset_of I)"
def fail(m): print("B3I08 FAIL_CLOSED:",m); raise SystemExit(1)
def load(p):
    q=ROOT/p
    if not q.exists(): fail("missing "+p)
    return json.loads(q.read_text())
def git_json(sha,p):
    try: t=subprocess.check_output(["git","show",f"{sha}:{p}"],cwd=ROOT,text=True)
    except subprocess.CalledProcessError: fail(f"cannot read {sha}:{p}")
    return json.loads(t)
r=load("integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json")
s=load("integration/animo-b3/ANIMO-B3I08_STATUS.json")
b3a10=load("integration/animo-b3/ANIMO-B3A10_STATUS.json")
c=load("integration/animo-b3/TCD025_RESTRICTED_CORRECTION_CONTRACT.json")
if b3a10.get("decision") != "QUALIFIED_TCD025_RESTRICTED_LEDGER_CORRECTION_READY_FOR_SEPARATE_SCOPED_ADMISSION_WORKUNIT_PARENT_SCOPE_BLOCKED" or b3a10.get("qualified") is not True: fail("B3A10 authority mismatch")
if b3a10.get("parent_tcd025_admission_ready") is not False: fail("B3A10 parent boundary lost")
if c.get("interval_gate",{}).get("required_expression") != PRED or c.get("interval_gate",{}).get("partial_cut") != "FORBIDDEN_NOT_SOURCE_CLOSED": fail("B3A10 predicate mismatch")
old=git_json(B3I07,"integration/animo-b3/ANIMO-B3I07_STATUS.json")
if old.get("status") != "QUALIFIED_TCD037_CANONICAL_CHILD_ROUTING_TIER_A_CANDIDATES_NO_ADMISSION": fail("B3I07 authority mismatch")
if old.get("intake",{}).get("canonical_register_tail_after_work") != "TCD-042": fail("canonical tail mismatch")
if r.get("base_authority") != "ANIMO-B3A10@"+BASE or r.get("aggregate_authority") != "ANIMO-RG05J@"+RG05J: fail("base authority mismatch")
if r.get("prior_routing_authority") != "ANIMO-B3I07@"+B3I07: fail("routing authority mismatch")
if r.get("boundary_predicate") != PRED: fail("routing widened predicate")
children=r.get("children",[]); ids=[x.get("id") for x in children]
if ids != ["TCD-025-A1","TCD-025-A2","TCD-025-A3","TCD-025-A4","TCD-025-A5"]: fail("child identity/order mismatch")
for x in children[:4]:
    if x.get("kind") != "BOUNDED_CHILD_CORRECTION" or x.get("admission_candidate") is not True: fail("A1-A4 not bounded candidates")
    if x.get("risk_tier") != "C_STATE_OR_CONTROL_VOLUME_SEMANTICS": fail("A1-A4 risk tier mismatch")
    if x.get("scope_expansion_allowed") is not False: fail("child scope expansion allowed")
    if x.get("shared_readiness_authority") != "ANIMO-B3A10@"+BASE: fail("child readiness pin mismatch")
a5=children[4]
if a5.get("kind") != "UNRESOLVED_PARENT_SCOPE_BLOCKER" or a5.get("admission_candidate") is not False or a5.get("state") != "BLOCKED_NOT_SOURCE_CLOSED": fail("A5 blocker mismatch")
if r.get("parent",{}).get("admitted") is not False or r.get("parent",{}).get("automatic_admission_from_A1_A4_forbidden") is not True or r.get("parent",{}).get("A5_disposition_required_before_parent_completion") is not True: fail("parent guard mismatch")
reg=r.get("canonical_register",{})
if reg.get("new_top_level_tcd_reserved") is not False or reg.get("canonical_register_modified") is not False or reg.get("tail_remains") != "TCD-042": fail("canonical register boundary mismatch")
if s.get("parent_admitted") is not False or s.get("child_admission_count") != 0 or s.get("new_top_level_tcd_reserved") is not False: fail("status admission boundary mismatch")
allowed={".github/workflows/animo-b3i08-tcd025-routing.yml","docs/b3i08/TCD025_CHILD_SCOPE_ROUTING.md","integration/animo-b3/B3I08_TCD025_CHILD_ROUTING.json","integration/animo-b3/ANIMO-B3I08_STATUS.json","tools/validate_b3i08_tcd025_routing.py"}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"..HEAD"],cwd=ROOT,text=True).splitlines()
extra=sorted(set(changed)-allowed)
if extra: fail("scope escape: "+", ".join(extra))
for p in changed:
    if p.startswith("src/") or p.startswith("reference/"): fail("forbidden source/reference change")
if s.get("work_status",{}).get("qualified") is True:
    if s.get("status") != "QUALIFIED_TCD025_CHILD_SCOPE_PARTITION_A1_A4_BOUNDED_A5_BLOCKED_NO_ADMISSION": fail("final status mismatch")
    print("B3I08 PASS qualified child routing; A1-A4 bounded, A5 blocked, no admission")
else:
    print("B3I08 PASS persisted routing candidate; final closeout pending")
