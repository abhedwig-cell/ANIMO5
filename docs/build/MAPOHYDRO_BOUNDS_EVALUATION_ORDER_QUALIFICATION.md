# ANIMO-BUILDQ02 — MAPOHYDRO bounds and evaluation-order qualification

Status: `QUALIFIED_RUNTIME_LANGUAGE_HAZARD_SCOPE_EXPANDED_NO_SCIENTIFIC_TCD`

## Canonical routing boundary

B3I01 routes the BUILDQ01 MAPOHYDRO index-0 finding as:

`BUILD_RUNTIME_HAZARD_NOT_TCD`

It is explicitly not part of TCD-025 without independent evidence of a separate scientific state or flux discrepancy. BUILDQ02 preserves that disposition.

The new result is that the source-level hazard is broader than the original Task-1 wet-domain search. The actual `Hydro_detailed -> Modflux -> Mapohydro Task 2` call seam contains two additional index-zero evaluation-order exposures.

## 1. Task-1 bottom wet-layer search

Revision 53 evaluates:

`FrHeWeMpWl(Dn,LnBoMp(Dn)) < 1e-7 .AND. LnBoMp(Dn) >= 1`

The array has second-dimension lower bound 1. If a domain has no wet macropore layer, `LnBoMp(Dn)` decrements to zero and the next condition evaluation may read index zero before or regardless of the second conjunct.

With GNU `-fcheck=bounds`, the unmodified source terminates at `MAPOHYDRO.FOR:78` in three of four controlled dry/partially dry cases:

`Index '0' of dimension 2 of array 'frhewempwl' below lower bound of 1`

A diagnostic copy that sequences the lower-bound test before the array access completes all four cases.

## 2. Task-1 domain-2 top search

The same logical pattern occurs at the domain-2 top search:

`FrHeWeMpWl(2,Ln) > 1e-7 .AND. Ln >= 1`

The safe-domain condition again appears after the array expression. BUILDQ02 treats it as the same Task-1 lower-bound/evaluation-order family.

## 3. Task-2 backward scan after MODFLUX

The stronger new finding is in Task 2.

`Hydro_detailed.for` calls `Modflux` between MAPOHYDRO Task 1 and Task 2. `Modflux` constructs the solute calculation sequence `Sqnu(0:Nl)`. With ponding active (`Flpn=1`), layer zero is a legitimate sequence member.

A controlled exact-call-order probe used:

1. unchanged MAPOHYDRO Task 1;
2. unchanged `Modflux`;
3. unchanged MAPOHYDRO Task 2.

For `Nl=2`, the unchanged `Modflux` generated:

`Sqnu = [1,0,2]`

from a simple hydrological flux configuration. Thus zero at a later sequence position is produced by the actual preceding routine rather than manually inserted into MAPOHYDRO.

The Task-2 backward scan evaluates `FlMpInEf(1,Ln)` and `FlMpInEf(2,Ln)` while its `K >= KBegMpReko` stopping condition appears later in the compound condition. `FlMpInEf` is declared with second-dimension lower bound 1.

In the zero-macropore-outgoing-flux coupled case, the unmodified source terminates under GNU bounds checking at revision-53 line 250 when `Ln=0`. This occurs under both static and automatic local-storage modes.

A structurally sequenced diagnostic candidate checks the sequence bound first and treats the ponding layer as having no `FlMpInEf` coordinate. It completes and gives `KBegMpReko=2`, `KEndMpReko=1`, representing an empty outgoing-macropore iteration interval.

## 4. Task-2 CoStat classification at layer zero

A second coupled case gives outgoing macropore flux in both soil layers while `Modflux` still generates:

`Sqnu = [1,0,2]`

Here `KBegMpReko=0` and `KEndMpReko=2`, so the Task-2 `CoStat` loop legitimately visits layer zero.

Revision 53 contains adjacent branches:

`If (Ln.Ne.0 .And. FlMpInEf(1,Ln)+FlMpInEf(2,Ln).Gt.1.d-6) ...`

and

`If (Ln.Eq.0 .And. FlMpInRuRv(1)+FlMpInRuRv(2).Gt.1.d-6) ...`

The first branch relies on `.AND.` to protect an array that has no index zero. GNU bounds checking terminates at line 264 before the intended layer-zero branch can serve as the alternative.

A diagnostic structural `If (Ln.Ne.0) Then ... Else ... Endif` completes the same coupled case and retains the existing distinction between soil-layer exfiltration and ponding/runon input.

## 5. In-domain non-interference

The structural diagnostic variant was tested on a 64-case matrix deliberately restricted to states where the original source stays inside its declared array domain.

The complete Task-1 through Task-4 output is byte-identical between original static-local execution and the automatic-local structural candidate at O0, O2, bounds-checking and signalling-NaN initialization variants.

All produce SHA-256:

`16dc28adce374a956e77dc17420d814b64bf112ae3ff5524afe2422cb29433e3`

This supports non-interference for the tested in-domain envelope. It does not convert the diagnostic variant into an admitted correction.

## Classification

The qualified runtime finding is now:

`MAPOHYDRO_TASK1_AND_TASK2_OUT_OF_DECLARED_DOMAIN_INDEX0_EVALUATION_ORDER_HAZARD`

Evidence strength:

- source-confirmed;
- GNU bounds-check confirmed;
- Task-2 reachability confirmed through the actual `Modflux` call seam in controlled B1 diagnostics;
- historical Intel manifestation unknown;
- no distinct scientific state or flux discrepancy established under a qualified historical execution contract.

Therefore canonical disposition remains:

`BUILD_RUNTIME_HAZARD_NOT_TCD`

## Migration rule

A future ANIMO5 implementation must structurally establish a valid index/domain before evaluating an array or arithmetic expression that is undefined outside that domain. `.AND.` and `.OR.` are not safety guards.

That rule is a runtime-language contract. Any change to physical process equations, active-layer definitions or flux semantics would require separate qualification.

`new_canonical_tcd_allocated=false`

`production_migration_admitted=false`
