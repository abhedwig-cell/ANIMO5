# ANIMO-KT03F01 Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Immutable authoring head reviewed: `9e31afe36ca1bc8f4c90dab024c811c87337cbc0`.

Exact-head CI: run `35283726500`, conclusion `SUCCESS`.

This review challenges the candidate H0 disposition rather than assuming that absence of a field means a zero-valued physical state.

## Challenge 1: could Hlpimp=1 contain a hidden interception state?

No identified producer field, ANIMO 4.0 exchange field, revision-53 read path, or Hlpimp=1 state-promotion path supplies such a state. `input1` and `Input_hydro` omit `sSic/sSict` from Hlpimp=1 records, while `Init` promotes `Sic=Sict` only for Hlpimp=11. A hidden-state interpretation would therefore require a reconstruction rule or authority not present in the inspected evidence.

Disposition: **H1 not supported in the bounded evidence**.

## Challenge 2: does omitting the state merely force the balance to look good?

The evidence is not one tuned testcase. Four frozen Hlpimp=1 lineages from SWAP3.0beta through SWAP 3.2.36 independently close the revision-53 whole-profile identity without an interception-storage term, with mean absolute residuals of roughly `3.6e-08` to `5.6e-08 m` per step. The later Hlpimp=11 LWKM layout explicitly supplies the state; on that file, including the supplied `Sict-Sic` reduces mean absolute residual from `4.124e-05 m` to `2.284e-06 m`, about `18.06x`.

This contrast is stronger than simply observing that zero avoids an error. It shows two different producer exchange contracts: an older layout whose hydrological payload is already balanced without a separate interception-storage state and a later layout whose explicit storage delta materially belongs in the identity.

Disposition: **candidate absent-state exchange contract supported**.

## Challenge 3: is KT03-F01 only an accounting issue already settled by TCD-018?

No. In `Hydro_detailed`, changing `Sict-Sic` changes `Dif`. Before clamping, a change `dI` shifts `Dif` by `dI/St`; wherever the `Evso = Max(0, Evso-Dif)` clamp is not saturated, it correspondingly changes `Evso` and the recomputed `Flab(1)`. `Modflux` then converts `Flab` into transport-facing inflow/outflow terms. The effect may saturate when soil evaporation reaches zero, but it is not confined to output accounting.

TCD-018 remains an adjacent reporting-ledger authority for a state that exists. It cannot authorize use of a state absent from the Hlpimp=1 exchange contract.

Disposition: **KT03-F01 remains a distinct scientific/source surface**.

## Challenge 4: can revision-53 historical behaviour be reconstructed from the undefined locals?

No. TCD-010 and TCD-011 already identify default-real and local-storage build-contract dependencies. The source assigns from `sSic/sSict` even when those locals were not read. The resulting historical executable value is therefore not scientifically recoverable from source alone and is not needed for the corrected interface disposition.

Disposition: **historical executable behaviour remains unknown; no B2 claim**.

## Challenge 5: is the proposed correction broader than the evidence?

The source's `else` path also covers values other than Hlpimp=1, including the documented Hlpimp=2 macropore format. KT03-F01 has no active Hlpimp=2 testbank qualification and does not generalize its conclusion to that layout. The qualified statement is strictly `Iopthyvs=1, Hlpimp=1`.

Disposition: **scope remains bounded; Hlpimp=2 is an adjacent unqualified question**.

## Challenge 6: does this qualify a corrected executable implementation?

No. The probe evaluates the source water-balance identity over frozen producer records and the source causal chain. It does not execute a modified `Hydro_detailed` path or prove whole-model output equivalence. A successor adapter/implementation workunit must apply the qualified semantic guard and then test its actual downstream behaviour.

Disposition: **semantic/source qualification only, not implementation qualification**.

## Review verdict

`PASS_KT03F01_HLPIMP1_ABSENT_INTERCEPTION_EXCHANGE_STATE_SOURCE_DISPOSITION_NONPRODUCTION`

No material finding blocks the bounded scientific/source disposition. The review requires the closeout to preserve four limits explicitly: Hlpimp=1 only, B1-not-B2 evidence, no corrected executable claim, and no production/B3 admission.
