# B3 Qualification Classes

Work unit: `ANIMO-B3Q01`

This classification governs how a discrepancy may be qualified. Classification is not admission.

## Class A: Accounting or reporting-only correction

Use Class A only when the physical state and process flux trajectories are already represented and the defect is confined to a ledger, accumulator, reporting balance or balance interface.

Typical examples:

- omitted beginning or end storage in a balance;
- omitted side of an internal transfer;
- detailed accumulator seeded from the wrong reporting slot;
- existing physical state omitted from a public balance interface.

A Class A correction must prove:

- physical state trajectory unchanged;
- process flux trajectory unchanged;
- only declared ledger or reporting quantities change;
- the intended conservation or reporting identity is restored;
- non-interference outside the declared reporting surface.

Normal B2 route:

- compare historical ledger/report output where available;
- preserve historical disagreement explicitly;
- show corrected ledger identity and exact unchanged state/flux evidence.

Historical uncertainty route:

- requires a closed accounting identity or equivalent authoritative definition;
- requires state and flux equivalence evidence independent of the proposed ledger code;
- requires second-line review;
- may not be used when the proposed change alters initialization, state, process flux or numerical policy.

If state or flux changes occur, the item is not Class A.

## Class B: Local algebra, index or species correction

Use Class B for a local implementation defect where the intended mathematical operation can be identified without introducing a new state model or changing numerical policy.

Typical examples:

- wrong array index;
- wrong species term;
- sign error;
- duplicated algebraic term;
- local conservation term counted twice.

A Class B correction must prove:

- exact causal code path and trigger condition;
- the mathematical or species identity that the legacy expression violates;
- the proposed local correction;
- exact expected affected states, fluxes and outputs;
- branch coverage of both defective and corrected paths;
- conservation impact where applicable;
- non-interference outside the affected process surface;
- historical disagreement retained as evidence.

Normal B2 route:

- reproduce the relevant path under B2 where technically possible;
- compare unrounded affected states or fluxes when the effect is smaller than report precision;
- do not treat historical agreement as proof that the algebra is scientifically correct.

Historical uncertainty route:

- requires authoritative theory or an unambiguous local mathematical identity;
- requires at least two independent forms of causal evidence, for example source algebra plus a conservation closure test;
- requires stronger branch coverage and second-line review;
- synthetic coverage may establish causality but cannot establish historical prevalence.

A local correction that also changes tolerance, solver convergence or state representation must be split or reclassified.

## Class C: Missing physical state or incomplete state model

Use Class C when the discrepancy cannot be corrected without adding, splitting or redefining a physical storage or phase state.

Typical examples:

- dry-solute mass has no representable continuation state;
- unresolved sorbed, precipitated or phase storage is required to conserve mass;
- restart semantics cannot represent a physically required store.

Class C is not a local bugfix class.

A Class C qualification must prove:

- authoritative theory for the missing state or phase;
- state variable definition, units and ownership;
- initialization and restart semantics;
- transfer in and out of the state;
- phase-transition or activation conditions;
- conservation closure over all connected processes;
- expected differences to state and flux trajectories;
- edge-case tests, including appearance and disappearance of the state;
- non-interference outside the connected physical subsystem.

Normal B2 route:

- B2 is used to characterize historical behaviour and quantify the divergence introduced by the new state representation;
- B2 cannot by itself justify a physically incomplete state model.

Historical uncertainty route:

- requires authoritative theory strong enough to define the missing state independently of legacy behaviour;
- requires independent scientific review, not only code review;
- must keep historical behaviour explicitly unknown;
- if the state formulation is not adequately documented, the item remains `UNRESOLVED_NOT_ADMITTED`.

Class C may result in a scientifically qualified corrected legacy behaviour only through a dedicated state-model admission workunit.

## Class D: Representation-only modernization

Use Class D for implementation restructuring that changes representation but not admitted behaviour.

Typical examples:

- moving state ownership into an explicit owner object;
- replacing parallel ledger arrays by typed transfer events;
- reducing an interface while preserving values and call semantics;
- changing storage layout without changing model equations or numerical policy.

