# TRACE-ELEM-ANIMO-B01-001 reconciliation

Date closed: 2026-09-19
Prospective result: `NO_CONFIRMED_DISCREPANCY`
Candidate IDs: `TRACE-ANIMO-0001` (excluded)

## Element

TCD-015 nitrate transport algebra, selected before detailed inspection as the first documented B3 process/transport subject in Exposure Batch 01.

## Historical scientific discrepancy

The duplicated moisture-storage contribution in the second negative-concentration NITRATE `Reko` reconstruction was known and qualified before the TRACE protocol freeze. It is therefore historical/pilot context and cannot be counted as a prospective TRACE discrepancy.

The source identity remains pinned through the revision-53 manifest:

- `ANIMO_4.1.5.53/Transsub.for`
- SHA-256 `c548e5d372ffbc7f4d4e4d8d86609cf1f34cf70ea513d345e3c7fada5cf6b552`

The current source manifest independently retains that exact member hash.

## Representation and evidence trace

Current scientific/admission surfaces inspected:

- `docs/b3/TCD015_B3_ADMISSION_CLOSEOUT.md`
- `docs/b3/TCD015_GOV03_FORMAL_DISPOSITION.md`
- `integration/animo-b3/TCD015_B3_DISPOSITION_GOV03.json`
- `integration/animo-b3/TCD015_B3_ADMISSION_CLOSEOUT.json`
- `integration/animo-b3/ANIMO-B3D12_STATUS.json`
- `integration/animo-reg/RG05E_B3_ADMISSION_INVENTORY.json`
- `integration/animo-reg/ANIMO-RG05E_STATUS.json`
- `tools/validate_b3d12_tcd015_admission.py`
- `reference/source/source_manifest.csv`

The known scientific identity is internally consistent across the later admission package: `Hv` is already included in `Hv1`, while the explicit storage term already represents the moisture-storage change. The qualified candidate removes one duplicated `Avc*Hv` contribution and remains NITRATE-only, `GreenHouseGasOption=0`, with historical behaviour explicitly UNKNOWN.

## Prospective candidate outcome

TRACE-ANIMO-0001 was registered before resolving an apparent status conflict:

- retained B3D09 disposition: NOT_ADMITTED, independent review pending;
- later B3D12 closeout: admitted after independent review.

The candidate was excluded after reconstruction showed that these are temporally ordered authority states. The B3D12 validator deliberately reads the pinned B3D09 predecessor, requires its then-pending review blocker, reads the later independent review separately, and only then validates the admission. RG05E explicitly integrates that successor admission.

Therefore the two status values are not simultaneous competing scientific claims.

## TRACE disposition

No new prospectively eligible TCD-015 scientific discrepancy was confirmed. One prospective candidate was correctly frozen and then excluded.

The element remains in the denominator with `no_discrepancy_observed=true`. This is a null prospective observation, not evidence that TCD-015 never contained a historical defect.
