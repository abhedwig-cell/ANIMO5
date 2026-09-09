# ANIMO-B3A03: TCD-018 Class-A admission readiness

Status: `QUALIFIED_TCD018_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

Target: `TCD-018`

Class: `A_ACCOUNTING_REPORTING_ONLY`

This workunit qualifies one narrow corrected-legacy claim: the already-existing canopy interception storage change belongs in the water ledger for the selected detailed-hydrology control volume. It does not change SWAP hydrology, ANIMO hydrology equations, water-state representation, state promotion, or any physical flux.

No admission is performed here.

## 1. Evidence boundary

The workunit is based on the frozen revision-53 source and testbank identities:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- `Hydro_detailed.for` SHA-256: `f3b8adc7ae56fc6f7002ce667c15288511984423e66ca619ccb4e90622bfbf5d`
- `Outbal_calc.for` SHA-256: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`
- `Init.for` SHA-256: `287db00773ea21a155383b01a3ea35426c216117085822069e7bd844f71e0058`

The evidence stack used is PREP01, PREP06, MASSQ01, SYNQ01, B3Q01 and GOV02. The diagnostic PREP02 Class-A probe is used as supporting non-interference evidence, not as historical B2 evidence.

## 2. Sic and Sict are physical hydrology state

PREP06 records `W-IC` as the canopy interception water store:

| property | source-bound value |
| --- | --- |
| begin state | `Sic` |
| end state | `Sict` |
| storage dimension | m water |
| physical owner/mutator | `Hydro_detailed` / `Input_hydro` |
| state promotion | `Init: Sic = Sict` on the applicable detailed-hydrology route |
| legacy balance family | `Bawa` |

This matters for the Class-A boundary. TCD-018 is not a request to invent a canopy state. The physical store already exists and participates in hydrology. The defect is that the public/main water ledger does not observe the store completely.

The frozen source supports the same ownership directly. `Hydro_detailed` receives `Sic` and `Sict`; `Init` promotes the result store back to the current store for the applicable detailed-hydrology route. A corrected ledger must therefore read existing state only. It must not mutate either value.

## 3. Begin/end storage contribution and detailed hydrology closure

PREP06 defines the detailed profile identity as:

`external water in - external water out - delta(matrix water + snow + ponding + interception) = 0`

Internal vertical layer transfers cancel when the whole profile is selected. For interception, the required storage term is:

`delta S_interception = Sict - Sic`

The revision-53 `Hydro_detailed.for` already applies that term. Its whole-profile `Badev` expression contains:

`... - (Sict-Sic) - (Pnt-Pn) - (Snt-Snla) ...`

and then includes the matrix-water storage changes over the layers.

The natural B1 LWKM case confirms that this detailed hydrology closes much more tightly than the legacy public Bawa report. For the annual total-profile period ending in 2008:

| quantity | value |
| --- | ---: |
| summed `Hydro_detailed Badev` | `-0.0000526405876 mm` |
| initial `Sic` | `+0.0600000000000 mm` |
| final `Sict` | `0.0000000000000 mm` |
| `Sict-Sic` | `-0.0600000000000 mm` |
| formatted legacy `Bawa(Ddev)` | `-0.0601 mm` |

PREP01 extended this reconciliation over all 25 annual total-profile periods. To formatted-output precision:

`legacy BAWADV = sum(Hydro_detailed Badev) + final interception storage - initial interception storage`

The sign and magnitude reverse with the interception-store change across years. This is causal evidence for a missing ledger state term, not evidence of water disappearing from SWAP or from `Hydro_detailed`.

The observed `0.0601 mm` is not and must never become a conservation tolerance.

## 4. Omission from the Bawa interface

`Outbal_calc.for` accounts precipitation, irrigation, runon/inundation, interception evaporation, snow and pond evaporation, soil evaporation, runoff, drainage, lower-boundary flux and the existing snow, ponding and soil-moisture storage terms.

It does not receive `Sic` or `Sict`. The frozen routine contains no `Sic` or `Sict` reference. Its `Bawa(Ddev)` finalization subtracts ponding, snow and soil-moisture storage changes but has no corresponding canopy-interception storage term.

The mismatch is therefore structural:

`Hydro_detailed control-volume state = matrix + snow + ponding + interception`

while the relevant public Bawa storage interface observes:

`matrix + snow + ponding`

Interception evaporation is present as a flux, but interception storage is absent as a begin/end store. This is the exact TCD-018 seam.

## 5. Proposed accounting-only observation

The admissible candidate is deliberately narrow. At each applicable hydrologic step, the reporting layer may observe:

`delta_interception_mm = (Sict - Sic) * 1000`

and accumulate that term with the same balance-period ownership/reset semantics already used by Bawa. At Bawa residual finalization:

`Bawa_Ddev_corrected = Bawa_Ddev_legacy - accumulated_delta_interception_mm`

Equivalent designs are acceptable only when they preserve the same semantics: existing `Sic/Sict` are read-only physical state and the correction occurs solely in the ledger/reporting projection.

The candidate must not:

- modify `Hydro_detailed` physics;
- alter the SWAP/SWATRE payload;
- change `Sic` or `Sict` values or promotion;
- add a replacement water store;
- perturb interception evaporation or any other water flux;
- compensate unrelated water residuals.

## 6. Natural B1 activation

`LWKM_gras_1040.2021.2045` is the natural activation case. PREP01 shows repeated annual positive and negative approximately `0.06 mm` Bawa deviations tracking the net interception storage change. Its temporary TCD-specific ledger probe accumulated `(Sict-Sic)*1000` and removed that characteristic reporting deviation without changing hydrologic state, hydrologic fluxes, forcing, soil-water equations or testcase input.

