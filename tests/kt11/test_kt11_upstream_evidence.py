from __future__ import annotations
import base64
import json
from pathlib import Path
import zlib

ROOT=Path(__file__).resolve().parents[2]
summary_path=ROOT/"reference/kt11/LWKM_SEQUENCE_SUMMARY_KT08.json"
anchors_path=ROOT/"reference/kt11/LWKM_REPRESENTATIVE_ANCHOR_PACKETS_KT09.json.zlib.b64"

summary=json.loads(summary_path.read_text())
assert summary["workunit"]=="ANIMO-KT08"
assert summary["evidence_class"]=="B1_DERIVED_FROM_PINNED_B0_PRODUCER_NOT_B2"
seq=summary["sequence"]
assert seq["packet_count"]==1800
assert seq["chain_violation_count"]==0
assert seq["unique_endpoint_count"]==1800
assert seq["first_origin_day"]==0.0
assert seq["last_endpoint_day"]==18263.0
assert seq["duration_histogram_days"]=={"8":37,"9":13,"10":1400,"11":350}
assert "multi-packet forcing-provider semantics" in summary["nonclaims"]

encoded=anchors_path.read_text().strip()
bundle=json.loads(zlib.decompress(base64.b64decode(encoded)))
assert bundle["workunit"]=="ANIMO-KT09"
assert bundle["source_sha256"]==summary["source_sha256"]
assert bundle["anchor_count"]==8
assert [a["index_zero_based"] for a in bundle["anchors"]]==[0,2,5,41,449,899,1349,1799]
assert {int(a["diagnostic_normalized_step"]["producer_step_days"]) for a in bundle["anchors"]}=={8,9,10,11}
assert "KT02 or KT06 runtime integration" in bundle["nonclaims"]

print("KT11 upstream KT08/KT09 evidence identity: PASS")
