# PREP02 organic-P ploughing array audit

Status: `DIAGNOSTIC_LEDGER_FAMILY_CAUSALLY_SUPPORTED_NOT_REFERENCE_QUALIFIED`.

## Purpose

The first TCD-017 probe established that `Outbal_calc.for` omits the top-reservoir dissolved-organic-P redistribution term `Addiorpotoppl`. The corrected-legacy plan deliberately left two P-specific ploughing arrays open before TCD-017 could be treated as generic beyond the measured LWKM case:

- `AdStdiorpopl`, stable dissolved organic P redistribution;
- `Adhuexpopl`, P associated with humus originating from exudates.

This audit resolves that source-level question without changing the frozen source or admitting a corrected reference.

## Frozen and diagnostic provenance

The audit uses the PREP01 identities:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- deterministic GNU diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`.

A clean local reconstruction reproduced the exact diagnostic executable hash before any probe variant was built.

The probes are `DIAGNOSTIC_NOT_REFERENCE`. They operate on extracted execution copies only.

## Source audit

`Addit.for` explicitly constructs all three organic-P redistribution families during ploughing.

For the top reservoir it records:

```fortran
Addiorpotoppl(I) = - Sudiorpo
```

For stable dissolved organic P it subtracts the pre-plough layer store and adds the redistributed store through `AdStdiorpopl(I,Ln)`.

For exudate-derived humus it subtracts and adds P quantities explicitly through `Adhuexpopl(I,Ln)`.

`Outbal_calc.for` does not mirror that information completely:

1. the original TCD-017 code omits `Addiorpotoppl` from `Bapo(Redi)`;
2. it adds `Addiorpopl` but omits `AdStdiorpopl`;
3. it reconstructs the exudate-humus P term as `Adhuexpl * Pofrhu` instead of consuming the already explicit P-valued `Adhuexpopl` array.

The nitrogen analogue is informative for the stable dissolved pool: its redistribution ledger sums `Addiornipl + AdStdiornipl`. This strengthens the structural case that the P stable-pool omission is not an intentional whole-ledger asymmetry.

## Natural supplied-case coverage

The supplied testbank contains three phosphorus-enabled cases with ploughing events that complete under the PREP01 GNU diagnostic contract:

- `LWKM_gras_1040.2021.2045`;
- `STONE_akk_0006.2001.2015`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

An observer-only diagnostic build emitted the P-specific redistribution arrays without changing model state. In all naturally occurring ploughing events in these three cases, both `AdStdiorpopl` and `Adhuexpopl` remained zero. Inspection of the supplied LWKM initial state is consistent with that result: the stable dissolved organic pools under `>sdomin:` and the exudate-humus pool under `>humexu:` are initialized to zero.

Therefore the supplied natural cases cannot, by themselves, establish whether the two open terms are correctly represented in the organic-P ledger.

The known top-reservoir term is naturally active in LWKM. For the three LWKM balance profiles the maximum absolute period organic-P residual is `4.94e-2 kg/ha P` in the frozen diagnostic execution. Adding only `Addiorpotoppl` reduces the maxima to:

| profile | top-term diagnostic maximum absolute period residual |
| --- | ---: |
| RP | `2.33e-10 kg/ha P` |
| GP | `4.06e-8 kg/ha P` |
| TP | `6.54e-7 kg/ha P` |

After normalization of only the PREP01 volatile timestamp and CPU-time fields, the baseline-to-top-term differences are confined to the organic-P balance surfaces in LWKM. The other two natural P/ploughing cases show no normalized output differences because the relevant top-reservoir term is also dormant there.

## Controlled stable-DOP activation probe

A diagnostic activation probe was created from the LWKM execution copy. It is not a supplied testcase and must not become a golden case.

Only two diagnostic-input changes were made:

- non-zero, depth-varying `CoStdiorpo` values were inserted in the initial `>sdomin:` stable-DOP row;
- the RP balance lower boundary was moved from compartment 5 to compartment 2 so that the balance control volume cuts through the four-compartment ploughing zone.

Hydrology, forcing, process source and management events were otherwise unchanged.

Two executables were compared:

- top-term variant: TCD-017 `Addiorpotoppl` correction only;
- stable-ledger variant: top-term correction plus `AdStdiorpopl` in `Bapo(Redi)` and the corresponding detailed redistribution ledger.

Results:

| profile | top-term only max abs period residual | with `AdStdiorpopl` |
| --- | ---: | ---: |
| RP, partial plough zone | `1.43e-4 kg/ha P` | `2.34e-10 kg/ha P` |
| GP | `2.84e-4 kg/ha P` | `9.50e-8 kg/ha P` |
| TP | `2.85e-4 kg/ha P` | `6.53e-7 kg/ha P` |

The observer detected non-zero `AdStdiorpopl` elements during the activated ploughing events. After volatile-field normalization, top-term and stable-ledger runs have identical ordinary non-balance outputs. Differences are confined to P balance and detailed P-transformation balance files.

Interpretation:

`AdStdiorpopl` is a real missing organic-P ploughing ledger term when the stable dissolved pool is active. Its natural testbank dormancy had hidden the defect.

## Controlled exudate-humus-P activation probe

A second diagnostic LWKM activation probe set a depth-varying non-zero initial `Huex` state under `>humexu:` and again placed the RP lower balance boundary inside the four-compartment ploughing zone. Stable DOP remained at its supplied zero state.

Two executables were compared:

- top-term variant, retaining the legacy `Adhuexpl * Pofrhu` reconstruction;
- P-explicit variant, replacing that redistribution ledger term with `Adhuexpopl`.

Results:

| profile | legacy `Adhuexpl * Pofrhu` max abs period residual | with `Adhuexpopl` |
| --- | ---: | ---: |
| RP, partial plough zone | `4.52e1 kg/ha P` | `2.34e-10 kg/ha P` |
| GP | `9.03e1 kg/ha P` | `4.06e-8 kg/ha P` |
| TP | `9.03e1 kg/ha P` | `6.54e-7 kg/ha P` |

Non-zero `Adhuexpopl` values were observed directly in the activated events. Again, after volatile-field normalization, the two executions have identical ordinary non-balance outputs. Only P balance and detailed P-transformation balance surfaces differ.

This is strong causal evidence that `Adhuexpopl`, rather than reconstruction from the net `Huex` redistribution using the post-event `Pofrhu`, is the ledger quantity needed for conservation when the exudate-humus pool is active.

## Compatibility caveat discovered during execution

The supplied modernized text inputs contain lines such as:

```text
PrintBalLabel='RP'! comment
```

The historical/Intel parser path tolerates that form when the right-hand side is subsequently read list-directed. GNU internal list-directed character input rejects the trailing inline `!` in this context.

For these diagnostic executions only, the execution copy stripped the trailing comment from `PrintBalLabel` assignments while preserving the quoted two-character value exactly. This is an execution-environment compatibility adaptation, not a testcase translation and not reference evidence. It must be included explicitly in any later GNU-equivalence harness rather than applied silently.

## Classification

The source and diagnostic evidence now support treating TCD-017 as a small family of Class-A organic-P ploughing ledger defects:

1. missing top-reservoir DOP term `Addiorpotoppl`;
2. missing stable-DOP redistribution term `AdStdiorpopl`;
3. incorrect reconstruction of exudate-humus P redistribution where the explicit `Adhuexpopl` ledger quantity is available.

All three candidate changes are located in reporting/balance accounting. The diagnostic probes show no ordinary state/output trajectory differences between the compared ledger variants.

This remains narrower than reference admission. The stable-DOP and exudate-humus terms are exercised only by controlled activation probes, not by the supplied natural cases. A historical native or otherwise independently qualified reference must still anchor corrected-legacy admission.

## Gate

`DIAGNOSTIC_TCD017_LEDGER_FAMILY_CAUSALLY_SUPPORTED_NOT_REFERENCE_QUALIFIED`

Production correction and ANIMO5 process migration remain `NOT_ADMITTED`.
