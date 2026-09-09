# ANIMO-ARCH07 hydrology adapter qualification test specification

Status: `CANDIDATE_TEST_SPECIFICATION_ONLY`.

## Qualification target

A hydrology adapter is an ownership-safe translator between an external hydrology producer and the ARCH05 `EX-HYDROLOGY` frame. It is not a second hydrology model and must not leak producer implementation conventions into the ANIMO kernel.

## Positive frame families

The future adapter test suite must construct at least:

- a detailed-hydrology frame with matrix begin/end storage, applicable surface stores and interval-integrated transport/water-balance transfers;
- an aggregated-hydrology frame containing only fields admitted for that topology;
- optional snow examples when snow is active;
- producer-native sign examples that are explicitly normalized at the boundary.

A positive frame is valid only when schema, configuration, feature, geometry, physical-layout, exchange-binding, interval and accepted-generation identities all agree.

## Required negative mutation space

For each field that is required under a selected configuration, the runtime adapter qualification harness must be able to mutate the valid fixture one dimension at a time and prove fail-closed rejection for applicable dimensions:

- remove required field;
- add field whose activation condition is false;
- wrong semantic unit;
- wrong layer/interface/domain shape;
- wrong geometry or physical-layout identity;
- stale configuration or exchange-binding identity;
- accepted-start generation mismatch;
- mutation under an existing immutable frame ID.

The purpose is not combinatorial brute force. It is to prove that each contract dimension is actually enforced rather than merely documented.

## Sign convention

ARCH05 sign semantics are canonical. A concrete producer adapter may consume another native convention only when the mapping is explicit in adapter qualification evidence.

The test must use values that distinguish sign reversal from absolute-value handling. The adapter must preserve direction and magnitude according to the separately admitted representation policy. ARCH07 defines no floating-point tolerance.

## Interception seam

TCD-018 showed that interception storage can be omitted by a public legacy balance even when evaporation is represented. Therefore the adapter qualification fixture for detailed hydrology must contain a case with:

- nonzero interception beginning storage;
- nonzero interception ending storage;
- nonzero interception evaporation.

The test is not a corrected-legacy admission. It verifies that a future exchange adapter supplies enough explicit state/transfer information for the candidate control-volume observer to avoid reproducing the interface omission.

## Chemistry separation

Water movement and hydrological storage belong to the hydrology exchange frame. Irrigation/runon/bottom-inflow solute composition, deposition chemistry and management material composition do not.

A negative adapter case must reject or otherwise fail contract validation when undeclared chemistry is smuggled through hydrology-specific fields or producer-private metadata that the kernel would need to interpret.

## Macropore extension

The five `HYD-MP-*` fields are deliberately covered, but current cases are blocked:

- supplying them while macropores are inactive must fail;
- selecting macropores without a matching admission identity must fail;
- a future positive macropore adapter test requires an admitted feature contract plus active scientific case and must exercise storage, infiltration, matrix exchange and direct drainage together.

Passing ordinary matrix hydrology tests does not qualify the macropore extension.

## Read-only ownership

The qualification harness must instrument or otherwise prove that ANIMO cannot mutate the producer-owned hydrology frame or persistent producer state. A rejected ANIMO trial must leave the producer accepted generation unchanged.
