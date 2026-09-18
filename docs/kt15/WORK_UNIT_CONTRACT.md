# ANIMO-KT15 Work Unit Contract

Workunit: `ANIMO-KT15 - Atomic Composite Application Commit for Bounded TCD-042 Execution`.

Execution discipline: `RECONCILE -> AUTHORITY BINDING -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT15 implements one logical application-level transaction over the already qualified bounded components:

`accepted science store + hydrology continuation + Runinu continuation + boundary cursor`.

For one interval, KT15 creates all candidate outputs on a private application-state copy and publishes the full validated aggregate only after science and continuation coherence pass.

## Authorities

- Program: `ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`
- Composite continuation identity: `ANIMO-STATEQ11@c2bd0d17ac6921fcd9f22d6289a510cae454153d`
- Opaque boundary frame: `ANIMO-BOUNDQ02B@de6eef3122354e74405ff9c92286794714bdee82`
- Opaque boundary science composition: `ANIMO-KT14B@46e9e7397be751f245069033bae655b4382b63bd`
- Remediated TCD-042 composition beneath KT14B: `ANIMO-KT13A@df2310cc69e3fe16187ba2235843222f8acfb726`

KT14B exact-final CI authority: run `35375383770 -> success`.

## Logical atomic group

The externally visible KT15 state contains:

1. the KT02 accepted science store;
2. the STATEQ11 composite continuation.

STATEQ11 binds the same lineage, generation and accepted time to:

- detailed hydrology origin state;
- explicit `Runinu` call-entry continuation;
- static-boundary year cursor.

KT15 requires this identity to match the accepted science store before execution.

## Interval execution

For each interval KT15:

1. validates the accepted application aggregate;
2. reconstructs the HYDROEXEC01 start context from accepted continuation plus static hydrology configuration;
3. creates a BOUNDQ02B opaque content-bound frame and a candidate next boundary cursor;
4. deep-copies the accepted application aggregate to private working state;
5. runs KT14B science only against the private working science store;
6. creates the candidate next STATEQ11 continuation from accepted endpoint values, resolved `Runinu` and candidate boundary cursor;
7. validates candidate continuation against the working accepted science store;
8. validates the complete working application aggregate;
9. publishes the aggregate by one derived-type assignment `state = working`.

No externally visible science store, hydrology continuation or boundary cursor is mutated before step 9.

This is logical model-instance atomicity. It is not a claim about lock-free thread atomicity or distributed transactions.

## Opaque forcing identity

KT15 accepts a canonical lowercase SHA-256 string as boundary content identity and passes it to BOUNDQ02B.

KT15 does not hash or verify source file bytes.

The content identity is preserved in the trace and in the BOUNDQ02B forcing identity.

## Multi-interval bounded qualification

KT15 tests two consecutive accepted intervals using the published continuation from interval 1 as the origin for interval 2.

This qualifies bounded in-memory application continuation through:

- science generation;
- accepted time;
- hydrology endpoint-to-origin transfer;
- explicit Runinu continuation;
- static-boundary cursor continuation.

It does not qualify restart serialization, canonical checkpoint admission or production orchestration.

## Failure atomicity

A candidate boundary cursor may be constructed before science.

If science subsequently rejects, the external application aggregate must retain:

- original science generation and payload;
- original accepted time;
- original hydrology continuation;
- original Runinu continuation;
- original boundary cursor.

An invalid content identity similarly fails before frame binding or publication.

## Initial state boundary

KT15 requires a coherent pre-existing STATEQ11 composite continuation.

It does not invent first-interval `Runinu`.

Synthetic tests may explicitly supply `Runinu=0`; that is a fixture value only and is not historical or model-evolution authority.

## Hard boundaries

No source file hashing.
No public mutable BOUNDQ02 frame science consumption.
No first-call Runinu rule.
No checkpoint schema admission.
No canonical state admission.
No production source.
No process-science change.
No TCD re-admission.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.

## Governance

KT15 is a cross-module state/science/forcing composition and is conservatively GOV04 Tier D.

Same-agent adversarial review can qualify the candidate but cannot satisfy independent Tier D admission.
