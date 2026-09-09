# ANIMO-PREP07 — Transfer-edge and species-identity audit

Status: `QUALIFIED_SOURCE_BOUND_TRANSFER_EDGE_AUDIT_REFERENCE_ADMISSION_BLOCKED`.

## Purpose

PREP06 established that the legacy balance arrays are observers rather than canonical physical state. PREP07 follows the physical transfer edges through the transformation, management and balance routes and asks a stricter question:

> for every internal transfer, does the producer, state update and ledger consumer preserve the same store, chemical element, constitutive site and amount exactly once?

The audit is deliberately source-bound. It does not change the frozen ANIMO source, does not change physics or numerical policy and does not admit production migration.

## Frozen identity

Source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Testbank SHA-256:

`44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`

The deterministic audit is implemented in `tools/audit_transfer_edges.py`. It verifies both archive hashes before reading source or testcase content.

The persisted run passes `25/25` static checks.

## 1. Existing species-identity guard

The audit first keeps TCD-023 visible as a regression guard. In `resp_miner.for`, stable-DOM Case(2) still contains:

```fortran
Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)
Transfop(20,Ln) = AsfaSDO       * Transfon(17,Ln)
```

although the P-specific source amount is `Transfop(17,Ln)`. PREP04 already established the causal P consequence. PREP07 does not reopen or renumber that defect.

## 2. TCD-028 — exudate-humus ploughing ledger double count

### Physical state and expected transfer identity

The supplied ANIMO 4.0 User's Guide defines `HUEX` as the areic mass of humus originating from exudates. `HUEX` and `HUOS` together form humus. This makes `Huex(Ln)` a physical organic-matter state, not merely a reporting variable.

For an internal ploughing redistribution, the ledger contribution of that state must be:

```text
net redistribution = new redistributed state - old state
```

Each physical amount must enter the transfer ledger once.

### Source sequence in `Addit.for`

The old layer state is first removed from the redistribution accumulator:

```fortran
Adhuexpl(I,Ln) = Adhuexpl(I,Ln) - Huex(Ln)
```

After redistribution, the new `Huex(Ln)` is added:

```fortran
Adhuexpl(I,Ln) = Adhuexpl(I,Ln) + Huex(Ln)
```

Later in the same ploughing path, the same new C/OM amount is added a second time:

```fortran
Adhuexpl(I,Ln)   = Adhuexpl(I,Ln) + huex(Ln)
```

The element-specific N and P arrays at this latter location are added once:

```fortran
Adhuexnipl(I,Ln) = Adhuexnipl(I,Ln) + huex(Ln)*Nifrhu(Ln)
Adhuexpopl(I,Ln) = Adhuexpopl(I,Ln) + huex(Ln)*Pofrhu(Ln)
```

The carbon/organic-matter accumulator therefore represents:

```text
legacy = -old + new + new
correct internal-transfer identity = -old + new
legacy excess = +new
```

The PREP07 audit includes an exact algebraic control proving that the excess equals the redistributed new state.

### Consumer-side species reconstruction

`Outbal_calc.for` consumes `Adhuexpl` directly for the humus/organic-matter redistribution ledger.

For organic N and P, however, the explicit element-specific arrays are not consumed. Instead the code reconstructs element mass from the generic `Adhuexpl` amount and post-event fractions:

```fortran
Dum = Adhuexpl(I,Ln) * Nifrhu(Ln) * Z
Dum = Adhuexpl(I,Ln) * Pofrhu(Ln) * Z
```

The source therefore couples two problems:

1. the generic exudate-humus redistribution amount is double-counted;
2. N and P are reconstructed from that corrupted generic amount instead of consuming the explicit element-valued transfer arrays already created by `Addit.for`.

### Existing causal P evidence

This source finding connects directly to the earlier controlled TCD-017 activation probe. When non-zero exudate-derived humus was activated, the legacy `Adhuexpl * Pofrhu` reconstruction produced maximum absolute period organic-P residuals of approximately:

```text
RP: 45.2 kg/ha P
GP: 90.3 kg/ha P
TP: 90.3 kg/ha P
```

Replacing the reconstruction by explicit `Adhuexpopl` reduced those residuals to approximately:

```text
RP: 2.34e-10 kg/ha P
GP: 4.06e-8  kg/ha P
TP: 6.54e-7  kg/ha P
```

That earlier diagnostic evidence establishes the P-ledger consequence of using the generic reconstructed path. PREP07 adds the independent source proof that `Adhuexpl` itself contains a duplicate new-state contribution.

PREP07 does **not** claim that the duplicate alone explains every previously measured P residual. The source defects must remain independently attributable during corrected-reference qualification.

### Classification

`SOURCE_CONFIRMED_EXUDATE_HUMUS_PLOUGHING_LEDGER_DOUBLE_COUNT_AND_SPECIES_RECONSTRUCTION_GAP`

The duplicate `Adhuexpl` update is a ledger/accounting defect. A corrected-legacy candidate is expected to be Class A only if state/output trajectory equivalence is independently demonstrated. The N/P reconstruction issue overlaps the already established TCD-017 ledger family and must be composed carefully rather than silently folded into it.

## 3. TCD-029 — multi-site fast-sorption management integration gap

### Documented and source-visible contract

