# ANIMO-MASSQ04 - TCD-016-C1 continuation-state NH4 balance ontology

Target: `TCD-016-C1`

Base science authority: `ANIMO-SQ05@897ba742630f06381a2b89290db80d5f405ab51d`

Mass-balance predecessor: `ANIMO-MASSQ03@68a8c202bd01bf55b31b7c944884fb2f78a6a8e8`

This workunit qualifies observer/accounting semantics only. It does not define dry NH4 chemistry, rewetting kinetics, production code, B3 admission, or a whole-model golden baseline.

## Legacy NH4 balance ontology

Alterra Report 224 Annex 2 defines the public ANIMO 4.0 NH4 balance with two explicit storage classes:

- `BANHST` / `BANHSTT`: NH4-N storage in soil solution at beginning/end of the balance period;
- `BANHCX` / `BANHCXT`: NH4-N storage at the soil complex at beginning/end of the balance period.

It separately names inputs such as additions, mineralisation and dry deposition and outputs such as surface runoff, crop uptake, nitrification and volatilisation.

The frozen revision-53 source preserves this split. `Outbal_Init.for` and `Outbal_calc.for` construct liquid NH4 storage from `Conh`/`Rsconh` times represented water storage, with a separate `Conhtop`/`Rsconhtop` additions-reservoir contribution when the selected balance interval starts at layer 0. Soil-complex storage is accumulated from `Cxnh`/`Rscxnh` only over `max(1,Ln1)..Ln2`.

The source-bound mass-balance deviation equation subtracts final liquid and complex storage and includes named external/process terms, but it has no third storage term for a persistent non-aqueous surface continuation mass.

## Consequence for TCD-016-C1

SQ02-SQ05 qualify a chemically noncommittal model-evolution state topology `M_surface_NH4_non_aqueous_continuation [kg N m-2]`, while leaving its process physics unqualified.

That state is semantically neither:

1. soil-solution NH4, because it must remain finite when represented aqueous volume is zero;
2. soil-complex NH4, because revision-53 `Cxnh/Rscxnh` is a soil-layer owner and excludes layer 0 from the complex-storage loops;
3. the `Conhtop/Rsconhtop` virtual additions reservoir, because that reservoir has addition-specific provenance.

Therefore any future implementation of C1 must extend the accounting storage ontology instead of silently folding the continuation mass into an existing legacy storage field.

## Qualified observer contract

For a selected control volume that owns the continuation state, define total represented NH4 storage as:

`S_NH4 = S_aq + S_complex + S_cont`

where `S_cont` is the areic continuation mass converted to the reporting unit exactly once.

A wet-to-continuation transfer and a continuation-to-qualified-receiver transfer are internal transfers. They may change storage partitioning but must not be counted as external input or output. For an isolated transfer:

`S_before = S_after`

exactly under the chosen exact arithmetic oracle.

If future science qualifies an actual loss process from the continuation state, that loss must enter a named process/output term exactly once. It may not be represented simultaneously as disappearance from `S_cont` and as an unexplained balance deviation.

The MassLedger or public balance writer is an observer. It may not synthesize, restore, destroy, or infer the continuation state from a residual.

## Legacy-output compatibility boundary

MASSQ04 does not prescribe a final public variable name or file format. It qualifies only the semantic requirement that the new storage owner be separately observable or be included through an explicitly versioned aggregate whose components remain auditable.

Reusing `BANHST`, `BANHCX`, or `BANHVO` with changed meaning without versioned documentation is not qualified.

## Negative controls

The following are rejected:

- classify continuation mass as soil solution at zero aqueous volume;
- classify continuation mass as soil-complex storage without an admitted surface-to-soil process;
- alias continuation mass to the additions reservoir;
- count wet-to-continuation or continuation-to-receiver transfers as external source/sink terms;
- repair a balance after the fact by assigning unexplained residual to the continuation state;
- infer physical volatilisation, nitrification, sorption or rewetting from an accounting requirement.

## Decision

`QUALIFY_TCD016_C1_EXPLICIT_THIRD_STORAGE_OWNER_AND_INTERNAL_TRANSFER_ACCOUNTING_CONTRACT_FOR_MODEL_EVOLUTION; NO_PROCESS_LAW_OR_B3_ADMISSION`

Historical behavior remains `UNKNOWN_WITHOUT_B2`.
