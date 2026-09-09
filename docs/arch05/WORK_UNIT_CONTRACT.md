# ANIMO-ARCH05 — External Hydrology and Crop Exchange Contract Architecture

Status: `CANDIDATE_ARCHITECTURE_DESIGN_ONLY_NOT_CANONICAL_ADMISSION`.

## Purpose

ARCH05 defines candidate external exchange contracts for hydrology and externally owned crop state using the ownership and transaction boundaries already established by ARCH01–ARCH04.

This workunit does not implement SWAP coupling, WOFOST coupling, runtime orchestration, canonical TIME semantics, production memory layouts, or corrected legacy behaviour. It defines the information boundary that such implementations must satisfy later.

## Starting point

Branch base: ARCH04 closeout `87930bbdfc413ad626176ce119f52ea409198f1d`.

ARCH04 already requires:

- hydrological coordinates to remain externally owned;
- crop mode to be one of `none`, `animo`, or `external`;
- external exchange schemas to participate in physical-layout compatibility;
- accepted/trial state and rollback semantics to remain separate;
- optional persistent state to exist only when active and admitted.

PREP06 supplies source-bound evidence for hydrological storage/flux families and crop nutrient/dry-matter transfer identities. ARCH05 uses that evidence to define candidate exchange semantics without claiming that legacy argument lists or file interfaces are canonical APIs.

## Scope

ARCH05 shall define:

1. exchange-domain ownership;
2. immutable frame identity and compatibility metadata;
3. hydrology accepted-state coordinates and interval-integrated transfer fields;
4. external crop owner state/demand observations and ANIMO-to-crop realized-transfer results;
5. coupled transaction and commit-barrier rules;
6. fail-closed compatibility requirements;
7. a machine-readable field registry and transaction-rule registry;
8. structural CI evidence.

## Hard rules

- No frozen legacy source modification.
- No testcase modification.
- No physics change.
- No numerical-policy change.
- No corrected-legacy admission.
- No production coupling implementation.
- No canonical STATE, TIME, MASS, EX or process-gate admission.
- ANIMO may not access internal SWAP or crop-model state.
- External owners may not access internal ANIMO state.
- Exchange frames are explicit immutable values for one identified interval/trial.
- Hydrology coordinates are consumed by ANIMO but remain owned by the hydrology model.
- External crop persistent state remains owned by the crop model; ANIMO receives only declared observations/demands and returns declared realized transfers/results.
- A rejected coupled trial cannot commit ANIMO state, external owner state, or physical transfer events.
- Units and sign conventions are explicit at the contract boundary.
- Numerical tolerances and precision are references only and are not invented here.

## Evidence distinction

PREP06 source-bound ledger evidence supports which physical quantities must cross the coupling boundary. ARCH05 does not infer exact future SWAP/WOFOST API field names from legacy variable names. Candidate field names are semantic ANIMO5 contract names.

## Maximum decision

`QUALIFIED_CANDIDATE_EXTERNAL_EXCHANGE_CONTRACT_ARCHITECTURE`

This decision means that the exchange boundary is structurally explicit and internally consistent. It does not mean that SWAP, WOFOST, legacy ANIMO, or any future coupled executable has been behaviourally qualified against the contract.

## Required false flags

- `canonical_state_gate_admitted=false`
- `canonical_time_gate_admitted=false`
- `canonical_mass_gate_admitted=false`
- `canonical_exchange_gate_admitted=false`
- `reference_qualified=false`
- `production_implemented=false`
- `production_migration_admitted=false`

## Deliverables

- `docs/arch05/EXTERNAL_EXCHANGE_MODEL.md`
- `docs/arch05/HYDROLOGY_EXCHANGE_CONTRACT.md`
- `docs/arch05/CROP_EXCHANGE_CONTRACT.md`
- `docs/arch05/COUPLED_TRANSACTION_BOUNDARY.md`
- `integration/animo-architecture/ARCH05_EXCHANGE_DOMAINS.csv`
- `integration/animo-architecture/ARCH05_EXCHANGE_FIELDS.csv`
- `integration/animo-architecture/ARCH05_TRANSACTION_RULES.csv`
- `integration/animo-architecture/ARCH05_COMPATIBILITY_SCHEMA.csv`
- `tools/audit_arch05_exchange_contracts.py`
- `.github/workflows/arch05-exchange-contracts.yml`
- `integration/animo-architecture/ARCH05_CONSISTENCY_TEST.json`
- `integration/animo-architecture/ANIMO-ARCH05_STATUS.json`
