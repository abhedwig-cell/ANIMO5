# ANIMO-TH03 — HETOP reservoir lineage and zero-endpoint provenance recovery

Status target: provenance qualification only. No production change, input-policy change, TCD reservation or B3 admission.

## 1. Question

ANIMO-UBQ04 established that the available ANIMO 4.0 user documentation and revision-53 source do not uniquely define the meaning of `HETOP=0`. TH03 therefore asks a narrower historical question: what does pre-4.0 ANIMO theory say about the surface/addition reservoir, and does that lineage uniquely resolve the zero endpoint?

## 2. Recovered ANIMO 3.5 process theory

The official WUR catalogue identifies Groenendijk and Kroes (1999), *Modelling the nitrogen and phosphorus leaching to groundwater and surface water with ANIMO 3.5*, Report 144, with official document locator `https://edepot.wur.nl/363774`.

Direct opening of the official PDF endpoint remained blocked in the execution environment. However, during TH03 closeout strengthening, the WUR edepot search index itself exposed the relevant Section 2.1.3 paragraph text. The same passage was cross-checked against the previously located secondary full-text mirror. The process reconstruction below therefore has WUR-hosted paragraph-level support; the secondary mirror is corroboration only, not the sole textual source.

Section 2.1.3, *Upper soil storage and surface runoff*, establishes the following model concept in ANIMO 3.5:

- an imaginary storage reservoir is placed at the soil surface for manure and fertilizer additions;
- additions are immediately dissolved in that reservoir;
- migration inside the reservoir is represented as piston flow;
- the stored quantity is depleted after cumulative precipitation equals the reservoir volume;
- the release rate is controlled by the selected reservoir thickness;
- remaining material is maintained by bookkeeping;
- surface-runoff solute routing uses the concentration of this surface reservoir.

These are process-theory statements, not implementation guesses. They show that the reservoir concept predates ANIMO 4.0 and that its thickness has physical/numerical meaning as a storage-volume and release-timescale parameter.

## 3. ANIMO 4.0 continuity evidence

The ANIMO 4.0 user guide describes `HETOP` as the thickness of the virtual reservoir from which fertilizer additions are leached in proportion to cumulative precipitation since the fertilization event. It publishes the range `[0.0 ... 0.2] m`.

The official metadata for Groenendijk, Renaud and Roelsma (2005), Alterra Report 983, states that ANIMO 4.0 introduced new formulations after 3.5 concerning soil-moisture effects on mineralization and denitrification and support for externally supplied daily crop uptake. This is supporting lineage context only. It is not treated as an exhaustive statement that no upper-reservoir code changed.

TH03 therefore qualifies concept continuity, but not bitwise or source-level identity between ANIMO 3.5 and revision 53.

## 4. What the lineage rules out

No recovered theory identifies reservoir thickness zero as an explicit feature flag or disable sentinel. Revision-53 source likewise contains no explicit general `HETOP==0` sentinel branch. Consequently, treating zero as a known legacy switch is unsupported.

The lineage also makes clear why silently relabelling `HETOP` as a purely numerical tuning parameter would be wrong. Its documented role is tied to a conceptual storage volume and precipitation-controlled release.

## 5. What the lineage does not resolve

The ANIMO 3.5 theory passage does not define the exact `Zsurf=0` endpoint. The recovered ANIMO 3.5 user-guide material confirms that a dedicated SOIL.INP table existed, but TH03 did not recover a trustworthy text rendering of the `HETOP` row from that guide. It therefore does not claim that the inclusive `[0.0 ... 0.2]` range itself is proven to originate in 3.5.

Three interpretations remain materially different:

1. zero was accidentally admitted by input bounds and should be invalid;
2. zero was intended as a zero-capacity limiting case with instantaneous routing;
3. zero was intended only under a restricted option combination.

The first is compatible with the positive-volume theory but lacks explicit authority. The second is mathematically plausible for some positive-throughflow limits, but not globally defined when load/storage terms remain nonzero or throughflow vanishes. The third requires an option contract that has not been recovered.

## 6. Relation to TCD-042

This work does not widen or modify `TCD-042-B1` or `TCD-042-E1`. Their positive-`HETOP` results remain intact.

In particular, the NQ03 small-`P` policy cannot be extrapolated to `HETOP=0`: for fixed positive `Flux`, `P = St*Flux/HETOP` moves toward large, not small, values as `HETOP` approaches zero.

The HETOP endpoint remains a domain/provenance blocker, not a newly admitted TCD-042 child and not a basis for reserving a new top-level TCD.

## 7. Qualified disposition

TH03 qualifies the following statement:

`HETOP` is the descendant of an ANIMO 3.5 surface/addition reservoir thickness that controls storage volume and precipitation-driven release. The recovered lineage does not define zero as a sentinel and does not uniquely define the exact zero-thickness endpoint.

Decision:

`QUALIFIED_HETOP_RESERVOIR_CONCEPT_LINEAGE_TO_ANIMO35_ZERO_ENDPOINT_UNRESOLVED`

No input rejection, zero-capacity passthrough, fallback, epsilon, production patch, TCD allocation or scientific admission follows from this result.

## 8. Next evidence that could change the result

High-value evidence is now very specific:

- a trustworthy rendering or copy of the ANIMO 3.5 SOIL.INP input table showing the historical lower bound for the reservoir-thickness parameter;
- older ANIMO source or input examples that execute a zero-thickness case;
- the full text of Alterra Report 983 around the upper-reservoir formulation, sufficient to establish whether ANIMO 4.0 changed or retained the 3.5 formulation;
- internal release notes or model-maintenance documentation explicitly defining the zero endpoint.

Absent such evidence, the correct disposition remains fail closed.
