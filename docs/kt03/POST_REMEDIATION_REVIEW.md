# ANIMO-KT03 Post-Remediation Adversarial Review

Review mode: `same-agent / not genuinely independent`.

Assurance label: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

Frozen remediation target: `e844c7658a95819fc0463c55737f9bd41b29a6da`.

Exact-head GitHub Actions run: `35282453399`, conclusion `SUCCESS`.

This review rechecks only the findings from `ADVERSARIAL_REVIEW.md` and the relevant delta after the reviewed pre-remediation head. It does not reopen unrelated ANIMO5 science or governance.

## Finding disposition

### KT03-R1, legacy file identity in normalized payload

**RESOLVED.**

`HydrologyStep` no longer requires `Hlpimp` or a file-record SHA. Legacy-specific identity is isolated in `LegacyStepProvenance`, with `ANIMO41_SWAP3_RECORD_LAYOUT_V1` and a source-record digest generated from the legacy record group. A future in-memory producer can therefore construct the normalized payload without pretending to be a legacy file.

### KT03-R2, producer time versus runtime time authority

**RESOLVED.**

The normalized fields are now explicitly named `producer_endpoint_day` and `producer_step_days`. The contract states that these are producer-coordinate metadata and scientific input, not KT02 runtime authority. A future runtime adapter must validate the producer interval against the authoritative runtime interval before execution. The payload cannot select, advance, subdivide or retry runtime time.

### KT03-R3, implicit cross-model units

**RESOLVED.**

The payload now carries `ANIMO_HYDROLOGY_UNITS_V1`, with an explicit field-unit map. No silent numerical conversion was introduced. A future producer must convert to the declared contract before constructing the payload.

### KT03-R4, weak digest validation

**RESOLVED.**

The digest moved out of the physical payload into legacy provenance and is validated as a 64-character hexadecimal SHA-256 value.

### KT03-R5, Dble_trunc historical authority

**BOUNDARY RETAINED.**

The Python normalization remains diagnostic only. Evidence class remains `B1_DIAGNOSTIC_ADAPTER_PROBE_NOT_B2`. No historical Intel/compiler equivalence is claimed.

### KT03-R6, Hlpimp=1 missing interception-storage endpoint

**BOUNDARY RETAINED.**

The Hlpimp=1 CranMais payload still does not provide `Sict`; the adapter represents that absence explicitly and refuses a complete `Hydro_detailed` projection. The Hlpimp=11 LWKM file supplies `sSict` explicitly and demonstrates the complete file-derived projection within that bounded envelope. `KT03-F01` remains a separate scientific/source disposition surface.

## Additional bounded observation

`Wabaer` is a formal output of revision-53 `Input_hydro` and is present in the legacy SWATRE record, but source-wide inspection did not identify a downstream revision-53 consumer after the call. In the current nonproduction V1 prototype it remains a normalized producer diagnostic field and is not part of `hydro_detailed_boundary()`. This is not used to establish any scientific claim. Before a production coupling schema is frozen, contract minimization should either remove it or document an explicit consumer.

This observation does not reopen KT03 because the V1 result is nonproduction and the field does not create file-format or model-state coupling. It is recorded so a later production schema does not acquire an unnecessary obligation by inertia.

## Post-remediation verdict

`SELF_REVIEW_PASS_NONPRODUCTION_FILE_INDEPENDENT_TYPED_HYDROLOGY_CONTRACT_WITH_EXPLICIT_HLPIMP1_SICT_BOUNDARY`

The mandatory pre-close findings R1-R4 are resolved at the frozen remediation target. R5 and R6 remain explicit qualification boundaries rather than hidden compatibility assumptions. No production, B3, B4, Status-A or historical-equivalence claim follows from this review.