After the probe, the largest total-profile period residual was approximately `2.07e-4 mm`, on the scale of accumulated detailed-hydrology `Badev`. That remaining value is not accepted by a new tolerance and is not used to widen the TCD-018 claim.

MASSQ01 independently keeps the same natural event visible as `LEGACY_REPORTING_ONLY_DIFFERENCE`: the observer control volume includes `Sic/Sict`, while legacy Bawa does not. MASSQ01 explicitly states that the raw approximately `-0.0601 mm` value is not a tolerance.

## 7. Independent conservation cross-check

SYNQ01 `SYNQ-O003` supplies a strongly independent interception control-volume oracle:

`S0 + precipitation - evaporation - throughfall - S1 = 0`

Its decimal-exact microcase uses `S0=0.06`, precipitation `0.10`, evaporation `0.04`, throughfall `0.08`, `S1=0.04 mm` and closes at exactly `0 mm`.

The oracle shares no ANIMO code, control flow, indexing, convergence logic or approximation. It proves that begin/end interception storage belongs in the selected control-volume identity. It does not prove historical Intel behaviour, SWAP correctness, or B3 admission.

## 8. State and flux non-interference

The Class-A claim requires physical non-interference, not merely a smaller residual.

For readiness, three evidence layers agree:

1. The TCD-specific PREP01 causal probe records no hydrologic state change and no hydrologic flux change. It changes only the Bawa observation.
2. The PREP02 combined Class-A diagnostic probe for TCD-017 and TCD-018 records `state_or_process_physics_changed=false`. Across eight compatible natural cases, 379 outputs were compared, with 12 intended reporting differences in the activated LWKM case and zero unintended differences.
3. MASSQ01 qualifies a read-only water observer. Across the same eight natural cases, 379 physical outputs had zero physical differences after only declared volatile normalization. No scientific numeric tolerance was applied.

The intended TCD-018 non-interference contract is therefore:

- `Sic` and `Sict` trajectories unchanged;
- matrix, ponding, snow and groundwater-related water state unchanged;
- precipitation, irrigation, snow, interception evaporation, other evaporation, runoff, drainage, lower-boundary and internal profile flux trajectories unchanged;
- testcase and hydrological input bytes unchanged;
- only the declared water reporting/ledger surface may change.

This is qualified for admission readiness. It still requires independent second-line review before any admission authority may treat the evidence as closed.

## 9. Expected reporting difference and whitelist

PREP02's eight-case Class-A matrix contains both TCD-017 and TCD-018. In the only naturally activated case, LWKM, the combined probe changed 12 reporting files and produced zero unintended differences. Six are organic-P files belonging to TCD-017. The source-localized TCD-018 water-only subset is:

- `bawaGP.Out`
- `bawaRP.Out`
- `bawaTP.Out`
- `ani_waGP.Bal`
- `ani_waRP.Bal`
- `ani_waTP.Bal`

A TCD-018 candidate may change those files only where the corresponding selected Bawa control volume/report period has nonzero net interception storage change. Non-water output and ordinary physical output are outside the whitelist.

This workunit does not claim that a new isolated TCD-018-only eight-case executable was run. The whitelist is qualified for readiness from the TCD-specific source seam, the natural PREP01 probe and the water-only subset of the combined Class-A comparison. Independent review should verify that isolation before admission.

## 10. Unrelated residuals remain visible

TCD-018 is not a claim that all natural water-ledger residuals are now explained. MASSQ01 retains, for example, a CranGrass `TITO=724` water observer residual of `-0.0030198960466805147 mm` as `UNEXPLAINED_RESIDUAL`.

That residual is not corrected, absorbed, reclassified or used as a tolerance here. This is necessary to keep TCD-018 atomic.

## 11. B3Q01 and GOV02 route status

B3Q01 classifies TCD-018 as Class A only if existing state and process flux trajectories remain unchanged and only the declared reporting surface differs. The evidence above meets that requirement at readiness level.

Admission is nevertheless blocked by the evidence route. GOV02 makes B2 claim-scoped rather than a global prerequisite, but it does not permit skipping route closure. For a Class-A item without qualified B2, the historical-uncertainty route requires documented reasonable B2 acquisition closure plus independent review.

The live PREP02R status remains:

`BLOCKED_HISTORICAL_REFERENCE_ARTIFACT_NOT_YET_OBTAINED`

Specifically:

- historical reference artifact obtained: `false`
- native reference run completed: `false`
- reference qualified: `false`
- external archival request sent: `false`

Therefore the normal B2 route is not available, and the GOV02 historical-uncertainty route is not yet eligible. Readiness can be qualified now, admission cannot.

Independent second-line review is also still pending.

## 12. Gate result

| gate | readiness result |
| --- | --- |
| TCD identity and Class A scope | PASS |
| `Sic/Sict` physical ownership | PASS |
| begin/end storage identity | PASS |
| `Hydro_detailed` storage-aware closure | PASS |
| Bawa interface omission | PASS |
| natural B1 activation | PASS |
| independent interception CV oracle | PASS |
| accounting-only candidate | PASS FOR READINESS |
| hydrological state non-interference | PASS FOR READINESS, SECOND-LINE REVIEW PENDING |
| hydrological flux non-interference | PASS FOR READINESS, SECOND-LINE REVIEW PENDING |
| reporting-output whitelist | PASS FOR READINESS |
| no tolerance from `0.0601 mm` | PASS |
| valid B3 evidence route | PENDING |
| independent second-line review | PENDING |
| TCD-018 admitted | NO |

Final workunit decision:

`QUALIFIED_TCD018_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

The next admissible action is not a physical patch. It is route closure under GOV02/PREP02R and independent second-line review of this atomic evidence package. A later admission decision must be recorded separately and fail closed if either condition remains unresolved.
