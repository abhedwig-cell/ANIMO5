# TCD-027 Independent Second-Line Review

Work unit: `ANIMO-B3A01R`

Semantic result: `INCOMPLETE`

Review branch: `review/animo-b3a01r-tcd027-independent-second-line`

Review-object handoff head: `f348d0509ddfbb60473d41a7fe25e67d8e088e7f`

## Review boundary

This is a separate-context second-line review of the atomic TCD-027 Class-A claim only:

```fortran
! frozen legacy statement
Bafop(24,Ly)=Bafop(25,Ly)+Dum

! candidate statement
Bafop(24,Ly)=Bafop(24,Ly)+Dum
```

The scope is restricted to detailed organic-P reporting accumulator slot 24, `redis_EXP`, in `Outbal_calc.for`. No organic-P process physics, TCD-017, TCD-026, TCD-028, stable-DOM correction, composition, production patch, B4 action, central-regie update or admission is part of this review.

The review records separate ChatGPT-context independence only. It does not claim human or organizational independence. The B3D10 authoring-context source recheck was treated as supporting evidence only and was not allowed to satisfy an independent source gate.

## Live heads and identities rechecked

The following live authority heads were rechecked before review authoring:

- review handoff: `f348d0509ddfbb60473d41a7fe25e67d8e088e7f`;
- ANIMO-B3A01 readiness: `b2bac82512fef0fa232e759f0c68b472567c11d5`;
- ANIMO-B3D10 formal route reconciliation: `a7b11b334f8b2604d5036edc04365006800944e0`;
- ANIMO-GOV03 historical route: `cbd262bdabe92923113b7326f2f42822ce9a971c`;
- ANIMO-B3Q01 framework: `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- retained PREP06 evidence head inspected: `9b1f1ea51c24fb82823290193651830dc61ea3c8`.

Frozen B0 identities are consistent across the hash pins and the retained source-reverification record:

- source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- `Outbal_calc.for` member SHA-256: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`;
- `Outbal_write.for` member SHA-256: `cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea`.

The public repository intentionally retains only hashes/manifests for the frozen source archive, not the source archive bytes. The documentation baseline likewise states that the ANIMO 4.0 guide is not an exact specification of ANIMO 4.1.5 revision 53.

## Evidence independently inspected

The review independently inspected the frozen identity pins and manifests, PREP06 source-reverification and diagnostic records, PREP06 transfer-ledger classification, B3A01 readiness evidence, B3Q01, GOV03 acquisition closure, the B3D10 route object, current branch heads, current issue #30 and its comments, and current B2-related repository surfaces.

The PREP06 post-close source reverification is source-bound to the frozen source SHA and reports direct parsing of 77 uncommented detailed accumulator assignments. It identifies exactly one cross-slot self-reference, `Bafop(24,Ly)=bafop(25,Ly) + Dum`, at `Outbal_calc.for` line 1428. PREP06 explicitly remains non-reference B1/preparatory evidence.

The retained TCD-027 diagnostic record reports natural activation in `LWKM_gras_1040.2021.2045`, period 1997. Its discriminator changes `redis_EXP` from approximately `-7.0644 kg/ha P` to `0.0 kg/ha P`, with the changed-output set limited to `transfopGP.Out`, `transfopRP.Out` and `transfopTP.Out`. The same bounded diagnostic reports no change to physical-state trajectory, process-flux trajectory, total organic-P balance, total mass balance, `redis_OP`, `redis_DOP`, `redis_HUP`, or ordinary non-reporting outputs across the 58 common top-level outputs. These observations are treated only as B1 diagnostic evidence, never as historical B2 or as a numerical tolerance/oracle.

## Fail-closed check matrix

