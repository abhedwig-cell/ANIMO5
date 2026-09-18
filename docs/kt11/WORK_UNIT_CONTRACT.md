# ANIMO-KT11 Work Unit Contract

Workunit: `ANIMO-KT11 - Typed Multi-Packet Hydrology Provider and Forcing Lifecycle`.

Execution discipline: `RECONCILE -> IMPLEMENT -> QUALIFY -> REVIEW -> CLOSE/HANDOFF`.

## Purpose

KT06 admits one complete KT05 explicit-state hydrology packet bound to one KT02
requested interval while KT02 remains sole accepted-time and publication
authority.

KT11 owns only the missing provider layer:

> Can an immutable collection of complete KT05 hydrology packets select exactly
> one packet from the KT02 requested interval, remain stateless across repeated
> requests, fail closed on missing or duplicate interval keys, and delegate the
> selected packet through the admitted KT06 binding without changing KT02 time,
> transaction or publication ownership?

## Bounded provider semantics

A packet is keyed by the exact pair:

- producer endpoint day;
- producer step duration.

Both values must satisfy the same bounded exact nonnegative REAL64 integer
contract used by frozen KT06. Duplicate keys are rejected at provider
initialization.

Runtime selection uses the KT02 origin and endpoint plus the configured
nonnegative producer-day offset. Storage order is not semantic. There is no
mutable cursor and no packet is consumed by selection, so repeating the same
runtime request selects the same packet.

Missing packets fail closed before a KT06 candidate can be returned.

## Ownership

KT02 remains sole owner of accepted time, private interval execution and
external publication.

KT11 owns packet lookup only. Selected forcing remains client-owned and outside
accepted continuation state.

KT11 delegates the selected complete packet to the frozen, admitted KT06
runtime-binding implementation. It does not duplicate or modify KT06
publication semantics.

## Evidence boundary

KT08 is consumed only as B1 evidence that the pinned LWKM producer file contains
1800 unique, gap-free producer intervals with duration classes 8, 9, 10 and 11
days.

KT09 is consumed only as B1 evidence for eight representative complete real
LWKM packets across those duration classes and sequence positions.

KT11 imports exact blobs from those evidence branches for executable tests.
Neither KT08 nor KT09 becomes runtime authority.

## GOV04

Packet selection and forcing lifetime can change model behaviour if wrong.
KT11 is therefore a `GOV04_TIER_C_RUNTIME_SEMANTICS` candidate.

Same-agent review may harden the workunit but cannot satisfy the genuinely
independent second-line review gate.

## Explicit exclusions

KT11 does not qualify:

- full 1800-packet payload materialization or execution;
- packet generation from SWATRE.UNF at runtime;
- retry or timestep-selection policy;
- fractional or subday time mapping;
- generic calendar conversion;
- Hlpimp=1 or Hlpimp=2 semantics;
- Hydro_detailed scientific execution;
- ANIMO scientific admissibility;
- production coupling or migration;
- B3/B4 or Status A/AA.
