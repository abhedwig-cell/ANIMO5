# ANIMO-SQ04 — TCD-016-C1 existing-process reuse audit

Work unit: `ANIMO-SQ04`

Target: `TCD-016-C1`

Parent: `TCD-016`

Branch: `work/animo-sq04-tcd016-c1-existing-process-reuse-audit`

Base: `ANIMO-SQ03@58dc3c5c108ee97fd6bea107b7a9e686596617b1`

Global B3 closure authority at authoring start: `ANIMO-B3Q06@11e9bcdc6654e63f84875bf1f28dc54abe725700`

Aggregate authority at authoring start: `ANIMO-RG05O@bc9e6ed997a078336645210ebb4d99ae976893fe`

GOV05 authority: `ANIMO-GOV05@f65a47724e4a4fca7f2d8b8d6de9eeee51867904`

No production source, frozen B0, central queue, canonical TCD registry, B3 admission or B4 surface is modified.

## 1. Question

SQ03 established a fail-closed interface around unresolved dry-period and rewetting physics. SQ04 asks whether an **existing revision-53 NH4 process route** can be attached to the continuation owner unchanged, so that a new process formulation would be unnecessary.

The audit is deliberately bounded to the existing routes that are plausible candidates for TCD-016-C1 reuse:

- management-addition NH4 volatilization through `Frvo`;
- soil NH4 nitrification/transformation;
- soil NH4 sorption;
- the `Conhtop/Rsconhtop` upper-boundary reservoir and its release route;
- direct reuse of existing aqueous transport at zero-water continuation state.

It does not claim to classify every nitrogen process in ANIMO for every purpose.

## 2. Frozen-source identity

The session-local frozen source archive was re-hashed before this audit:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The frozen testbank hash remains:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The source file hashes used by the audit match the repository source manifest. No source byte is republished or changed.

## 3. Management-addition volatilization is provenance-specific

A source-wide search for `Frvo`, `NH3`, `ammonia`, and volatilization terminology found the operative NH4 volatilization fraction only in the management-addition route and its reporting surfaces.

`Input_addit.for` reads `Frvo(I)` together with one addition event's material number, quantity, placement and ploughing settings, and bounds it to `[0,1]`.

`Addit.for` multiplies the NH4 fraction of that **newly added material** by `(1-Frvo(I))` before the retained part is introduced into ponding water, the additions reservoir, or soil layers.

`Outbal_calc.for` reports the volatilized amount using the same addition-event variables, including `Qumt(I)`, `Frnh(Mtnu(I))` and `Frvo(I)`.

Therefore `Frvo` is an input-event partition on management additions. It is not a state-dependent volatilization operator that consumes arbitrary pre-existing surface NH4 mass. Reusing it unchanged for `M_surface_NH4_non_aqueous_continuation` would silently change its provenance, activation variables, state owner and balance semantics.

Disposition:

`FRVO_ADDITION_VOLATILIZATION = NOT_REUSABLE_UNCHANGED`

This does not prove that dry continuation NH4 cannot volatilize. It proves only that the existing `Frvo` route is not that process law.

## 4. Existing nitrification/transformation is soil-layer scoped

`Rates.for` constructs temperature, pH, moisture and transformation reduction factors in loops over `Ln=1..Nl`. Its NH4 nitrification coefficient `Rekinh(Ln)` is likewise calculated inside the soil-layer loop.

`Denitr.for` evaluates nitrification-related oxygen demand and nitrate production only for `Ln=1..Nl`.

`resp_miner.for` may receive arrays indexed from zero, but its main compartment loop explicitly diverts `Ln=0` to a skip label before the soil mineralization logic. Final `Rekonh` production is then formed in a `Ln=1..Nl` loop.

Thus the existing transformation machinery is tied to soil-layer environmental states and owners. It does not define transformation of a nonaqueous continuation mass in the surface control volume.

Disposition:

`SOIL_NITRIFICATION_TRANSFORMATION = NOT_REUSABLE_UNCHANGED`

A future model may deliberately transfer continuation mass into an admitted soil state and then let existing soil process laws act there. That transfer itself is new scientific semantics and is not qualified by SQ04.

## 5. Existing NH4 sorption is soil-owner specific

`Inicalc.for` maps `Socfnh` and `Rhbd` from soil horizons to layers only for `Ln=1..Nl`. It initializes adsorbed NH4 `Cxnh(Ln)` only for `Ln=1..Nl` and computes the soil-specific uptake/sorption factor over the same soil-layer domain.

`UBoundconc.for` can place dry-deposition NH4 into layer 1 and then apply the existing layer-1 sorption identity, but that is an explicitly routed **external input into soil layer 1**, not a generic owner for residual mass from disappearing ponding water.

Disposition:

