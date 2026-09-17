# ANIMO-KT03F01 Work Unit Contract

Workunit: `ANIMO-KT03F01 — Hlpimp=1 Interception-State Scientific Source Disposition`.

Execution discipline: `RECONCILE -> QUALIFY -> REVIEW -> CLOSE`.

This is a bounded scientific/source-disposition workunit created from the explicit `KT03-F01` handoff. It may inspect frozen revision-53 source, supplied documentation and pinned testbank hydrology bytes; create diagnostic analysis tooling, derived evidence, tests and qualification documentation; and qualify a bounded scientific interface disposition. It may not modify ANIMO production source, rewrite the frozen KT03 normalized hydrology contract, mutate the canonical TCD register, admit B3/B4, or silently choose a replacement value for an undefined legacy variable.

## Question

For SWAP-style detailed hydrology with `Iopthyvs=1` and `Hlpimp=1`, what scientifically defensible contract applies to canopy-interception storage at the `Input_hydro -> Hydro_detailed` boundary?

The question is necessary because revision-53 has three facts that cannot all be treated as one coherent legacy contract without review:

1. the Hlpimp=1 file grammar does not supply initial `Sic` or dynamic `Sict`;
2. `input1` and `Input_hydro` nevertheless normalize local `sSic`/`sSict` unconditionally after the Hlpimp-specific reads;
3. `Hydro_detailed` consumes `Sict-Sic` both in its top-boundary correction and its whole-profile water-balance calculation.

## Frozen consumed authorities and evidence

- KT03 closeout: `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT03 frozen contract/implementation target: `e844c7658a95819fc0463c55737f9bd41b29a6da`;
- KT03 closeout CI: run `35282911835`, `SUCCESS`;
- revision-53 source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- supplied ANIMO 4.0 user-guide SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`;
- supplied testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- adjacent TCD-018 B3 closeout: `ANIMO-B3D06@11286faafcc59717196ed045d96c9d215c74abeb`.

TCD-018 is adjacent authority for an interception-storage reporting-ledger correction. It does **not** settle KT03-F01 because KT03-F01 concerns whether the hydrology producer state exists at all for Hlpimp=1 and because the legacy `Sict-Sic` term can affect `Evso`, `Flab(1)` and transport-facing water fluxes before output accounting.

## Semantic ownership

Consumed frozen contracts:

- `ANIMO_HYDROLOGY_STEP_V1` and `ANIMO_HYDROLOGY_UNITS_V1` from KT03: `FROZEN`;
- revision-53 source bytes and supplied testbank bytes: `FROZEN`;
- TCD-018 admitted accounting claim: `FROZEN`, adjacent only.

Owned semantic surface:

- interpretation of interception-storage availability for `Iopthyvs=1, Hlpimp=1` at the detailed-hydrology boundary;
- classification of the unconditional `sSic/sSict -> Sic/Sict` source path;
- bounded scientific disposition for whether a missing interception-storage delta may participate in the Hlpimp=1 `Hydro_detailed` equations.

Forbidden overlap:

- no change to Hlpimp=11 semantics;
- no general redesign of `Hydro_detailed`;
- no transport, nutrient, crop, macropore or solver-policy change;
- no canonical TCD ID allocation or register mutation;
- no production source patch.

Parallelism class: `PARALLEL_AFTER_PINNING`. This work consumes exact immutable authorities and does not mutate aggregate, routing, canonical B3 or production surfaces.

Research maturity: `RESEARCH_ISOLATED` until a separate admission path says otherwise.

## Candidate hypotheses

The workunit shall distinguish, not conflate, the following hypotheses:

- **H0, absent-state contract:** Hlpimp=1 does not represent interception storage as producer state; therefore the scientifically meaningful interception-storage change for this interface is absent and must not be read from undefined locals. A corrected Hlpimp=1 balance/transformation contract would omit the `Sict-Sic` term rather than fabricate state.
- **H1, hidden-state contract:** Hlpimp=1 does represent a physically required interception-storage state through some other qualified source or reconstruction rule not yet identified.
- **H2, historically indeterminate:** the intended revision-53 semantics cannot be established sufficiently; the workunit must close negative rather than invent a value.

A positive H0 disposition requires source/interface evidence plus hydrological balance evidence. It is not established merely because zero makes a test pass.

## Required qualification evidence

Before positive close, establish at minimum:

1. exact Hlpimp=1 versus Hlpimp=11 grammar difference for initial and dynamic interception storage;
2. source-wide causal path from `Sic/Sict` through `Hydro_detailed`, including any effect on transport-facing fluxes;
3. version-limited documentary evidence for the older SWATRE exchange contract;
4. derived whole-profile balance evidence on multiple frozen Hlpimp=1 files without inventing interception state;
5. contrast evidence from a frozen Hlpimp=11 file where explicit `Sic/Sict` exists;
6. explicit treatment of TCD-010/TCD-011 compiler-kind/storage uncertainty so undefined-local values are never promoted to historical truth;
7. mandatory same-agent adversarial review labeled `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`;
8. exact-head CI for all repository-resident diagnostic tests.

## Exit conditions

Positive close may qualify only a nonproduction scientific/source disposition such as:

`HLPIMP1_INTERCEPTION_STORAGE_NOT_PART_OF_PRODUCER_STATE_CONTRACT`

with an explicit candidate corrected equation boundary.

It may not claim historical bitwise behaviour, production admission, B3 admission or a production source change.
