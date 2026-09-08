# Precision policy baseline

## Legacy precision

Status: `NOT_ASSESSED_SOURCE_UNAVAILABLE`.

Testcase text contains decimal and exponential values, but file formatting does not establish internal Fortran precision. PREP01 therefore makes no claim about use of default REAL, DOUBLE PRECISION, REAL*8, or explicit kinds in legacy ANIMO.

## Provisional ANIMO5 reference policy

This is an architecture policy, not a migrated implementation:

- canonical scientific/reference computation should be conservative toward `real64` until evidence supports another choice;
- mass accounting must not be reduced in precision without qualification evidence;
- exchange precision must be explicit in interface contracts;
- FP32 or mixed precision may only be introduced as an explicit numerical policy with reference qualification;
- precision changes must be separated from physics changes where practical.
