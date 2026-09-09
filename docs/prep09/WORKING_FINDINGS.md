# ANIMO-PREP09 — element-transfer sequencing and slow-sorption tillage audit

Status: `PERSISTED_WORKING_CHECKPOINT_DIAGNOSTIC_NOT_REFERENCE`.

## Frozen provenance

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- reproduced GNU diagnostic executable SHA-256: `0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`
- evidence class for all probes in this workunit: `DIAGNOSTIC_NOT_REFERENCE`

The frozen source and supplied testcase ZIPs are not modified.

## TCD-030 dynamic causal checkpoint

PREP08 established a source-level sequencing gap for exudate-derived humus during ploughing. `Addit.for` subtracts the old `Huex*Nifrhu` and `Huex*Pofrhu` amounts, redistributes `Huex`, adds the new element-specific ledger quantities with the pre-redistribution layer fractions, and only afterwards recomputes `Nifrhu` and `Pofrhu` from redistributed humus.

PREP09 has now activated that difference in the real `Addit` route. A diagnostic first-plough state injection used four non-uniform `Huex`, `Nifrhu` and `Pofrhu` layers and observed both the exact pre/post element stores and the explicit `Adhuexnipl` / `Adhuexpopl` transfer arrays.

At the first plough event (`Tito=2414`, `Pl=4`):

- old exudate-humus N store: `4.0000000000000008e-02 kg m-2 N`;
- post-plough N store: `3.4309421243672103e-02 kg m-2 N`;
- exact physical state change: `-5.6905787563279048e-03 kg m-2 N`;
- explicit legacy N transfer ledger: `-5.0000000000000053e-03 kg m-2 N`;
- mismatch: `+6.9057875632789947e-04 kg m-2 N`, or about `+6.9057875633 kg ha-1 N`.

For P at the same event:

- old store: `4.0000000000000001e-03 kg m-2 P`;
- post-plough store: `3.4309421243672112e-03 kg m-2 P`;
- explicit-transfer mismatch relative to exact state change: `+6.9057875632788797e-05 kg m-2 P`, or about `+0.6905787563 kg ha-1 P`.

Later plough events in this diagnostic activation are effectively zero-mismatch because the first redistribution makes the relevant humus fractions uniform over the ploughed zone. This strengthens the causal interpretation: the defect is specifically the temporal-side mismatch between pre-redistribution and post-redistribution element fractions, not a generic drift term.

These synthetic magnitudes are not qualification tolerances and are not a natural-case error estimate.

## Slow non-equilibrium P sorption tillage checkpoint

The supplied ANIMO 4.0 User's Guide defines `PL` as the number of model compartments to be ploughed / redistributed and defines `AMCXSL` as the adsorbed non-equilibrium phosphorus mass concentration per site and compartment.

Revision-53 `Addit.for` contains explicit slow-sorption tillage code, but all four parts are commented with `!-19-10-2010`:

- accumulation of `Amcxsl(J,Ln)*He(Ln)` into `Supocxsl(J)`;
- subtraction into `Adpocxslpl`;
- redistribution back into `Amcxsl`;
- addition into `Adpocxslpl`.

`Outbal_calc.for` still actively consumes `Adpocxslpl` in the inorganic-P redistribution ledger, while `Init.for` resets it each step. Therefore the ledger interface still contains an intended slow-sorption redistribution edge although the producer path is disabled.

Natural LWKM coverage is present: `OPTCXSL=3`, `NCXSL=3`, four plough events, and all three slow-sorption sites contain non-zero and spatially heterogeneous `Amcxsl` values at each observed plough event. For the first event the areic slow-sorption totals over the four ploughed layers are approximately `0.00528265`, `0.0356732` and `0.0477165 kg m-2 P` for sites 1–3 respectively.

No defect classification is yet promoted solely from the disabled code. The next causal step is to compare the frozen behaviour with a diagnostic conservative site-preserving redistribution variant and separate documented tillage semantics from any intentionally retained immobile-sorption policy.
