# ANIMO-B3D11 TCD-040 GOV03 disposition and restore discriminator qualification

Status: `PERSISTED_ROUTE_OPEN_DISCRIMINATOR_QUALIFIED_VALIDATION_PENDING_NO_ADMISSION`

Target: `TCD-040`

Class: `B_LOCAL_RESTORE_INITIALIZATION_IDENTITY`

Central regie authority: `ANIMO-RG05D@f3d6b9780631bd627f8bca0658a8e3878746e666`

Readiness authority: `ANIMO-B3B04@19e38ae0dfc211e88fe782b4b7d6e42b1b7f5865`

This workunit reconciles the TCD-040 readiness evidence with GOV03 and qualifies only the missing restart versus cold-start discriminator contract and the corresponding atomic implementation seam. It does not perform independent second-line review, does not admit TCD-040, and does not produce a production patch.

## Live collision and authority check

Before branch creation, no `ANIMO-B3D11` branch and no later TCD-040 disposition or review branch was found. The only TCD-040 work branch found was `work/animo-b3b04-tcd040-layer0-restart-readiness` at the expected readiness closeout. The current central regie branch was rechecked at the exact RG05D hash above. GOV03 remains `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`.

Relevant current authorities are:

- `ANIMO-STATEQ02@cb7c23524df6560e65a5bdc1ed19e0b6e3bd46c6`;
- `ANIMO-B3I04@400b7cd79f89043e091751707dfa96537587dcf6`;
- `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c`.

## Independent recheck of the atomic mechanism

The frozen B0 archives were re-hashed before this disposition:

- source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

The frozen source was re-inspected rather than treating B3B04 prose as sufficient. `Animo.for:143-169` calls `Inicalc` after input. `Inicalc.for:125-129` unconditionally executes:

```fortran
Conh(0)=0.0
Coni(0)=0.0
Codiorma(0)=0.0
Codiorni(0)=0.0
Codiorpo(0)=0.0
```

No restart selector guards this block. `Init.for:352-364` confirms the ordinary accepted-state ownership relation on later timesteps by copying `Rsconh`, `Rsconi`, `Rscodiorma`, `Rscodiorni` and `Rscodiorpo` back into their current owners for `Ln=0,Nl`. `Init.for:227-245` zeroes result arrays on the first timestep but does not erase the corresponding current-owner values read from initial input. This matters for locating the smallest restore seam.

The frozen GrassPeat testbank input was independently read. Its layer-0 values are nonzero for all five target families: NH4 `6.885736E-03`, NO3 `5.743774E-04`, DOM `9.904185E-02`, DON `5.673512E-03`, and DOP `5.456775E-04`. PO4 is `3.703004E-03` and remains the explicit non-target control coordinate. This confirms natural activation without testcase mutation.

The split-282 values recorded by B3B04 were also checked against their raw little-endian IEEE-754 representations. All five values reproduce the recorded raw hex strings exactly. The evidence arithmetic is internally exact: the first divergent record index is 564, which is the first record after the 564-record accepted prefix; `564 + 1236 = 1800`. The corrected and continuous trajectory hashes are identical, while the defective trajectory hash differs. The split-67 exact-zero negative control retains the same full-trace hash. The B3B04 validation run `34386299961` was rechecked live and concluded `success`.

This B3D11 workunit does not claim to have re-executed the full 1,800-record compiler harness. It rechecks the frozen source and testbank directly, independently checks the raw-value encoding and evidence arithmetic, and rechecks the persisted B3B04 CI result. The executable B3B04 evidence remains the readiness authority.

## What is and is not the restore object

The five TCD-040 coordinates are:

| Species | Current owner | Accepted owner |
| --- | --- | --- |
| NH4 | `Conh(0)` | `Rsconh(0)` |
| NO3 | `Coni(0)` | `Rsconi(0)` |
| labile DOM | `Codiorma(0)` | `Rscodiorma(0)` |
| DON | `Codiorni(0)` | `Rscodiorni(0)` |
| DOP | `Codiorpo(0)` | `Rscodiorpo(0)` |

`Copo(0)` and `Rscopo(0)` are outside TCD-040. TCD-016 remains outside TCD-040 because TCD-016 concerns runtime wet-to-low-storage NH4 continuation science, not startup restoration of an already accepted aqueous coordinate.