| # | Required review item | Result | Independent assessment |
|---|---|---|---|
| 1 | Frozen B0 source/testbank identities | PASS | Hash pins and PREP06 source reverification agree exactly. |
| 2 | Legacy/candidate expressions and local construction/meaning of `Dum` | INCOMPLETE | The frozen legacy cross-slot statement is independently retained by the PREP06 source parser, and the candidate text is consistently declared in the review object. The exact local construction and meaning of `Dum` is not retained in an independent source extract. The frozen source bytes are not published in GitHub, so this separate connector-only context cannot re-read that source neighbourhood. B3D10 cannot substitute for this gate. |
| 3 | Exact `Outbal_write.for` mapping 24 `redis_EXP`, 25 `redis_OP`, 26 `redis_DOP`, 27 `redis_HUP` | INCOMPLETE | B3D10 records this mapping after an authoring-context source recheck, but no independently retained PREP06 source extract exposes the exact writer statements and the frozen source bytes are unavailable in this context. |
| 4 | `Bafop` seam is reporting accumulator, not physical state owner | PASS | PREP06 transfer-ledger model classifies detailed `Bafop` as reporting-only and explicitly separates reporting accumulators from conserved-state ownership. |
| 5 | Analogue accumulators and P slots 25/26/27 self-accumulate | INCOMPLETE | PREP06 diagnostic evidence retains the exact OM and N slot-24 analogues, and the source parser reports only one cross-slot self-reference among 77 assignments. The exact slot-25/26/27 P statements are not independently retained as source excerpts, so the full requested source-bound check cannot be closed without inferring beyond the retained record. |
| 6 | Natural LWKM activation, period 1997 | PASS | Retained PREP06 B1 diagnostic evidence identifies the exact case and period. |
| 7 | `redis_EXP` discriminator `-7.0644` versus `0.0` | PASS | Rechecked as a bounded diagnostic discriminator only, not a tolerance or historical oracle. |
| 8 | Changed-output whitelist is exactly three `transfop*.Out` files | PASS | Retained machine evidence gives exactly `transfopGP.Out`, `transfopRP.Out`, `transfopTP.Out`. |
| 9 | Physical state trajectory unchanged | PASS | Retained B1 non-interference evidence reports unchanged state trajectory; no B2 meaning is assigned. |
| 10 | Process flux trajectory unchanged | PASS | Retained B1 non-interference evidence reports unchanged process-flux trajectory. |
| 11 | Total organic-P balance unchanged | PASS | Retained diagnostic evidence reports unchanged total organic-P balance. |
| 12 | Total mass balance unchanged | PASS | Retained diagnostic evidence reports unchanged total mass balance. |
| 13 | `redis_OP` unchanged | PASS | Retained diagnostic evidence reports unchanged. |
| 14 | `redis_DOP` unchanged | PASS | Retained diagnostic evidence reports unchanged. |
| 15 | `redis_HUP` unchanged | PASS | Retained diagnostic evidence reports unchanged. |
| 16 | Ordinary non-reporting outputs unchanged across 58 common outputs | PASS | Retained comparison evidence reports only the three declared detailed-transfer outputs changed. |
| 17 | GOV03 route remains live and valid | PASS | Live GOV03 branch still resolves to `cbd262bd...`; its qualified state remains B2 unavailable after reasonable acquisition effort with G6U eligible, no B2 and no admission. |
| 18 | No qualified B2 has appeared since B3D10 | PASS | Current live GOV03 head is unchanged; B2-named branch search exposes only GOV03 and an older RG04 reconciliation branch; current issue search found no `QUALIFIED_B2` issue and no TCD-027 B2 replacement. No newer qualified B2 was found. |
| 19 | Historical revision-53 behaviour remains `UNKNOWN` | PASS | GOV03 explicitly preserves `UNKNOWN` when B2 is absent. |
| 20 | Independent B3Q01 historical-uncertainty-route sufficiency | INCOMPLETE | GOV03 acquisition closure, bounded Class-A scope, causal discriminator, conservation/non-interference evidence and explicit historical uncertainty are present. However B3Q01 requires fail-closed independent checking. Items 2, 3 and 5 cannot be independently source-closed in this context, so the second-line gate is not sufficiently discharged for a PASS. |
| 21 | PREP06 and B3A01 remain B1/readiness, never B2 | PASS | Both packages explicitly deny reference qualification; GOV03 also forbids promoting rebuild/source/diagnostic evidence to historical B2. |
| 22 | ANIMO 4.0 guide not used as revision-53 slot-algebra authority | PASS | The frozen documentation README explicitly says it is not an exact specification of revision 53. This review does not use it for slot algebra. |
| 23 | Other TCDs and organic-P/stable-DOM corrections excluded | PASS | They are outside the reviewed claim and receive no scientific disposition here. |
| 24 | No composition, production patch, B4, central-regie update or admission | PASS | This review changes review evidence/tooling only; the scope guard enforces the allowed review files. |

## Independent B3Q01 reassessment

The historical-uncertainty route itself is still open: GOV03 documents the completed acquisition effort and explicitly keeps historical behaviour unknown. The narrow Class-A evidence is materially stronger than a mere residual-improvement argument because the retained PREP06 package contains a hash-bound structural cross-slot finding, reporting-state separation, a natural discriminator and a tightly bounded non-interference surface.

That is not enough for this second-line review to return PASS. B3Q01 is fail closed, and this review contract specifically requires a fresh source-bound check of the local `Dum` construction, the writer mapping, and the neighbouring organic-P self-accumulator expressions. The public GitHub repository does not contain the frozen source archive bytes, while the existing independent PREP06 derivatives do not persist those exact source details. Using B3D10's authoring-context recheck to fill the gap would violate the stated independence boundary.

The correct semantic result is therefore `INCOMPLETE`, not `FAIL`: no contradictory evidence was found, but required independent evidence cannot be completed from the currently accessible source-bound record.

## Residual uncertainties

1. Exact local `Dum` construction and semantic provenance at the TCD-027 statement remain unverified by this separate review context.
2. Exact frozen `Outbal_write.for` slot-24 through slot-27 source statements remain unverified by this separate review context.
3. Exact frozen organic-P slot-25, slot-26 and slot-27 self-accumulator statements remain unverified by this separate review context.
4. Historical revision-53 behaviour remains `UNKNOWN`; no historical B2 exists.
5. Controlled immutable B0 retention remains a wider repository governance limitation recorded outside this atomic review; it is not silently upgraded here.

Closing items 1 through 3 requires access, in a genuinely independent review context, to the exact hash-matching frozen source bytes or to an independently generated source extract that preserves the needed source neighbourhood and writer statements with verifiable identity. Until then, this review must remain `INCOMPLETE`.

## Result boundary

`INCOMPLETE` is review evidence only. TCD-027 is not admitted. No production patch is authorized. No B4, composition or central-regie action is performed. A later review may supersede this result only after the unresolved source-bound evidence has been independently closed.