`SOIL_NH4_SORPTION = NOT_REUSABLE_UNCHANGED_AS_CONTINUATION_OWNER`

Existing sorption can act after a separately qualified transfer reaches the soil phase. It cannot be used as an implicit destination merely to close the TCD-016 balance.

## 6. The top reservoir is an upper-boundary input reservoir, not residual ponding state

`UBoundconc.for` forms loads from precipitation, irrigation, runon and other upper-boundary inputs. Under no ponding it evolves `Conhtop/Rsconhtop` over `Hetop` using a residence-time formulation driven by upper-boundary water flux. Under ponding it empties that reservoir into the active boundary mixture.

SQ01 had already established that this reservoir has management/addition provenance and is semantically distinct from layer-0 residual solute. The fresh source audit adds no evidence that would change that ownership conclusion.

Disposition:

`TOP_RESERVOIR = NOT_REUSABLE_UNCHANGED`

Reusing it would alter provenance, release kinetics and restart meaning.

## 7. Existing aqueous transport cannot represent continuation mass at zero water

The continuation state exists precisely because a concentration coordinate cannot retain finite mass when its aqueous storage reaches zero. Re-entering `Transsub/TRANSPORT` without first creating an admitted receiving aqueous state would therefore recreate the missing-state problem or require an invented water floor.

The existing transport route can become applicable only after a separately qualified transfer places mass into an admitted aqueous owner.

Disposition:

`AQUEOUS_TRANSPORT = NOT_A_CONTINUATION_PROCESS_LAW`

## 8. Cross-route conclusion

For every plausible existing route audited here, at least one semantic contract is incompatible with unchanged reuse:

| route | existing owner/provenance | mismatch with continuation state | disposition |
| --- | --- | --- | --- |
| `Frvo` volatilization | one management-addition event | input-event partition, not state-dependent dry mass loss | `NOT_REUSABLE_UNCHANGED` |
| nitrification/transformation | soil layers 1..Nl | requires soil environmental/phase state | `NOT_REUSABLE_UNCHANGED` |
| NH4 sorption | soil solid/aqueous owner, layers 1..Nl | no surface continuation solid owner | `NOT_REUSABLE_UNCHANGED` |
| `Conhtop/Rsconhtop` | upper-boundary additions/input reservoir | incompatible provenance and release law | `NOT_REUSABLE_UNCHANGED` |
| aqueous transport | aqueous concentration state | cannot own finite mass at zero aqueous storage | `NOT_A_CONTINUATION_PROCESS_LAW` |

The bounded conclusion is therefore:

`NO_AUDITED_EXISTING_REV53_NH4_ROUTE_IS_SEMANTICALLY_REUSABLE_UNCHANGED_FOR_TCD016_C1_CONTINUATION_STATE`

This is not a claim that ANIMO5 must invent every equation from scratch. Existing scientific formulations may later be reused or adapted after their state mapping, activation domain, parameters, units, ordering and balance semantics are separately qualified. The word **unchanged** is controlling.

## 9. Strong counter-hypotheses

### Frvo is already an NH4 volatilization fraction, so reuse is natural

Rejected for unchanged reuse. Its source contract partitions a named addition amount before storage and its balance accounting is indexed by the same addition event. A continuation-state sink would require state-dependent activation and removal from a persistent owner.

### Existing soil nitrification can act if the continuation store is viewed as topsoil NH4

Rejected because that view changes the state owner. The continuation shell is intentionally not soil aqueous or sorbed NH4. A transfer into soil may be a future process, but it must be explicit.

### Conhtop already persists without ponding, so it is the missing state

Rejected because persistence alone does not establish semantic identity. `Conhtop` carries an upper-boundary reservoir with a defined flux-driven release law and management/input provenance.

### The continuation owner can simply wait until water returns and then use Transport

Partly compatible with SQ03 only after a receiving aqueous state and transfer law are qualified. It does not qualify the transfer destination, fraction, timing or ordering and therefore is not an existing unchanged process law.

## 10. Qualification decision

SQ04 qualifies only the negative reuse audit:

`QUALIFY_TCD016_C1_EXISTING_PROCESS_REUSE_AUDIT; NO_AUDITED_EXISTING_REV53_NH4_ROUTE_IS_REUSABLE_UNCHANGED; NEW_OR_EXPLICITLY_ADAPTED_PROCESS_SEMANTICS_REQUIRE_SEPARATE_SCIENTIFIC_QUALIFICATION`

TCD-016-C1 remains `UNRESOLVED_NOT_ADMITTED`. Parent TCD-016 remains `UNRESOLVED_NOT_ADMITTED`. TCD-016-E1 remains blocked. Historical behavior remains `UNKNOWN_WITHOUT_B2`. No production or central-regie action follows from SQ04.
