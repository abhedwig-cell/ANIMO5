# ANIMO-STATEQ01 checkpoint contract surface/restricted-core addendum

Status: `QUALIFIED_CONTRACT_ADDENDUM_NOT_STATE_ADMISSION`

This addendum narrows `CHECKPOINT_COMPLETENESS_CONTRACT.md` after source qualification of the surface transport predicates.

## 1. General core versus restricted core

The checkpoint completeness predicate is profile-scoped.

For `CORE_CNP`, layer-0 surface transport is in scope. `checkpoint_complete(CORE_CNP)` is false while either of the following remains open:

- TCD-016-C1, the unresolved NH4 low-storage continuation science;
- `RG02-LCL-LAYER0-AQUEOUS-RESTART-INIT-ZEROING`, the local source-confirmed restart initialization finding.

For `CORE_CNP_SUBSURFACE_ONLY`, layer-0 state is excluded by a source-bound application envelope. The restricted profile is eligible for later checkpoint testing only when all incoming layer-0 restart coordinates are zero and the bound hydrology start/end surface storage is exactly zero.

## 2. Source-bound restricted envelope

Aggregated hydrology:

```text
Pn == 0
Pnt == 0
```

Detailed hydrology:

```text
Pn + Snla == 0
Pnt + Snt == 0
```

These equalities are stricter than the legacy `Flpn` threshold because a checkpoint profile may not hide positive physical storage below a process activation tolerance.

## 3. Upper-boundary reservoirs remain core

`Con*top/Rscon*top` reservoirs remain physical continuation coordinates inside the restricted profile. `UBoundconc` evolves them when no surface compartment is active, and transport uses them as the upper boundary concentration for soil layer 1.

They are not a substitute for layer-0 state and are not an optional feature that can be removed from the core checkpoint merely because `Flpn=0`.

## 4. Restore failure boundary

Restricted-core restore must fail before accepted-state construction if:

- any layer-0 restart coordinate is nonzero;
- surface hydrology coordinates needed by the envelope are unavailable;
- the accepted or candidate hydrology frame has positive surface storage;
- restoring would require clipping, zeroing, projection or remapping of layer-0 mass.

The unadmitted SQ01 non-aqueous NH4 continuation proposal may not be synthesized during restore.

## 5. Trial failure boundary

The guard is evaluated after exact hydrology frame binding and before chemistry/management mutation. A candidate interval that would leave the zero-surface envelope is rejected and cannot be promoted to accepted state under the restricted profile.

## 6. Qualification dependency

Restricted-core checkpoint evidence cannot be submitted for B3 review until:

1. the fail-closed guard is implemented in a diagnostic/admission harness;
2. positive-surface-storage and nonzero-layer0-restart sentinels prove failure before mutation;
3. uninterrupted versus split-run tests pass inside the envelope;
4. upper-boundary reservoir continuity is explicitly exercised;
5. management cursor continuation is qualified.

This addendum changes no physics and grants no admission.