The supplied ANIMO 4.0 User's Guide documents that ANIMO 4.0 allowed only one equilibrium sorption site, `NCXFA=1`, although the input table already presents the general site-indexed parameter structure.

Revision 53 expands the parser contract:

```fortran
Call Checkint(Uoer,Error,Label,'Ncxfa',Ncxfa,1,3)
```

and `Transorp.for` treats `NCXFA` as the number of instantaneous-sorption fractions and loops over all admitted sites.

Thus the supplied revision-53 source advertises and numerically uses a later multi-site fast-sorption capability beyond the documented 4.0 restriction.

### Single-site compatibility helpers

`Inicalc.for` initializes the legacy helper variables only under the explicit single-site condition:

```fortran
If (Optcxfa.Eq.2 .And. Ncxfa.Eq.1) Then
   Socfpo(Ln) = Pacxfaln(3,1,Ln)
   Ampoma(Ln) = Pacxfaln(2,1,Ln)
End If
```

The source-wide PREP07 scan found no alternative initialization of these helpers for `Ncxfa>1`.

### Management/addition path remains site-1 coupled

`Addit.for` still uses `Ampoma(Ln)` and `Socfpo(Ln)` repeatedly and writes `Amcxfa(1,Ln)` rather than a site-indexed fast-sorption collection. It does not receive `Parcxfa`, so it cannot apply the site-specific constitutive parameters used by `Transorp`.

During ploughing the routine can sum fast-sorption amounts over `J=1,Ncxfa`, but the reconstruction/update route remains bound to site 1. In the observed source this creates an incomplete contract:

```text
parser:          NCXFA = 1..3 admitted
transport:       site-indexed NCXFA loop
initial helpers: populated only for NCXFA=1
management:      legacy helper parameters + Amcxfa(1) path
```

For `NCXFA>1`, the management route therefore cannot be assumed to preserve site identities, constitutive parameters or conserved sorbed mass.

### Supplied-testbank coverage

The audit found seven explicit `NCXFA` records in the supplied testbank. All seven have:

```text
NCXFA = 1
```

No supplied testcase exercises the discrepant multi-site management route. PREP07 therefore does not assign a behavioural magnitude and does not invent a correction.

### Classification

`SOURCE_CONFIRMED_MULTISITE_FAST_SORPTION_MANAGEMENT_INTEGRATION_GAP_TESTBANK_UNEXERCISED`

This is not a Class-A reporting issue. A correction can change sorbed P state and later transport. Before `NCXFA>1` can be admitted, qualification requires a dedicated two/three-site case with unequal site parameters and at least one management redistribution/addition event.

## 4. Negative findings deliberately not promoted to defects

The transfer-edge scan also examined balance terms that are accumulated but not directly referenced by a `Ddev` equation. PREP07 does not classify the following as new defects from source structure alone:

- `N2Od` and `PDen` in the nitrate/denitrification reporting family;
- `CH4f`, `CO2f` and `Dssi` decomposition-detail terms in organic-matter reporting.

These can be subordinate decompositions of already-accounted total process terms. Revision-specific GHG theory is incomplete, so absence from the top-level residual equation is insufficient evidence of omission.

The existing macropore `Dra4` finding remains TCD-025 because PREP06 separately established that the specialized macropore control volume contains storage/direct-drainage terms the main ledger interface cannot represent.

## 5. Architectural constraints for ANIMO5

PREP07 adds the following constraints to the eventual migration design:

1. an internal transfer should have an explicit source store, destination store, conserved species/element, amount, unit and control-volume scope;
2. the same physical amount must not be independently reconstructed at the ledger boundary when an element-specific transfer quantity already exists;
3. C, N and P transfer identities must be type- or structure-separated enough that a C/N/P array substitution is not syntactically trivial;
4. constitutive site identity must remain explicit through management events, not only inside the transport solver;
5. solver iteration indices, sorption-site indices and species indices require separate typed roles;
6. balance arrays remain observers and must not become the owner of physical state;
7. every admitted option combination requires path coverage, including management events that cross process-module boundaries.

## 6. Qualification requirements

### TCD-028

Before corrected-legacy admission:

- reproduce frozen ploughing behaviour under a qualified historical/reference environment;
- independently remove the duplicate `Adhuexpl` contribution and capture unrounded C/OM ledger effects;
- independently bind N and P ledgers to their explicit transfer arrays;
- demonstrate ordinary state/process trajectory invariance for any claimed Class-A correction;
- then compose with the existing TCD-017 organic-P ledger corrections.

### TCD-029

Before any multi-site fast-sorption production support:

- construct a controlled `NCXFA=2` and preferably `NCXFA=3` qualification case;
- use unequal site capacities/affinities so site collapse is observable;
- include fertilizer/addition and ploughing redistribution events;
- capture unrounded `Amcxfa(site,layer)` before and after management;
- prove total P conservation and site-specific constitutive consistency;
- qualify against a trusted reference or authoritative 4.1.x formulation before migration.

## Gate

`QUALIFIED_SOURCE_BOUND_TRANSFER_EDGE_AUDIT_TWO_NEW_GAPS_REFERENCE_ADMISSION_BLOCKED`

Production correction and ANIMO5 process migration remain `NOT_ADMITTED`.
