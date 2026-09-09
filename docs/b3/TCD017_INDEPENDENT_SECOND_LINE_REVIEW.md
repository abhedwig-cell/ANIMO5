# ANIMO-B3A02R — Independent Second-Line Review of TCD-017 Class-A Admission Readiness

## Result

`PASS_TCD017_INDEPENDENT_SECOND_LINE_READINESS_REVIEW`

This is an independent second-line readiness review only. A PASS here is not B3 admission, does not authorize a production patch, and does not establish historical fidelity.

## Independence statement

This review was performed in a separate ChatGPT context from the B3A02 and B3D01 authoring contexts. Their conclusions were not accepted as authority. The frozen B3A02 files were treated as claims to be checked against pre-authoring source-bound evidence, frozen provenance, independent conservation evidence and current route governance.

No organizational or human independence is claimed.

## Frozen object and live route reconciliation

Reviewed frozen object:

`3ff8f4bda77c631b82110b83317c6a9b42b867ad`

Immediately before review persistence, branch `review/animo-b3a02r-tcd017-second-line` was rechecked live and still pointed exactly to that commit.

Primary frozen object blobs:

- `docs/b3/TCD017_CLASS_A_ADMISSION_READINESS.md` @ `dcca801d1a1e5636bfa887d1198188a70f731bfa`
- `integration/animo-b3/TCD017_EXPECTED_DIFFERENCE.json` @ `fc8d57197ddecb7f1c5f4229e9fd1de80e6668c3`
- `integration/animo-b3/TCD017_CLASS_A_READINESS.json` @ `4cf792b282f8d97493eacee26ff7103998a666ae`
- `integration/animo-b3/ANIMO-B3A02_STATUS.json` @ `4607a819f131628f69cdb034b08d28f7f8730e5a`

The issue #25 body is stale with respect to the B2 route. The latest handoff comment was rechecked and agrees with the live GOV03 branch.

Live route authorities checked:

- GOV03 head: `cbd262bdabe92923113b7326f2f42822ce9a971c`
- qualified closure: `B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`
- G6U: `ELIGIBLE_HISTORICAL_UNCERTAINTY_ROUTE_SUBJECT_TO_CLAIM_SCOPED_B3_REQUIREMENTS`
- B3D01 head: `6ada2522101587ab74974a70f980b50e64cf9b86`
- B3D01 disposition at review time: `UNRESOLVED_NOT_ADMITTED`

GOV03 does not create B2. Its persisted boundary is that historical behaviour remains unknown without B2. B3D01 likewise leaves admission unresolved pending this second-line review.

## Atomic claim reviewed

Only this claim was reviewed:

The existing top-reservoir dissolved-organic-P ploughing loss `Addiorpotoppl(I)` is omitted from the `Bapo(Redi,Ly)` redistribution ledger, while `Addiorpopl(I,Ln)` already records the corresponding redistributed layer change and the encompassing top-plus-layer physical redistribution is conservative.

Candidate accounting-only statement:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

No physical-state patch, ploughing-physics change, transport-policy change or numerical-policy change is included.

## Independent evidence reconstruction

### Frozen source identity

The frozen source archive remains identified by SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

The exact source manifest identifies:

