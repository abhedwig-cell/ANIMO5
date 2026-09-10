#!/usr/bin/env python3
"""Compare an independently generated B3B04E3 report to frozen B3B04 targets.

This script is deliberately separate from the generator. The generator must not
read TCD040_REPLAY_EXPECTATIONS.json. The historical B3B04 full-trace SHA values
are not required to match because their serializer schema was not persisted;
E3 uses a new, explicitly versioned reconstructed trace schema.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

NAME_TO_COORD = {
    "NH4": "Conh(0)",
    "NO3": "Coni(0)",
    "DOM": "Codiorma(0)",
    "DON": "Codiorni(0)",
    "DOP": "Codiorpo(0)",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("generated_report", type=Path)
    parser.add_argument("expectations", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    got = json.loads(args.generated_report.read_text(encoding="utf-8"))
    exp = json.loads(args.expectations.read_text(encoding="utf-8"))
    failures: list[str] = []
    checks: dict[str, object] = {}

    def req(name: str, cond: bool, detail: object = None) -> None:
        checks[name] = {"pass": bool(cond), "detail": detail}
        if not cond:
            failures.append(name)

    req("workunit", got.get("workunit") == "ANIMO-B3B04E3")
    req("target", got.get("target") == "TCD-040")
    req("generator_did_not_load_expected_results", got.get("generator_expected_scientific_results_loaded") is False)
    req("source_archive_identity", got["frozen_b0"]["source_sha256"] == exp["frozen_b0"]["source"]["sha256"])
    req("testbank_archive_identity", got["frozen_b0"]["testbank_sha256"] == exp["frozen_b0"]["testbank"]["sha256"])
    req(
        "source_member_identity",
        got["source_member_identity_before_instrumentation"] == exp["source_member_identity"],
        {"generated": got["source_member_identity_before_instrumentation"], "expected": exp["source_member_identity"]},
    )

    sgot = got["split282"]
    sexp = exp["split_282"]
    req("split282_step", sgot["split_step"] == sexp["split_step"])
    req("split282_stageA_records", sgot["stageA_records"] == sexp["stage_a_records"])
    req("full_trace_record_count", got["continuous"]["records"] == sexp["full_trace_records"])
    req("stageA_exact_prefix", sgot["stageA_exact_continuous_prefix"] is True)
    req("checkpoint_matches_accepted_owner_bytes", sgot["checkpoint_matches_stageA_accepted_owner_bytes"] is True)

    ckpt = sgot["checkpoint"]
    exp_values = {NAME_TO_COORD[name]: value for name, value in ckpt["values"].items()}
    req("checkpoint_values", exp_values == sexp["checkpoint_values"], {"generated": exp_values, "expected": sexp["checkpoint_values"]})
    exp_hex = {NAME_TO_COORD[name]: value for name, value in ckpt["binary64_little_endian_hex"].items()}
    req("checkpoint_binary64_hex", exp_hex == sexp["checkpoint_binary64_little_endian_hex"], {"generated": exp_hex, "expected": sexp["checkpoint_binary64_little_endian_hex"]})
    req("checkpoint_sha256", ckpt["file_sha256"] == sexp["checkpoint_sha256_reported_by_b3b04"], {"generated": ckpt["file_sha256"], "expected": sexp["checkpoint_sha256_reported_by_b3b04"]})
    req("checkpoint_serialization_one_40_byte_record", ckpt["logical_records"] == 1 and ckpt["payload_size_bytes"] == 40 and ckpt["file_size_bytes"] == 48)

    req("corrected_restore_full_trace_exact", sgot["corrected_restore_full_trace_exact"] is True)
    req(
        "corrected_restore_reconstructed_trace_hash_equals_continuous",
        sgot["corrected_restore_trace_sha256_reconstructed_schema"] == got["continuous"]["trace_sha256_reconstructed_schema"],
    )

    diff = sgot["defective_comparison"]
    f = diff["first_divergence"]
    req("first_divergence_record_index", f["record_index"] == sexp["first_defective_divergence"]["reported_record_index"])
    req("first_divergence_step", f["step"] == sexp["first_defective_divergence"]["step"])
    req("first_divergence_phase", f["phase"] == sexp["first_defective_divergence"]["phase"])
    got_first_coords = sorted(NAME_TO_COORD[name] for name, layer, *_ in f["coordinates"] if name in NAME_TO_COORD and layer == 0)
    req("first_divergence_coordinates", got_first_coords == sorted(sexp["first_defective_divergence"]["coordinates"]), {"generated": got_first_coords, "expected": sexp["first_defective_divergence"]["coordinates"]})
    req("Copo0_boundary_control", sgot["Copo0_modified_at_boundary"] is False)
    req("changed_records", diff["changed_records"] == 1236, diff["changed_records"])

    expected_layers = {"NH4": "0:30", "NO3": "0:30", "DOM": "0:30", "DON": "0:30", "DOP": "0:30", "PO4": "1:29"}
    req("changed_layer_envelopes", {k: diff["changed_layers"][k] for k in expected_layers} == expected_layers, {"generated": {k: diff["changed_layers"][k] for k in expected_layers}, "expected": expected_layers})

    # These values were recorded in the B3B04 readiness evidence and are compared only here,
    # after independent E3 generation.
    original_max_abs = {
        "NH4": 0.0008977310061221382,
        "NO3": 8.767359689234193e-06,
        "DOM": 0.004381575788713558,
        "DON": 0.00012267733059957502,
        "DOP": 1.2267733059957505e-05,
        "PO4": 1.4751153212333792e-10,
    }
    max_ok = all(diff["max_abs_difference"][k] == v for k, v in original_max_abs.items())
    req("max_abs_differences", max_ok, {"generated": {k: diff["max_abs_difference"][k] for k in original_max_abs}, "expected": original_max_abs})
    req("non_target_control_scalars_unchanged", all(v == 0.0 for v in diff["scalar_max_abs_difference"].values()), diff["scalar_max_abs_difference"])
    req("MOFRT_unchanged", diff["changed_layers"]["MOFRT"] is None and diff["max_abs_difference"]["MOFRT"] == 0.0)

    zgot = got["split67_zero_control"]
    zexp = exp["split_67_zero_control"]
    req("split67_step", zgot["split_step"] == zexp["split_step"])
    req("split67_stageA_records", zgot["stageA_records"] == zgot["split_step"] * got["trace_schema"]["records_per_step"])
    req("split67_checkpoint_exact_positive_zero", zgot["checkpoint"]["all_exact_positive_zero"] is True)
    req("split67_full_trace_exact", zgot["defective_zero_application_full_trace_exact"] is True)
    req(
        "split67_reconstructed_trace_hash_equals_continuous",
        zgot["defective_trace_sha256_reconstructed_schema"] == got["continuous"]["trace_sha256_reconstructed_schema"],
    )

    trace_hash_boundary = {
        "status": "NOT_APPLICABLE_UNPERSISTED_ORIGINAL_TRACE_SERIALIZATION_SCHEMA",
        "original_continuous_trace_sha256": sexp["continuous_trace_sha256"],
        "original_corrected_restore_trace_sha256": sexp["corrected_restore_trace_sha256"],
        "original_defective_trace_sha256": sexp["defective_restart_trace_sha256"],
        "reconstructed_schema_continuous_trace_sha256": got["continuous"]["trace_sha256_reconstructed_schema"],
        "reconstructed_schema_corrected_restore_trace_sha256": sgot["corrected_restore_trace_sha256_reconstructed_schema"],
        "reconstructed_schema_defective_trace_sha256": sgot["defective_trace_sha256_reconstructed_schema"],
        "reason": "B3B04 did not persist its full-trace serializer schema or payloads; E3 intentionally uses a distinct documented trace schema and does not claim byte-identical reconstruction of those files.",
    }
    checks["original_full_trace_sha_comparison"] = trace_hash_boundary

    result = {
        "schema_version": "1.0",
        "workunit": "ANIMO-B3B04E3",
        "comparison_role": "POST_GENERATION_COMPARISON_ONLY",
        "result": "PASS_B3B04E3_RECONSTRUCTED_REPLAY_SEMANTICS" if not failures else "FAIL_B3B04E3_RECONSTRUCTED_REPLAY_SEMANTICS",
        "checks": checks,
        "failures": failures,
        "original_trace_serialization_bytes_reconstructed": False,
        "scientific_semantic_match": not failures,
    }
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
