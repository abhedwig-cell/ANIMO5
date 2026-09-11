# ANIMO-B3D27 — TCD-037 parent composition qualification

Status at this authoring surface: `COMPOSITION_CANDIDATE_READY_FOR_GOV05_ADVERSARIAL_REVIEW`.

This work unit evaluates the parent TCD-037 claim after the four canonical child atoms were separately admitted. Child admission is evidence, not a parent-admission shortcut. No production source, frozen B0, central registry, aggregate authority, B4 surface or production-migration surface is changed here.

## 1. Exact parent scientific claim

TCD-037 is qualified only as a composed **GHG observer-accounting contract**. It is not one physical GHG scalar and it is not a climate CO2-equivalent calculation.

For an active GHG balance-observer call, every affected balance field must consume the source-owned current-timestep amount whose physical and accounting meaning matches that field:

1. `Bfom/Bahu/Bdom(CH4f)` and their associated `CO2f` partition terms use CH4 layer formation amount `QPrCH4(Ln) * St`, `Ln=1..Nl`.
2. `Btom(CH4e)` uses the signed atmosphere-boundary CH4 exchange amount `(QEmCH4Dif + QEmCH4Ebl + QEmCH4Flw + QEmCH4Plt) * St`.
3. `Btom(CO2e)` remains the existing formation-side dissimilation complement and therefore uses total CH4 formation `sum(QPrCH4(1:Nl) * St)`, not atmosphere emission. This is not a claim of a complete CO2 ledger.
4. `Bani(N2Od)` uses N2O denitrification layer formation amount `QPrN2Oden(Ln) * St`.
5. `Bani(N2Oe)` uses the signed atmosphere-boundary N2O exchange amount `(QEmN2ODif + QEmN2OFlw) * St`.
6. Existing `Banh(N2On)` nitrification accounting remains outside the correction and retains its existing locally reconstructed production meaning. `QRdN2O` remains a separate reduction sink and is not substituted into production or emission observer fields.

The parent claim is the conjunction of those ownership statements plus their noninterference boundaries. Composition does not introduce an equation equating formation, storage, reduction and atmospheric exchange. Those quantities may differ within a timestep.

## 2. Frozen identities and authorities

The parent reconstruction reuses immutable evidence only after exact-pin verification.

- frozen source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `Outbal_calc.for` SHA-256: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`;
- aggregate at start: `ANIMO-RG05I@94afe7d649a8c60758a41996f0059de0acddd2fc`;
- routing: `ANIMO-B3I07@54679c7555a963133dfd686648af334f479c5808`;
- runtime ownership: `ANIMO-RUNTIMEQ02@45e8073fa95035b3565bd8b373ac327915cf1af5`;
- runtime semantics: `ANIMO-RUNTIMEQ03@a3e822f8e97fe1312a7dfa73601a49ae7375163e`;
- governance: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`, `ANIMO-GOV04@1bbe4c211197590f346803106e45dca5faae79fc`, `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`, `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`, `ANIMO-B3Q02@1db63b17cb5f48cbd8ae28116a2e716b4bdaadf3`.

Exact-final child admissions and CI:

| child | authority | exact-final CI | conclusion |
| --- | --- | ---: | --- |
| A1 | `ANIMO-B3D21@331f6ed91d4a1c15a23ae0c1ad75d1b540f61858` | 34540047043 | success |
| A2 | `ANIMO-B3D24@0f85d7102945c7c4d77bc49885f9ecca688209e3` | 34547891772 | success |
| A3 | `ANIMO-B3D25@4da2dd067069944a5e3eeb5f532566a23402bd68` | 34549748497 | success |
| A4 | `ANIMO-B3D26@49e5ef141850296df17317da181a561def239117` | 34554010568 | success |

No live B3D27, equivalent parent-composition workunit or later parent admission was found before branch creation. No new TCD-037 issue or PR superseded the pinned evidence.

## 3. Child-to-parent coverage

A1 covers the layer CH4 formation ownership and the local CH4/CO2 formation partition. A2 covers the index-0 semantic split: atmosphere exchange for `CH4e` and formation-total for the legacy `CO2e` dissimilation complement. A3 covers layer denitrification N2O formation. A4 covers total atmosphere N2O exchange and explicitly rejects production-total substitution.

Together the four atoms cover every disconnected or semantically overloaded GHG observer surface identified by RUNTIMEQ02/RUNTIMEQ03. Existing N2O nitrification output is not a missing atom: its current-call scratch producer is defined and its existing reporting-threshold policy is unchanged. `QRdN2O` is a deliberately separate sink. No fifth correction atom is required by this reconstruction.

## 4. Producer, lifetime and observer ownership

