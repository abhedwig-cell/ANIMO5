# ANIMO-RG05B — Second Atomic B3 Admission Integration

## Purpose

RG05B is a governance-only incremental project-regie update after the qualified TCD-024 B3 admission.

It preserves RG05 and RG05A as historical snapshots and does not rewrite their frozen admission counts.

Authoritative incremental base:

- `ANIMO-RG05A@a4eb1bb1632a573c93b7d44186f7d200a862c6e7`
- `ANIMO-B3D04@a42e1158b3eda670ca08329bc55943c7c6c9d655`

RG05B does not reopen RG05 or RG05A.

## Current atomic B3 admission inventory

The project now has exactly two qualified atomic B3 scientific admissions:

1. `TCD-017`, Class A accounting/reporting correction, admitted by `ANIMO-B3D02@bf31ffa96b4f71541c13d1426ccf48eac9536b24` after independent review `ANIMO-B3A02R@8b38b03ac489c349192ae9fa55a8fe51cea183cb`.
2. `TCD-024`, Class B local algebra/index/species correction, admitted by `ANIMO-B3D04@a42e1158b3eda670ca08329bc55943c7c6c9d655` after independent review `ANIMO-B3B03R@b36aedb4406c3f92d6ee7cd2fa4231ed872620ec`.

Both admissions use the GOV03 historical-uncertainty route. No qualified B2 behavioural reference exists for either claim. Historical behaviour remains `UNKNOWN`; historical fidelity is not claimed.

## TCD-024 bounded admission

The admitted TCD-024 atomic identity is:

```fortran
Yy = One + Parcxsl(3,J) * Avc
```

instead of the legacy slow-Langmuir expression:

```fortran
Yy = One + Parcxsl(3,I) * Avc
```

The scientific claim is limited to binding the site-specific slow-Langmuir affinity parameter to slow-sorption site index `J` rather than nonlinear trial counter `I`.

The supplied frozen natural testbank contains no positive `Optcxsl=2` activation. Positive discrimination is therefore synthetic and exact, while natural `Optcxsl=3` evidence remains a negative control. This limitation remains part of the admission.

TCD-019 is not composed into TCD-024 and remains a separate numerical-policy item.

## Queue effect

Relative to RG05A:

- scientific admissions: `1 -> 2`;
- active canonical TCD queue: `24 -> 23`;
- `WAITING_ON_ROUTE_AND_REVIEW`: `6 -> 5`;
- TCD-024 leaves the active queue and becomes `ADMITTED_B3_WITH_HISTORICAL_UNCERTAINTY`.

All other queue-state counts remain unchanged.

The canonical TCD register remains at 25 top-level entries with tail `TCD-042`. `TCD-043` is not reserved.

## High-level gate state

`G6U` remains:

`ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`

`G7` is now best summarized as:

`TWO_ATOMIC_SCIENTIFIC_ADMISSIONS_B3_INCOMPLETE`

This does not constitute a whole-model B3 baseline.

## Hard boundaries

RG05B performs no production source change, no legacy source change, no frozen-testcase change, no canonical TCD-register change and no evidence-strength promotion.

It authorizes neither B4 nor production migration.

The two admitted atomic corrections are scientific dispositions only. Their production implementation, composition with other admitted corrections, integrated regression qualification and any eventual B4 admission require separate downstream workunits.

## Current project interpretation

The important project-state change is no longer merely that the historical-uncertainty route exists. Two concrete atomic correction claims have now traversed readiness, route reconciliation, independent second-line review and formal B3 admission.

The next high-leverage work should continue to reduce the remaining route/review backlog using genuinely independent second-line reviews for already-mature dossiers. New readiness work should not be started merely to increase activity while mature reviewed candidates remain available.
