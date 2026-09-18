# ANIMO-KT18 Qualification Rationale

Before KT18, the modern bounded application stack could execute real TCD-042 science transactionally, carry its cross-module continuation, checkpoint it, restore it and verify exact split-run behavior, but the application still accepted one already selected hydrology packet as a direct argument.

KT11 already owns exact multi-packet selection, but its public runtime-probe client returns a transaction candidate rather than the selected typed hydrology packet. KT18 adds the smallest read-only seam needed to connect those two existing responsibilities.

The returned object is explicitly a copy. Provider ownership remains immutable, and selection itself has no continuation state.

The selected packet is still revalidated inside the downstream application path by KT06 using the application configuration. This creates a useful defense in depth: provider configuration and application configuration cannot silently diverge.

A positive KT18 qualification means:

`AN_IMMUTABLE_KT11_MULTI_PACKET_PROVIDER_CAN_SELECT_THE_EXACT_PACKET_FOR_THE_CURRENT_ACCEPTED_APPLICATION_INTERVAL_AND_DRIVE_THE_BOUNDED_KT15A_APPLICATION_TO_AN_ATOMIC_COMMIT`.

It does not mean the provider/application composition is centrally admitted, production-ready, or independently reviewed.