- `Addit.for`: `e3cf8f427e9a4b3743742039c89aae57864cb7268893e45797c7a17427dc8f5d`
- `Outbal_calc.for`: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`

The raw licensed source bytes are deliberately not republished in this repository. Therefore this review does not claim a fresh raw-byte parse of those two Fortran files. Source semantics were rechecked independently of B3A02 by cross-reading the exact hash-bound PREP01 and PREP02 source audits, PREP06 conserved-state/transfer inventories, source manifest, runtime diagnostics and observed main-program ordering. This provenance limitation is retained as residual uncertainty rather than silently upgraded to direct source-byte evidence.

### Ownership and omission

PREP01 and PREP02 independently predate the B3A02 admission-readiness dossier and both identify `Addiorpotoppl` as the top-reservoir dissolved-organic-P loss produced in `Addit`. They identify `Addiorpopl(I,Ln)` as the redistributed layer change.

PREP06 maps the same transfer as `PLOUGH-DOM`, with the top DOP reservoir and layer DOP stores inside one internal control volume. Its conserved-state inventory keeps TOP-DOP and DOM-L-P as distinct physical stores.

The source-bound balance audit identifies the legacy reporting asymmetry: `Bapo(Redi,Ly)` includes `Addiorpopl(I,Ln)*Z`, but omits `Addiorpotoppl(I)*Z`, whereas analogous redistribution ledgers include their relevant top term. The candidate therefore adds the missing reporting side of an already executed internal transfer. It does not create the transfer.

### Natural activation and physical closure

The natural LWKM path contains a nonzero target event. The independently reviewed diagnostics give:

- top-reservoir DOP loss: `-0.15380316471773922 kg/ha P`
- redistributed layer DOP change: `+0.15380316471773947 kg/ha P`
- stable-DOP contribution in this target event: `0`
- encompassing top-plus-layer residual: approximately `2.5e-16 kg/ha P`

Thus the physical redistribution closes before the reporting correction is applied.

SYNQ-O002 supplies a separate conservation oracle for the same abstract internal-transfer identity. It is used here only as independent conservation evidence. Its own contract explicitly does not make it B2 and does not admit TCD-017.

### Reporting-only write-set and non-interference

The candidate write-set is one accumulation into `Bapo(Redi,Ly)` in `Outbal_calc`. The PREP01 orchestration inventory places `Outbal_calc` after the timestep physical process, transport, transformation and uptake sequence and inside the reporting stage.

The bounded diagnostic evidence reports unchanged physical/process trajectories and no normalized ordinary non-balance output changes for the target correction. The observed difference is confined to the organic-P balance/reporting surface. Together, the source-bound write target and runtime comparison support the Class-A readiness claim that the candidate does not write physical state or process flux.

This is a bounded readiness statement. It is not a whole-program historical-equivalence statement.

## Twelve-gate review

1. **Source/destination ownership: PASS.** `Addiorpotoppl` is the top-reservoir DOP loss; `Addiorpopl` is the layer redistribution. PREP06 independently maps the corresponding source and destination stores.

2. **Exact Bapo omission: PASS.** Hash-bound PREP01/PREP02 source audits identify `Addiorpopl(I,Ln)*Z` in `Bapo(Redi,Ly)` and the absence of `Addiorpotoppl(I)*Z`.

3. **Natural LWKM activation: PASS.** The target top term is nonzero in natural LWKM evidence.

4. **Physical control-volume closure before correction: PASS.** The natural top-plus-layer redistribution closes to approximately `2.5e-16 kg/ha P`; SYNQ-O002 independently confirms the internal-transfer conservation identity.

5. **Candidate write-set reporting/ledger only: PASS.** The candidate changes `Bapo(Redi,Ly)` only. No `Addit`, state, transport, reaction or management write is introduced.

6. **Physical-state trajectory cannot be affected within the bounded candidate: PASS.** The write occurs in reporting after the physical process chain, and diagnostic state/output comparisons show no non-report trajectory change.

7. **Process-flux trajectory cannot be affected within the bounded candidate: PASS.** No process-flux variable is written and the bounded comparisons show no ordinary process-output change.

8. **Expected-difference whitelist complete: PASS.** Allowed differences are `Bapo(Redi,Ly)` for active target events, derived organic-P balance fields and `bapo*.Out` reporting surfaces. Physical state, process fluxes, `Bafop` and non-whitelisted outputs are forbidden.

9. **Other organic-P changes excluded: PASS.** TCD-027 is the separate `Bafop(24)` detailed-accumulator defect. TCD-028 is the separate stable-DOM plough event-accumulator lifecycle candidate and can affect physical redistribution under affected storage semantics. `AdStdiorpopl` and `Adhuexpopl` are separately identified PREP02 findings. None is part of TCD-017.

10. **SYNQ-O002 role bounded correctly: PASS.** It is independent conservation evidence only, never B2 and never admission evidence.

11. **PREP01/PREP02/PREP06/B3Q01/GOV03/SYNQ01 consistency: PASS.** The evidence agrees on internal-transfer ownership and conservation, the reporting-only Class-A boundary, the absence of B2, the historical-uncertainty route and the requirement that this review itself is not admission.

12. **Residual uncertainty explicit: PASS.** Historical revision-53 behaviour is unknown because B2 does not exist. The raw licensed source bytes are not republished in GitHub, so this review independently checks the pre-authoring source-bound audits and hashes rather than claiming a new byte-level source parse. Natural activation is demonstrated for LWKM only; separate organic-P defects remain excluded.

## Expected-difference boundary

Allowed:

- `Bapo(Redi,Ly)` for active TCD-017 redistribution events
- derived organic-P balance fields
- `bapo*.Out` balance/report output

Forbidden:

- any physical state
- any process flux
- ploughing physics
- transport or reaction policy
- numerical policy
- `Bafop`
- TCD-027
- TCD-028
- `AdStdiorpopl`
- `Adhuexpopl`
- any other organic-P correction
- non-whitelisted output

## Residual uncertainty and limits

Historical revision-53 behaviour remains `UNKNOWN` because no qualified B2 behavioural reference exists. Neither the source rebuild, the problematic executable, SYNQ-O002 nor this review is promoted to B2.

The frozen source archive is hash-pinned, but its licensed Fortran bytes are not present in GitHub. This review therefore independently verifies the claim through multiple frozen pre-authoring source audits and source-derived evidence, not through a fresh extraction from the archive.

The natural activation statement is bounded to the supplied LWKM evidence. Inactive cases do not prove broader activation.

TCD-027, TCD-028, `AdStdiorpopl`, `Adhuexpopl`, `Bafop` and all other organic-P changes remain unresolved or separately routed as applicable and are not altered by this result.

## Disposition of this review

`PASS_TCD017_INDEPENDENT_SECOND_LINE_READINESS_REVIEW`

This review closes only the requested independent second-line readiness check. It does not modify production source, does not perform B3 admission and does not authorize B4 or migration. Any B3 admission decision must occur in a separate closeout step under the applicable B3Q01/GOV03 route.
