# ANIMO-TIME02 executable vector qualification

Status: `SYNTHETIC_EXECUTABLE_CONTRACT_CHECK_NON_B2`.

TIME02 already selected an exact rational civil-day coordinate from source/testbank analysis. This follow-up adds an executable checker for the persisted `TIME02_TEST_VECTORS.json` so the qualification does not rely only on manually inspected examples.

The checker uses Python integer arithmetic and `fractions.Fraction` for coordinate comparison. It validates Gregorian calendar cases, management `(t0,t1]`, harvest `[t0,t1)`, exact one-second before/after cases, split ownership, changed-`t1` retry identity requirements, hydrology frame exact mismatch rejection, and the source-derived management/noon mappings.

No floating tolerance is used anywhere in event or frame identity. Python `datetime` is used only to construct/validate the finite civil dates in the synthetic vectors; canonical comparison remains exact rational arithmetic.

This executable check is still synthetic contract evidence. It does not execute revision-53 ANIMO, does not compare against a historical binary, does not establish B2, and does not admit canonical TIME. A passing workflow only demonstrates that the persisted candidate contract and vectors are internally executable and mutually consistent.
