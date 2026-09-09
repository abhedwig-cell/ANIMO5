# ANIMO5 Consolidated Candidate Architecture

Work unit: `ANIMO-ARCHG01`

Decision: `QUALIFIED_CONSOLIDATED_CANDIDATE_ARCHITECTURE_PRODUCTION_IMPLEMENTATION_NOT_ADMITTED`

Status: candidate architecture consolidation, revalidated after ANIMO-TS01 closeout. This document does not admit a production architecture, a B3 scientific baseline, a numerical policy, a canonical TIME policy, or a B4 implementation.

## 1. Current governance and authority position

ARCHG01 remains on `work/animo-archg01-candidate-architecture-consolidation` and is based on the linear ARCH01 through ARCH07 candidate-design lineage ending at `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`.

RG02 has now qualified branch-authority governance and a provenance-qualified preparatory aggregate at live branch head `ec8709cd6a37c985ab7452bc0f2e6e64a430db6a`, with decision `QUALIFIED_BRANCH_AUTHORITY_GOVERNANCE_CONVERGENCE_AND_PREPARATORY_AGGREGATE_G5_PENDING`.

RG02 confirms ARCH01 through ARCH07 as authoritative candidate designs at the heads used by ARCHG01. Its older authority snapshot still records ARCHG01 itself as unresolved because that snapshot was taken before independent ARCHG01 persistence. RG02 explicitly requires a live G5 refresh when later persisted ARCHG01 evidence exists. ARCHG01 therefore prepares a G5 attachment packet but does not modify RG02 governance history or claim canonical integration authority.

| Work unit | Authoritative candidate branch | Head |
|---|---|---|
| ARCH01 | `work/animo-arch01-state-ownership-typed-transfers` | `24f57d8daab828f88446a79bd6a276f2925c828b` |
| ARCH02 | `work/animo-arch02-restart-checkpoint-sufficiency` | `a079d93c965f6073586c55ee4b3544dd8873b723` |
| ARCH03 | `work/animo-arch03-mass-ledger-observer` | `bc27bd7cf0c8148b38768315d2fa54014f5a6cf9` |
| ARCH04 | `work/animo-arch04-feature-activation-state-allocation` | `87930bbdfc413ad626176ce119f52ea409198f1d` |
| ARCH05 | `work/animo-arch05-external-exchange-contracts` | `99b6098a19db405ce34928af89bb78b856dce7cd` |
| ARCH06 | `work/animo-arch06-normalized-model-configuration` | `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4` |
| ARCH07 | `work/animo-arch07-adapter-qualification-spec` | `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6` |

## 2. Evidence basis and non-admissions

The consolidation uses the B0 to B4 governance model, PREP03 interface and parser evidence, PREP06 conserved-state and transfer evidence, TQ01 testcase qualification, B3Q01 scientific admission classes, NQ01 numerical qualification architecture, ARCH01 through ARCH07, and now qualified source-bound TS01 temporal semantics.

Relevant live supporting heads at this revalidation are:

- TH01: `a3360415364ef4a66a81d7b6715bcd400829df1b`;
- TQ01: `5c43ee16df37a0a1357614fdec527f25e5ca8c16`;
- NQ01: `e558dff12b127e0662cad62beea7527b42ad89ac`;
- B3Q01: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- TS01: `ed12a678cfba19ce851eb2f380e6da3f49203fe4`.

Frozen B0 source, testbank and documentation identities are unchanged. No B1 diagnostic observation is promoted to B2 or B3. No architecture choice closes a theory, scientific-admission, reference, or numerical-policy gap.

## 3. Consolidated candidate object graph

```text
ModelConfiguration
        |
        v
AcceptedState ---- immutable ExternalExchange frames
        |                     |
        | begin_trial         |
        v                     v
TrialState <------------- StepContext
        |
        +---- TrialScratch / provisional results
        |
        +---- TransferEvent journal
        |
        +---- trial DiagnosticsView
        |
        +---- reject -> discard trial state + events + scratch
        |
        +---- accept -> next AcceptedState + committed event journal
                              |
                              +---- MassLedger observer
                              |
                              +---- RestartSnapshot at accepted boundary
```

