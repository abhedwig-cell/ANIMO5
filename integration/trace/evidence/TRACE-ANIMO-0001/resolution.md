# TRACE-ANIMO-0001 resolution

Date: 2026-09-19
Outcome: `EXCLUDED`
Prospective candidate: yes
Confirmed discrepancy: no

## Frozen observation

At pre-resolution commit `dda2c4bbb8029c829f6e249068126ba2e1705c11`:

- `docs/b3/TCD015_B3_ADMISSION_CLOSEOUT.md` states that TCD-015 is admitted after independent second-line review.
- `integration/animo-b3/TCD015_B3_DISPOSITION_GOV03.json` retains `UNRESOLVED_NOT_ADMITTED`, `admitted=false`, and a pending independent review.

Read without temporal context, these appear inconsistent.

## Authority reconstruction

The later B3D12 admission package explicitly treats B3D09 as a predecessor state, not as a competing current admission authority.

`tools/validate_b3d12_tcd015_admission.py` reads the B3D09 disposition from its pinned predecessor commit and requires:

- the historical uncertainty route already PASS;
- all B3D09 scientific gates except independent review PASS;
- the B3D09 independent-review gate still equal to `FAIL_PENDING_NOT_COMPLETED`.

The same validator then independently reads B3B01R and requires its review status and semantic result to be PASS. It validates the B3D12 admission object only after those temporally ordered facts are reconciled.

Current B3D12 machine state records:

- `scientific_b3_admission_qualified=true`;
- decision `ADMIT_TCD015_ATOMIC_CLASS_B_SCIENTIFIC_NITRATE_TRANSPORT_ALGEBRA_CORRECTION_WITH_HISTORICAL_UNCERTAINTY`;
- historical behaviour remains UNKNOWN;
- no production migration is implied.

RG05E subsequently integrates B3D12 and lists TCD-015 among the five admitted atomic B3 scientific corrections.

## Disposition

The candidate is excluded because the observed representations do not make simultaneous claims about the same authority state. They are a predecessor disposition and its explicit validated successor.

This is therefore useful negative TRACE evidence: merely finding different status values in current repository files is insufficient. Temporal provenance and successor authority must be reconstructed before classifying a discrepancy.

No scientific or documentation repair is required for TRACE-ANIMO-0001.
