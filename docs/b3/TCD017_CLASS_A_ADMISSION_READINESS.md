# ANIMO-B3A02 — TCD-017 Class-A admission readiness

Status: `QUALIFIED_TCD017_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

Target: `TCD-017`

Class: `A_ACCOUNTING_REPORTING_ONLY`

Admission performed: **no**.

This workunit qualifies one atomic claim only: revision-53 already performs the physical dissolved-organic-P redistribution during ploughing, but the public organic-P redistribution ledger omits the matching top-reservoir loss. The proposed correction adds that already-computed loss to `Bapo(Redi,Ly)`. It does not change ploughing physics, physical state, process fluxes, transport, management, or any other organic-P finding.

## 1. Authority and frozen identity

The workunit starts from canonical branch `work/animo-b3i01-canonical-register-append` at `383c7a83e84a578969f92113280dc715b7bdddb4`.

Frozen B0 identities used throughout:

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

Evidence authorities:

| Authority | Evidence used here |
| --- | --- |
| PREP01 | `docs/prep01/ORGANIC_P_REDISTRIBUTION_BALANCE_DEFECT.md`, blob `f5122fd4182f829fa2806d9c06d5ece485e7f0a5` |
| PREP02 | `docs/prep02/ORGANIC_P_PLOUGHING_ARRAY_AUDIT.md`, blob `d262af83bdb930b7919fd2d2044ed063791a8abd`, but only the top-term-only natural LWKM method/evidence is imported |
| PREP06 | `integration/animo-prep/PREP06_TRANSFER_LEDGER.csv`, blob `9caf62061ffbfefd28940b9ac170d6ae12b4d638` |
| B3Q01 | `integration/animo-b3/B3_EXISTING_TCD_CLASSIFICATION.csv`, blob `5cc126298bb7ce04e0dba5b64de07e0a51f50938`; `docs/governance/B3_SCIENTIFIC_ADMISSION_FRAMEWORK.md`, blob `878ec3033eccf11ff278afa76bd6ddc9809fe769` |
| GOV02 | branch `work/animo-gov02-evidence-dag-reconciliation` at `db7add6f9561730bbf352aa7fd3f3968405cfaa3`; `B2_REQUIREMENT_SCOPE.md` blob `7602faf85d425775b7d50c43596c5e13fa5a3421`; `PREP02R_BOUNDED_ACQUISITION_CLOSURE.md` blob `75ff02a4de10a395e7a61edf74b896893bba71bb` |
| SYNQ01 | branch `work/animo-synq01-independent-synthetic-oracles` at `842f72300fd03ede0b9024537a7ee6126722a121`; oracle `SYNQ-O002` in `SYNTHETIC_ORACLE_REGISTER.json`, blob `4c215d19844614de8868380fb03f93268ea4c5d8` |

B3Q01 already classifies TCD-017 as `ATOMIC_LEDGER_CLAIM`, Class A, not admitted. This workunit does not broaden that atom.

## 2. Exact physical source and destination terms

The revision-53 ploughing path is in `Addit.for`.

The top-reservoir dissolved organic P present before mixing is constructed as:

```fortran
If (Ipo.Eq.1) Sudiorpo = Codiorpotop * Hetop
```

The corresponding source loss is recorded explicitly:

```fortran
If (Ipo.Eq.1) Addiorpotoppl(I) = - Sudiorpo
```

This is the required `Addiorpotoppl` source loss. Its sign is negative because the separate top reservoir is emptied into the ploughing redistribution.

For each ploughed soil layer, `Addit.for` first subtracts the pre-plough dissolved-organic-P store from `Addiorpopl(I,Ln)`, then assigns the redistributed concentration, then adds the post-plough store back to `Addiorpopl(I,Ln)`. Therefore `Addiorpopl(I,Ln)` is the net layer destination gain or loss produced by the already-existing physical redistribution.

The physical state update itself is independent of the public balance ledger, including:

```fortran
If (Ipo.Eq.1) Codiorpo(Ln) = Help * Sudiorpo
```

No proposed B3A02 change touches these statements or any `Addit.for` state mutation.

## 3. Exact current ledger omission

The public organic-P redistribution ledger is assembled in `Outbal_calc.for` under the existing phosphorus and ploughing path.

For the top reservoir (`Ln.Eq.0`), the current code records the analogous inorganic-P top term:

```fortran
Bapp(Redi,Ly) = Bapp(Redi,Ly) + Adpotoppl(I)*Z
```

For the ploughed soil layers it records dissolved organic P as:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpopl(I,Ln)*Z
```