`ModelState` is only the logical aggregate root for ANIMO-owned continuation-critical physical state. It does not absorb immutable configuration, foreign-owned hydrology or crop state, forcing, diagnostics, journals, or scratch.

`AcceptedState` and `TrialState` are modern lifecycle roles. TS01 confirms that revision 53 has meaningful start/current and result/end generations, but it also shows that legacy current/start arrays are mutated during the interval and that legacy has no literal atomic end-step commit. The modern lifecycle is therefore an abstraction whose behavioural equivalence remains subject to TIME and reference qualification.

## 4. TS01 revalidation result

TS01 closes with `QUALIFIED_SOURCE_BOUND_TEMPORAL_SEMANTICS_PREPARATORY_EVIDENCE`. It reconstructs source order and state-generation visibility but does not qualify a canonical ANIMO5 TIME controller or production transaction policy.

The candidate object separation survives TS01 without adding a mega-state or changing ownership. The following constraints are now binding on future migration seams:

1. same-step management and residue mutations must be visible to later processes exactly where the source observes them;
2. management uses `(t0,t1]`, annual harvest/root residue uses `[t0,t1)`, and balance reporting uses its own half-step crossing rule;
3. addition precedes ploughing within one management row;
4. potential biochemical results are provisional and must not enter the committed physical transfer journal as actual transfers;
5. generic solute and phosphorus layer processing follows `Sqnu` order, with same-step downstream propagation where source-defined;
6. `Resp_miner` contains intentional previous-step neighbour reads that must remain distinguishable from latest trial values;
7. soil-side crop uptake and plant-side result integration represent one physical nutrient transfer, not two removals;
8. first-step, ordinary-step and final-step generations are asymmetric;
9. `Outbal_calc` and report resets are observer/report continuation semantics, not physical acceptance;
10. `INITIAL.OUT` is not a canonical checkpoint schema and `Output_Init` is not a pure serializer.

TS01 therefore resolves source-order uncertainty, but not behavioural equivalence of a modern atomic commit, retry/reject policy, mid-step checkpointing, runtime topology changes, or the future canonical time representation.

## 5. State ownership reconciliation

Every continuation-critical physical store has one canonical runtime owner.

- ANIMO owns soil chemical state and optional ANIMO-owned crop state.
- Hydrological state remains externally owned even when its coordinates are needed for aqueous storage and transport.
- External crop state remains externally owned in external crop mode.
- Reporting accumulators, detailed process arrays, derived totals and scratch are not physical owners.
- Crop is an explicit conservation compartment when whole soil-crop closure is requested.
- Macropore physical state must exist explicitly if that feature is admitted.
- Inactive optional physical state is absent rather than hidden as persistent zero state.
- Parser-visible but unsupported dormant surface stable DOM/DON/DOP is not canonical state.
- Site-resolved phosphorus state remains site-resolved.
- GHG state remains conditional and blocked pending theory-to-ledger qualification.

## 6. Read-generation contract

TS01 makes one refinement mandatory: a process API cannot expose only a generic `state` view.

Each migrated process seam must state whether a read is from:

- beginning accepted state;
- post-management trial state;
- provisional potential-pass result;
- actual same-step result;
- explicitly previous-step neighbour state;
- same-step upstream average/result propagated in `Sqnu` order;
- immutable external-owner observation.

This is a contract requirement, not permission to change source order. A future scheduler may be cleaner than the legacy main program, but any changed ordering or read generation requires explicit B3, NQ or reference qualification as applicable.

## 7. Restart and checkpoint consistency

The candidate restart model remains structurally coherent:

- checkpoint only accepted physical state;
- exclude uncommitted trial state and provisional scratch;
- serialize ANIMO-owned stores in canonical owner representation;
- coordinate external hydrology/crop restore through their owners;
- fail closed on incompatible configuration, layout, geometry, feature, site-count, ownership or schema identity;
- keep diagnostic continuation separate from physical state.

TS01 adds two hard constraints. First, strong continuous-versus-split equivalence remains unqualified because `INITIAL.OUT` omits continuation context such as management/event cursors, reporting accumulators and complete external-owner synchronization state. Second, `Output_Init` can clamp a negative phosphorus crop result before writing. A modern `RestartSnapshot` must remain a read-only serialization of accepted canonical state. Any legacy restart compatibility transformation must be explicit and separately qualified.

