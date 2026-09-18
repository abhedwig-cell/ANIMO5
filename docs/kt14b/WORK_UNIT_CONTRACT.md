# ANIMO-KT14B Work Unit Contract

Workunit: `ANIMO-KT14B - Opaque Content-Bound Boundary Frame TCD-042 Composition Remediation`.

KT14B remediates the already qualified KT14 composition so that all new scientific composition consumes the qualified BOUNDQ02B opaque immutable frame instead of the public mutable BOUNDQ02 frame.

## Authorities

- Program: `ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`
- Remediated science composition: `ANIMO-KT13A@df2310cc69e3fe16187ba2235843222f8acfb726`
- Original boundary composition: `ANIMO-KT14@3e4dc99baa5c343041857f8cd44cd316481fb478`
- Static year binding: `ANIMO-BOUNDQ02@fb0c0c842aed9a90378aca613279e09a856ad09b`
- Opaque frame: `ANIMO-BOUNDQ02B@de6eef3122354e74405ff9c92286794714bdee82`

The frozen BOUNDQ02B implementation blob is `eae62a2ce077e3e568a8a73b25ac45d20c432bae`.

## Required remediation

KT14B must:

1. accept `immutable_static_boundary_interval_frame_t` only;
2. validate and copy out frame content exclusively through the BOUNDQ02B public inspector;
3. bind exact origin and endpoint identity before science;
4. propagate the 64-character boundary content SHA-256 into the composition trace;
5. keep dry deposition separately observable but outside the wet/advective TCD-042 forcing;
6. pass only the copied-out validated chemistry to KT13A;
7. preserve all KT14/KT13A transaction and scientific scope limits.

The private fields of BOUNDQ02B are not accessed directly.

## Content identity boundary

BOUNDQ02B binds chemistry forcing identity to:

`SHA256=<64 lowercase hex>:SLOT=<selected slot>`.

KT14B does not verify source file bytes itself. It preserves the already qualified BOUNDQ02B identity and exposes that identity in its trace.

Two frames with identical chemistry but different content identities may yield identical science values while remaining distinct provenance identities.

## Hard boundaries

No BOUNDARY parser change.
No source hash verification.
No dry deposition process migration.
No chemistry correction.
No TCD-042 scope widening.
No multi-interval cursor admission.
No canonical state admission.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.

## Governance

This remains a GOV04 Tier D scientific composition candidate. Same-agent review is process assurance only and cannot satisfy the required independent Tier D review.
