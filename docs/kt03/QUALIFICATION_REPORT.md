# ANIMO-KT03 Qualification Report

## Disposition

KT03 supports a bounded positive result for the **defined CranMais file-to-typed hydrology boundary**, and a bounded negative result for **full downstream `Hydro_detailed` compatibility**.

Exact qualification statement:

`QUALIFIED_NONPRODUCTION_CRANMAIS_FILE_TO_TYPED_HYDROLOGY_FIELDS_WITH_FULL_DOWNSTREAM_COMPATIBILITY_BLOCKED_BY_UNDEFINED_SICT_FOR_HLPIMP_1`

This is an architecture/adapter qualification only. It does not change ANIMO scientific equations, B3 admission, B4, production source, SWAP5 production coupling, Status A or Status AA.

## Frozen executable/prototype target

- branch: `work/animo-kt03-real-hydrology-adapter`;
- prototype head: `6b6a263239184d710d6e57e8826353d3ea038360`;
- exact-head GitHub Actions run: `35281025858`;
- CI conclusion: `SUCCESS`;
- frozen CranMais `Swatre.unf` SHA-256: `538827d517f7be4c060e2d62131e1942f8e0e76fdeae49dc0268486984cc9eaf`.

The exact-head CI executes the synthetic adapter-contract tests. The frozen CranMais binary itself is not stored in the public repository; its byte-derived probe metadata is retained in `reference/kt03/CRANMAIS_HYDROLOGY_PROBE.json`.

## Qualified adapter evidence

Within the frozen CranMais layout, the probe establishes:

- PowerStation framing can be consumed using the already existing fail-closed logical-record parser;
- static layout is `Hlpimp=1`, 22 layers, 5 horizons and 0 drainage systems;
- the dynamic stream has 3287 timesteps and exactly 8 logical records per timestep;
- the dynamic tail contains 26296 logical records;
- the diagnostic parser observes exact `Tiwa=1..3287` and `St=1` throughout the case;
- no groundwater sentinel below `-9.98` occurs in this frozen case;
- the initial temperature record selects the legacy `Ioptte=0` path;
- file-backed values can be represented by an explicit typed `HydrologyStep` without ANIMO chemistry/process state;
- layout, dimensions, non-finite values, missing provenance and groundwater-sentinel normalization fail closed;
- an independently constructed typed packet can use the same contract as a file-backed packet;
- local-only SWAP3 records read into `Soco`, `Lai`, `Dpro`, `Hecr`, `Avdate` and `SDum` are validated as legacy stream grammar but are not incorrectly promoted into the shared typed coupling API.

The raw dynamic logical-payload SHA-256 recorded by the bounded probe is:

`e68c1056fa241a1daec8c78cd0279c0f0a5af1aeed2c1d63589adee4ef01808c`.

## Normalization boundary

The prototype includes a diagnostic reimplementation of the revision-53 `Dble_trunc` intent so the file-to-typed seam can be exercised.

This is explicitly classified as:

`B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`

because historical Intel intrinsic/build semantics are not independently recovered by KT03. The result must not be promoted to B2 historical compiler equivalence.

## Material blocker

`KT03-F01` is material to the final downstream seam.

For CranMais `Hlpimp=1`, the dynamic first record has 18 REAL(4) values and does not contain `sSict`. Revision-53 `Input_hydro` nevertheless assigns `Sict` from `sSict`, and `Hydro_detailed` uses `(Sict-Sic)` in the SWAP3 water-balance equations.

KT03 therefore refuses to synthesize `Sict` and represents interception-storage availability explicitly as false. Calling the prototype compatibility gate for `Hydro_detailed` fails closed.

This means requirement 4 of the KT03 work-unit contract, full downstream call compatibility with every required input defined, is not positively satisfied for the selected case.

## Requirement disposition

1. Exact source-to-field provenance for the selected SWATRE timestep representation: **PASS within frozen CranMais layout**.
2. Typed carrier with no ANIMO chemical/process state: **PASS**.
3. File-backed and independently supplied typed packet contract: **PASS in bounded prototype tests**.
4. Downstream `Hydro_detailed` compatibility without scientific rewrite: **BLOCKED by KT03-F01 / undefined Sict**.
5. Bounded CranMais probe with classified differences: **PASS for input-boundary reconstruction; downstream replay not claimed**.
6. No parser cursor/file handle in accepted scientific continuation state: **PASS by carrier structure**.
7. No KT02 model-neutral runtime dependency on file grammar: **PASS; KT03 code is outside `prototype/kt02/runtime/`**.
8. Fail-closed dimension/layout/provenance mismatch: **PASS in exact-head CI**.

## Review status

No claim of independent review is made. This qualification is authoring-agent evidence plus exact-head CI. Before any production or scientific admission step, the material `Sict` finding requires a separate scientific/source disposition under the appropriate authority.

## Conclusion

The architecture decision survives its first real ANIMO file boundary: the legacy file grammar can be isolated behind a typed hydrology packet without leaking ANIMO chemistry or SWAP solver policy into the shared runtime.

The test also demonstrates why the adapter must fail closed. A real legacy ambiguity appears exactly at the file/science seam. The architecture exposes it rather than burying it in a compatibility shim.
