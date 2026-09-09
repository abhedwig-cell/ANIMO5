# ANIMO-B3B04 TCD-040 nonzero layer-0 aqueous restart identity qualification

Status: `QUALIFIED_ATOMIC_CLASS_B_RESTART_IDENTITY_READINESS_ONLY`

Target: `TCD-040`

Class: `B_LOCAL_RESTORE_INITIALIZATION_IDENTITY`

Base: `ANIMO-B3I04@400b7cd79f89043e091751707dfa96537587dcf6`

This workunit qualifies only the atomic readiness claim that existing nonzero layer-0 aqueous state must retain its accepted owner identity across an explicitly identified restart/restore seam. It does not admit canonical STATE, does not admit TCD-040 into B3, does not modify production source, and does not compose TCD-016 or internal-crop state.

## Frozen evidence identity

Every executable probe is pinned to:

- source archive SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank archive SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

STATEQ02 is used only for the already qualified accepted-boundary and restricted-core semantics. Its natural split-282 rejection sentinel is activation evidence, not TCD-040 qualification: STATEQ02 rejected the case before checkpoint creation.

## Exact legacy source path

The frozen source reads layer-0 values from the initial-state input. Relevant source anchors include:

- `input1.for:3201`: `Conh(0:Nl)`;
- `input1.for:3213`: `Coni(0:Nl)`;
- `input1.for:3267`: `Codiorma(0:Nl)`;
- `input1.for:3277`: `Codiorni(0:Nl)`;
- `input1.for:3390`: `Codiorpo(0:Nl)`.

`Animo.for:143-169` then calls `Inicalc` after input. In the same frozen source, `Inicalc.for:125-129` unconditionally executes:

```fortran
Conh(0)=0.0
Coni(0)=0.0
Codiorma(0)=0.0
Codiorni(0)=0.0
Codiorpo(0)=0.0
```

Ordinary accepted-state continuation uses the opposite identity relation. `Init.for:352-364`, in loops over `Ln=0,Nl`, copies:

```text
Rsconh -> Conh
Rsconi -> Coni
Rscodiorma -> Codiorma
Rscodiorni -> Codiorni
Rscodiorpo -> Codiorpo
```

The physical owner pairs are therefore unambiguous for this narrow claim:

| Species/state | current owner | accepted owner |
|---|---|---|
| NH4 | `Conh(0)` | `Rsconh(0)` |
| NO3 | `Coni(0)` | `Rsconi(0)` |
| labile DOM | `Codiorma(0)` | `Rscodiorma(0)` |
| DON | `Codiorni(0)` | `Rscodiorni(0)` |
| DOP | `Codiorpo(0)` | `Rscodiorpo(0)` |

`Copo(0)` / `Rscopo(0)` is a physical layer-0 aqueous control coordinate but is not zeroed by this `Inicalc` block.

The user guide independently states that `INITIAL.OUT` contains profile state variables in the same sequence as `INITIAL.INP` and can initialize another simulation run. The frozen source has no explicit cold-start/restart discriminator around the five zero assignments. Therefore an unconditional deletion of those assignments is not qualified: it would silently change cold-start semantics as well.

## Natural nonzero startup witness

Frozen testbank case `GrassPeat` supplies a natural nonzero layer-0 witness. Immediately before `Inicalc`:

- `Pn = 0`;
- `Snla = 0.0034548`;
- `NH4(0) = 0.006885736`;
- `NO3(0) = 0.0005743774`;
- `DOM(0) = 0.09904185`;
- `DON(0) = 0.005673512`;
- `DOP(0) = 0.0005456775`;
- `PO4(0) = 0.003703004`.

Immediately after `Inicalc`, all five target values are raw IEEE-754 positive zero. `PO4(0)` remains byte-identical. This directly activates the source mechanism without relying on a synthetic nonzero value.

## Separate-process atomic split qualification

The executable witness is frozen testbank case `LWKM_gras_1040.2021.2045`. The harness is qualification-only and deliberately narrower than STATEQ02: Stage A and an independent Stage B process each replay the immutable deterministic inputs to the accepted split boundary. Only the five target accepted owners cross the atomic checkpoint seam. This is not a whole-model checkpoint implementation or canonical STATE claim.

GNU Fortran 14.2 was used with the existing diagnostic compatibility contract, including eight-byte default REAL/DOUBLE and `-fno-automatic`. The source archive hash is asserted before build.

### Nonzero split 282

At accepted boundary 282, the five checkpoint owners are:

| owner | exact value |
|---|---:|
| `Rsconh(0)` | `8.977310061221382e-4` |
| `Rsconi(0)` | `8.767359689234193e-6` |
| `Rscodiorma(0)` | `4.381575788713558e-3` |
| `Rscodiorni(0)` | `1.2267733059957502e-4` |
| `Rscodiorpo(0)` | `1.2267733059957505e-5` |

