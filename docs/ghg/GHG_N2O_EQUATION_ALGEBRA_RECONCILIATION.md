# ANIMO-GHG01 — N2O denitrification algebra reconciliation

Status: `A10_EXACTLY_RECONCILED_A11_AERATION_FACTOR_CONFLICT_SHARPENED`

This note performs the explicit algebraic crosswalk between the peer-reviewed 2011 ANIMO Appendix A equations and the frozen revision-53 source. It does not decide which side of a remaining document-source conflict is authoritative.

Evidence:

- Stolk, Hendriks, Jacobs, Moors & Kabat (2011), Biogeosciences 8, 2649-2663, DOI `10.5194/bg-8-2649-2011`, Appendix A9-A14;
- frozen `ghg_n2o.for`, SHA-256 `493bf88d4b321df64817a7c0eaa2725ad614a45df0a0f16cefa96ac348254175`;
- frozen `Aeration_original.for`, SHA-256 `cc02a097df98cfe36abd64403522fc6cf2b14addcc36cee2d4749916a21bd169`.

## 1. Variable mapping

For the organic-matter-limited denitrification branch define:

- `N = cw,NO3`;
- `Z = cw,N2O`;
- `P = fpH * fT,den * fae * Eaf`;
- `C = Cfracom`;
- `R = anaerobic organic-matter respiration`.

Revision 53 constructs:

`RatFacN2O = P / 4`

when the source symbols are mapped as:

- `RdfaphN2O -> fpH`;
- `CrfaTeN2ONO3 -> fT,den`;
- `RatAer -> fae`;
- `RelK_N2Ode -> Eaf`.

The aeration mapping is direct. `Aeration_original.for` sets `Rdfantfc = Aevo*(1-Tian)` as the aerated fraction and `Aevoan = 1-Rdfantfc`; `ghg_n2o.for` then computes `RatAer` from `Aevoan` with the same square-root relation printed as Appendix A14.

Revision 53 also defines:

`StoichNO3 = (14/12) * C`

and

`StoichN2O = 4*(14/12) * C = (14/3)*C`.

Appendix A8 gives potential electron production as:

`Rpr,el,an = (C/3) * R`.

Layer thickness `He` converts the source's volumetric rate to its stored/output areal rate and therefore cancels from the conceptual comparison below.

## 2. Appendix A10 versus revision-53 N2O production

Appendix A10 can be rewritten as:

`Rpr,N2O,den = [14*N / (4*N + P*Z)] * Rpr,el,an`

Substituting Appendix A8:

`Rpr,N2O,den = [14*N / (4*N + P*Z)] * (C/3)*R`

or equivalently:

`Rpr,N2O,den = [N / (N + (P/4)*Z)] * (14/12)*C*R`.

Revision 53, organic-matter-limited branch, is:

`QPrN2Oden = AvCoNO3/(AvCoNO3 + RatFacN2O*AvCoN2O) * StoichNO3 * Respoman * He`

After the mappings `AvCoNO3=N`, `AvCoN2O=Z`, `RatFacN2O=P/4`, `StoichNO3=(14/12)C`, and removing only the expected `He` volumetric-to-areal conversion, this is algebraically identical to Appendix A10.

Verdict:

`N2O_DENITRIFICATION_PRODUCTION_A10_EXACT_ALGEBRAIC_MATCH_FOR_OM_LIMITED_BRANCH`

Provenance:

`INDEPENDENT_THEORY`

This is stronger than merely a structural match.

## 3. Appendix A11 versus revision-53 N2O reduction

Let:

`G = fpH * fT,den * Eaf`

so that `P = fae*G`.

Appendix A11, as printed in the peer-reviewed paper, can be rewritten as:

`Rrd,N2O = [14*G*Z / (4*N + P*Z)] * Rpr,el,an`

and using A8:

`Rrd,N2O = [14*G*Z / (4*N + P*Z)] * (C/3)*R`.

Revision 53 uses:

`QRdN2O = Z/(N/(P/4) + Z) * StoichN2O * R`

which reduces to:

`QRdN2O = [P*Z / (4*N + P*Z)] * (14/3)*C*R`

or:

`QRdN2O = [14*fae*G*Z / (4*N + P*Z)] * (C/3)*R`.

Therefore the source and Appendix A11 differ by exactly one multiplicative `fae` factor in the reduction numerator, assuming the printed A11 equation is authoritative as rendered.

This is not merely a vague implementation-shape difference. It is an algebraically isolated theory-source discrepancy:

`REV53_REDUCTION_RATE = fae * APPENDIX_A11_REDUCTION_RATE`

for otherwise identical mapped state and response variables in this branch.

The equality above concerns the local instantaneous algebra before branch limits, availability corrections, iteration and time integration. It does not assert that whole-timestep output differs by the same factor.

Verdict:

`DOCUMENT_SOURCE_A11_EXTRA_AERATION_FACTOR_IN_REV53_REDUCTION_NUMERATOR`

Local key:

`GHG01-LCL-N2O-REDUCTION-AERATION-FACTOR-DOC-SOURCE`

Classification remains:

`UNRESOLVED`

because the detailed Hendriks derivation/source history has not been recovered. The paper may contain a notation/typesetting issue, the source may implement a different revision of the formulation, or the source may be inconsistent with the published equation.

## 4. Nitrate-limited branch

Revision 53 also contains a nitrate-limited branch in `NO3N2OReduc`. There `QPrN2Oden` initially follows the existing first-order nitrate reduction and `RespomanN2O` is calculated from the same `RatFacN2O` competition expression, followed by a total anaerobic-respiration capacity correction.

Appendix A9 expresses N2O production as the minimum of a nitrate-reduction-limited term and the electron-production-limited competition term. This supports the two-limit conceptual structure, but a complete exact crosswalk of all revision-53 iterative correction semantics is outside this short algebra note.

No contradiction is claimed for the nitrate-limited branch here.

## 5. Nitrification temperature sign context

Appendix A17 prints a positive Q10 exponent for the temperature response of the fraction of nitrified NH4 emitted as N2O. Revision 53 uses a negative exponent with base 2.

The source explicitly attributes this dependence to Maag & Vinther (1996). Their peer-reviewed experimental abstract states that the percentage of N2O-N produced by nitrification decreased as temperature increased. That direction supports the negative response encoded in revision 53 and conflicts with a naive reading of the positive exponent in Appendix A17.

This does not prove that Appendix A17 is a typographical error, because definitions and normalization details may differ. It does strengthen the disposition from a symmetric source-versus-document ambiguity to:

`PUBLICATION_EQUATION_SIGN_SUSPECT_SOURCE_DIRECTION_SUPPORTED_BY_CITED_EMPIRICAL_STUDY`

The formal provenance remains `UNRESOLVED` until the detailed ANIMO GHG derivation or change history fixes the intended equation.

## 6. Qualification consequence

The 2011 theory-authority recovery can now be stated more precisely:

- Appendix A10 and the revision-53 organic-matter-limited N2O production equation are algebraically equivalent after explicit stoichiometric and state-variable mapping;
- Appendix A11 and revision-53 N2O reduction differ by one isolated aeration-response factor in the numerator;
- the revision-53 nitrification temperature direction is independently consistent with the cited Maag & Vinther experimental finding, although the published ANIMO Appendix A17 sign remains unresolved.

No production correction is specified. No historical behavioural claim is made. The two document-source discrepancies remain B3 blockers until authoritative scientific disposition.
