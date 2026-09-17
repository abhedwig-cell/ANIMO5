# ANIMO-KT05 Work Unit Contract

Workunit: `ANIMO-KT05 — Explicit-State Hydrology Runtime Interval Binding`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE`.

## Purpose

KT05 continues only the safe explicit-state architecture line while KT03F01 Hlpimp=1 interception semantics remain blocked on GOV04 Tier C independent review.

The bounded question is:

> Can the frozen KT02 model-neutral interval runtime drive an ANIMO adapter attempt with a KT03-compatible explicit hydrology forcing view while keeping runtime time authoritative and keeping forcing outside accepted scientific continuation state?

KT05 consumes:

- `ANIMO-KT02@1f88db4dc87fc4d93075884ac35a59711f0725bf`;
- KT02 frozen executable head `1909709e7a244b5d0ee53342a26bab74815c118c`;
- `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- frozen KT03 hydrology contract implementation `e844c7658a95819fc0463c55737f9bd41b29a6da`.

KT05 does **not** consume KT03F01 as qualified authority.

## Bounded mapping rule

The first proof deliberately accepts only producer-time metadata that are exact whole-day integers in REAL64 and only exact whole-day KT02 runtime coordinates. A nonnegative integer adapter offset maps runtime day index to producer day coordinate.

This avoids introducing an epsilon policy or allowing producer floating time to become runtime authority.

The bounded gate is:

- exact runtime interval: `origin_day -> endpoint_day`;
- producer step metadata equals `endpoint_day - origin_day` exactly;
- producer endpoint metadata equals `endpoint_day + configured_offset` exactly;
- subday runtime or fractional producer metadata fails closed.

This is intentionally narrower than the full KT03 real-file envelope. It is an architecture proof, not a general time-mapping qualification.

## Ownership

KT02 runtime owns accepted time, trial origin, endpoint request and commit/reject mechanics.

The hydrology binding is interval forcing. It is not accepted continuation state and cannot advance time, select retry, choose timestep scale or commit itself.

The ANIMO runtime-probe accepted payload contains only a state token. Explicit hydrology forcing is held by the client adapter outside that payload.

## Explicit-state dependency

KT05 uses only the already explicit interception-state capability corresponding to the KT03 Hlpimp=11 envelope. The forcing view requires an explicit interception-storage endpoint. Missing interception state fails closed.

No Hlpimp=1 absent-state rule is executed or inferred.

## Governance

Because this work introduces runtime interval binding that can alter model behaviour if wrong, the candidate review tier is GOV04 Tier C. Implementation and CI may proceed in this isolated branch, but positive qualification/closeout requires genuinely independent second-line review.

## Exclusions

No production source changes, no Hlpimp=1 or Hlpimp=2 semantics, no full HydrologyStep field transport, no Hydro_detailed science, no Modflux/transport equivalence, no retry/timestep policy, no subday mapping, no B2 historical claim, no B3/B4 admission, no shared production runtime library and no Status A/AA claim.
