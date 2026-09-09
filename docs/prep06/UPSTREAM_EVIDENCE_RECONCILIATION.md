# ANIMO-PREP06 upstream evidence reconciliation

Date: 2026-09-09.

PREP06 is continued on its existing dedicated branch `work/animo-prep06-conserved-state-ledger`. The live bootstrap branch remains `work/animo-prep01-bootstrap` at `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`.

The two branches are intentionally divergent from merge base `cbd71f1e651d312c4f1d7573269e6cbd18178801`. PREP06 was not restarted and the bootstrap branch was not merged into it merely to import evidence files.

For this extension, the latest PREP05 evidence on the bootstrap branch was read live and reconciled conceptually:

- `docs/prep05/CROSS_SPECIES_SYMMETRY_AUDIT.md` reproduces only the two already confirmed TCD-023 stale-N-sibling statements in the stable-DOM phosphorus branch and opens no additional high-confidence cross-species TCD;
- `integration/animo-prep/ANIMO-PREP05_STATUS.json` keeps TCD-024 classified as `CONFIRMED_LEGACY_WRONG_INDEX_DEFECT_AND_LATENT_BOUNDS_RISK`, distinguishes it from TCD-019, and retains reference/production admission as blocked;
- the PREP05 composition evidence therefore supports keeping TCD-019 and TCD-024 as separate mineral-P conservation seams in the PREP06 ledger.

The PREP06 extension maps TCD-014, TCD-015, TCD-016, TCD-017, TCD-018, TCD-019, TCD-023 and TCD-024 explicitly and also carries forward TCD-025 through TCD-027. No new discrepancy is inferred merely from branch divergence or from the state/transfer inventory.

This note is evidence reconciliation only. It does not merge branches, change frozen source, change testcases, change physics or admit corrected legacy behaviour.