`QPrCH4`, `QPrN2Oden` and the atmosphere-exchange components are source-owned GHG process rates. Multiplication by `St` converts them to current-timestep amounts before observer accounting. They are not persistent state and are not checkpoint fields introduced by TCD-037.

The defective legacy locals `AmCH4` and `AmN2Odeni` have no valid producer/lifetime contract. `AmN2Onitr` is different: it is rebuilt inside the active `Outbal_calc` call before use. Parent composition therefore must not recreate one shared `Am...(0:Nl)` ownership model.

Balance accumulators are observer/reporting state over their configured balance interval. This workunit changes no serialization or restart state. It admits no claim that arbitrary split-run balance-report accumulators are checkpoint-identical. The scientific correction is bounded to correct ownership of observer increments during an uninterrupted accepted timestep.

## 5. Signed exchange and index semantics

The frozen GHG source defines CH4 and N2O atmosphere-emission rates with **negative values meaning uptake by the soil**. Therefore the atmosphere-boundary sums are signed exchanges. Parent composition preserves the sign exactly; it must not apply absolute values, positivity clamps or a production-only interpretation.

Layer indices `1..Nl` denote formation in soil layers. Index 0 cannot be treated as a universal profile-total slot with the same owner as the layers. In CH4 accounting, the legacy index-0 consumer surface actually contains two different meanings: formation total for the `CO2e` dissimilation complement and atmosphere exchange for `CH4e`. For N2O, total production is not the owner of `N2Oe`; the atmosphere-boundary exchange tuple is.

## 6. Units and dimensional compatibility

CH4 source rates are `kg C m-2 d-1`; after `* St` they are `kg C m-2`. The organic-matter balance converts CH4-C by `/ Cfracom` and by `Z=10000` to the balance's organic-matter mass basis in `kg ha-1`. Consequently the legacy slot name `CO2e` must not be interpreted as a greenhouse-warming CO2-equivalent metric.

N2O source rates are `kg N m-2 d-1`; after `* St` and `Z=10000` the N balance uses `kg N ha-1`. Carbon/organic-matter and nitrogen observer ledgers remain dimensionally separate. The parent does not sum CH4 and N2O terms across elements.

## 7. Overlap, gaps and double counting

The only intentional cross-child reuse is CH4 formation: A1 owns layer formation increments while A2 uses their profile sum for the formation-side `CO2e` complement. That is a layer-to-total identity inside the same formation quantity, not an additional emission. `Btom(CH4e)` remains independently atmosphere-owned. No field receives both the A1 formation amount and A2 atmosphere amount.

Likewise A3 denitrification formation and A4 N2O atmosphere exchange are not two additive descriptions of the same transfer. Formation enters the modeled gas system; atmosphere exchange crosses the top boundary. Dynamic storage and reduction allow them to differ. `QRdN2O` is not counted in either observer term.

No uncovered defective observer surface was found. Nitrification `N2On` is valid existing context, not a missing child. No dependency on TCD-032 through TCD-036 is required for the parent claim; those domains remain noninterference exclusions and are not composition inputs.

## 8. Conservation and scientific meaning

TCD-037 improves observer-accounting ownership. It does **not** prove complete GHG carbon closure, complete N2O mass closure, historical numerical equivalence, or whole-model conservation. A same-timestep identity `formation = atmosphere emission` would be physically wrong in the presence of gas storage, CH4 oxidation or N2O reduction.

The only new parent-level scientific meaning is compositional: the four admitted atoms are mutually compatible when interpreted as orthogonal observer mappings in two element-specific ledgers. The parent is therefore a conjunction of bounded corrections, not a new physical process model.

## 9. Risk-tier determination

`STRICTEST_APPLICABLE_RISK_TRIGGER_WINS` gives **GOV04 Tier D** for the parent decision surface. Tier A is unavailable because this is explicitly non-atomic composition. The parent combines four separately admitted atoms, shared CH4 formation information, layer/profile/boundary semantics and conservation-sensitive reporting meaning. B3D26 also routed the completed children to a separate composition decision surface.

This Tier-D classification does not authorize B4 or production migration. Under GOV05 the composition authoring head must be frozen first, then reviewed by a same-agent adversarial pass explicitly classified as `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`. If that pass finds a substantive defect, this authoring surface must be replaced by a new immutable checkpoint and reviewed again.

## 10. Composition disposition before adversarial review

All parent reconstruction predicates are presently supported and no remediation blocker has been found. The bounded disposition of this authoring surface is:

`COMPOSITION_CANDIDATE_READY_FOR_GOV05_ADVERSARIAL_REVIEW`

It is **not yet** the formal parent B3 admission. Admission is permitted only after the immutable authoring head passes the GOV05 adversarial review and the final admission package passes exact-head CI.
