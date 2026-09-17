# ANIMO-KT03F01 Qualification Report

## Decision

KT03-F01 is qualified positively as a bounded nonproduction scientific/source disposition.

Qualification verdict:

`QUALIFIED_NONPRODUCTION_HLPIMP1_INTERCEPTION_STORAGE_NOT_PART_OF_PRODUCER_EXCHANGE_STATE_CONTRACT`

The qualified statement is deliberately narrow:

> For revision-53 detailed hydrology with `Iopthyvs=1, Hlpimp=1`, interception storage is not part of the producer exchange-state contract. The unconditional legacy use of `Sic/Sict` cannot be treated as scientifically defined input. A corrected Hlpimp=1 transformation must omit the interception-storage delta from the affected `Hydro_detailed` identities rather than fabricate, default or recover an undefined state.

This says nothing about whether interception storage exists physically inside the producing hydrology model. It says that Hlpimp=1 does not deliver it as a separate ANIMO exchange state.

## Frozen qualification evidence

Authoring head:

`9e31afe36ca1bc8f4c90dab024c811c87337cbc0`

Exact-head CI:

`35283726500` -> `SUCCESS`.

Review assurance:

`PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Adversarial review verdict:

`PASS_KT03F01_HLPIMP1_ABSENT_INTERCEPTION_EXCHANGE_STATE_SOURCE_DISPOSITION_NONPRODUCTION`.

Evidence class:

`B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`.

## Scientific/source basis

The disposition rests on converging evidence rather than a single source statement:

1. revision-53 Hlpimp=1 static and dynamic records omit `sSic/sSict`;
2. revision-53 nevertheless normalizes those unread locals unconditionally;
3. previous interception state is promoted in `Init` only for Hlpimp=11;
4. the supplied ANIMO 4.0 SWATRE exchange table contains no interception-storage state;
5. four frozen Hlpimp=1 SWAP files close the revision-53 whole-profile water identity without a separate interception term at mean absolute residuals around `10^-8 m` per timestep;
6. the frozen Hlpimp=11 LWKM file explicitly supplies the state and its inclusion improves mean absolute closure by about `18.06x`;
7. `Sict-Sic` participates in the `Dif -> Evso -> Flab(1) -> Modflux` chain, so the undefined Hlpimp=1 value is not merely an output-ledger concern.

## Qualified corrected equation boundary

For the bounded exchange contract, define an interception-storage delta only when that state is explicitly supplied by the qualified producer layout.

For Hlpimp=1:

`delta_interception = NOT_PRESENT_IN_EXCHANGE_CONTRACT`

and the `Sict-Sic` contribution is omitted from both:

- the `Iopthyvs=1` top-boundary `Dif` identity;
- the whole-profile `Badev` identity.

For Hlpimp=11, KT03-F01 changes nothing. The explicit initial `Sic`, dynamic `Sict`, lifecycle promotion and delta terms remain the qualified observed layout behaviour for the bounded KT03 evidence.

At the equation level, omitting an absent term has the same arithmetic contribution as zero. Semantically these are not the same operation: the qualified contract does **not** create a zero-valued interception state for Hlpimp=1. The state is absent, so an adapter or future module contract must not expose fabricated `Sic/Sict` values.

## Relationship to KT03

KT03 correctly failed closed for Hlpimp=1 full downstream projection because the producer payload did not contain `Sict`. KT03-F01 now qualifies the missing scientific rule needed to continue architecture work: Hlpimp=1 projection does not require synthesizing `Sict`; it requires a layout-qualified projection whose equations omit the absent storage term.

The frozen `ANIMO_HYDROLOGY_STEP_V1` payload remains unchanged. Its explicit availability semantics are therefore preserved.

## Relationship to TCD-018

TCD-018 remains valid and separate. It concerns an output water-ledger interface when `Sic/Sict` is a real existing state. KT03-F01 concerns a producer layout that does not supply that state and where unconditional use can affect transport-facing hydrology transformation. Neither disposition replaces the other.

## Historical uncertainty

The exact revision-53 executable behaviour of unread `sSic/sSict` is not qualified. Default-real and local-storage compiler semantics are known historical build-contract dependencies. KT03-F01 therefore does not claim that historical ANIMO happened to use zero, retained memory, or any other specific value on Hlpimp=1 runs.

The qualified result is a corrected scientific interface disposition under historical uncertainty, not a reconstruction of undefined historical memory behaviour.

## Explicit nonclaims

KT03-F01 does not qualify or admit:

- Hlpimp=2 interception semantics;
- a corrected executable `Hydro_detailed` implementation;
- whole-model numerical equivalence after applying the guard;
- B2 historical behaviour;
- a canonical TCD identity or register mutation;
- B3 or B4 admission;
- production source changes;
- Status A or Status AA.

Production `src/` is unchanged.

## Next safe action

Return to the architecture line in a separate successor adapter workunit. That workunit may consume this frozen disposition to implement a nonproduction Hlpimp=1 `Hydro_detailed` projection path with an explicit layout-qualified interception rule, then prove that file-backed and typed-provider paths produce the same transport-facing hydrology transformation for the bounded cases. It must still keep Hlpimp=11 explicit-state semantics separate and must not promote the result into production without its own admission path.
