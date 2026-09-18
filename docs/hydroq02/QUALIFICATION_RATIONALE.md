# ANIMO-HYDROQ02 Qualification Rationale

HYDROQ02 closes a precise contract gap exposed by UBFORCE02.

The load equations need `Rupr` and `Runinu`. Those are not chemistry variables and are not owned by the load resolver. They are outputs of the hydrology-resolution responsibility.

The frozen source contains an important historical detail: the near-zero runoff branch explicitly resets `Rupr`, `Rurv` and `Ruso`, but does not locally assign `Runinu`. HYDROQ02 therefore does not replace revision-53 behavior with a cleaner formula such as `max(0,-Ru)`.

Instead it creates a typed capture boundary for the values actually produced by one identified hydrology execution and binds those values to an exact interval.

Positive qualification means:

`RUPR_AND_RUNINU_HAVE_AN_EXPLICIT_RESOLVED_HYDROLOGY_CAPTURE_CONTRACT_FOR_TCD042_LOAD_COMPOSITION`.

It does not mean the runoff partition itself has been migrated or repaired.
