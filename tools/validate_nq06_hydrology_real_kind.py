#!/usr/bin/env python3
import csv, json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parents[1]
BASE="56b041ddb30b65fe1e77540dbbc36400ee49b1b1"
NQ01_BRANCH="work/animo-nq01-numerical-qualification-architecture"

def fail(msg):
    print("NQ06 FAIL_CLOSED:",msg)
    raise SystemExit(1)
def load(path):
    return json.loads((R/path).read_text())

st=load("integration/animo-numerics/ANIMO-NQ06_STATUS.json")
ev=load("integration/animo-numerics/NQ06_REV53_BUILD_PRECISION_EVIDENCE.json")

if ev.get("evidence_role")!="USER_SUPPLIED_BUILD_METADATA_PLUS_FROZEN_SOURCE_DECLARATION_EVIDENCE_NOT_B2":
    fail("evidence role")
vf=ev.get("supplied_artifacts",{}).get("vfproj",{})
if vf.get("sha256")!="f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a":
    fail("vfproj hash")
if vf.get("copied_into_repository") is not False:
    fail("vfproj must not be vendored")
exe=ev.get("supplied_artifacts",{}).get("executable",{})
if exe.get("sha256")!="40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d":
    fail("exe hash")
if exe.get("role")!="SUPPORTING_LINEAGE_ONLY_NOT_PROOF_OF_EXACT_PROJECT_OPTIONS":
    fail("exe evidential role")

cfg=ev.get("vfproj_configurations",[])
if len(cfg)!=4:
    fail("configuration count")
expected_names={"Debug|Win32","Release|Win32","Debug|x64","Release|x64"}
if {x.get("name") for x in cfg}!=expected_names:
    fail("configuration identities")
for x in cfg:
    if x.get("RealKIND")!="realKIND8":
        fail("non-kind8 config "+str(x.get("name")))
    if x.get("FloatingPointModel")!="source":
        fail("non-source fp model "+str(x.get("name")))

inf=ev.get("inference",{})
if inf.get("source_default_real_kind_under_supplied_project_configuration")!="REAL_KIND_8":
    fail("precision inference")
if inf.get("prototype_precision_candidate")!="IEEE_BINARY64_OR_COMPILER_REAL_KIND_8_EQUIVALENT":
    fail("prototype candidate")
if inf.get("historical_executable_equivalence_proven") is not False:
    fail("historical equivalence overclaim")
if inf.get("B2_created") is not False:
    fail("B2 overclaim")

manifest={}
with (R/"reference/source/source_manifest.csv").open(newline="") as fh:
    rd=csv.reader(fh)
    for row in rd:
        if len(row)>=4:
            manifest[row[0]]=row[3]
pins={
 "ANIMO_4.1.5.53/Hydro_detailed.for":"f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d",
 "ANIMO_4.1.5.53/MODFLUX.FOR":"0c0909922e88ee59233cabc307fb18243ea86023b4722879f6301259780de93d",
 "ANIMO_4.1.5.53/UBoundconc.for":"b9a7ec980d40c0f76279077852190788e36cd976d185b12683a38da0c7dfecf7"
}
for path,sha in pins.items():
    if manifest.get(path)!=sha:
        fail("source manifest pin "+path)

allowed_prefixes=("docs/numerics/ANIMO_NQ06_","integration/animo-numerics/NQ06_","tools/nq06/")
allowed_exact={
 "integration/animo-numerics/ANIMO-NQ06_STATUS.json",
 ".github/workflows/animo-nq06-hydrology-real-kind.yml",
 "tools/validate_nq06_hydrology_real_kind.py"
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
    print("PASS_NQ06_AUTHORING")
elif st.get("state")=="QUALIFIED_REV53_BUILD_METADATA_REAL_KIND8_FOR_BOUNDED_HYDROLOGY_PROTOTYPES_NO_B2_EQUIVALENCE":
    rv=load("integration/animo-numerics/ANIMO-NQ06_ADVERSARIAL_REVIEW.json")
    if rv.get("outcome")!="SELF_REVIEW_PASS":
        fail("review outcome")
    if rv.get("assurance")!="PROCESS_SELF_REVIEWED_NOT_INDEPENDENT":
        fail("review assurance")
    if st.get("selected_bounded_candidate_precision")!="real64":
        fail("selected precision")
    if st.get("historical_numerical_equivalence") is not False or st.get("b2_created") is not False:
        fail("historical overclaim")
    print("PASS_NQ06_QUALIFIED_BUILD_METADATA_PRECISION")
else:
    fail("unexpected status")
