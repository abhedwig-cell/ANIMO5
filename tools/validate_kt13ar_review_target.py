#!/usr/bin/env python3
import json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
TARGET="df2310cc69e3fe16187ba2235843222f8acfb726"

def fail(msg):
    print("KT13AR FAIL_CLOSED:",msg)
    raise SystemExit(1)

def show_blob(sha,path):
    raw=subprocess.check_output(["git","show",f"{sha}:{path}"],cwd=R)
    p=subprocess.run(["git","hash-object","--stdin"],cwd=R,input=raw,stdout=subprocess.PIPE,check=True)
    return p.stdout.decode().strip()

st=json.loads((R/"integration/animo-kt13ar/ANIMO-KT13AR_STATUS.json").read_text())

pins={
 "prototype/kt13/mod_animo_tcd042_bounded_composition.f90":"6e2e4c73e9b43f5d1bda58dc9387a56be8b2e2b1",
 "tests/kt13/test_kt13_bounded_composition.f90":"66d74245497b4d93428fdb4f16476b0778e2c037",
 "integration/animo-kt13a/ANIMO-KT13A_STATUS.json":"6ae35bb08fad72c1dd49e6460daaee4ce2cce885",
 "integration/animo-kt13a/KT13A_INDEPENDENT_REVIEW_HANDOFF.json":"3312bc9eb30d5e94cc3accf0a686dd2855b807f9",
 "integration/animo-kt13a/KT13A_MATERIAL_FINDING_F01.json":"bead06a31801c7516154aa274bd2bfd07171d31e"
}
for path,expected in pins.items():
    if show_blob(TARGET,path)!=expected:
        fail("review target drift "+path)

allowed_prefixes=("docs/kt13ar/","integration/animo-kt13ar/")
allowed_exact={
 ".github/workflows/animo-kt13ar-independent-review.yml",
 "tools/validate_kt13ar_review_target.py"
}
changed=subprocess.check_output(["git","diff","--name-only",TARGET+"..HEAD"],cwd=R,text=True).splitlines()
for path in changed:
    if path in allowed_exact or path.startswith(allowed_prefixes):
        continue
    fail("review branch modifies authoring target: "+path)

for k,v in st.get("admission",{}).items():
    if v is not False:
        fail("review scaffold/adjudication attempted admission: "+k)
for k,v in st.get("hard_boundaries",{}).items():
    if v is not False:
        fail("hard-boundary overclaim: "+k)

axes=st.get("review_axes",{})
if not axes:
    fail("no review axes")

state=st.get("state")
if state=="AWAITING_GENUINELY_INDEPENDENT_TIER_D_REVIEW":
    if st.get("outcome") is not None:
        fail("awaiting state with outcome")
    if st.get("independence",{}).get("genuinely_independent") is not False:
        fail("independence prematurely satisfied")
    if any(v!="NOT_REVIEWED" for v in axes.values()):
        fail("review axis dispositioned in awaiting scaffold")
    if (R/"integration/animo-kt13ar/ANIMO-KT13AR_INDEPENDENT_REVIEW.json").exists():
        fail("independent review artifact exists while status says awaiting")
    print("PASS_KT13AR_REVIEW_SCAFFOLD")
elif state in {
    "INDEPENDENT_TIER_D_REVIEW_PASS",
    "INDEPENDENT_TIER_D_REVIEW_FAIL",
    "INDEPENDENT_TIER_D_REVIEW_INCOMPLETE"
}:
    p=R/"integration/animo-kt13ar/ANIMO-KT13AR_INDEPENDENT_REVIEW.json"
    if not p.exists():
        fail("completed review missing artifact")
    rv=json.loads(p.read_text())
    att=rv.get("independence_attestation",{})
    if att.get("genuinely_independent") is not True or att.get("same_authoring_context") is not False:
        fail("independence attestation")
    if rv.get("review_target_head")!=TARGET:
        fail("reviewed wrong target")
    outcome=rv.get("outcome")
    expected={
      "INDEPENDENT_TIER_D_REVIEW_PASS":"PASS",
      "INDEPENDENT_TIER_D_REVIEW_FAIL":"FAIL",
      "INDEPENDENT_TIER_D_REVIEW_INCOMPLETE":"INCOMPLETE"
    }[state]
    if outcome!=expected:
        fail("state/outcome mismatch")
    allowed={"PASS","FAIL","INCOMPLETE"}
    if set(axes.values())-allowed:
        fail("invalid review-axis result")
    if outcome=="PASS":
        if any(v!="PASS" for v in axes.values()):
            fail("PASS with non-PASS axis")
        if rv.get("unresolved_material_findings"):
            fail("PASS with unresolved material findings")
    print("PASS_KT13AR_REVIEW_RECORD_STRUCTURE_"+outcome)
else:
    fail("unexpected review state")
