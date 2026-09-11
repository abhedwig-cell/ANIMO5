# ANIMO-B3D40 — TCD-033 atomic B3 admission decision

This workunit decides only whether the exact-final `ANIMO-GHG02` scientific identity for canonical `TCD-033` is admissible into B3 under GOV05 Tier-C review.

The candidate identity is local to `CH4produc`: with `A=1-Rdfaox`, the existing `A<1.0e-8` early return remains unchanged; for `S=0`, total and component production are zero; otherwise the source-family daughter components are `Q_i=Q*S_i/S`, equivalently `E*A*S_i`, so `sum_i(Q_i)=Q` and proportional source shares are retained. Parent and daughters all have units `kg C m-2 d-1`.

The historical revision-53 implementation is not used as a fidelity target where it contradicts the qualified component identity. Historical behavior remains `UNKNOWN_WITHOUT_B2`. The GHG02 64-ulp bound is an equation-oracle verification bound only and is not a model tolerance.

B3D40 does not modify or admit TCD-032 or TCD-034, does not reopen the total CH4 production law, does not change `Rdfaox`, transport or other GHG physics, does not patch production source, does not create a whole-model golden baseline, and does not open B4 or production.

A successful exact-final B3D40 is the first scientific admission after RG05N. Normal aggregate cadence is therefore not reached; RG05O is not opened by this workunit.
