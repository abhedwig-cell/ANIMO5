#!/usr/bin/env python3
"""Independent exact-rational validator for ANIMO-SYNQ04 / TCD-037-A3."""
from __future__ import annotations
import json, subprocess, sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "0f85d7102945c7c4d77bc49885f9ecca688209e3"
RG05H = "3e4247928bb43f30def951fa8804560636affbef"
B3I07 = "54679c7555a963133dfd686648af334f479c5808"
RUNTIMEQ03 = "a3e822f8e97fe1312a7dfa73601a49ae7375163e"
SYNQ01 = "842f72300fd03ede0b9024537a7ee6126722a121"
GOV05 = "f65a47724e4a4fca7f2d8b8d6de9eeee51867904"
GOV04 = "1bbe4c211197590f346803106e45dca5faae79fc"
GOV03 = "cbd262bdabe92923113b7326f2f42822ce9a971c"

ORACLE = ROOT / "integration/animo-synthetic/SYNQ04_TCD037_A3_ORACLE.json"
STATUS = ROOT / "integration/animo-synthetic/ANIMO-SYNQ04_STATUS.json"

Z = Fraction(10000)
BASELINE = Fraction(100)
STATE = (Fraction(11), Fraction(22), Fraction(33))
FLUX = (Fraction(7), Fraction(13))
A1, A2, A4, OTHER = map(Fraction, (31, 41, 51, 77))
QPR = (Fraction(1,16384), Fraction(1,8192), Fraction(3,16384))
ZERO = (Fraction(0),)*3
HALF = tuple(x/2 for x in QPR)
PERM = (QPR[2], QPR[0], QPR[1])
CASES = {
    "ACTIVE_NONZERO": (True, QPR, Fraction(1,4)),
    "ZERO_DENI": (True, ZERO, Fraction(1,4)),
    "PERMUTED": (True, PERM, Fraction(1,4)),
    "RATE_TIME_EQUIVALENT": (True, HALF, Fraction(1,2)),
    "INACTIVE": (False, QPR, Fraction(1,4)),
}

def require(c,m):
    if not c: raise AssertionError(m)

def run(*args):
    return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True).stdout

def show_json(commit,path):
    return json.loads(run("git","show",f"{commit}:{path}"))

def exact(actual, expected, label):
    ef=float(expected)
    require(actual == ef, f"{label}: expected {ef.hex()}, got {actual.hex()}")

def expected(active,qpr,st):
    if not active:
        return (BASELINE,)*3
    return tuple(BASELINE + Z*q*st for q in qpr)

def parse(path):
    rows={}
    for raw in Path(path).read_text().splitlines():
        if not raw.strip(): continue
        p=raw.split()
        require(len(p)==17, f"bad row shape {len(p)}: {raw}")
        require(p[0] in CASES and p[0] not in rows, f"bad case {p[0]}")
        rows[p[0]]=tuple(float(x.replace("D","E")) for x in p[1:])
    require(set(rows)==set(CASES), f"case set mismatch {rows.keys()}")
    return rows

def validate_probe(rows):
    for case,(active,qpr,st) in CASES.items():
        v=rows[case]
        for i,q in enumerate(qpr): exact(v[i],q,f"{case}/QPrN2Oden[{i+1}]")
        exact(v[3],st,f"{case}/St")
        exp=expected(active,qpr,st)
        for i,x in enumerate(exp): exact(v[4+i],x,f"{case}/Bani(N2Od)[{i+1}]")
        for i,x in enumerate(STATE): exact(v[7+i],x,f"{case}/state[{i+1}]")
        for i,x in enumerate(FLUX): exact(v[10+i],x,f"{case}/flux[{i+1}]")
        exact(v[12],A1,f"{case}/A1")
        exact(v[13],A2,f"{case}/A2")
        exact(v[14],A4,f"{case}/A4")
        exact(v[15],OTHER,f"{case}/other")
    active=rows["ACTIVE_NONZERO"]
    zero=rows["ZERO_DENI"]
    perm=rows["PERMUTED"]
    rte=rows["RATE_TIME_EQUIVALENT"]
    inactive=rows["INACTIVE"]
    require(active[4:7] != zero[4:7], "nonzero denitrification must activate N2Od")
    require(active[4:7] == rte[4:7], "rate-time equivalent amounts must match exactly")
    require(perm[4:7] == (active[6],active[4],active[5]), "permutation must preserve per-layer ownership mapping")
    require(inactive[4:7] == (100.0,100.0,100.0), "inactive branch changed N2Od")

