# ANIMO-TQ01 B2/B3 testcase selection guidance

Status: `PREPARATORY_SELECTION_GUIDANCE_NOT_REFERENCE_ADMISSION`.

This note translates the TQ01 lineage, process, option and evidence-strength matrices into a case-selection strategy for later B2 historical-reference capture and B3 scientific qualification. It does not promote any case to B2 or B3.

## Selection principle

Do not choose one historical testcase and treat it as a universal reference. The supplied cases are complementary. Case selection must follow the process or discrepancy being qualified.

A useful B2/B3 sequence is:

1. establish a simple native execution and capture contract;
2. add a rich multi-process case with naturally reached management and P pathways;
3. add targeted natural cases for known discrepancy classes;
4. use synthetic descendants only where the historical bank has no natural route coverage;
5. keep GHG outside revision-53 behavioural qualification until lineage is recovered.

## Candidate roles

### RuurloGrass: first native capture / smoke case

PREP02R already designates `RuurloGrass` as the native-first case. TQ01 supports that choice as an operational starting point because it is revision-53 parser-compatible under B1, P is disabled, and it avoids the unresolved GHGMais lineage. Its role is to validate receipt, execution, deterministic capture and formatted/unrounded comparison plumbing. It is not sufficient for P, ploughing, GHG, macropore or restart qualification.

### LWKM_gras_1040.2021.2045: primary rich-process case

LWKM currently carries the deepest natural diagnostic evidence among the supplied compatible cases. It has active C/N/P, external crop uptake, aeration option 1, natural plough events, fast Langmuir sorption and slow Freundlich sorption. Natural observers also show nonzero heterogeneous slow-sorbed P at ploughing. It is therefore the strongest candidate for later B2/B3 qualification of P management, P numerical/conservation seams, accounting-only corrections and several restart questions.

Its breadth is also a limitation: when a discrepancy needs causal isolation, a simpler natural case or a controlled diagnostic descendant may be required. Synthetic descendants remain diagnostic only.

### Puitmijn_Cranendonck_60: dry-down and stable-DOM case

Puitmijn has natural case-specific evidence for the NH4 surface dry-down state-model gap and for the stable-DOM phosphorus partition defect. It is therefore a preferred natural qualification case for those discrepancy families once B2 evidence is available. It should not be substituted by LWKM merely for convenience because the relevant natural events differ.

### CranGrass: PO4 initialization case

CranGrass naturally exposes the first-step PO4 initialization/state-consistency seam. It is the preferred supplied case for qualification of that initial-state problem. This role is distinct from steady-state P transport or ploughing qualification.

### GrassPeat and STONE: external-crop / restart evidence

Both are useful for later restart qualification because natural diagnostic evidence observes nonzero plant state at restart-relevant boundaries. STONE additionally has 15 observed natural plough events. A future continuous-versus-split reference program should include at least one of these in addition to a simpler first native case.

### CranMais: non-P management/plough control

CranMais has nine natural plough events while phosphorus is disabled. That makes it useful as a control for management redistribution and non-P accounting paths, especially when checking that P-specific changes do not perturb C/N behaviour.

### Zuiderzeeland_MeeuwenTocht_1_Akkerbouw_AWA: internal-crop plough/restart case

This case has three natural plough events and nonzero actual plant restart state. TQ01 also established that the active management/crop mapping selects the ANIMO grassland branch despite `Akkerbouw_AWA` in the directory name. The active input contract, not the folder label, must determine qualification semantics.

### GHGMais: lineage recovery target only

GHGMais is the only supplied GHG-active artifact but is structurally incompatible with revision-53 GHG/material input parsing. It must not be used for revision-53 B2 behaviour. Its immediate value is provenance recovery: identify the source/executable lineage that natively consumes the supplied schema, or obtain a provenance-qualified GHG case that matches revision 53.

## Coverage that no supplied natural case can close

The current historical bank cannot by itself qualify:

- active macropores;
- slow Langmuir sorption (`Optcxsl=2`);
- slow linear sorption (`Optcxsl=1`);
- multi-site fast sorption (`Ncxfa>1`);
- aggregated hydrology (`Iwa=1`) and its dependent options;
- separate soil-temperature-file mode;
- P initialization modes 2 and 3;
- several other parser-admitted option values listed in `OPTION_COVERAGE_MATRIX.csv`.

For these gaps, synthetic or transformed cases may establish branch reachability, conservation identities, causality, bounds/index behaviour and non-interference. They do not create historical reference evidence. If a missing route is intended for production support, later B3 qualification requires an explicit scientific/provenance argument and, where historical behaviour matters, an independently trustworthy reference route.

## Recommended B2 capture order

This is a prioritization for evidence acquisition, not an admission ladder:

1. `RuurloGrass` for native execution/capture plumbing;
2. `LWKM_gras_1040.2021.2045` for broad C/N/P and plough/P evidence;
3. `Puitmijn_Cranendonck_60` for NH4 dry-down and stable-DOM discrepancies;
4. `CranGrass` for PO4 initialization;
5. one restart-rich external-crop case, preferably `STONE_akk_0006.2001.2015` or `GrassPeat`, using an explicit continuous-versus-split contract;
6. `CranMais` as a P-disabled plough/non-interference control;
7. remaining compatible cases as cross-case replication where the qualification question benefits from them.

GHGMais is not part of this revision-53 B2 order until its lineage gap is closed.

## B3 use

A B3 admission packet should cite only the cases relevant to the discrepancy or process under review and must state what each case proves. A successful B2 comparison in one case does not automatically qualify an option that the case never activates. Likewise, exact agreement in an inactive path is non-interference evidence, not positive process qualification.

No tolerance is defined here. No correction is admitted here. Production migration remains `NOT_ADMITTED`.
