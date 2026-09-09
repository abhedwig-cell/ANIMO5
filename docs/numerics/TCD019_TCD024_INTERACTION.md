# ANIMO-NQ02 — TCD-019 and TCD-024 interaction

Status: `FOUR_WAY_SYNTHETIC_INTERACTION_CHARACTERIZED_NO_COMPOSITION_ADMISSION`.

## Separation rule

TCD-019 and TCD-024 remain different claims.

- TCD-019 is Class E: nonlinear P numerical-policy conservation/convergence.
- TCD-024 is Class B: wrong slow-Langmuir site index.

The historical LWKM TCD-019 case uses slow Freundlich, so TCD-024 is not naturally active there. Its TCD-019 convergence study therefore does not silently contain a TCD-024 correction.

## Activated synthetic interaction probe

A one-layer source-bound `Conc_unl` harness was constructed solely to activate both defects with unequal slow-Langmuir site parameters. It has no external transport and is B1 synthetic evidence only. It cannot establish historical prevalence or B2 behaviour.

The four variants were built as separate hashed descendants:

| variant | TCD-019 policy | TCD-024 index | Transorp SHA-256 | executable SHA-256 |
| --- | --- | --- | --- | --- |
| `LEGACY_BOTH` | legacy | legacy wrong index | `2a23128faae1917b063851f48ab25a4d7e8bc7f3fed9e1b9a2c76c4cb8048d3f` | `196f87100e3e50eda222932447d4a8133e303a2e46fb0b67d908082ef35bae0e` |
| `TCD024_ONLY` | legacy | site index corrected | `a2ae5fc9738e006da33df6d90e5179a80ceabce823689c6d384a2ffa04965447` | `c261ccbaf5e7bdfce4688aac8d683006cb23e07320bccaa96726d65e50a09c79` |
| `TCD019_ONLY` | exact fast storage + `Small=1e-8` diagnostic | legacy wrong index | `11775faa0f77b7370645fc194d0430fe68b6a086d5bdf72148391caa9fd02d6a` | `a81f6e130a85841c852366bec170119305882952c9e79a2508ad46150a9e0986` |
| `COMBINED_DIAGNOSTIC` | exact fast storage + `Small=1e-8` diagnostic | site index corrected | `e080298c6394e3f79079d8723bae521358d5d5f708ca1d7d7d2d06da87e603fc` | `2425fbfaac097f22f1fd3a69adf624ac66fa9d5a6c53129ba5c18d4ddeb18ad6` |

The harness starts slow-site stores progressively closer to their equilibrium values using perturbations `eps = 1e-1 ... 1e-6`. Because there are no external P sources or sinks, final minus initial total P is the local conservation residual.

## Results

| eps | legacy both | TCD-024 only | TCD-019 only | combined |
| ---: | ---: | ---: | ---: | ---: |
| `1e-1` | `-6.4669974702e-5` | `8.5423622342e-9` | `-6.4678491821e-5` | `3.0167535137e-13` |
| `1e-2` | `-6.4748200187e-6` | `8.2680184921e-10` | `-6.4756397721e-6` | `4.9222292908e-12` |
| `1e-3` | `-6.3383856691e-7` | `1.3839245139e-8` | `-6.4764198160e-7` | `4.9066306573e-13` |
| `1e-4` | `-6.3385117599e-8` | `1.3834378088e-9` | `-6.4764978269e-8` | `4.9016346537e-14` |
| `1e-5` | `-6.3385243720e-9` | `1.3833889589e-10` | `-6.4756888740e-9` | `8.2372997312e-13` |
| `1e-6` | `-6.3385258153e-10` | `1.3833822976e-11` | `-6.4756894291e-10` | `8.2378548427e-14` |

The units are the harness' conserved P amount units. The magnitudes are synthetic and must not be used as ANIMO tolerances.

## Interpretation

TCD-024 dominates this deliberately activated slow-Langmuir stress case. Correcting TCD-019 alone leaves almost the full residual because the wrong slow-site index remains. Correcting TCD-024 alone removes the dominant error but leaves a smaller numerical-policy residual. Only the combined diagnostic reaches the local floating/equation floor.

This is useful composition evidence because it rejects a tempting but wrong interpretation: a mass-balance improvement after one correction does not show that the other discrepancy is absent. The two defects can mask or expose one another inside the same coupled nonlinear solve.

The four-way result does not merge their admission routes. TCD-024 still needs its Class B evidence, TCD-019 still needs its Class E policy qualification, and any later combined production state needs a separate composition review.

Current state:

- TCD-019 corrected legacy admitted: `false`;
- TCD-019 B3 admitted: `false`;
- TCD-024 B3 admitted: `false`;
- combined composition admitted: `false`;
- production migration admitted: `false`.
