# ANIMO-IO01 closeout and handoff

Status: `CLOSEOUT_READY_BOUNDED_REPRESENTATION_QUALIFICATION_COMPLETE`

## Work unit

`ANIMO-IO01 — Legacy Text Input Contract Audit, TTUTIL Suitability & Adapter Qualification`

Repository: `abhedwig-cell/ANIMO5`

Branch: `work/animo-io01-legacy-text-input-contracts`

Qualification baseline head before closeout-only reconciliation:

`b45ff9b522155bba5b3ddf555a0f9535593333b9`

The closeout artifacts do not widen the qualified scope and do not admit production migration.

## Closeout decision

ANIMO-IO01 is complete for its bounded objective.

Decision:

`QUALIFIED_LEGACY_INPUT_CONTRACT_TTUTIL_SOURCE_DIRECT_AND_BOUNDED_MATERIAL_REPRESENTATION_PILOTS`

This means that IO01 has:

1. inventoried and classified the revision-53 input families;
2. separated parser/normalization semantics from scientific model semantics;
3. pinned the exact official TTUTIL 4.27 source carried by the supplied SWAP 4.3.1 distribution;
4. qualified a bounded DIRECT/animo.ini representation candidate;
5. qualified a bounded non-GHG Ruurlo MATERIAL representation candidate;
6. recorded negative numerical evidence against using TTUTIL DOUBLE as field-exact numeric authority for MATERIAL;
7. routed remaining legacy runtime/storage hazards to the appropriate runtime/governance streams rather than normalizing them away.

IO01 does **not** qualify a production-wide TTUTIL adapter and does **not** authorize migration of all legacy ANIMO input.

## Authority and frozen identities

The work unit started from RG02 G5 head:

`12ae76b23728d75fc6ca746ca1c67aa26e0ec005`

Referenced authority heads:

- PREP01-05: `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`
- TQ01: `5c43ee16df37a0a1357614fdec527f25e5ca8c16`
- ARCH05: `99b6098a19db405ce34928af89bb78b856dce7cd`
- ARCH06: `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4`
- ARCH07: `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`

Frozen B0 identities used by IO01:

- ANIMO revision-53 source ZIP SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- ANIMO testbank ZIP SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- supplied ANIMO documentation SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

No frozen B0 bytes were changed.

## TTUTIL source admission

Official SWAP distribution identity:

- SWAP 4.3.1 package SHA-256: `2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`
- embedded archive: `SWAP_4.3.1/tools/SWAP/source/TTUTIL.ZIP`
- embedded TTUTIL ZIP SHA-256: `ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193`
- TTUTIL version: `4.27`
- embedded file count: `168`
- Fortran compilation units: `153`
- per-file manifest: `integration/animo-io/TTUTIL-4.27-SHA256SUMS.txt`
- fail-closed materializer: `tools/materialize_ttutil427.py`

The public `SWAP-model/ttutil` repository remains reference-only because it is not byte-identical to the official embedded source.

The official TTUTIL source is not vendored into ANIMO5. Qualification runners require a user-supplied, hash-matching SWAP distribution and materialize TTUTIL into a temporary execution tree.

## Admitted qualification claims

| Claim | Status | Evidence |
|---|---|---|
| Revision-53 input-family contract inventory | `QUALIFIED` | `integration/animo-io/ANIMO_INPUT_CONTRACT_MATRIX.csv` |
| Defaults and error-contract inventory | `QUALIFIED` | `docs/io/INPUT_DEFAULTS_REGISTER.csv`, `docs/io/INPUT_ERROR_CONTRACT.md` |
| Official TTUTIL 4.27 source provenance | `QUALIFIED` | `docs/io/TTUTIL_SOURCE_PROVENANCE.md`, `integration/animo-io/TTUTIL-4.27-SHA256SUMS.txt` |
| TTUTIL compile/smoke feasibility | `QUALIFIED_BOUNDED` | 153 units compiled; RDINIT/RDSINT smoke passed |
| Legacy/native adapter separation | `QUALIFIED_POLICY` | `docs/io/TTUTIL_ADAPTER_POLICY.md` |
| DIRECT Pilot A | `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE` | `integration/animo-io/DIRECT-PILOT-QUALIFICATION.json` |
| Ruurlo old/full vs revision-53 sparse MATERIAL lineage | `QUALIFIED_NATURAL_LINEAGE_EVIDENCE` | `integration/animo-io/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json` |
| MATERIAL Pilot B | `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE_WITH_RUNTIME_HAZARD_EXCLUSIONS` | `integration/animo-io/MATERIAL-PILOT-B-QUALIFICATION.json` |
| Ruurlo omitted sparse FR/FRca cells normalize to zero | `QUALIFIED_FOR_RUURLO_LINEAGE` | exact old/full versus new/sparse equality after zero fill |
| MATERIAL exact numeric transport | `QUALIFIED_FOR_PILOT_B` | TTUTIL CHARACTER tokens plus explicit Fortran REAL(8) conversion, no tolerance |
| Direct TTUTIL DOUBLE numeric authority for MATERIAL | `REJECTED_FOR_FIELD_EXACT_REPRESENTATION` | 26 Ruurlo numeric leaves differ by one binary64 ULP |

