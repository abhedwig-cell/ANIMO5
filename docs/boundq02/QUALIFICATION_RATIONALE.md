# ANIMO-BOUNDQ02 Qualification Rationale

BOUNDQ01 exposed yearly chemistry arrays but deliberately did not select the active year. BOUNDQ02 resolves that missing runtime seam.

A simple "current year -> array slot" implementation would not be source-faithful. Revision-53 refreshes the yearly chemistry scalars on the first interval and then only when the interval origin is exactly 1 January.

BOUNDQ02 therefore introduces an explicit forcing-selection cursor. The cursor is trial-friendly: binding returns a candidate next cursor and never mutates the accepted cursor input.

The exact interval origin is interpreted under the TIME02 proleptic-Gregorian calendar contract. The selected chemistry is bound to an exact interval frame before it can be handed to UBFORCE02.

Dry deposition is carried in the frame but kept separate from the UBFORCE02 wet/advective chemistry forcing.

Positive qualification would mean:

`REV53_STATIC_BOUNDARY_YEAR_SELECTION_AND_INTERVAL_CHEMISTRY_BINDING_HAVE_AN_EXPLICIT_SOURCE_FAITHFUL_NONPRODUCTION_RUNTIME_REALIZATION`.

It would not admit the cursor into canonical state/restart, and it would not open production.
