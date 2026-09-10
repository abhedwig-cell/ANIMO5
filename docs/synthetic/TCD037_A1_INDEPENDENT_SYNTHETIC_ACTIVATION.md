# ANIMO-SYNQ02 — TCD-037-A1 Independent Synthetic Activation Qualification

Status target: `QUALIFIED_TCD037_A1_INDEPENDENT_SYNTHETIC_CAUSALITY_AND_SCOPE_NOT_B2`

This workunit supplies a purpose-built synthetic activation for the canonical child `TCD-037-A1`. It is an evidence workunit only. It does not admit a correction, grant a GOV04 Tier-A waiver, modify production source, or claim historical revision-53 behaviour.

## Authorities

Current aggregate authority at start:

`ANIMO-RG05H@3e4247928bb43f30def951fa8804560636affbef`

Canonical child routing:

`ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`

Accounting-semantics authority:

`ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`

Synthetic-oracle policy authority:

`ANIMO-SYNQ01@842f72300fd03ede0b9024537a7ee6126722a121`

Governance:

`ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`

No SYNQ02 branch or dedicated TCD-037-A1 synthetic-evidence workunit existed at the live start check.

## Evidence target

B3I07 canonically routes `TCD-037-A1` as:

`CH4 layer formation observer input`

with Class `A_ACCOUNTING_REPORTING_ONLY` and risk state:

`TIER_A_CANDIDATE_WAIVER_NOT_YET_AVAILABLE`.

RUNTIMEQ03 fixes the source-owned layer quantity as:

`CH4_FORMATION_AMOUNT(Ln) = QPrCH4(Ln) * St`.

The quantity is CH4-C formed during the accepted timestep. In the organic-matter balance, revision 53 converts it to organic-matter equivalent by division by `Cfracom`, and multiplies the per-square-metre amount by `Z=10000` to obtain the balance unit `kg/ha`.

The surrounding `Outbal_calc` algebra partitions ordinary organic-matter dissimilation into CH4 and CO2 reporting. For one layer with ordinary dissimilation components `Ffom`, `Fahu`, `Fdom` and `Btot=Ffom+Fahu+Fdom`, the qualified A1 accounting identity in the active, nondegenerate branch is:

`M_CH4 = 10000 * QPrCH4 * St / Cfracom`

`CH4_i = F_i / Btot * M_CH4`

`CO2_i = F_i - CH4_i`

for `i in {fom, ahu, dom}`.

Therefore:

`sum_i(CH4_i + CO2_i) = Btot`

and

`sum_i(CH4_i) = M_CH4`.

This is the bounded observer accounting identity qualified here. SYNQ02 does not claim that the wider GHG carbon ledger is closed.

## Independence design

The synthetic evidence is deliberately split into two implementations.

1. `tools/synq02/tcd037_a1_source_shaped_probe.f90` follows the source-shaped revision-53 observer control flow. It calculates `OmCH4`, `Btot`, `FHlp`, and the six A1 observer fields using the same algebraic arrangement as the audited `Outbal_calc` seam. It is not production ANIMO source and does not contain or call the GHG process model.
2. `tools/synq02/validate_tcd037_a1_synthetic.py` derives expected results independently with exact rational arithmetic using `fractions.Fraction`. It does not use `FHlp` and does not reuse the source-shaped algebraic arrangement. It instead computes the CH4 allocation directly from the stated accounting identity and obtains the CO2 term as the exact complement `F_i-CH4_i`.

The chosen numbers are dyadic or produce dyadic results after the fixed `Z=10000` conversion. Expected values therefore have exact binary64 representations. The validator requires exact floating-point equality, not an empirical tolerance.

This qualifies implementation/control-flow independence for the synthetic causality-and-scope test. It does **not** make the source-derived semantic contract itself an external scientific theory oracle. Scientific/source meaning remains owned by RUNTIMEQ03. The independence claim is intentionally limited to:

`INDEPENDENT_IMPLEMENTATION_AND_ALGEBRAIC_ORACLE_FOR_CAUSALITY_AND_SCOPE`.

