# ANIMO-GHG03 — TCD-032 Methanogenesis Carbon-Transfer Ownership Qualification

Status: `AUTHORING_FROZEN_PENDING_GOV05_TIER_C_ADVERSARIAL_REVIEW`

## Scope

This workunit qualifies only the carbon-transfer ownership identity needed to close `TCD-032`: the source-family organic-carbon debit that corresponds to CH4-C production. It does not modify production source, does not admit TCD-032, does not reopen TCD-033, and does not qualify N/P stoichiometry, CO2/subsidence output, `Rdas` timing, hidden task-local state, or historical runtime behaviour.

Base authority: `ANIMO-B3D40@83fedc7323cea6da696a81bc64e4e3b13d794880`.

Upstream scientific evidence: `ANIMO-GHG01@dac7b7b5c591b781b82ec968896edb5957664c88`.

Canonical allocation: `ANIMO-B3I01@383c7a83e84a578969f92113280dc715b7bdddb4:TCD-032`.

Current negative queue gate: `ANIMO-B3Q05@997d867a2b107ec8e28efce530c82a204719de46`.

Current aggregate: `ANIMO-RG05N@8758bd30e302b75dd7854ac00fd2e29473669a13`.

## Frozen source identity

Frozen revision-53 source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.

Relevant members:

- `ghgasses.for`: `4bf5906f571a586d4312d8e7b0d57f6df3b4b6c2073410335616f3d3c042da93`;
- `ghg_ch4.for`: `00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98`;
- `Rates.for`: `7a1a8aee4715d85b9b7e9e172f83756e4aee8b8278386c804210ef77dc2a857a`;
- `resp_miner.for`: `938d35c043bd3e1f14c20ec1c0b2395e9944beb2797746bc4e7cdfb38bb98106`.

GHG01 already establishes three source facts relevant here. First, `CH4produc` can draw CH4-C from DOM, exudates, humus/biomass and fresh organic-matter fractions. Second, `Rates2` contains an active DOM methanogenesis sink while the comprehensive `GHG_Miner` calls in `resp_miner.for` are commented out. Third, `GHG_Miner` itself describes methanogenesis mineralisation as analogous to ordinary mineralisation and contains source-family storage/mineralisation transfers, including the explicit note that DOM methanogenesis is handled through `Transca` via `Recfpddiorma`.

## Why direct reactivation is not the qualified policy

`GHG_Miner` is not admitted as an implementation recipe. Its task-1/task-2 design depends on cross-call local state, its calls are inactive, and its exact `Rdas`/assimilation timing is entangled with the ordinary mineralisation iteration. Reactivating it unchanged would also create a serious ownership question for DOM because `Rates2` already debits the DOM route. GHG03 therefore qualifies a transaction-level carbon identity rather than a call-level legacy implementation.

## Qualified carbon-transfer identity

For each CH4 source family `j` define:

- `Q_j >= 0`: the TCD-033-qualified source-family CH4-C production rate, kg C m-2 d-1;
- `dt > 0`: accepted timestep duration, d;
- `f_C > 0`: organic-matter carbon fraction, kg C per kg organic matter;
- `a_j` with `0 <= a_j < 1`: the accepted effective fraction of gross decomposed organic matter internally retained/transferred to humus/biomass rather than converted to CH4-C.

The gross organic-matter debit and matching internal humus/biomass credit are

`G_j = Q_j * dt / (f_C * (1-a_j))`

and

`I_j = a_j * G_j`.

The mandatory carbon identity is therefore

`f_C * (G_j - I_j) = Q_j * dt`.

For the humus/biomass source family, the bounded GHG03 policy uses `a_hu = 0`, matching the source form in which the humus CH4 term is a direct net mineralisation term rather than a gross-debit-plus-reincorporation pair.

For DOM, exudates and fresh-OM families, the workunit does **not** select how the effective `a_j` is computed from `Rdas`, `Asfaca`, `Asfaex` or `Asfa(Fn)`. It only requires that the accepted value be explicit to the transfer transaction and used exactly once.

## Ownership rules

1. Every positive `Q_j` has exactly one organic-C source owner debit.
2. Every internal incorporation amount `I_j` has exactly one matching humus/biomass credit.
3. DOM must not be debited once in `Rates2` and again by a second methanogenesis owner. A production implementation may retain the existing DOM route only if it is proven equivalent to the qualified `G_dom` debit and is paired with the same transaction's `I_dom` credit.
4. Exudate and fresh-OM source families require one source debit plus their matching internal credit when `a_j>0`.
5. The humus/biomass CH4 source uses a direct source debit with `a_hu=0` in this bounded policy.
6. `Q_j=0` implies `G_j=I_j=0`.
7. `a_j>=1`, `a_j<0`, `f_C<=0`, `dt<=0`, non-finite values or negative `Q_j` are outside the qualified domain and must fail closed.

Because B3D40 already admits the TCD-033 parent/daughter identity `sum_j(Q_j)=Q_total`, summing the qualified TCD-032 family transfers gives

`sum_j f_C*(G_j-I_j) = Q_total*dt`.

This is the bounded C-conservation bridge from organic source ownership to CH4-C production. It is not a whole-model C-balance claim: CH4 storage, oxidation, CO2 and atmospheric boundary fluxes remain separate control-volume terms.

## Oracle and adversarial controls

`tools/ghg03/tcd032_c_transfer_oracle.py` uses exact rational arithmetic, so no numerical tolerance is introduced. It covers zero transfer, zero incorporation, partial incorporation, high-but-bounded incorporation, multiple simultaneous source families and exact parent/daughter closure. Negative controls must detect both a duplicated DOM debit and a missing internal humus credit.

Counter-hypotheses retained for GOV05 review:

- CH4 production can be treated as diagnostic and need not debit organic source pools;
- the inactive `GHG_Miner` can simply be re-enabled unchanged;
- source pools can be debited only by `Q_j/f_C`, ignoring explicit internal incorporation semantics;
- DOM can keep its active sink while a second methanogenesis routine independently debits DOM again.

The qualification package is designed to reject all four.

## Hard boundaries

Historical revision-53 behaviour remains `UNKNOWN_WITHOUT_B2`. GHG03 creates no historical B2, no production source change, no TCD admission, no canonical register/queue mutation, no N/P transfer law, no `Rdas` timing rule, no hidden-state repair, no CO2/subsidence correction, no B4 opening and no production migration authority.
