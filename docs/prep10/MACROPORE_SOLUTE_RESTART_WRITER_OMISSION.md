# ANIMO-PREP10 — Macropore solute restart-writer omission

Status: `SOURCE_CONFIRMED_PERSISTENT_STATE_WRITER_OMISSION_TESTBANK_UNEXERCISED`.

The frozen revision-53 source and supplied testbank remain unchanged.

## 1. Scope

This finding concerns restart continuity only. It is distinct from TCD-025, which concerns missing macropore storage/direct-drainage terms in the public/main mass-balance ledger.

## 2. Active restart reader

When macropores are active, `mapoinput.for` with `Nupa=4` reads persistent macropore solute state from `INITIAL.INP`.

`>MPnitr:` reads:

```text
CoMpNh(1:2)
CoMpNi(1:2)
```

`>MPorgs:` reads:

```text
CoMpDiorMa(1:2)
CoMpDiorNi(1:2)
```

and, when phosphorus is active, `>MPphos:` reads:

```text
CoMpPo(1:2)
CoMpDiorPo(1:2)
```

These are therefore not merely dead declarations or reporting fields.

## 3. Persistent accepted/result state

`Init.for` explicitly carries the result concentrations from the previous accepted step back to the next-step accepted state:

```fortran
CoMpDiorMa(Dn) = RsCoMpDiorMa(Dn)
CoMpDiorNi(Dn) = RsCoMpDiorNi(Dn)
CoMpNh(Dn)     = RsCoMpNh(Dn)
CoMpNi(Dn)     = RsCoMpNi(Dn)
CoMpDiorPo(Dn) = RsCoMpDiorPo(Dn)
CoMpPo(Dn)     = RsCoMpPo(Dn)
```

Thus the six concentration families participate in the time-step state lifecycle.

## 4. Restart writer omission

`Output_Init.for` contains the expected `>mpnitr:`, `>mporgs:` and `>mpphos:` writer block, but the entire block is commented out, including its `If (Ioptmp.Eq.1)` guard and all state writes.

The active standard `INITIAL.OUT` writer therefore emits no macropore solute concentrations even when the model state contains them.

The lifecycle is consequently asymmetric:

```text
INITIAL.INP read        = present
accepted/result state   = present
accepted-step carry     = present
INITIAL.OUT write       = absent
subsequent restart read = expects the missing fields
```

## 5. Testbank coverage

All supplied `MacroPoreOption` values are zero. PREP10 therefore does not claim a measured supplied-case split-run error magnitude.

That absence of behavioural coverage does not erase the source-level restart contract failure: for any admitted active-macropore state with nonzero solute concentrations, the standard writer has no representation for the state the reader expects.

## 6. Classification

`SOURCE_CONFIRMED_PERSISTENT_MACROPORE_SOLUTE_RESTART_WRITER_OMISSION_TESTBANK_UNEXERCISED`

This is a restart/state-contract defect, not a physics correction.

```text
physics_changed = false
state_owner_missing = false
restart_reader_present = true
restart_writer_present = false
behavioural_magnitude_measured = false
reference_qualification_required = true
production_migration_admitted = false
```

## 7. Related but separate validation candidate

In the same `>MPnitr:` reader, checks labelled `CoMpNi(1)` and `CoMpNi(2)` pass `CoMpNh(1)` and `CoMpNh(2)` to `Checkrea`. Nitrate is therefore read but ammonium is validated twice. PREP10 keeps this as a separate parser-validation candidate and does not fold it into TCD-032.

## 8. ANIMO5 requirement

Every persistent state family admitted to a restartable kernel must have one explicit state owner and a versioned, round-trip restart representation. A reader without a matching writer is a failed restart contract, even if a supplied testbank happens to disable the feature.

A later behavioural qualification must use a dedicated active-macropore case, preserve nonzero C/N/P macropore solute states across a split run, and compare the continuation against an uninterrupted qualified reference trajectory.

Production migration remains `NOT_ADMITTED`.
