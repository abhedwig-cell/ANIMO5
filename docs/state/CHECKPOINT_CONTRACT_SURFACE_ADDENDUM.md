# ANIMO-STATEQ01 checkpoint contract surface/restricted-core addendum

Status: `QUALIFIED_CONTRACT_ADDENDUM_NOT_STATE_ADMISSION`

This addendum narrows the interpretation of `CHECKPOINT_COMPLETENESS_CONTRACT.md` after the surface-state scope correction.

## 1. General core versus restricted core

The checkpoint completeness predicate is profile-scoped.

For `CORE_CNP`, layer-0 aqueous solute activation is in scope. Because TCD-016-C1 leaves NH4 continuation incomplete across low-storage deactivation, `checkpoint_complete(CORE_CNP)` is false until the missing-state science is admitted and its restore semantics are separately qualified.

For `CORE_CNP_SUBSURFACE_ONLY`, layer-0 aqueous solute activation is excluded by an explicit application-envelope invariant. The profile can be used for later checkpoint testing only after that invariant has been source-qualified and shown to fail closed before physical mutation.

A zero initial layer-0 concentration is not enough to establish the restricted envelope.

## 2. Addition reservoirs are separate

`Con*top/Rscon*top` management/addition reservoirs are distinct persistent coordinates. They are not the layer-0 aqueous state and are not a substitute for TCD-016 dry/non-aqueous continuation.

A checkpoint profile that includes addition reservoirs must serialize their accepted state when active, but doing so does not make general layer-0 NH4 continuation complete.

## 3. Restore failure boundary

For the restricted core, restore and trial execution must fail closed if exact accepted hydrology/configuration/event information cannot prove that layer-0 aqueous solute state remains outside the profile envelope.

No restore path may:

- discard residual layer-0 mass;
- map it into an addition reservoir;
- synthesize the unadmitted SQ01 non-aqueous continuation state;
- continue under the restricted profile after layer-0 activation becomes possible.

## 4. Qualification dependency

The restricted profile remains structurally incomplete for B3 purposes until:

1. source predicates for layer-0 activation are qualified;
2. the fail-closed envelope guard is specified;
3. uninterrupted versus split-run tests are executed inside that envelope;
4. deliberate envelope-violation sentinels prove no invalid state can be accepted.

This addendum changes no physics and grants no admission.
