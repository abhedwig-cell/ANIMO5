# ANIMO-B3D04 — TCD-024 B3 Admission Closeout

Target: `TCD-024`

Class: `B_LOCAL_ALGEBRA_INDEX_SPECIES`

Admission route: `INDEPENDENT_SCIENTIFIC_ADMISSION_WITH_HISTORICAL_UNCERTAINTY`

## Atomic correction admitted

Legacy expression:

```fortran
Yy = One + Parcxsl(3,I) * Avc
```

Admitted scientific correction identity:

```fortran
Yy = One + Parcxsl(3,J) * Avc
```

The admitted claim is only that the site-specific slow-Langmuir affinity belongs to slow-sorption site index `J`, not nonlinear trial counter `I`, in the local `Conc_unl` slow-Langmuir kinetic exponent.

## Authorities

- route reconciliation: `ANIMO-B3D03@a3e194573b3a7ce95d5ef15fc179ddb3a613d8a6`;
- readiness: `ANIMO-B3B03@446f57f3aeff6e7db56ce473f0724bdb58cad94f`;
- independent second line: `ANIMO-B3B03R@b36aedb4406c3f92d6ee7cd2fa4231ed872620ec`;
- historical acquisition closure: `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`;
- B3 framework: `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

The independent review ran in a separate ChatGPT context from the B3B03/B3D03 authoring context and passed. No organizational or human independence is claimed.

## Evidence basis

The wrong selector is source-bound to the frozen `Transorp.for` member and the correct ownership is demonstrated by the slow-site loop/index domain. Unequal-site synthetic fixtures make `I` versus `J` numerically discriminating. Independent high-precision recomputation verifies the site-state and site-transfer consequences and the isolated multi-site storage/counter-transfer conservation identity closes exactly.

The supplied natural frozen testbank does **not** contain positive `Optcxsl=2` activation. It does provide the required inactive-route negative control because the active-P cases use `Optcxsl=3`. The positive evidence is therefore synthetic and exact. This is sufficient for the bounded local scientific identity, but it does not establish natural historical prevalence.

## Expected difference

When `Optcxsl == 2` and the affected slow-site kinetic update is reached, the admitted correction may change:

- the site-J relaxation factor `Yy` when the site-specific affinity differs from the value selected through `I`;
- affected slow-sorbed P site state;
- site-local slow-sorption transfer;
- dissolved PO4-P and other P states and reports downstream through the already-existing conservation coupling.

It does not admit changes to:

- the nonlinear trial loop or its ordering;
- the slow-site loop or its ordering;
- `Recf(J)` rate ownership;
- input parameter values;
- TCD-019 finite-change, stopping or convergence policy;
- solver tolerances or clipping thresholds;
- `Optcxsl=1` or `Optcxsl=3` constitutive routes;
- inactive zero-rate-site identity;
- hydrology;
- C/N families outside existing P coupling.

## Historical uncertainty

No qualified B2 behavioural reference exists. Historical revision-53 prevalence and behavioural effect of the `Optcxsl=2` defect therefore remain `UNKNOWN`.

This admission is deliberately not a historical-fidelity claim. It does not state that an unavailable historical executable behaved in a particular way, and it does not infer prevalence from the synthetic fixture.

## Admission decision

`ADMIT_TCD024_ATOMIC_CLASS_B_SCIENTIFIC_INDEX_CORRECTION_WITH_HISTORICAL_UNCERTAINTY`

Canonical disposition:

`HISTORICAL_BEHAVIOUR_UNKNOWN_SCIENTIFIC_ADMISSION_WITH_UNCERTAINTY`

This is an atomic B3 scientific admission only. It does **not** authorize a production patch, TCD-019 composition, B4 composition, whole-model equivalence, canonical-register mutation or production migration.