## 8. MassLedger derivation rule

For an ANIMO-owned control volume, `MassLedger` derives from beginning/end canonical owner projections plus the committed `TransferEvent` journal.

For control volumes containing foreign-owned stores, use a read-only ownership-aware `CanonicalStateView`: ANIMO accepted state plus immutable authoritative external-owner observations. Foreign state is never copied into `ModelState` merely for accounting convenience.

The ledger remains an observer. It cannot repair residuals, create balancing fluxes, choose tolerances, or cause commit.

## 9. External exchange and typed transfers

`ExternalExchange` and `TransferEvent` remain different semantic types.

External frames may contain state observations, forcing, producer and generation identity, interval transfer quantities, and crop demand. Only validated physical transfer quantities normalize exactly once into directed non-negative `TransferEvent` records. State observations stay observations and control metadata stays metadata.

TS01 additionally requires interval identity and event timing to preserve source-observed boundary semantics. Hydrology record alignment remains an explicit future adapter validation seam rather than an implicit sequence assumption.

## 10. Configuration, feature activation and adapters

Normalized configuration remains fail closed. Parser visibility does not imply runtime or scientific admission. Unsupported or ambiguous legacy options must produce an explicit unsupported/error disposition rather than hidden activation.

The `LegacyInputAdapter` remains outside the scientific process kernel. It may translate only explicitly supported and qualified semantics, preserve B0 provenance, resolve convenience defaults before normalization, and never invent feature admission, scientific defaults, units, tolerance or process semantics.

Concrete adapters remain unqualified until ARCH07-style runtime evidence exists.

## 11. Numerical and scientific boundaries

NQ01 remains binding. ARCHG01 defines no epsilon, tolerance, floating precision, convergence criterion or nonlinear policy. Reordered layer execution, altered stale/current reads, or other nonexact numerical differences require separate qualification.

B3Q01 remains authoritative for scientific dispositions. Architecture cannot close GHG theory, macropore state/ledger admission, stable DOM issues, phosphorus site/index semantics, negative-concentration/dry-solute continuation semantics, Class E numerical changes, Class F physics changes, or historical-behaviour uncertainty that needs B2/reference evidence.

## 12. Migration readiness after TS01

| Area | Candidate design coherent | Production implementation admitted |
|---|---:|---:|
| state ownership | yes | no |
| accepted/trial lifecycle | yes as modern abstraction | no, behavioural TIME/reference qualification still required |
| source process order and read generations | reconstructed by TS01 | no reordering admitted |
| event endpoint semantics | source-bound reconstructed | no normalization change admitted |
| restart payload structure | yes | no, split-run/reference evidence required |
| MassLedger observer model | yes | no, runtime event producers and scientific admissions required |
| feature allocation | yes | no |
| external exchange schemas | yes | no concrete coupled adapter qualified |
| normalized configuration | yes | no production parser/adapter qualified |
| numerical acceptance policy | intentionally absent | no |
| B3 scientific dispositions | referenced only | no |

The serial architecture gate is therefore no longer blocked by unknown legacy ordering. It is blocked by the distinction between source-bound temporal reconstruction and a qualified modern TIME/transaction implementation.

## 13. Governance handoff

RG02 identifies G5 as the next safe integration gate: attach independent theory, testcase, numerical, temporal, scientific and architecture streams by explicit authority references without collapsing their evidence strength.

ARCHG01 provides `integration/animo-architecture/ANIMO-ARCHG01_G5_ATTACHMENT.json` and `docs/architecture/ANIMO5_ARCHG01_G5_ATTACHMENT.md` for that purpose. This is an attachment packet, not a merge request and not a B3/B4 admission.

## 14. Decision

After TS01 closeout, ARCH01 through ARCH07 plus the ARCHG01 reconciliation still form an internally coherent candidate architecture. TS01 requires stricter process read-generation and ordering contracts, but it does not invalidate the core type separation, ownership model, typed-transfer model, observer-only ledger, fail-closed configuration, or external exchange boundary.

The closeout decision remains:

`QUALIFIED_CONSOLIDATED_CANDIDATE_ARCHITECTURE_PRODUCTION_IMPLEMENTATION_NOT_ADMITTED`