The checkpoint file SHA-256 is `833363cc2f8457a617b450bfa283842532efcb8d321a57eca5e05584b0224b2e`. Its payload exactly matches the five Stage-A pre-checkpoint owner bytes. Writing the checkpoint does not change them.

For the corrected restore-identity branch, independent Stage B reads the checkpoint and leaves the five target owner bytes exactly unchanged. The complete 1,800-record instrumented aqueous/hydrology trajectory has SHA-256:

`29055b1be962d9550781b87f56ab34cd44630965439e21b6e5375954a6144a48`

That is byte-for-byte identical to the uninterrupted continuous trajectory over all 1,800 records. Maximum observed difference is exactly zero. No tolerance is used.

For the defective legacy-erasure branch, Stage B first reaches the same accepted boundary and verifies the same checkpoint bytes. It then applies exact positive zero to only the five target owners. `PO4(0)` remains unchanged at the boundary. The resulting trace SHA-256 is:

`920cc04388d812e5668edab3e654b7e006926522bbe61923b1a202b346cf4e38`

The first divergence from continuous execution is exactly the first post-restore record, step 283, phase 0, layer 0, and occurs simultaneously on the five target coordinates. There is no earlier divergence.

The observed downstream aqueous consequence envelope continues through the horizon. NH4, NO3, DOM, DON and DOP eventually differ in layers 0 through 30. PO4, although not erased, becomes downstream-sensitive in layers 1 through 29. The maximum observed absolute differences are:

| field | maximum absolute difference |
|---|---:|
| NH4 | `8.977310061221382e-4` |
| NO3 | `8.767359689234193e-6` |
| DOM | `4.381575788713558e-3` |
| DON | `1.2267733059957502e-4` |
| DOP | `1.2267733059957505e-5` |
| PO4 | `1.4751153212333792e-10` |

This is an observed consequence envelope on the instrumented aqueous surface, not a claim that no other derived/report quantity can differ. In the same B282 restore-versus-erasure harness family, water-balance outputs remain identical while multiple C/N/P, organic-matter, transport and final-state outputs differ, as expected from the changed aqueous trajectory.

### Exact zero-state negative control at split 67

At accepted boundary 67 all five target checkpoint coordinates are exact positive zero. Applying the same legacy zero operation is therefore an identity operation. Independent Stage B produces a full 1,800-record trace with the same SHA-256 as uninterrupted execution:

`29055b1be962d9550781b87f56ab34cd44630965439e21b6e5375954a6144a48`

The full trajectory is byte-identical. This rejects the weaker explanation that the split harness itself causes the divergence.

## Atomic correction contract

The readiness-qualified correction is deliberately narrow:

> On an explicitly identified restart/restore path, preserve or restore exactly `Rsconh(0)`, `Rsconi(0)`, `Rscodiorma(0)`, `Rscodiorni(0)` and `Rscodiorpo(0)` into their current owners before first post-restore process execution. Do not apply the cold-start layer-0 zero initialization to those restart-owned coordinates.

Additional constraints:

- retain existing cold-start semantics unless separately qualified;
- do not modify `Copo(0)` / `Rscopo(0)` as part of TCD-040;
- no tolerance, clipping or normalization;
- no new physical state;
- no TCD-016 composition;
- no internal-crop composition;
- no broad restart redesign.

Because the frozen source has no explicit restart discriminator at the destructive initialization site, this workunit does not qualify a concrete production edit. A future implementation must introduce or consume an already qualified restart-mode distinction at the initialization seam. Simply deleting `Inicalc.for:125-129` is not the admitted correction.

## Readiness disposition

The atomic TCD-040 mechanism satisfies the requested Class-B readiness evidence:

- exact causal source path and trigger are identified;
- physical owner identity is unambiguous;
- natural nonzero activation exists;
- exact corrected and defective branches are both exercised;
- checkpoint-before/after identity is demonstrated;
- continuous versus independent-process split comparison is exact;
- first post-restore divergence is localized;
- a downstream consequence envelope is measured;
- the exact zero-state negative control passes;
- no numerical tolerance is introduced.

Disposition:

`QUALIFIED_ATOMIC_CLASS_B_RESTART_IDENTITY_READINESS_ONLY`

Explicit non-admissions:

`canonical STATE admission = false`

`production patch = none`

`TCD-040 B3 admission = false`

`historical fidelity/prevalence claim = false`

The current GOV02 historical-uncertainty route remains inactive while B2 acquisition is still active. This readiness result does not bypass that governance gate.
