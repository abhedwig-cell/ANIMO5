# ANIMO-TH01 theory evidence reconciliation with canonical TCD register

Status: `EXISTING_TCD_SET_RETAINED_WITH_STRONGER_THEORY_CONTEXT_NO_FALSE_CLOSURE`

TH01 synchronized the canonical `docs/quality/THEORY_CODE_DISCREPANCY_REGISTER.csv` with the qualified PREP06 register through `TCD-027` before completing this reconciliation. This avoids silently dropping PREP06 findings when the TH01 branch was created from the EB01 evidence-governance branch.

TH01 does not create a new TCD merely because a revision-53 option lacks complete independent theory. The extension-provenance register is the primary owner for those evidence gaps unless a concrete theory/code discrepancy or unsupported operational surface is established.

## Existing TCDs strengthened by TH01

### TCD-007 macropore

The uncertainty is narrower than at initial PREP01 discovery.

The two-domain Main Bypass / Internal Catchment hydrological architecture has independent SWAP theory support and the ANIMO 4.0 guide already exposes the intended macropore interface while explicitly marking it non-operational in 4.0. Revision 53 contains active ANIMO macropore water and solute routines.

What remains unresolved is the ANIMO-specific nutrient-transfer formulation and version-specific operational contract. TCD-025 separately records the source-confirmed mismatch between the specialized macropore control volume and the public/main balance interface.

TCD-007 remains `OPEN`.

### TCD-008 greenhouse gases

Public SWAP-ANIMO literature independently confirms a process-based CO2/CH4/N2O extension and the frozen source contains matching process families and implementation-history comments.

TH01 can therefore classify the broad scientific intent as `THEORY_PARTIALLY_RECONSTRUCTED` rather than source-only invention. Exact revision-53 equations, parameter provenance and parser/testcase lineage remain unqualified. TCD-013 continues to block the supplied GHGMais case as a revision-53 reference.

TCD-008 remains `OPEN`.

### TCD-021 stable dissolved organic matter

TH01 found independent post-2005 development/provenance evidence for a second stable dissolved-organic-matter pool. A 2008 WUR study recommends the added pool. A 2011 BMBF/UFZ report describes development from ANIMO 3.8, records active participation by Alterra ANIMO developers, and contains a stable-DOM carbon process diagram with parameter names that strongly overlap the frozen revision-53 source, including `Ratio_rd_st`, `sdofr`, `recfSDO`, `recfHSDO` and `asfaSDO`.

This is sufficient to strengthen the broad carbon-process intent evidence, but not to declare the exact revision-53 C/N/P algebra authoritative. The 2011 report calls its modified branch `ANIMO Version 4.0`, while the supplied canonical 2005 ANIMO 4.0 User's Guide has only one DOM pool and predates that development project. TH01 therefore classifies the release-number relation as `CONFLICTING_EVIDENCE` rather than silently mapping the external version label onto the frozen source lineage.

TCD-021 remains `OPEN` as a version/lineage and N/P-formulation gap. TCD-023 remains the separate source-confirmed stable-DOM P algebra defect.

### TCD-024 slow Langmuir

TH01 strengthens the theory side materially: the supplied ANIMO 4.0 guide explicitly documents `OPTCXSL=2` slow Langmuir, one to three non-equilibrium sites and site-specific adsorption/desorption parameters. Slow Langmuir is therefore an inherited documented option, not merely a revision-53 source artifact.

That makes the revision-53 use of the nonlinear trial counter `I` where the site index `J` is required even less ambiguous as a theory/data-model conflict. PREP05 already provides causal synthetic evidence and non-interference evidence for the Freundlich branch.

TCD-024 remains `OPEN` because the corrected historical behavior is not independently qualified. Its scientific interpretation is strengthened, not its admission status.

## Parser-visible surfaces without a new TCD

`PClassOption` / `PClassYearSwitch` / `PClass` are retained in TH01 as `CODE_DEFINED_THEORY_UNCONFIRMED`. Source comments tie the selector to an EMW2012 context, and public EMW2012 material confirms P-status-class policy changes existed in that policy-evaluation period, but TH01 did not find evidence that defines the exact class-indexed crop-forcing arrays or switching semantics in revision 53. That is not enough to assert a concrete code defect.

`SoilTempFile` is treated as a later parser/input-routing surface over inherited temperature-dependent process theory. No physics discrepancy is claimed without evidence of a changed response relation.

`SulphateSimulation` already has TCD-022 because the parser-visible option lacks an observable corresponding process implementation/balance writer in the frozen source.

## Canonical-register decision

No existing TCD is closed or downgraded by TH01.

No new defect TCD is opened solely from missing theory.

The canonical register is synchronized through PREP06 `TCD-027`; TH01's process-specific theory qualification documents and `REV53_THEORY_PROVENANCE_REGISTER.csv` carry the strengthened evidence classes and B3-readiness judgements.

Production migration remains `NOT_ADMITTED`.
