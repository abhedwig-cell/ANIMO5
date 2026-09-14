# ANIMO-GHG14 — TCD-034 Class-F Readiness Reassessment after GHG09–GHG13

## Scope

GHG14 is a serial scientific-readiness composition workunit. It starts from exact-green `ANIMO-GHG13@a5f3c0ff662017791c6ccf6303b9e98c570d9d42` and reassesses only whether the accumulated TCD-034 model-evolution evidence now satisfies the Class-F requirements defined by `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

No Class-F admission, B3 admission or production migration is performed. Historical revision-53 selector intent is not reopened or rewritten.

## Preserved dual-track disposition

The historical track remains unchanged:

- revision-53 executes the reconstructed `Te(Nuroup+1)` behavior under positive root depth;
- authoritative historical intent for that selector remains unresolved;
- no active historical B2 path validates plant-mediated CH4 behavior;
- therefore historical TCD-034 remains `UNRESOLVED_NOT_ADMITTED`.

The model-evolution track is separately bounded by GHG06A and GHG07 and has gained additional evidence through GHG09–GHG13.

## Evidence accumulated since GHG08

### GHG09 — parameter-transfer implications

GHG09 showed analytically that selector evolution is not safely parameter-neutral. A single global multiplier on `Kpl*FvegCH4` cannot generally preserve the response, changing `Tegr` changes process semantics, and `PvCH4Ox` only redistributes plant transfer rather than compensating total plant removal. The defensible implication is explicit: unchanged parameter transfer is not assumed; recalibration or validation is required.

### GHG10 — material selector difference on a frozen driver case

The ten-year GHGMais environmental-driver replay contains 1604 active-root days. The two selectors differ by a mean absolute 1.158 degC and by as much as 5.385 degC; the `fGrow` regime changes on 231 days, 14.40 percent of active-root days. This proves that the model evolution is not representation-only or numerically negligible on that case. The case has `FvegCH4=0` and lineage limits, so it does not validate methane flux and does not close the application envelope.

### GHG11 — external scientific lineage and validation design

External literature strengthens the scientific T50 and plant-transport lineage and shows that the process family has observational support. It also reinforces the need for process-resolved positive plant-CH4 data and parameter-constraining validation. All external literature remains new model-evolution evidence, never historical ANIMO authority.

### GHG12 — public validation candidate identified

A materially stronger candidate stack has been identified around SPRUCE S1 Bog, including direct plant-mediated methane transport measurements and overlapping environmental, water-table, whole-ecosystem methane and root/vegetation datasets. File-level schema, checksum and observation-level joinability have not yet been qualified. No empirical validation has yet been performed.

### GHG13 — bounded source-ledger conservation compatibility

GHG13 reconstructs that the same phase-adapted `K1plant` coefficient participates in the frozen transport process balance and in reported plant oxidation/emission. The time-integrated plant-transfer identity closes layerwise and over the rooted profile. This qualifies bounded source-ledger compatibility for the evolved selector composition. It is not a whole-model executable methane-balance qualification.

## Class-F gate reassessment

B3Q01 requires Class F to define scientific rationale/theory, relationship to the preserved baseline, calibration and parameter implications, conservation implications, process-appropriate validation evidence, expected changes over the intended application envelope, and independent scientific review.

GHG14 assesses these gates as follows.

1. **Scientific rationale and authoritative theory: PASS_STRENGTHENED.** The fixed-depth T50 concept and plant-mediated transport structure have authoritative external scientific support, while the actual GHG06A interpolation remains explicitly a bounded model-evolution operator.
2. **Relationship to the preserved B3/historical baseline: PASS_BOUNDED_WITH_HISTORICAL_UNCERTAINTY.** Legacy intent remains unresolved; the evolved selector is not relabeled as historical behavior; GHG10 demonstrates material difference on one frozen driver case.
3. **Calibration and parameter implications: PASS_BOUNDED_NONTRANSFERABILITY_DEFINED.** GHG09 and GHG11 define the implication: existing plant-path parameters cannot be assumed transferable unchanged. Empirical estimation remains part of the still-open validation work, not an undefined semantic gap.
4. **Conservation implications: PASS_BOUNDED_SOURCE_LEDGER_COMPATIBILITY.** GHG13 closes the plant-transfer source ledger algebraically. Whole-model executable conservation is intentionally deferred to implementation/production qualification and is not claimed here.
5. **Validation evidence appropriate to the process: FAIL_MATERIAL.** No file-level joined positive plant-mediated CH4 validation package has yet been qualified and no evolved-selector empirical validation has been executed.
6. **Expected changes over intended application envelope: PARTIAL_MATERIAL_GAP.** GHG10 demonstrates materiality on one ten-year environmental driver case, but one case does not define the intended broader wetland/peatland application envelope.
7. **Independent scientific review: FAIL_MATERIAL.** GOV05 same-agent adversarial reviews are process self-review, not genuinely independent scientific review. B3Q01 explicitly requires independent scientific review for Class F.

## Minimum remaining material gates

Three material Class-F readiness gates remain:

- `PROCESS_RESOLVED_EMPIRICAL_VALIDATION_WITH_ANTI_COMPENSATION_DESIGN`;
- `INTENDED_APPLICATION_ENVELOPE_EXPECTED_CHANGE_EVIDENCE`;
- `GENUINELY_INDEPENDENT_CLASS_F_SCIENTIFIC_REVIEW`.

The first gate includes file-level extraction and joining of the SPRUCE candidate stack, reconstruction of both selector inputs on matched observations, and calibration/validation separation sufficient to prevent parameter compensation from hiding selector error.

The second gate cannot be closed by silently narrowing scope after the fact. A bounded single-site scientific admission could only be considered if the intended scope is explicitly defined that narrowly before review; otherwise representative multi-condition or multi-site evidence is required.

## Disposition

`QUALIFIED_TCD034_CLASS_F_READINESS_REASSESSMENT_NOT_READY_THREE_MATERIAL_GATES_REMAIN_V1`

TCD-034 remains not ready for separate Class-F scientific admission. The historical path remains unresolved and not admitted. No production source or central scientific-admission register is changed.