The legacy formatted `INITIAL.OUT` surface is restart-style input, but its decimal formatting is not a raw-byte checkpoint contract. Therefore this disposition does not infer bitwise whole-model restart identity from `INITIAL.OUT`. The exact byte identity in the B3B04 split evidence belongs to its bounded atomic checkpoint fixture. TCD-040 only requires that a restore path must not destroy the target values delivered to the restore seam.

## Restore discriminator qualification

No existing legacy state variable, input value, filename, start date, P option, ponding value or other model datum provides a unique cold-start versus restart discriminator at `Inicalc.for:125-129`. In particular, a nonzero layer-0 value cannot serve as a discriminator because such values are legal reader inputs and occur naturally in GrassPeat. Filename or `INITIAL.OUT` provenance cannot serve as a discriminator because the initial-state grammar carries no provenance marker and files may be renamed or supplied directly.

A unique atomic discriminator can nevertheless be specified without changing physical state or redesigning restart architecture. The qualified discriminator is explicit control-plane initialization intent with exactly two semantic values:

`COLD_START`

`RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE`

The selector must come from the invoking driver or restore-capable entrypoint. It must not be inferred from model-state values or file contents. Existing legacy invocation remains `COLD_START` unless and until a separately qualified restore-capable invocation explicitly supplies restore intent. Any restore-capable entrypoint must require an explicit recognized value and fail closed on an invalid or unavailable selector. It must never silently infer or default to restore mode.

This is a control discriminator, not new physical state. It is not serialized into the canonical model state by this workunit and it does not qualify a whole-model checkpoint representation.

## Unique atomic implementation seam

The smallest qualified semantic seam is the existing layer-0 concentration initialization transaction in `Inicalc.for:125-129`, after `Input1` has populated the current owners and before the first post-initialization process execution.

The required behaviour is:

1. Under `COLD_START`, execute the existing five zero assignments exactly as revision 53 does today.
2. Under `RESTORE_ACCEPTED_LAYER0_AQUEOUS_STATE`, do not apply those five destructive zero assignments. Preserve the five current-owner values supplied by the explicit restore operation exactly as presented at the seam.
3. Do not conditionalize or alter the other `Inicalc` initialization work.
4. Do not touch `Copo(0)`, crop state, macropore state, GHG state, numerical policy, hydrology state or any TCD-016 continuation mechanism.
5. Before first post-restore process execution, each of the five current owners must equal the corresponding accepted restore value for this atomic payload. The payload is limited to these five coordinates and is not a claim of checkpoint completeness.

There are two equivalent implementation forms that satisfy the same seam contract: guard the five zero assignments with explicit cold-start intent, or preserve and rebind the same five values around the unconditional block. This workunit does not choose source syntax because no production patch is authorized. The observable contract is unique: cold start retains revision-53 zeroing, explicit restore retains the five supplied accepted values, and all non-target initialization remains unchanged.

Simply deleting `Inicalc.for:125-129` is specifically not qualified because that would also change cold-start behaviour. Inferring restore from nonzero state is also specifically not qualified.

## GOV03 route reconciliation

GOV03 qualifies:

`B2_REFERENCE_UNAVAILABLE_AFTER_REASONABLE_ACQUISITION_EFFORT`

and makes the historical-uncertainty route eligible subject to claim-scoped B3 requirements. Historical revision-53 behaviour for the missing B2 reference remains `UNKNOWN`; no historical-fidelity or prevalence claim is made.

For TCD-040, B3B04 supplies bounded Class-B readiness evidence. B3D11 adds the missing discriminator and implementation-seam contract. The historical-uncertainty route can therefore be opened for independent scientific review, but it cannot be completed here because B3Q01 requires genuine independent second-line review separate from authoring.

## Formal disposition

Canonical disposition remains:

`UNRESOLVED_NOT_ADMITTED`

Workunit decision after successful validation:

`UNRESOLVED_NOT_ADMITTED_INDEPENDENT_SECOND_LINE_PENDING_ROUTE_AND_RESTORE_DISCRIMINATOR_QUALIFIED_BY_GOV03`

The route is open, but TCD-040 is not admitted. Independent review must separately verify source ownership, atomicity, the two-state control discriminator, the seam sufficiency, the non-interference boundary and the distinction from TCD-016.

Hard boundaries remain unchanged: no production patch, no B4, no composition, no canonical STATE admission, no whole-model checkpoint qualification, no historical-fidelity claim and no central regie update.
