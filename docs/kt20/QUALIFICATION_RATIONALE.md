# ANIMO-KT20 Qualification Rationale

KT19 proved that the exact pinned LWKM SWATRE.UNF bytes can be reconstructed as the complete KT08 immutable packet sequence. KT18 separately proved that KT11 packet selection can drive the bounded accepted application.

The remaining technical gap is that KT19 is currently a Python file/provider adapter while KT18 consumes the Fortran normalized packet type.

KT20 closes only that seam.

The packet frame deliberately uses exact binary64 identities instead of textual decimals. The Python side retains authority for the KT03 JSON typed-step digest and verifies a full frame roundtrip against it. The Fortran side reconstructs the same field values bit-for-bit and reuses KT05 validation before the packet enters KT11.

The first real LWKM packet is intentionally a negative application case. It can be materially real at the provider seam while still remaining outside the current bounded TCD-042 science envelope. Rejecting it without mutating accepted application state demonstrates that evidence provenance and scientific admission remain separate.

A synthetic bounded packet then demonstrates that the same bridge mechanics can reach a successful KT18 atomic application commit.

A positive KT20 qualification may establish only:

`EXACT_KT19_NORMALIZED_PACKET_VALUES_CAN_CROSS_THE_NONPRODUCTION_PYTHON_FORTRAN_ADAPTER_SEAM_AND_ENTER_KT18_WITH_FAIL_CLOSED_APPLICATION_SEMANTICS`.

It does not establish whole-source accepted scientific execution, B2 equivalence, a production ABI or central provider admission.
