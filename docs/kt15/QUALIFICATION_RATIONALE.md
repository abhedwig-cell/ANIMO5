# ANIMO-KT15 Qualification Rationale

STATEQ11 qualified the identity of the accepted cross-module continuation but deliberately did not implement an atomic group commit. KT14B qualified one opaque content-bound boundary frame driving one bounded TCD-042 science interval but deliberately did not own continuation publication.

KT15 joins those two responsibilities without redefining either.

The key implementation property is that KT14B is invoked against `working%science_store`, not the externally visible accepted store. The candidate next boundary cursor and hydrology continuation are likewise held off to the side. Only after their generation, lineage and time identity match the working accepted science store is the whole application aggregate published.

This directly prevents the failure mode in which science advances while the boundary cursor or hydrology origin remains old, or vice versa.

The two-interval test verifies that the accepted aggregate can advance coherently from generation 0 to 1 to 2. A rejection test verifies that a successfully prepared boundary candidate is not externally published when downstream TCD-042 science rejects.

A positive KT15 qualification means:

`THE_BOUNDED_NONPRODUCTION_TCD042_APPLICATION_CAN_PUBLISH_SCIENCE_AND_ITS_REQUIRED_CROSS_MODULE_CONTINUATION_AS_ONE_LOGICAL_ACCEPTED_GROUP`.

It does not admit those continuation fields to the canonical production state or checkpoint schema.
