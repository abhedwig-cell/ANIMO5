#!/usr/bin/env python3
import json, math, subprocess
from pathlib import Path

BASE="97913b04906eb23c28b47a68ec9def7392174be5"
EXPECTED="QUALIFIED_TCD034_SELECTOR_SENSITIVITY_AND_PARAMETER_NONTRANSFERABILITY_RISK_V1"
ALLOWED=(
 ".github/workflows/animo-ghg09-tcd034.yml",
 "docs/ghg/TCD034_SELECTOR_SENSITIVITY_PARAMETER_TRANSFER.md",
 "integration/animo-ghg/GHG09_TCD034_SELECTOR_SENSITIVITY_CONTRACT.json",
 "integration/animo-ghg/GHG09_TCD034_SELECTOR_SENSITIVITY_ORACLES.json",
 "integration/animo-ghg/ANIMO-GHG09_AUTHORING_FREEZE.json",
 "integration/animo-ghg/ANIMO-GHG09_INTERNAL_ADVERSARIAL_REVIEW.json",
 "integration/animo-ghg/ANIMO-GHG09_STATUS.json",
 "tools/ghg09/",
)

def j(p): return json.loads(Path(p).read_text())
def growth(T,Tgr):
    Tmat=Tgr+10.0
    if T<=Tgr: return 0.0
    if T<Tmat: return 4.0*(1.0-((Tmat-T)/10.0)**2)
    return 4.0

def changed():
    out=subprocess.check_output(["git","diff","--name-only",f"{BASE}..HEAD"],text=True)
    return [x for x in out.splitlines() if x]
def allowed(p): return any(p==q or (q.endswith('/') and p.startswith(q)) for q in ALLOWED)

def main():
    c=j("integration/animo-ghg/GHG09_TCD034_SELECTOR_SENSITIVITY_CONTRACT.json")
    o=j("integration/animo-ghg/GHG09_TCD034_SELECTOR_SENSITIVITY_ORACLES.json")
    f=j("integration/animo-ghg/ANIMO-GHG09_AUTHORING_FREEZE.json")
    s=j("integration/animo-ghg/ANIMO-GHG09_STATUS.json")
    p=j("integration/animo-ghg/ANIMO-GHG08_STATUS.json")
    assert c["work_unit"]==o["work_unit"]==f["work_unit"]==s["work_unit"]=="ANIMO-GHG09"
    assert f["base_head"]==BASE
    assert c["predecessor"]==s["base_predecessor"]==f"ANIMO-GHG08@{BASE}"
    assert p["state"]=="QUALIFIED_NEGATIVE_TCD034_PARENT_READINESS_NO_ADMISSION"
    assert c["decision"]==EXPECTED
    assert c["growth_response"]["global_lipschitz_per_degC"]==0.8
    assert c["frozen_Kpl_d_minus_1"]==0.24
    assert c["parameter_transfer"]["Kpl_Fveg_global_scaling"]=="NOT_GENERALLY_TRANSFERABLE"
    assert c["parameter_transfer"]["Tegr_adjustment"]=="SEMANTIC_CHANGE_NOT_NEUTRAL_RECALIBRATION"
    assert c["parameter_transfer"]["PvCH4Ox"]=="PARTITION_ONLY_CANNOT_COMPENSATE_TOTAL_QPLANT"
    assert c["b3_admission_performed"] is False and c["class_f_admission_performed"] is False and c["production_authorized"] is False
    for case in o["cases"]:
        go=growth(case["T_old"],case["Tegr"]); gn=growth(case["T_new"],case["Tegr"])
        if "expected_g_old" in case: assert math.isclose(go,case["expected_g_old"],abs_tol=1e-12)
        if "expected_g_new" in case: assert math.isclose(gn,case["expected_g_new"],abs_tol=1e-12)
        if "expected_scale" in case: assert math.isclose(go/gn,case["expected_scale"],abs_tol=1e-12)
        if "expected_ratio_old_over_new" in case: assert math.isclose(go/gn,case["expected_ratio_old_over_new"],abs_tol=1e-12)
    # Global Lipschitz check on a dense deterministic grid spanning all branches.
    vals=[-10.0+i*0.05 for i in range(1001)]
    for a,b in zip(vals,vals[1:]):
        assert abs(growth(a,7.0)-growth(b,7.0)) <= 0.8*abs(a-b)+1e-12
    # Demonstrate non-universal multiplicative compensation.
    ca=next(x for x in o["cases"] if x["id"]=="GHG09-O05-NONUNIVERSAL-MULTIPLIER-A")
    cb=next(x for x in o["cases"] if x["id"]=="GHG09-O06-NONUNIVERSAL-MULTIPLIER-B")
    sa=growth(ca["T_old"],ca["Tegr"])/growth(ca["T_new"],ca["Tegr"])
    sb=growth(cb["T_old"],cb["Tegr"])/growth(cb["T_new"],cb["Tegr"])
    assert not math.isclose(sa,sb,rel_tol=0.0,abs_tol=1e-6)
    assert s["analytic_sensitivity_qualified"] is True
    assert s["application_envelope_difference"]=="OPEN_REQUIRES_REPRESENTATIVE_SELECTOR_REPLAY"
    assert all(v is False for v in s["hard_boundaries"].values())
    bad=[x for x in changed() if not allowed(x)]
    assert not bad,bad
    rp=Path("integration/animo-ghg/ANIMO-GHG09_INTERNAL_ADVERSARIAL_REVIEW.json")
    if rp.exists():
        r=j(rp)
        assert r["same_agent"] is True and r["genuinely_independent"] is False and r["independence_claimed"] is False
        assert r["decision"]=="PASS_TCD034_SELECTOR_SENSITIVITY_PARAMETER_TRANSFER_V1"
        assert r["gates"]["lipschitz_bound"]=="PASS"
        assert r["gates"]["nontransferability_not_overclaimed"]=="PASS"
        assert s["review"]["completed"] is True
        assert s["work_status"]["qualified"] is True and s["work_status"]["workunit_complete"] is True
        assert s["state"]=="QUALIFIED_SELECTOR_SENSITIVITY_PARAMETER_TRANSFER_NO_ADMISSION"
        assert s["primary_disposition"]==EXPECTED
    print("GHG09 TCD034 selector sensitivity and parameter-transfer validation PASS")

if __name__=="__main__": main()