There is no matching `Addiorpotoppl(I)*Z` contribution to `Bapo(Redi,Ly)` in the `Ln.Eq.0` branch. The public ledger therefore counts the destination-side layer redistribution while omitting the source-side top-reservoir loss.

That is the complete TCD-017 claim qualified here.

## 4. Proposed atomic correction

The proposed correction is one ledger-only accounting statement in the existing `Ln.Eq.0` ploughing branch of `Outbal_calc.for`, already inside the phosphorus-enabled scope:

```fortran
Bapo(Redi,Ly) = Bapo(Redi,Ly) + Addiorpotoppl(I)*Z
```

No source patch is applied by ANIMO-B3A02. The expression is frozen here only as the candidate expected difference for a later correction workunit after an admissible route and independent review exist.

The correction consumes an already-existing accounting value. It does not recompute physical mass, concentrations, redistribution fractions, or rates.

## 5. Conservation identity and natural LWKM evidence

PREP06 classifies `PLOUGH-DOM` as an internal transfer. For an encompassing control volume, the top-reservoir loss plus the redistributed layer gains must cancel:

`Addiorpotoppl source loss + sum(Addiorpopl layer changes) = 0`, for the TCD-017 dissolved-organic-P atom.

SYNQ01 independently encodes the same closed-transfer identity in `SYNQ-O002`:

`-source + sum(destinations) = 0`.

The synthetic oracle is decimal-exact, strongly independent of ANIMO implementation control flow, and is used only as a conservation oracle, never as B2 historical evidence.

The supplied natural case `LWKM_gras_1040.2021.2045` activates the top-reservoir TCD-017 path. PREP01 measured, for all three configured balance profiles:

- cumulative top-reservoir organic-P redistribution: `-0.15380316471773922 kg/ha P`;
- cumulative layer dissolved-organic-P redistribution: `+0.15380316471773947 kg/ha P`;
- stable-DOP contribution in this natural case: `0.0 kg/ha P`;
- top plus layer redistribution: approximately `2.50e-16 kg/ha P`.

Thus the physical redistribution is already closed to floating representation noise. The legacy public organic-P ledger omits the negative top term and consequently exposes approximately `+0.154 kg/ha P` as a spurious cumulative redistribution input.

A PREP01 diagnostic copy adding only the proposed top term changed the LWKM GP organic-P balance deviation as follows:

- 1997: `+4.41e-2` to `+5.07e-13 kg/ha P`;
- 1998: `+4.94e-2` to `+4.61e-10 kg/ha P`;
- final cumulative deviation: approximately `+1.54e-1` to `+2.78e-8 kg/ha P`.

PREP02's top-term-only natural LWKM probe reports maximum absolute period residuals of `2.33e-10`, `4.06e-8`, and `6.54e-7 kg/ha P` for RP, GP, and TP respectively. After normalization of only known volatile timestamp and CPU-time fields, baseline-to-top-term differences were confined to organic-P balance surfaces.

These residual values are evidence of causal effect, not tolerances and not an admission criterion. The scientific identity is the closed internal-transfer relation.

## 6. Class-A non-interference proof

### Physical state trajectory

`PASS_FOR_ADMISSION_READINESS`.

The candidate statement writes only `Bapo(Redi,Ly)` in `Outbal_calc.for`. It does not write `Codiorpotop`, `Codiorpo`, any fresh/stable/humus organic-P state, PO4 state, soil water state, crop state, or management state. The physical redistribution is completed earlier in `Addit.for` and the input accounting arrays `Addiorpotoppl` and `Addiorpopl` are already fixed before the public ledger consumes them.

PREP01 explicitly performed the top-term probe without changing model state, process rate, transport calculation, or testcase input. PREP02's top-term-only natural comparison found no normalized ordinary non-balance output difference.

