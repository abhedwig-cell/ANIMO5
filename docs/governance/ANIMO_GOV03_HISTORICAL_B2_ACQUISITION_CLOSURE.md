# ANIMO-GOV03 Historical B2 Acquisition Closure

Work unit: `ANIMO-GOV03`

Branch: `work/animo-gov03-historical-b2-acquisition-closure`

Base: `ANIMO-RG05@f127528e148b9106149daec02d48ad972581e6df`

GOV02 authority: `work/animo-gov02-evidence-dag-reconciliation@db7add6f9561730bbf352aa7fd3f3968405cfaa3`

PREP02R authority: `work/animo-prep02r-historical-reference-recovery@a2fda49871ee3c7104daf7e06cd8dffdac06b125`

## Purpose

GOV03 records acquisition work that had actually been completed outside the repository but was not yet represented in the governance state. The purpose is narrow: determine whether the GOV02 bounded acquisition contract is now satisfied and whether the historical-uncertainty route may be considered for later claim-scoped B3 dispositions.

GOV03 does not create B2 evidence, does not prove historical behaviour, and does not admit any scientific correction.

## Completed expert/archive acquisition

The project owner records that the historical ANIMO archive search was carried out over several days and completed on 2026-09-09. Directly involved ANIMO experts were asked extensively about surviving ANIMO archives and each checked their own available archive material.

Named routes included:

- Piet Groenendijk;
- Leo Renaud;
- Marius Heinen.

No additional usable provenance-qualified historical executable, preserved official testcase output bundle, or archival release package suitable as a behavioural B2 reference was recovered.

The material that remained available was the existing Fortran source/code repository and an already known historical executable that did not provide a usable reference path. The practical reference therefore remains a rebuild made from the available frozen Fortran source under explicit provenance and hash control.

Piet Groenendijk additionally concurred that proceeding from the available code with such a rebuild is the correct route. GOV03 uses that statement only as independent expert concurrence with the acquisition stopping/continuation rationale. It is not treated as historical output evidence and is not a scientific B3 review.

## GOV02 reasonable-effort mapping

The authoritative GOV02 closure contract defines `DOCUMENTED_REASONABLE_B2_ACQUISITION_EFFORT` using seven conditions. GOV03 maps the completed record as follows.

1. **Targeted institutional/expert route actually executed: PASS.** Named direct ANIMO expert contacts were used and their archives were searched.
2. **Response or negative evidence trail persisted: PASS.** The named negative acquisition outcome is now persisted in `GOV03_ACQUISITION_EVIDENCE.json`.
3. **Additional plausible route attempted: PASS.** Multiple separate expert/archive routes were used, not a single failed contact.
4. **Search history persisted: PASS.** PREP02R already persists the internal/public repository and artifact search history; GOV03 adds the completed named expert/archive phase and completion date.
5. **Stopping rationale: PASS.** The directly relevant expert archives were searched, no usable B2 reference was recovered, and further generic searching has low expected value for this defined scope.
6. **Independent stopping-rationale review: PASS for acquisition closure only.** Piet Groenendijk independently searched archive material and concurred that continuing from the source with a rebuild is the correct route. This is not reused as an independent scientific review of any TCD.
7. **No known high-probability route deliberately left unexplored: PASS on project-owner attestation.** No additional concrete high-probability archive route was identified after the multi-expert search.

## Qualified closure interpretation

If structural validation succeeds, GOV03 qualifies:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

This state does **not** mean that a B2 reference exists. It means the bounded acquisition contract has been executed and closed without recovering a usable B2 behavioural reference.

The resulting G6U interpretation is:

`ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`

That eligibility is only a route opening. Every later B3 disposition must still satisfy its own class-specific GOV02/B3Q01 scientific, causal, numerical, state, coverage, and independent-review requirements. Historical behaviour remains `UNKNOWN` where no B2 evidence exists.

## Explicit non-claims

GOV03 does not:

- promote the problematic historical executable to B2;
- promote the rebuild to historical B2;
- promote source code to a behavioural oracle;
- claim whole-model historical equivalence;
- admit corrected legacy behaviour;
- admit canonical STATE, TIME, MASS, or external exchange;
- establish B4;
- modify production source;
- modify the canonical TCD register;
- waive independent B3 review requirements.

## Reopening rule

If a credible historical artifact is discovered later, B2 qualification reopens immediately for the relevant scope. The GOV03 stopping rationale records why acquisition was reasonably closed on 2026-09-09; it is not a reason to ignore later evidence.
