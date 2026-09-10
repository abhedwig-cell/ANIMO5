#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/"integration/animo-b3/TCD027_FROZEN_B0_SOURCE_EVIDENCE_MANIFEST.json"; S=ROOT/"integration/animo-b3/ANIMO-B3A01E_STATUS.json"; D=ROOT/"docs/b3/TCD027_FROZEN_B0_SOURCE_EVIDENCE_REMEDIATION.md"
ARCH="183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"; TB="44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84"; REVIEW="510c9313926457cd9bfd8e71a551255297bdfbb3"; FORMAL="a7b11b334f8b2604d5036edc04365006800944e0"
def f(x): raise AssertionError(x)
def main():
 m=json.loads(M.read_text()); s=json.loads(S.read_text()); d=D.read_text()
 if m.get("workunit")!="ANIMO-B3A01E" or m.get("tcd_ids")!=["TCD-027"] or m.get("class")!="A_ACCOUNTING_REPORTING_ONLY": f("atomic identity")
 if m["base_review"]["head"]!=REVIEW or m["base_review"]["semantic_result"]!="INCOMPLETE" or not m["base_review"]["result_retained_unchanged"]: f("retained review")
 if m["authorities"]["formal_disposition_head"]!=FORMAL: f("formal authority")
 if m["frozen_b0"]["source_archive_sha256"]!=ARCH or m["frozen_b0"]["testbank_sha256"]!=TB: f("B0 hashes")
 gaps={x["id"] for x in m["review_gaps_remediated"]}
 if gaps!={"R1_DUM_LOCAL_CONSTRUCTION","R2_OUTBAL_WRITE_SLOT24_27_MAPPING","R3_P_SLOT25_26_27_SELF_ACCUMULATORS"}: f("gap set")
 if any(x["status"]!="SOURCE_BYTES_PERSISTED_FOR_NEW_REVIEW" for x in m["review_gaps_remediated"]): f("gap status")
 ids={x["id"] for x in m["source_neighbourhoods"]}
 if ids!={"P_REDISTRIBUTION_TCD027_SEAM","OM_SLOT24_ORTHOGONAL_ANALOGUE","N_SLOT24_ORTHOGONAL_ANALOGUE","ORGANIC_P_DETAILED_HEADER","ORGANIC_P_DETAILED_WRITE_RESET"}: f("neighbourhood set")
 for r in m["source_neighbourhoods"]:
  b=base64.b64decode(r["exact_bytes_base64"],validate=True)
  if hashlib.sha256(b).hexdigest()!=r["sha256_exact_bytes"] or len(b)!=r["size_bytes"]: f("neighbourhood hash")
  if r["classification"]!="FROZEN_SOURCE_EVIDENCE": f("source classification")
 mapping=m["mechanically_derived_header_index"]
 if mapping["required_mapping"]!={"24":"redis_EXP","25":"redis_OP","26":"redis_DOP","27":"redis_HUP"} or mapping["term_count"]!=30 or not mapping["reviewer_must_rederive_independently"]: f("mapping contract")
 c=m["atomic_claim_context"]
 if c["legacy"]!="Bafop(24,Ly)=bafop(25,Ly) + Dum" or c["candidate"]!="Bafop(24,Ly)=bafop(24,Ly) + Dum" or not c["candidate_not_applied_in_this_workunit"]: f("atomic claim")
 b=m["boundaries"]
 if b["prior_review_result_remains"]!="INCOMPLETE" or any(b[k] for k in ["admitted","production_source_changed","frozen_b0_changed","composition_performed","b4_performed","central_regie_updated","independent_rereview_performed"]): f("manifest hard boundary")
 if b["next_required"]!="NEW_GENUINELY_SEPARATE_ANIMO-B3A01R2_REREVIEW": f("next review")
 if s["workunit"]!="ANIMO-B3A01E" or s["target"]!="TCD-027" or s["base_review_head"]!=REVIEW or s["prior_review_result_retained"]!="INCOMPLETE": f("status identity")
 if any(s["boundaries"][k] for k in ["independent_rereview_performed","review_result_changed","admitted","production_source_changed","frozen_b0_changed","composition_performed","b4_performed","central_regie_updated"]): f("status hard boundary")
 if "does **not** perform the independent second-line re-review" not in d or "`ANIMO-B3A01R = INCOMPLETE`" not in d or "new genuinely separate" not in d.lower(): f("human boundary")
 if any(x in d for x in ["TCD-027 = ADMITTED","ADMITTED_TCD027","PASS_TCD027_INDEPENDENT"]): f("forbidden conclusion")
 print("PASS_B3A01E_TCD027_FROZEN_B0_SOURCE_EVIDENCE_REMEDIATION")
if __name__=="__main__":
 try: main()
 except Exception as e: print(f"FAIL_B3A01E: {e}",file=sys.stderr); raise SystemExit(1)