def validate_authorities():
    b3d24=show_json(BASE,"integration/animo-b3/ANIMO-B3D24_STATUS.json")
    require(b3d24["state"]=="ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY","B3D24 base not admitted")
    require(b3d24["target_child_atom"]=="TCD-037-A2","wrong B3D24 target")
    require(b3d24["candidate_admission_effect"]["parent_tcd_admitted"] is False,"parent admitted")
    require(b3d24["candidate_admission_effect"]["sibling_atoms_admitted"]==[],"sibling already admitted")
    require(b3d24["aggregate_policy"]["rg05i_created"] is False,"unexpected RG05I at base")

    atom=show_json(B3I07,"integration/animo-b3/B3I07_TCD037_ATOMIZATION.json")
    atoms={x["atom_id"]:x for x in atom["atoms"]}
    a3=atoms["TCD-037-A3"]
    require(a3["class"]=="A_ACCOUNTING_REPORTING_ONLY","A3 class changed")
    require(a3["source_owner"]=="QPrN2Oden(Ln)*St","A3 source owner changed")
    require(a3["allowed_observer_fields"]==["Bani(N2Od)"],"A3 allowed surface changed")
    require(a3["natural_activation"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH","natural activation changed")
    require(a3["admitted"] is False and a3["tier_a_waiver_granted"] is False,"A3 already admitted or waived")

    rq=show_json(RUNTIMEQ03,"integration/animo-runtime/ANIMO-RUNTIMEQ03_STATUS.json")
    require(rq["semantic_qualification"]["n2o_denitrification_layer_formation_owner"]=="QPrN2Oden(Ln)*St","RUNTIMEQ03 A3 owner changed")
    require(rq["expected_difference"]["physical_state"]=="NONE" and rq["expected_difference"]["process_flux"]=="NONE","non-interference basis changed")
    require(rq["natural_active_ghg_case"]=="BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH","natural case state changed")
    require(rq["historical_intel_behavior"]=="UNKNOWN","history promoted")

    synq=show_json(SYNQ01,"integration/animo-synthetic/ANIMO-SYNQ01_STATUS.json")
    require(synq["status"]=="QUALIFIED_INDEPENDENT_SYNTHETIC_ORACLE_EVIDENCE_LAYER_NO_HISTORICAL_REFERENCE_CLAIM","SYNQ01 changed")

    g5=show_json(GOV05,"integration/animo-governance/ANIMO-GOV05_STATUS.json")
    require(g5["work_status"]["qualified"] is True and g5["assurance_change"]["scientific_gate_reduction"] is False,"GOV05 not qualified or weakened")

    g3=show_json(GOV03,"integration/animo-governance/ANIMO-GOV03_STATUS.json")
    require(g3["qualified_closure_state"]=="B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT","GOV03 B2 closure changed")

    oracle=json.loads(ORACLE.read_text())
    require(oracle["work_unit"]=="ANIMO-SYNQ04" and oracle["target"]=="TCD-037-A3","wrong oracle identity")
    require(oracle["evidence_strength"]=="B1_SYNTHETIC_NOT_B2","evidence promoted")
    require(oracle["accounting_contract"]["source_owner"]=="QPrN2Oden(Ln)*St","oracle source owner changed")
    require(oracle["accounting_contract"]["observer_increment"]=="10000*QPrN2Oden(Ln)*St","observer identity changed")
    require(oracle["allowed_difference_surface"]==["Bani(N2Od)"],"scope widened")
    require(oracle["historical_behavior"]=="UNKNOWN","history promoted")
    require(oracle["natural_case"]["translation_performed"] is False,"testcase translated")
    require(oracle["gov05_tier_a_activation_predicate"]["independently_qualified_for_causality_and_scope"]=="PASS","activation predicate not passed")

    st=json.loads(STATUS.read_text())
    require(st["scientific_admission"] is False and st["tier_a_waiver_granted"] is False,"SYNQ04 overclaims")
    require(st["production_source_modified"] is False and st["b4_opened"] is False,"scope violation")

    changed=run("git","diff","--name-only",BASE,"HEAD").splitlines()
    allowed_prefixes=("docs/synthetic/TCD037_A3_","docs/synq04/","integration/animo-synthetic/ANIMO-SYNQ04_STATUS.json",
                      "integration/animo-synthetic/SYNQ04_TCD037_A3_ORACLE.json","tools/synq04/",
                      ".github/workflows/animo-synq04-tcd037-a3.yml")
    for p in changed:
        require(any(p.startswith(x) for x in allowed_prefixes),f"scope widened by {p}")

def main():
    require(len(sys.argv)==2,"usage: validate_tcd037_a3_synthetic.py <probe-output>")
    rows=parse(sys.argv[1])
    validate_probe(rows)
    validate_authorities()
    print("SYNQ04 PASS: exact A3 denitrification-formation observer causality and scope qualified at B1 synthetic strength; not B2")

if __name__=="__main__":
    main()
