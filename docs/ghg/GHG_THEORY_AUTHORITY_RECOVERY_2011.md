# ANIMO-GHG01 — 2011 ANIMO-specific N2O theory-authority recovery

Status: `ANIMO_SPECIFIC_N2O_EQUATION_AUTHORITY_RECOVERED_WITH_TWO_DOCUMENT_SOURCE_CONFLICTS`

This post-closeout evidence note strengthens the independent scientific authority for the revision-53 N2O subsystem without changing the ANIMO-GHG01 closeout, admitting B3, or asserting historical revision-53 behaviour.

Frozen revision-53 source archive SHA-256:

`183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`

Locally rechecked source-file identities:

- `ghg_n2o.for`: `493bf88d4b321df64817a7c0eaa2725ad614a45df0a0f16cefa96ac348254175`;
- `ghgtransport.for`: `d86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6`;
- `Aeration_original.for`: `cc02a097df98cfe36abd64403522fc6cf2b14addcc36cee2d4749916a21bd169`.

## 1. Recovered independent ANIMO-specific authority

Two 2011 peer-reviewed publications materially strengthen the authority chain for the N2O formulation.

1. Stolk et al. (2011), *Simulation of Daily Nitrous Oxide Emissions from Managed Peat Soils*, Vadose Zone Journal 10(1), 156-168, DOI `10.2136/vzj2010.0029`. The paper states that ANIMO had been extended for N2O production, consumption and transport and provides the main equations in its appendix.
2. Stolk, Hendriks, Jacobs, Moors & Kabat (2011), *Modelling the effect of aggregates on N2O emission from denitrification in an agricultural peat soil*, Biogeosciences 8, 2649-2663, DOI `10.5194/bg-8-2649-2011`. Section 2.1.2 explicitly labels the pre-mobile/immobile implementation as the `Original concept for N2O`, and Appendix A gives governing ANIMO equations for aeration, denitrification, nitrification and gas transport.

The Biogeosciences paper is especially useful because its original concept assumes instantaneous equilibrium between air-phase and water-phase N2O. That is the same state concept reconstructed from frozen revision 53. The paper then introduces a separate mobile-immobile extension for its experiment. The mobile-immobile extension must not be projected onto revision 53 unless source evidence independently shows it.

These publications cite a more detailed work by Hendriks, Groenendijk, Stolk, van den Akker & Renaud, *Modelling of greenhouse gas emissions with ANIMO 4.0*, Alterra, Wageningen, 2011. A separate October 2011 Alterra report cites that work as `in voorbereiding` and associates it with Alterra report 2054. Therefore report 2054 is retained only as:

`PUBLICATION_EXISTENCE_AND_REPORT_NUMBER_LEAD_NOT_FROZEN`

No claim is made that a final public Report 2054 has been recovered or that its final bytes/specification are known.

## 2. Version boundary

The independent 2011 equations are ANIMO-specific and temporally close to the GHG source lineage, but they are not a proven revision-53 release specification.

Frozen `ghg_n2o.for` identifies SVN revision 11 dated 2013-02-28 and a `tags/animo4.1.4` HeadURL. The archive-level package identifies ANIMO 4.1.5 revision 53. Thus equation matching can establish independent scientific authority for particular relations, but it cannot by itself establish that every coefficient and algebraic detail in revision 53 is the exact equation set intended by the 2011 publications.

For the required GHG01 provenance vocabulary, exact or substantive matches below are classified `INDEPENDENT_THEORY` with an explicit version-near boundary. Conflicting relations are `UNRESOLVED`. Source elaborations not fixed by the publications remain `SOURCE_ONLY`.

## 3. Equation-by-equation reconciliation

