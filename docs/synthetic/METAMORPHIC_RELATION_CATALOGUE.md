# ANIMO-SYNQ01 metamorphic relation catalogue

Status: `QUALIFIED_METAMORPHIC_RELATIONS_SCOPED_NON_B2`

Metamorphic tests are used when an absolute field-scale output is either unnecessary or would make the test depend on the implementation under test. The relation itself must be exact or scientifically required within a clearly stated scope.

## MR-01 species permutation for stable-DOM partition

Oracle: `SYNQ-O005`

Transformation:

1. keep the partition coefficient, moisture/rate factors and geometry fixed;
2. permute the C/N/P labels and the matching species concentrations together;
3. rerun the independent species-local partition map.

Required relation:

```text
F(PERMUTE(species_inputs)) = PERMUTE(F(species_inputs)).
```

Why it is useful: an accidental use of an N parent in a P daughter breaks the relation when N and P inputs differ.

What it cannot show: whether any historical field case reached the affected Case(2) route or how large the error was there.

## MR-02 management endpoint transformation

Oracle: `SYNQ-T001`

Candidate contract:

```text
management event belongs to interval iff t0 < E <= t1.
```

Transformations:

- move `E` from an interior point to exactly `t0`: membership changes from true to false;
- move `E` from an interior point to exactly `t1`: membership remains true;
- enlarge `t1` to a later exact event coordinate: the newly covered endpoint event becomes included.

No floating epsilon is allowed. This relation is `STRUCTURALLY_CORRELATED` with the source-reconstructed TIME01 contract and therefore is not an independent historical oracle.

## MR-03 harvest endpoint transformation

Oracle: `SYNQ-T002`

Candidate contract:

```text
harvest event belongs to interval iff t0 <= H < t1.
```

Transformations:

- move `H` to exactly `t0`: membership remains true;
- move `H` to exactly `t1`: membership changes to false.

This intentionally preserves the management/harvest endpoint asymmetry rather than normalizing it away.

## MR-04 accepted-boundary split execution

Oracle: `SYNQ-T003`

For a deterministic fully explicit state transition `G` and a complete side-effect-free serialization operator `S`:

```text
G_n(...G_2(G_1(x)))
=
G_n(...G_k(RESTORE(S(G_{k-1}(...G_1(x)))))).
```

The relation is valid only if the checkpoint contains all state needed for future evolution and is taken at an accepted boundary.

SYNQ01 demonstrates this relation for a deliberately complete scalar state. It refuses to generalize the result to unresolved ANIMO continuation state. TCD-016, GHG hidden state and MP02 macropore solute restart gaps therefore remain outside this relation.

## MR-05 identical-site permutation

Oracle: `SYNQ-L009`

If two sorption sites have identical parameters and identical initial state, permuting their site labels must not change the multiset or ordered equal-valued result.

Use: detects accidental dependence on site position when no physical distinction exists.

Limit: unequal-site behaviour needs the stronger analytical TCD-024 oracle.

## MR-06 identical-layer permutation

Oracle: `SYNQ-L010`

For isolated identical layers with no directional transport or position-dependent forcing, permuting them preserves total conserved storage.

Use: a negative-control relation for future layer ownership and aggregation tests.

Limit: it must not be applied when gravity, boundary conditions, transport direction, rooting or any other layer-position physics makes layers non-equivalent.

## MR-07 equivalent internal-transfer decomposition

Covered by `SYNQ-O002` and `SYNQ-O008`.

An internal transfer can be decomposed into several destinations without changing whole-control-volume mass if the destination gains sum exactly to the source loss. For example:

```text
-x + x = 0
```

and

```text
-x + x1 + x2 = 0, provided x1+x2=x.
```

This relation is useful for MassLedger projection tests because it tests ownership independently of report layout or transfer ordering.

## MR-08 inactive feature negative control

Oracle: `SYNQ-L012`

Activating the test harness while leaving the feature flag/state inactive must produce no feature-specific state or ledger delta.

This is a structural negative control only. It does not prove that the active feature is correct.
