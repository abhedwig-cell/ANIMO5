# TRACE-ELEM-ANIMO-B01-003 reconciliation

Date closed: 2026-09-19
Prospective result: `NO_CONFIRMED_DISCREPANCY`
Candidate IDs: none

## Element

Floating-point precision and legacy build-contract policy, selected before detailed inspection as the numerical-scientific-convention stratum of Exposure Batch 01.

## Source-bound evidence

`docs/numerics/PRECISION_POLICY_BASELINE.md` states that the legacy source contains:

- widespread default `REAL`;
- explicit `REAL(4)` hydrology staging;
- explicit `REAL(8)` utilities/calculations;
- `Dble_trunc` as an explicit `REAL(4)` to `REAL(8)` conversion.

The compiler/interface audit independently reaches the same classification. The former interpretation of the mixed caller declarations as a demonstrated historical defect was withdrawn. Under the evidence-derived eight-byte default-REAL contract, explicit default-`REAL` and `REAL(8)` declarations at this seam are type-equivalent. The remaining issue is a compiler-default build-contract dependency and architectural fragility from implicit interfaces.

## Diagnostic build evidence

`tools/build_gnu_diagnostic.py` is source-hash bound and uses:

- `-fdefault-real-8`;
- `-fdefault-double-8`;
- `-fno-automatic`;

alongside the documented legacy/free-form compatibility flags.

The tool fails closed on the source archive hash and expected 58-unit selection.

PREP01/PREP02 machine evidence records:

- deterministic GNU diagnostic executable SHA-256 `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`;
- eight successful deterministic diagnostic cases;
- four-byte default REAL as non-viable in the tested Ruurlo route;
- omission of `-fdefault-double-8` as numerically pathological;
- automatic local storage as incompatible with the tested final-balance path.

These observations are consistently classified as diagnostic evidence, not as historical executable equivalence.

## Historical Intel build uncertainty

`PREP01_REFERENCE_BUILD_CONTRACT.json` and `HISTORICAL_INTEL_BUILD_CONTRACT.md` agree that:

- Intel Visual Fortran Composer XE 12.1.0.233 is source-declared;
- no historical project/build files are present;
- eight-byte default REAL is strongly supported as required semantics;
- `/4R8` or `/Qautodouble` are candidate Intel settings, not historically proven settings;
- exact historical compiler flags, FP model, optimization and several other build properties remain unresolved.

PREP02 remains `BLOCKED_HISTORICAL_REFERENCE_ENVIRONMENT_REQUIRED`. It explicitly records:

- native historical reference not obtained;
- equivalent reference not admitted;
- unrounded native oracle not obtained;
- diagnostic reference qualified = false;
- production migration admitted = false.

## Precision-policy consequence

The provisional ANIMO5 policy is correspondingly conservative:

- use explicit `real64` or a project kind only when proven equivalent to the qualified legacy eight-byte path;
- keep exchange precision distinct from computational precision;
- convert four-byte hydrology payloads explicitly at the boundary;
- treat mixed/FP32 precision as a separate execution policy requiring qualification;
- do not hide numerical precision semantics in compiler-global defaults.

No current repository evidence inspected for this element silently promotes the GNU diagnostic build to a frozen legacy reference, claims the exact Intel flag spelling as known, or authorizes a production precision migration.

## TRACE disposition

No prospectively new discrepancy was observed between precision documentation, diagnostic tooling and governance/status evidence.

No candidate was registered.

This null result is deliberately narrow. It does not resolve the historical Intel build contract and does not establish numerical equivalence between the GNU diagnostic executable and the historical ANIMO release.