Therefore the proposed ledger statement has no write path into physical state and no observed physical-output trajectory effect on the natural activated case.

### Process flux trajectory

`PASS_FOR_ADMISSION_READINESS`.

The candidate statement neither reads nor writes transport fluxes to recompute them. It only maps an existing ploughing transfer accounting value into `Bapo`. Transport, reaction, crop, hydrology, and management calculations occur independently of this ledger addition. PREP01's direct soluble-organic-P transport audit also showed that the large public balance defect is not caused by the transport solver.

No process flux is on the expected-difference whitelist.

### Total physical mass

`PASS_FOR_ADMISSION_READINESS`.

The measured natural control volume already satisfies top-loss plus layer-gain closure before any ledger correction. Adding the omitted ledger term changes only the representation of that internal transfer. Total physical P before and after the ploughing event is unchanged by the candidate correction, and the complete run's physical trajectory is unchanged.

### Intended ledger identity

`PASS_FOR_ADMISSION_READINESS`.

The public organic-P ledger is brought into agreement with the already-existing internal-transfer ownership rule by adding the missing negative top-reservoir side. No compensating physical source or sink is introduced.

## 7. Output whitelist

Only the following surfaces are permitted to differ in a later TCD-017 correction qualification:

1. `Bapo(Redi,Ly)` for balance control volumes and periods in which the TCD-017 top-reservoir ploughing transfer is active;
2. organic-P balance quantities derived from that `Bapo` redistribution entry, including the resulting organic-P balance deviation;
3. corresponding `bapo<balance-label>.Out` reporting surfaces, such as the natural LWKM `bapoRP.Out`, `bapoGP.Out`, and `bapoTP.Out` where active.

Everything else is explicitly unchanged. This includes all physical states, all process fluxes, hydrology, transport outputs, crop outputs, management continuation state, other balance families, `Bapp`, ordinary state-output files, and detailed organic-P transformation/accumulator surfaces such as `Bafop`.

Any difference outside this whitelist fails the atomic TCD-017 qualification.

## 8. Explicit non-composition boundary

ANIMO-B3A02 does **not** qualify or compose any other organic-P issue.

Excluded from this workunit are, at minimum:

- the separate stable-DOP ledger findings involving `AdStdiorpopl` from later PREP02 activation work;
- the separate exudate-humus-P ledger findings involving `Adhuexpopl`;
- TCD-027, the detailed organic-P redistribution accumulator defect, including the `Bafop` slot issue;
- TCD-028, the stable-DOM plough redistribution accumulator lifecycle finding;
- any physical or numerical organic-P change.

The candidate statement does not modify `Bafop`, `AdStdiorpopl`, `Adhuexpopl`, stable-DOM accumulation, or any physical redistribution state. B3Q01 composition rules therefore remain outside this atomic readiness object.

## 9. Route and review gate

B3Q01 and GOV02 require a valid route before admission.

Current GOV02 mapping of PREP02R is `B2_ACQUISITION_STILL_ACTIVE`. A qualified B2 historical reference is not available, while the historical-uncertainty route is also not eligible because documented bounded acquisition closure has not been reached.

Accordingly:

- normal B2 route: **not available**;
- historical-uncertainty route: **not eligible**;
- independent second-line B3 review of this correction object: **pending**;
- corrected-legacy admission: **not performed**;
- production patch: **not performed**.

SYNQ01 cannot substitute for either route gate. Its role here is limited to the independent closed redistribution identity.

## 10. Readiness decision

The atomic Class-A scientific claim is ready for route-qualified review:

- `Addiorpotoppl` is the already-computed source loss;
- `Addiorpopl` is the already-computed layer destination redistribution;
- natural LWKM shows their TCD-017 dissolved-organic-P top-plus-layer contribution closes physically;
- the current public `Bapo` ledger omits the source side;
- the proposed one-line `Bapo` term restores the ledger identity only;
- physical state, process fluxes, and total physical mass are outside the change surface;
- the expected output delta is narrowly whitelisted;
- no other organic-P finding is included.

Final workunit status:

`QUALIFIED_TCD017_CLASS_A_ADMISSION_READINESS_ROUTE_AND_INDEPENDENT_REVIEW_PENDING`

This status is deliberately not an admission decision.