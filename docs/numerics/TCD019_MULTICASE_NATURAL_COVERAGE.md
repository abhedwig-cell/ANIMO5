# ANIMO-NQ02 — TCD-019 natural multi-case coverage

Status: `NATURAL_MULTICASE_B1_COVERAGE_EXECUTED_B3_NOT_ADMITTED`.

This extension tests whether the LWKM TCD-019 finding is confined to one testcase. It remains B1 diagnostic evidence. It does not establish B2, does not select `Small`, and does not admit a corrected-legacy or production policy.

## Frozen identity and scope

All runs fail closed on the same frozen identities used by the primary NQ02 study:

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Five additional supplied natural cases were exercised:

- `CranGrass`;
- `GrassPeat`;
- `STONE_akk_0006.2001.2015`;
- `Puitmijn_Cranendonck_60`;
- `Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA`.

Their supplied `CHEMPAR.INP` files use the same relevant option family as LWKM: one fast Langmuir site (`Optcxfa=2`, `Ncxfa=1`) and three slow Freundlich sites (`Optcxsl=3`, `Ncxsl=3`). TCD-024 is therefore not naturally activated in these runs.

The multi-case runner used for this extension had SHA-256 `28104f4e8e131d7cfcf1794f4504aac5fa7eca10ca9285630a91d37b90836958`. Every diagnostic `Transorp` descendant, observer descendant and executable is recorded in `TCD019_MULTICASE_EXTENSION.json`.

## Comparison route

The common comparison uses the threshold-free cancellation-safe Langmuir storage representation together with `Small=1e-7`. This value is a diagnostic refinement point only. It was selected because it lies inside the stable LWKM pre-fallback region, not because it is a candidate production tolerance.

Where useful, `Small=1e-8` was also run to characterize how fallback activation changes the apparent refinement envelope.

## Results

| case | baseline cumulative `R_cons` kg/ha | exact + `1e-7` cumulative `R_cons` kg/ha | baseline sum `|R_cons|` | exact + `1e-7` sum `|R_cons|` | bisections baseline / exact `1e-7` |
| --- | ---: | ---: | ---: | ---: | ---: |
| CranGrass | `-0.7658941622` | `-0.7235682813` | `0.8340663872` | `0.7917469137` | `0 / 0` |
| GrassPeat | `-0.02070815724` | `-0.001933511247` | `0.02318902703` | `0.004470369984` | `0 / 2` |
| STONE_akk_0006.2001.2015 | `-0.03327468374` | `+0.002840419209` | `0.03920607650` | `0.003687583632` | `0 / 1` |
| Puitmijn_Cranendonck_60 | `-0.07602187823` | `+0.001812103990` | `0.08100796202` | `0.005057010945` | `6 / 12` |
| Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA | `-0.06485622131` | `+0.003270349263` | `0.06521597707` | `0.01204479040` | `2 / 15` |

The result is not simply “smaller balance error everywhere”. Three more informative patterns emerge.

### 1. The legacy sign-biased drift is not LWKM-specific

All five additional baseline cases show a negative cumulative P conservation drift. The exact-storage plus refined-solver route removes most of the post-initial-step drift in GrassPeat, STONE and Puitmijn, and strongly reduces it in Zuiderzeeland. This is consistent with the source-bound TCD-019 mechanism being a process-family issue rather than a single-case accident.

### 2. CranGrass exposes a separate first-step seam

CranGrass has a first-timestep residual of about `-0.72358 kg/ha P`. It is almost unchanged by TCD-019 refinement. Excluding only that first timestep:

- baseline cumulative residual is `-0.04231165 kg/ha` with `sum |R_cons| = 0.04231703`;
- exact storage plus `Small=1e-7` gives `+1.26e-7 kg/ha` with `sum |R_cons| = 6.88e-6`.

The large first-step term must therefore not be used to reject or tune the TCD-019 route. It is retained as a separate initialization/state-consistency signal. Its exact attribution to TCD-014 requires the TCD-014 workunit and is not asserted here.

### 3. Fallback ownership is a natural-case issue, not only a very-tight-LWKM issue

Puitmijn already activates 6 bisection fallbacks under the unchanged legacy numerical policy, and Zuiderzeeland activates 2. Under exact storage plus `Small=1e-7`, fallback counts rise to 12 and 15 respectively. At `Small=1e-8` they rise further to 23 and 48.

The absolute residual does not improve monotonically with this tightening in every case. For example, Zuiderzeeland `sum |R_cons|` is `0.0120 kg/ha` at `1e-7` and `0.0180 kg/ha` at `1e-8`, despite a smaller Newton equation residual. GrassPeat shows the same direction: `0.00447` to `0.00510 kg/ha` while bisections increase from 2 to 6.

This strengthens a key NQ02 conclusion: a production policy cannot be specified as “use exact storage and tighten `Small`”. Newton and fallback acceptance form one numerical policy and must be qualified jointly.

## Coverage conclusion

Natural multi-case coverage is now established for the supplied fast-Langmuir/slow-Freundlich family. It supports the route-level classification:

`CONVERGENT_POLICY_CANDIDATE`

but with a sharper condition:

`FALLBACK_POLICY_MUST_BE_QUALIFIED_JOINTLY_WITH_NEWTON_POLICY`.

The evidence also demonstrates why a single scalar balance metric is unsafe. A large case total can be dominated by a separate first-step seam, while a smaller Newton residual can coexist with worse whole-run conservation after fallback activation.

## Remaining limits

This extension does not provide:

- natural fast-Freundlich coverage, because the inspected supplied P-active cases use fast Langmuir;
- independent historical B2 evidence;
- independent numerical review;
- a qualified production `Small`;
- a qualified fallback residual threshold or fallback algorithm;
- TCD-014 admission;
- TCD-024 admission or composition admission.

`TOLERANCE_NOT_YET_QUALIFIED` remains in force.
