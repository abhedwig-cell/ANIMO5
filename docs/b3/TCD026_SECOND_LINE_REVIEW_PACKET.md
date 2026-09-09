# TCD-026 independent second-line review packet

Request: `ANIMO-B3A04-TCD026-SECOND-LINE-REVIEW`

This packet is a handoff only. The ANIMO-B3A04 authoring activity is not an independent review and must not be recorded as one.

## Review target

Review exactly one claim:

`Ex(Ln)` is an existing restartable root-exudate organic-matter store. Revision 53 observes its result state `Rsex(Ln)` in final `Bfom` storage but omits `Ex(Ln)` from beginning `Bfom` storage. The only candidate Class-A correction is:

```fortran
Bfom(Inip_x,Ly) = Bfom(Inip_x,Ly) + Ex(Ln) * P
```

Do not review or admit any other organic-matter discrepancy in this packet.

## Pinned evidence

Review against these authorities:

- canonical base `work/animo-b3i01-canonical-register-append` at `383c7a83e84a578969f92113280dc715b7bdddb4`;
- frozen B0 source SHA-256 `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- frozen B0 testbank SHA-256 `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- PREP06 head `9b1f1ea51c24fb82823290193651830dc61ea3c8`;
- PREP06 defect evidence `docs/prep06/EXUDATE_INITIAL_STORAGE_LEDGER_DEFECT.md` blob `bbb7cd88c2beaa758e786e14e234a975b361b387`;
- PREP06 machine evidence `integration/animo-prep/PREP06_EXUDATE_INITIAL_STORAGE_DEFECT.json` blob `0e60d8aaf526c0b0127da1143b68c9c8235e9fe3`;
- PREP06 conserved-state inventory blob `838f224fc67a72371437c6d5b6e75cd03f5c8d51`;
- B3Q01 head `846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`;
- GOV02 head `db7add6f9561730bbf352aa7fd3f3968405cfaa3`;
- SYNQ01 head `842f72300fd03ede0b9024537a7ee6126722a121`;
- live PREP02R head observed by ANIMO-B3A04: `a2fda49871ee3c7104daf7e06cd8dffdac06b125`.

Before recording a final review result, recheck any authority whose live state can affect admission, especially PREP02R.

## Review questions

Record PASS, FAIL or INCOMPLETE for every item.

| Gate | Question |
| --- | --- |
| B0 identity | Do source and testbank hashes match the frozen baseline? |
| canonical scope | Does the canonical register still define TCD-026 as the initial exudate/fresh-OM ledger omission only? |
| atomicity | Is the proposed change limited to one Bfom beginning-storage term? |
| physical owner | Is `Ex` the accepted current state and `Rsex` the result state, with `Init: Ex=Rsex` and restart persistence? |
| ending storage | Does current `Bfom(Finp_x,Ly)` include `Rsex(Ln)*Z`? |
| beginning omission | Does current `Bfom(Inip_x,Ly)` omit `Ex(Ln)*P`? |
| N/P negative control | Do Bano and Bapo already include initial Ex via Nifrex/Pofrex, so they must not be modified? |
| causal discriminator | Does the PREP06 single-input 10 kg/ha Ex probe produce a legacy residual of -10 kg/ha? |
| ledger-only effect | Does adding only `Ex(Ln)*P` remove that deterministic omission without changing physical trajectories? |
| no tolerance | Are the roughly 1e-10 kg/ha residuals treated as diagnostic floating-point remainder only, never as a tolerance? |
| state non-interference | Is every physical state exactly outside the candidate write set, with PREP06 output evidence consistent with this? |
| flux non-interference | Are all process fluxes outside the candidate write set and unchanged in the evidence? |
| total mass non-interference | Is physical OM mass unchanged because the candidate observes an already-existing store only? |
| output whitelist | Are only Bfom-derived fresh-OM balance/report surfaces allowed to change? |
| zero-Ex negative control | Is the candidate exactly inert when initial Ex is zero? |
| natural activation | Is ordinary supplied B1 non-activation correctly classified as structural zero-initial-Ex unreachability? |
| SYNQ01 | Does current SYNQ01 still have no TCD-026-specific oracle? |
| route | Is corrected-legacy admission kept blocked unless GOV02 route requirements are actually satisfied? |
| independence | Is the reviewer genuinely separate from ANIMO-B3A04 authoring? |
| non-composition | Are all other OM ledger, physics and numerical issues excluded? |

## Expected-difference contract

Use `integration/animo-b3/TCD026_EXPECTED_DIFFERENCE.json` as the predeclared output contract.

The PREP06 Ruurlo synthetic comparison observed exactly six changed organic-matter balance files:

- `ani_omGP.Bal`
- `ani_omRP.Bal`
- `ani_omTP.Bal`
- `baomGP.Out`
- `baomRP.Out`
- `baomTP.Out`

That six-file list is evidence for the specific diagnostic run. The durable whitelist is semantic: only affected `Bfom` fresh-OM balance/report surfaces may change. Any physical, N, P, water or ordinary state/process difference fails the Class-A claim.

## Natural activation boundary

Do not turn zero coverage into a false natural PASS. PREP06 found all supplied initial `>orgexu:` values equal to zero, so the beginning-storage omission cannot affect ordinary supplied start-of-run balances.

A later independent review may strengthen path coverage with a model-produced restart that starts from nonzero persisted exudate state. That would be useful but is not evidence claimed by ANIMO-B3A04.

## SYNQ01 boundary

The current SYNQ01 TCD coverage matrix does not list TCD-026. Do not substitute `SYNQ-O003` merely because it also concerns a storage identity. O003 is an interception-water control-volume oracle and is not independent evidence for exudate organic matter.

## Route boundary

At the ANIMO-B3A04 live check, PREP02R still stated:

- normal B2 reference unavailable;
- historical-uncertainty route ineligible;
- historical reference not qualified.

Therefore a scientific review PASS may complete the review gate but still may not imply admission. Admission remains a separate fail-closed B3 action after a valid route exists.

## Required review record

The independent reviewer/workunit should record:

- reviewer/workunit identity;
- exact reviewed branch head;
- exact authority heads rechecked;
- PASS/FAIL/INCOMPLETE per table row;
- any contradictory evidence;
- whether a model-produced restart activation was additionally executed;
- route state at review time;
- final review value exactly one of `PASS_INDEPENDENT_REVIEW`, `FAIL_INDEPENDENT_REVIEW` or `INCOMPLETE_REVIEW`.

A review PASS must not set `admitted=true` in ANIMO-B3A04. It only satisfies the independent-review prerequisite for a later admission authority.
