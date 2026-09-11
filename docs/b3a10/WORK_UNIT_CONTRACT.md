# ANIMO-B3A10 work-unit contract

Target: `TCD-025`

Title: Restricted Public/Main Macropore Ledger Correction Readiness

Base authority: `ANIMO-RG05J@624bbad35add93de29ac89649155d9fa086a73af`.

Consumed qualification authorities:

- `ANIMO-B3A08@7a7309e913e8216a20ac134539470e3e5eb4302f`
- `ANIMO-MASSQ03@68a8c202bd01bf55b31b7c944884fb2f78a6a8e8`

This work unit does not admit TCD-025 and does not modify production source. It defines and tests a bounded observer-correction candidate only for public balance intervals that satisfy the MASSQ03 saturated-macropore boundary-admissibility predicate.

The correction candidate must preserve source ownership. It may add only source-owned macropore storage, source-owned vertical boundary transfer and Main-Bypass direct external drainage terms. Matrix/macropore exchange remains internal to the combined matrix plus macropore control volume. `FlMpOuDrSo` must not be counted as a second external loss.

The candidate must preserve DON/NH4/NO3 and DOP/PO4 species separation before any public-family aggregation. No residual-derived missing flux, geometric pseudo-allocation, new state, tolerance, solver policy, historical B2 claim or whole-model golden baseline is allowed.

MASSQ03 already proves that a selected interval which partially cuts a saturated mixed macropore reservoir is not source-closed for dissolved species. B3A10 may not weaken that result. The restricted candidate is therefore not automatically equivalent to the full canonical TCD-025 claim.

GOV05 applies. The complete substantive authoring package must be frozen before same-agent adversarial review. Such review is `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT` and must never be described as genuinely independent.