Class D is evaluated against an already admitted B3 scope. It cannot be used to define B3 scientific behaviour in the first place.

A Class D qualification must prove:

- exact admitted B3 target identity;
- behavioural equivalence within that admitted scope;
- state and flux equivalence at the required precision;
- no change to process ordering, initialization, restart or numerical policy unless separately qualified;
- ownership and unit consistency;
- non-interference across unaffected process domains.

Normal B2 route:

- B2 may remain a supplementary anchor, but the direct target is the admitted B3 behaviour.

Historical uncertainty route:

- a Class D change inherits any historical uncertainty already attached to the admitted B3 target;
- representation equivalence cannot reduce or erase that uncertainty;
- D cannot use uncertainty to widen scientific scope.

The only admitted disposition for a pure Class D item is `REPRESENTATION_CHANGE_ONLY`.

## Class E: Numerical-policy change

Use Class E when the proposed difference changes how an existing mathematical model is solved or approximated.

Typical examples:

- nonlinear solver tolerance;
- Newton convergence policy;
- local linearization or secant policy;
- precision or rounding policy;
- small-delta approximation;
- clipping or convergence threshold when it changes the numerical solution.

A lower mass-balance residual is not sufficient qualification.

A Class E qualification must prove:

- governing equations and conserved quantities;
- exact legacy numerical policy;
- proposed numerical policy;
- convergence behaviour across a defined envelope;
- precision sensitivity;
- conservation behaviour;
- state and flux trajectory sensitivity;
- failure and fallback behaviour;
- expected differences and accepted numerical bounds derived from the equations and convergence evidence, not from defective historical maxima.

Normal B2 route:

- characterize historical numerical behaviour with unrounded output where available;
- quantify whether B2 sits inside the qualified convergence envelope;
- preserve material historical differences explicitly.

Historical uncertainty route:

- permitted only for narrow, well-specified numerical changes with strong convergence evidence;
- requires independent numerical review and at least one precision or discretization sensitivity axis;
- cannot be used to justify arbitrary tolerances or broad solver replacement;
- broad policy changes remain `NUMERICAL_POLICY_CHANGE_REQUIRES_SEPARATE_QUALIFICATION` until a dedicated numerical workunit qualifies them.

A Class E item is never admitted merely because conservation improves.

## Class F: Physics or model evolution

Use Class F when the governing scientific formulation, constitutive theory or model scope changes.

Typical examples:

- adding a new governing process;
- changing a constitutive relationship for scientific reasons;
- changing phase definitions or process coupling beyond correction of a proven implementation error;
- replacing a documented legacy model formulation with a newer scientific model.

Class F is normally outside corrected legacy B3 admission.

A Class F qualification must define:

- scientific rationale and authoritative theory;
- relationship to the preserved B3 baseline;
- calibration and parameter implications;
- conservation implications;
- validation evidence appropriate to the process;
- expected changes over the intended application envelope;
- independent scientific review.

Normal B2 route:

- B2 is used only to characterize the historical model being evolved.

Historical uncertainty route:

- cannot convert new physics into a claim of corrected historical behaviour;
- historical behaviour remains unknown if B2 is unavailable;
- the change requires a separate scientific admission after the preservation baseline unless authoritative version-specific theory proves that the legacy implementation contradicted the intended model.

If authoritative intended theory proves a local legacy implementation mistake, the atomic correction should be reclassified to Class B or C as appropriate. Otherwise the disposition is `PHYSICS_CHANGE_REQUIRES_SEPARATE_SCIENTIFIC_ADMISSION`.

## Compound discrepancies

The qualification class applies to one atomic correction mechanism.

A parent TCD may expose more than one mechanism. The parent must then be marked `REQUIRES_ATOMIZATION` and split into child qualification records before any part is admitted.

The strictest class governs until the split is complete.

For example, an initial-state issue that can be addressed either by exposing a ledger adjustment or by changing a consistency threshold is not one Class A correction. The ledger addition is Class A. The threshold or projection policy is Class E. They require separate evidence and separate dispositions.