Evidence strength remains B1 synthetic, never B2.

## Synthetic cases

The probe contains five bounded cases over three asymmetric layers.

### ACTIVE

Nonzero `QPrCH4` activates the A1 mapping. Ordinary dissimilation totals are positive and well above the legacy `Btot > 1e-9` branch threshold. The independent oracle requires exact agreement for all six allowed A1 observer fields in every layer.

### ZERO_CH4

The same active GHG observer path is exercised with `QPrCH4=0`. The oracle requires all CH4 formation increments to be exactly zero and all CO2 complement increments to equal the ordinary dissimilation components.

### PERMUTED

Layer inputs are permuted. The oracle requires the complete A1 result to permute with the layer data, while aggregate accounting totals remain invariant. This guards against accidental fixed-layer or cross-layer indexing.

### RATE_TIME_EQUIVALENT

`QPrCH4` is halved while `St` is doubled. The product `QPrCH4*St` is unchanged. The oracle requires the A1 outputs to be exactly identical to ACTIVE. This independently tests that the observer consumes a timestep amount rather than a persistent rate.

### INACTIVE

The same nonzero synthetic source data are supplied with the GHG observer branch inactive. All A1 observer fields must remain at their nonzero baseline sentinels.

## Non-interference scope

The source-shaped probe carries separate state sentinels, process-flux sentinels and an unrelated-observer sentinel. They are passed through the synthetic transaction but are not part of the A1 write set. The independent validator requires bit-exact preservation in every case.

This is synthetic dynamic evidence for the already source-audited RUNTIMEQ03 direction:

`EXPECTED_PHYSICAL_STATE_DIFFERENCE = NONE`

`EXPECTED_PROCESS_FLUX_DIFFERENCE = NONE`

`EXPECTED_RESTART_STATE_DIFFERENCE = NONE`

`EXPECTED_SOLVER_OR_NUMERICAL_POLICY_DIFFERENCE = NONE`.

The only allowed A1 correction surface remains:

- `Bfom(CH4f)`;
- `Bahu(CH4f)`;
- `Bdom(CH4f)`;
- associated `Bfom(CO2f)`, `Bahu(CO2f)`, `Bdom(CO2f)` partition fields using the same layer CH4 formation amount.

No A2 index-0 emission semantics, A3 N2O denitrification accounting, A4 N2O atmosphere emission, TCD-032 through TCD-036 process semantics, or wider GHG ledger closure is tested or implied.

## Historical and natural-case boundary

The supplied `GHGMais` testcase remains incompatible with frozen revision 53. SYNQ02 does not translate or repair it.

Natural active-GHG revision-53 execution remains:

`BLOCKED_SOURCE_TESTCASE_LINEAGE_MISMATCH`.

Historical revision-53/Intel behaviour remains exactly:

`UNKNOWN`.

The synthetic case is designed only because the natural activation is unavailable. It must never be cited as historical reference evidence.

## GOV04 consequence

If the exact final SYNQ02 head passes its validator and O0/O2 reproduction, the specific GOV04 alternative activation predicate for `TCD-037-A1` can be considered satisfied at the evidence level:

`natural activation not reasonably available + documented absence + purpose-built synthetic activation independently qualified for causality and scope`.

That does **not** itself grant the Tier-A waiver. `ANIMO-B3A05` must still re-evaluate every Tier-A predicate, including atomicity, source seam, accounting identity, expected-difference contract, non-interference, absence of higher-tier triggers, validator/scope guard, evidence provenance, and historical-uncertainty discipline.

## Hard boundaries

No production source change. No scientific admission. No Tier-A waiver. No parent or sibling admission. No new top-level TCD. No canonical-register change. No B4. No RG05 update. No production migration. No historical fidelity claim.

## Next route if qualified

`ANIMO-B3A05 — TCD-037-A1 CH4 Layer Formation Observer Tier-A Readiness`

B3A05 may consume SYNQ02 only as independent synthetic causality/scope evidence. It must not inherit an admission decision or waiver from this workunit.
