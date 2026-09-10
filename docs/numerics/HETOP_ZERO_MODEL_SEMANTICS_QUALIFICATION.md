# ANIMO-UBQ04 HETOP zero-thickness intended model semantics qualification

Status: bounded theory/source reconciliation. No model policy, admission or production change is selected here.

## 1. Question

UBQ03 proved that `HETOP=0` is both documented and parser-admissible, while revision 53 contains several expressions that divide by `HETOP`. B3I06 therefore kept the finding as a runtime/input-domain hazard and deliberately did not reserve a new TCD.

UBQ04 asks the narrower next question: does the available controlled evidence uniquely tell us what `HETOP=0` is supposed to mean?

The answer is no.

## 2. Documentation evidence

The ANIMO 4.0 User's Guide defines `HETOP` in the SOIL.INP table as the thickness of the virtual reservoir from which fertilizer additions leach proportional to cumulative precipitation after the fertilization event. Its published range is `[0.0 ... 0.2]` m.

The theoretical transport chapter independently describes an extra artificial reservoir above the soil compartment division. Manure and fertilizer additions may be put in that reservoir and then leach into the soil proportional to cumulative precipitation.

Those statements strongly establish the positive-thickness physical role of `HETOP`. They do not define the meaning of the endpoint zero. In particular, the guide does not say that zero disables the reservoir, means instantaneous passage, is valid only under selected options, or is an input error.

There is also an internal documentation inconsistency that prevents using the worked examples to infer endpoint semantics. Table 6 gives the order `HETOP`, then `HE(0)`. The worked SOIL.INP examples contain `0.02 0.2`, but their explanatory prose assigns `0.02` to the top or ponding compartment and `0.2` to the addition reservoir. This is the opposite interpretation of the table ordering. Revision-53 source reads the pair as `Hetop, He(0)`. UBQ04 therefore treats the worked-example prose as conflicting evidence rather than as authority for the identity of either value.

The guide itself points to the separate ANIMO 4.0 process-description report by Groenendijk, Renaud and Roelsma (2005) for a more comprehensive formulation. That report has been identified bibliographically, but its full text is not part of the controlled evidence used in this workunit. Its existence is therefore a provenance lead, not evidence that closes the zero endpoint.

## 3. Revision-53 source semantics

Revision 53 accepts `HETOP=0` because `input1.for` checks `Hetop` against the inclusive range 0.0 to 0.2. No explicit branch on the value of `HETOP` was found.

The source uses positive `HETOP` in several distinct roles:

- `Addit.for` converts mass placed in the top addition reservoir into concentration by dividing by `HETOP`;
- `UBoundconc.for` uses `P = St*Flux/HETOP` in the positive-throughflow analytical reservoir solution;
- the ponding branch uses `C*HETOP` as initial areic stored mass;
- grass and plant uptake routines form `Flab(1)/HETOP` before their uptake conditions;
- balance routines also identify top-reservoir mass through concentration times `HETOP`.

This is important because a plausible zero interpretation must be coherent across storage, additions, no-flow periods, positive flow, ponding, crop uptake and balance ownership. A local fix to one division is not a model-level definition.

## 4. Governing positive-thickness reservoir

For the no-ponding positive-thickness top reservoir, the source algebra is consistent with

`HETOP * dC/dt = Load - Flux*C`.

With

`P = St*Flux/HETOP`, 

the positive-throughflow exact solution approaches a well-defined zero-capacity limit for fixed `Flux>0`:

`C_end -> Load/Flux`

and

`C_avg -> Load/Flux`

as `HETOP -> 0+`.

The initial stored mass `HETOP*C0` simultaneously tends to zero. Thus an instantaneous-passthrough interpretation is mathematically coherent for this one restricted condition.

It is not a complete zero-thickness model.

## 5. Why the positive-flow limit is insufficient

When `Flux=0`, the same governing equation reduces to

`HETOP * dC/dt = Load`.

For positive `Load`, the concentration increment scales as `Load*St/HETOP` and diverges as `HETOP -> 0+`, even though a finite areic mass can be accumulated. For `Load=0`, a finite concentration at zero thickness carries zero mass and is not identified by the physical storage.

The addition routine exposes the same structural issue: a positive fertilizer addition is converted to reservoir concentration by division by `HETOP`. Replacing that operation at zero would require a new decision about where the added mass resides or how it is routed within the time transaction.

Crop uptake introduces another independent limiting expression through `Flab(1)/HETOP`. Even where an analytical limit could be derived, revision 53 does not implement a zero-specific evaluation contract.

Therefore the zero-capacity positive-flow limit cannot simply be promoted to a universal `HETOP=0` policy.

## 6. Relation to TCD-042-E1 and NQ03

NQ03 qualifies a restricted small-`P` numerical policy for finite-positive `Flux` with `Hetop>0` and the observed natural envelope.

That policy cannot be extended toward `HETOP=0`: for any fixed positive `Flux`, `P = St*Flux/HETOP` grows without bound as `HETOP` tends to zero. The zero-thickness problem therefore leaves the NQ03 qualified small-`P` domain rather than becoming a special point inside it.

UBQ04 changes neither TCD-042-E1 nor TCD-042-B1.

## 7. Candidate interpretations and disposition

Three plausible interpretations were tested against the available evidence.

### Input endpoint invalid

One could change the contract to `HETOP>0`. This avoids the singular expressions and preserves the positive-thickness reservoir model. It is not qualified because the authoritative ANIMO 4.0 input table explicitly includes zero and no version-specific authority was found explaining that inclusion as an error.

### Zero-capacity instantaneous passthrough

One could define zero as no residence time and use the positive-flow limiting solution. This is mathematically unique for fixed `Flux>0`, but it fails to define finite concentration state for positive load at zero flow and does not define addition routing. The documentation also never declares zero to be such a sentinel.

### Conditionally admissible zero

One could allow zero only when no active feature needs the top-reservoir storage. This could reconcile an inclusive input range with some harmless multiplication-only paths. It is not presently executable as a contract because revision 53 has no documented safe-option matrix and crop-uptake paths evaluate `Flab(1)/HETOP` without a zero-specific guard.

None of these three candidates is sufficiently supported to become the model policy.

## 8. Qualified conclusion

UBQ04 qualifies the nonuniqueness itself:

`QUALIFIED_HETOP_ZERO_SEMANTIC_NONUNIQUENESS_NO_MODEL_POLICY_SELECTED`

This is a positive qualification result about the evidence boundary, not a scientific admission.

The following remain prohibited:

- silently changing the SOIL.INP lower bound from zero to a positive number;
- treating zero as an instantaneous-passthrough switch;
- inventing a feature matrix for conditionally safe zero use;
- widening NQ03 or either TCD-042 child to cover `HETOP=0`;
- reserving a new TCD solely because the endpoint remains unresolved;
- modifying production source.

## 9. What would close the question

A later workunit needs at least one authoritative version-specific source that explicitly resolves the endpoint, for example:

- ANIMO 3.5 or 4.0 process documentation that states the zero-reservoir semantics;
- source lineage showing an explicit zero branch or an input-contract change;
- a historical change specification explaining the inclusive lower bound;
- or an authoritative scientific/maintainer clarification that defines storage, additions, zero-flow and crop-uptake behaviour together.

Until then, the safe canonical position is `Hetop>0` for the already qualified B1/E1 scopes and fail closed for the broader zero endpoint.