DIRECT Pilot A covers 10 natural `animo.ini` instances and passes 10/10 field-exact semantic projection checks. Its GHGMais coverage is routing-only and does not admit the GHG schema.

MATERIAL Pilot B is restricted to `RuurloGrass` with `IPO=0`, `Ioptae=0`, and `IoptGHG=0`. No model physics is executed by the representation qualification.

## Explicit non-admissions

The following are **not admitted** by ANIMO-IO01:

- a generic production TTUTIL runtime adapter;
- production input migration;
- GENERAL migration or relaxation of its revision-53 sequential ordering contract;
- generic MATERIAL admission beyond the qualified Ruurlo non-GHG feature scope;
- GHG schema normalization or GHGMais schema migration;
- SOIL, PLANT, BOUNDARY or CHEMISTRY production migration;
- INITIAL or restart/checkpoint migration to generic configuration parsing;
- MANAGEMENT migration to generic TTUTIL parsing;
- external crop forcing or soil-temperature forcing migration to generic TTUTIL parsing;
- WATBAL configuration migration to generic TTUTIL parsing;
- binary hydrology conversion to TTUTIL;
- model-output equivalence from the parser-only pilots;
- scientific equation or parameter-policy changes;
- B4 admission;
- canonical merge or production activation solely on the basis of IO01.

Any extension to another input family or feature variant requires a separately scoped qualification work unit or an explicit governance decision. It should not silently expand IO01 after closeout.

## Runtime hazards handed off

### MAT-RH-001: sparse FR/FRca omitted-cell storage mechanism

Qualified intended normalized semantics for the Ruurlo lineage:

`OMITTED_SPARSE_CELL_IS_ZERO_FOR_QUALIFIED_RUURLO_LINEAGE`

Not qualified in IO01:

legacy storage/runtime mechanism by which omitted cells happened to acquire values before full-array validation.

Route: ANIMO-BUILDQ01, with canonical discrepancy intake through B3I01 if required.

### MAT-RH-002: IPO=0 Pofr range-check state

Qualified input semantics for Pilot B:

`Pofr = FEATURE_INACTIVE_NULL`

Not input-defined in revision 53:

the runtime value subsequently range-checked after a zero-element implied-DO read.

Route: ANIMO-BUILDQ01, with canonical discrepancy intake through B3I01 if required.

IO01 assigns no canonical TCD number to either hazard.

## Reproduction

Structural and unit qualification:

```bash
python tools/audit_io01_contracts.py
python -m unittest discover -s tests/io -p 'test_*.py'
```

Natural Ruurlo old/full versus sparse lineage audit:

```bash
python tools/audit_material_ruurlo_lineage.py \
  /path/to/ANIMO_testbank.zip \
  --output /tmp/MATERIAL-RUURLO-LINEAGE-EQUIVALENCE.json
```

DIRECT Pilot A from frozen user-supplied archives:

```bash
python tools/qualify_io01_direct_pilot.py \
  --swap-zip /path/to/SWAP_4.3.1.zip \
  --testbank-zip /path/to/ANIMO_testbank.zip \
  --output /tmp/DIRECT-PILOT-QUALIFICATION.json
```

MATERIAL Pilot B from frozen user-supplied archives:

```bash
python tools/qualify_io01_material_pilot.py \
  --swap-zip /path/to/SWAP_4.3.1.zip \
  --testbank-zip /path/to/ANIMO_testbank.zip \
  --output /tmp/MATERIAL-PILOT-B-QUALIFICATION.json
```

The runners fail closed on archive identity mismatches. They do not download TTUTIL and do not edit frozen source or testbank archives.

## Closeout CI baseline

The qualification baseline head `b45ff9b522155bba5b3ddf555a0f9535593333b9` completed the `IO01 input-contract audit` workflow successfully in GitHub Actions run `34337491169`.

Subsequent closeout-only commits must keep the same audit green and may not weaken the admitted/non-admitted boundaries above.

## Handoff

Primary handoff destinations:

- `ANIMO-BUILDQ01`: qualify MAT-RH-001 and MAT-RH-002 runtime/storage semantics;
- `ANIMO-B3I01`: canonical discrepancy intake/routing if either hazard qualifies as a discrepancy requiring canonical tracking;
- architecture/governance: consume `LegacyInputBinding/v1` and `MaterialParameterSet/v1` only as bounded candidate representations, not production contracts;
- any future input migration stream: start from the family-specific IO01 contract matrix and preserve strict legacy-vs-native representation separation.

## Final boundary

ANIMO-IO01 is closed as a qualification/evidence work unit.

Its useful result is not that “ANIMO input has been converted to TTUTIL”. The result is narrower and stronger: exact source provenance is pinned, legacy parsing contracts are explicit, two bounded representation candidates are qualified, known non-equivalences are preserved as negative evidence, and unresolved runtime hazards are handed off without being hidden by parser normalization.