| Relation | 2011 independent ANIMO authority | Frozen revision-53 source | Result | Provenance |
| --- | --- | --- | --- | --- |
| Total N2O system concentration | Original-concept Eq. 2: total concentration is dissolved N2O times water content plus gas N2O times air content under Bunsen equilibrium | `ghgtransport.for:190-196` reconstructs `AvCs`, `Cs`, `RsCs` from dissolved concentration, reciprocal Bunsen partitioning, water content and air content | `EXACT_CONCEPTUAL_MATCH` | `INDEPENDENT_THEORY` |
| N2O CT equation | Original-concept Eq. 1 contains simultaneous diffusion, air advection, water advection, drainage, nitrification production, denitrification production and N2O reduction | `GHGtransport` plus `GHG_NitrousOxide` implements the same source/sink and transport classes | `STRUCTURAL_MATCH` | `INDEPENDENT_THEORY` |
| Effective gas/water diffusion | Original-concept Eq. 3 and Appendix A19 use reciprocal Bunsen coefficient, gas-filled porosity diffusion term plus aqueous tortuosity term | `ghgtransport.for:372-393` uses `Fair*ReBuAv*Da0 + Tort*Mofr*Dw0`, with `Tort=0.66`, temperature-dependent free diffusion and a source-side cap on `Fair` | `MATCH_WITH_SOURCE_ELABORATION` | `INDEPENDENT_THEORY` for governing relation; cap and temperature functions `SOURCE_ONLY` unless separately qualified |
| Nitrification N2O production | Appendix A15: N2O-N production is fraction `Fnit` times NH4 oxidation | `ghg_n2o.for:88-95` uses `-FrNitrN2O*Rekinh*Avconh*Mofr*He`; `Rekinh` is negative reduction-rate convention | `STRUCTURAL_AND_SIGN_CONVENTION_MATCH` | `INDEPENDENT_THEORY` |
| WFPS dependence of nitrification fraction | Appendix A16/A18: minimum-to-maximum fraction controlled by thresholded normalized WFPS raised to an exponent | `FracN2Onitr`, `ghg_n2o.for:703-715`, implements the same threshold/min/max/exponent structure | `ALGEBRAIC_MATCH` | `INDEPENDENT_THEORY` |
| Nitrification temperature dependence | Appendix A17 text extraction gives a Q10-ratio factor with positive `(T-Tref)/10`; Table A1 gives ratio 2 | `ghg_n2o.for:717-720` uses `2**(-(Te-Terf)/10)` | `DOCUMENT_SOURCE_SIGN_CONFLICT` | `UNRESOLVED` |
| Denitrification pH response | Appendix A13 uses `min(1,10^((pH-6.5)/3))` | `ghg_n2o.for:263-264` is the same relation | `EXACT_ALGEBRAIC_MATCH` | `INDEPENDENT_THEORY` |
| Relative N2O/NO3 denitrification temperature response | Appendix A12 uses Q10 ratio to `(T-Tref)/10`; Table A1 gives 2.6 | `ghg_n2o.for:266-268` uses 2.6 with the same exponent | `EXACT_ALGEBRAIC_AND_PARAMETER_MATCH` | `INDEPENDENT_THEORY` |
| Relative aeration response | Appendix A14 defines the denitrification aeration response as a function of `Fae` and a relative aeration parameter | `ghg_n2o.for:270-282` uses `Aevoan=1-Rdfantfc` and an algebraically matching square-root form for `RatAer` | `ALGEBRAIC_MATCH_AFTER_VARIABLE_MAPPING` | `INDEPENDENT_THEORY` |
| Denitrification N2O production competition | Appendix A9/A10 partitions anaerobic electron production between NO3 reduction and N2O production using NO3, N2O, pH, temperature, aeration and relative electron affinity | the OM-limited branch at `ghg_n2o.for:547-561` partitions `Respoman` between `QPrN2Oden` and `QRdN2O` using `RatFacN2O`, NO3 and N2O concentration plus stoichiometry | `STRONG_ALGEBRAIC_STRUCTURE_MATCH` | `INDEPENDENT_THEORY`, with exact unit/stoichiometry mapping retained for deeper audit |
| N2O reduction competition | Appendix A11 uses the same denominator as production but, as printed/extracted, the numerator contains pH, temperature and electron affinity without the aeration factor | revision 53 folds `RatAer` into `RatFacN2O` and uses that factor in the reduction partition at `ghg_n2o.for:560-561` | `DOCUMENT_SOURCE_AERATION_FACTOR_PLACEMENT_CONFLICT` | `UNRESOLVED` |
| Atmosphere emission mechanisms | Original-concept description and Appendix A state simultaneous diffusion across the soil-atmosphere boundary plus air-flow advection | revision-53 N2O output/transport separates diffusion and air-flow emission | `PROCESS_MATCH` | `INDEPENDENT_THEORY` |

## 4. Two unresolved theory-code conflicts

### 4.1 Nitrification temperature sign

The independent 2011 appendix, as published and text-extracted, represents the nitrification temperature response with a positive Q10 exponent. Revision 53 uses a negative exponent.

This must not be declared a code defect solely from the publication. The source comment attributes its formulation to Maag & Vinther (1996), and literature describing that experimental result reports that the N2O fraction associated with nitrification decreases with increasing temperature. That makes either a publication notation/typographical issue or a deliberate later/source-specific convention plausible.

Required closure:

- recover the detailed Hendriks ANIMO GHG specification, preferably authoritative Report 2054 bytes or equivalent source documentation;
- inspect source history/change records between the documented formulation and the frozen source;
- only then classify the sign difference as documented intent, publication error, or code discrepancy.

Local reconciliation key:

`GHG01-LCL-N2O-NITRIFICATION-TEMPERATURE-SIGN-DOC-SOURCE`

### 4.2 N2O-reduction aeration-factor placement

Appendix A11, as printed/extracted, omits `fae` from the numerator of the N2O reduction term while retaining it in the denominator. Revision 53 constructs `RatFacN2O` from pH, temperature, aeration and electron affinity and uses that combined factor in the reduction partition.

This is potentially material because aeration can change the production-to-reduction ratio. It is not safe to infer which expression is authoritative without the detailed ANIMO GHG derivation or source history.

Local reconciliation key:

`GHG01-LCL-N2O-REDUCTION-AERATION-FACTOR-DOC-SOURCE`

Classification:

`DOCUMENT_SOURCE_AERATION_FACTOR_PLACEMENT_CONFLICT_REQUIRES_DETAILED_AUTHORITY`

## 5. Qualification consequence

The previous statement that the exact N2O equations are broadly only `SOURCE_ONLY` is now too conservative.

Independent ANIMO-specific peer-reviewed equation authority is now available for:

- the equilibrium N2O gas/water system-state relation;
- the original conservation-and-transport structure;
- effective combined gas/water diffusion;
- nitrification production structure;
- WFPS response;
- denitrification pH response;
- the relative denitrification temperature Q10 relation with value 2.6;
- the relative aeration-response relation;
- the broad denitrification production/reduction competition structure;
- diffusion and air-flow emission mechanisms.

Two exact-equation reconciliation issues remain unresolved, and several source-specific coefficient/functions still lack independent release-specific authority. CH4 exact kinetics remain substantially less well documented than N2O in the evidence recovered here.

The ANIMO-GHG01 final closeout therefore remains:

`QUALIFIED_GHG_THEORY_SOURCE_AND_INPUT_LINEAGE_EVIDENCE_WITH_HISTORICAL_REFERENCE_GAPS`

B3 remains blocked. Historical revision-53 behaviour is not established by this theory recovery, and no production migration is admitted.
