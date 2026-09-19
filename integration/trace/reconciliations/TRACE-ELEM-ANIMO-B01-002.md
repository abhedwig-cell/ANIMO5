# TRACE-ELEM-ANIMO-B01-002 reconciliation

Date closed: 2026-09-19
Prospective result: `NO_CONFIRMED_DISCREPANCY`
Candidate IDs: `TRACE-ANIMO-0002` (excluded)

## Element

TCD-032 methanogenesis carbon-transfer ownership, selected before detailed inspection as the transfer/ownership stratum of Exposure Batch 01.

## Scientific identity

The GHG03 scientific document and machine policy define the same bounded C-transfer relation for each TCD-033-qualified methane source family:

- gross source debit `G_j=Q_j*dt/(f_C*(1-a_j))`;
- internal humus/biomass credit `I_j=a_j*G_j`;
- exact family identity `f_C*(G_j-I_j)=Q_j*dt`;
- humus/biomass policy `a_hu=0`;
- exactly one source debit per positive `Q_j`;
- exactly one matching internal credit per nonzero `I_j`;
- duplicated DOM debit forbidden.

The admitted scope is C only. N/P transfer, effective `Rdas/Asfa` timing, hidden GHG_Miner task state, CO2/subsidence accounting, whole-model C balance and production implementation remain excluded.

## Source/evidence provenance

The current revision-53 source manifest preserves the source hashes pinned by GHG03:

- `ghgasses.for`: `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`;
- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`;
- `Rates.for`: `7a1a8aee4715d85b9b7e9e172f83756e4aee8b8278386c804210ef77dc2a857a`;
- `resp_miner.for`: `938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106`.

The GHG03 validator additionally requires the source-path reconstruction from GHG01, exact rational oracle checks, duplicate-DOM and missing-credit negative controls, and explicit historical uncertainty.

B3D41 admits exactly the GHG03 identity and does not broaden it into production authority.

## Prospective candidate outcome

TRACE-ANIMO-0002 was created because the frozen scientific document still says review pending while later GHG03/B3D41 machine evidence records completed review/qualification/admission.

The candidate was excluded after the explicit authoring-freeze contract showed that the scientific document is deliberately immutable pre-review evidence. Post-review status is intentionally stored in separate artifacts, and the validator requires that separation.

## TRACE disposition

No new prospectively eligible scientific discrepancy was confirmed.

This result does not assert that revision-53 active-GHG behaviour is historically validated. The existing authority explicitly says it is unknown without B2.

The element remains in the denominator with `no_discrepancy_observed=true`.
