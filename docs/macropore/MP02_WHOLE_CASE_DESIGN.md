# ANIMO-MP02 whole-case diagnostic design

Decision scope: complete-case B1 activation only. No descendant produced here is historical B2 evidence.

## 1. Parent and frozen evidence

All diagnostics descend from the supplied `CranGrass` case in the frozen ANIMO testbank.

Frozen identities:

- revision-53 source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The frozen artifacts are not modified. Each run is prepared in an execution copy. Runtime-only GNU adaptations are the already documented path-separator, case-insensitive path, `PrintBalLabel`, and sequential-unformatted framing adaptations.

`CranGrass` is suitable because it already uses detailed hydrology and has phosphorus enabled, while its historical macropore switches are off. The positive transform therefore makes the activation delta explicit rather than changing the entire scientific case.

## 2. Common positive activation transform

The common positive transform is intentionally small and deterministic:

- `MacroPoreOption: 0 -> 1` in the active `GENERAL.INP`;
- hydrology `Hlpimp: 1 -> 2`;
- `>MPfrac:` with `FrMpRuRv=0` and `FrMpDrSo=0`;
- explicit `>MPnitr:`, `>MPorgs:` and `>MPphos:` initial macropore concentrations;
- two nonzero macropore domains in the hydrology record stream;
- Main Bypass initial water storage `5e-5 m` in a static volume of `1e-4 m`;
- Internal Catchment initial water storage `2.5e-5 m` in a static volume of `2.5e-5 m`;
- wet-wall fractions chosen so revision-53 derives `Nd=2` without relying on an edge-case zero-domain geometry.

Hydrology default-`REAL` macropore records are encoded as eight-byte values because the qualified GNU diagnostic build uses `-fdefault-real-8`. Treating those records as four-byte values was rejected during preparation because revision-53 then reads past the logical record boundary. This is execution-contract evidence, not historical format authority.

## 3. Cases

### MP02-NO-MP

Exact B0 scientific inputs, with only the existing GNU runtime adapter. This is the negative control.

### MP02-STORAGE

Active two-domain macropore state with no deliberately injected exchange or direct drainage event. It tests complete-case reachability of macropore storage and the associated source-defined `MpWfps` coupling. It is not a claim that macropore storage is chemically inert: `MAPOHYDRO` includes macropore water in `MpWfps`, so an active stored-water state can alter downstream reaction conditions even when explicit exchange fluxes are zero.

### MP02-EXCHANGE

At the first simulated timestep, `2e-5 m d-1` is transferred from matrix layer 2 into Internal Catchment domain 2. Domain-2 storage is increased by the same `2e-5 m`. This is a closed internal water transfer by construction.

### MP02-DIRECT-DRAIN

At the first simulated timestep, `2e-5 m d-1` leaves Main Bypass domain 1 through direct drainage. Domain-1 storage is reduced by the same amount. `FrMpDrSo=0`, so the designed event targets the direct macropore drainage path rather than routing the event through soil drainage.

### MP02-SOLUTE-N and MP02-SOLUTE-P

The implemented transforms for these two labels are identical: matrix-to-domain2 transfer at timestep 1 followed by domain2-to-matrix transfer at timestep 2. Because the parent is already P-active and the generic macropore kernel transports all enabled species, the two labels do not constitute independent N-only and P-only experiments.

They are therefore reconciled as:

`ONE_COMBINED_N_P_TRANSFER_DIAGNOSTIC_PLUS_ONE_EXACT_INPUT_REPLICATE`

This correction matters. Counting the labels as two independent species qualifications would overstate the evidence.

## 4. Expected evidence

A positive case counts as complete-case B1 evidence only if:

1. the complete ANIMO simulation reaches successful completion;
2. revision-53 reports macropore iteration activity;
3. the intended hydrological event is present in the transform manifest;
4. no specialized macropore water or solute balance warning is emitted;
5. conclusions remain limited to the exercised synthetic path.

A pass does not establish historical prevalence, realistic parameter magnitude, a historical numerical oracle, B2, B3, or production readiness.

## 5. TCD-025 observer logic

MP02 does not correct `Outbal_calc`.

The diagnostic compares the specialized active route with the existing public balance observers. Under TCD-025, the important question is not whether every public residual must become nonzero. A public ledger that omits both a macropore storage change and its paired external direct drain can remain numerically quiet while still representing an incomplete control volume.

For matrix-to-macropore exchange, the stronger symptom is expected: matrix solute storage changes while corresponding macropore storage is absent from the public ledger, so the public species residual can move even though the specialized combined macropore balance closes.

## 6. Restart check

A complete active case also permits a direct output check of `Output/initial.out`. The qualification question is whether end-state macropore solute concentrations are serialized into the persistent restart file. This is separate from in-memory timestep promotion in `Init.for`.
