# ANIMO-B3D41 — TCD-032 Methanogenesis Carbon-Transfer Ownership Atomic B3 Admission

This workunit performs only the separate B3 admission decision for the bounded scientific identity qualified by `ANIMO-GHG03@9614e4a4733573c865aeece9f5b33628cbc7ee2d`.

Target: canonical top-level `TCD-032`.

Candidate admitted identity:

`TCD032_SINGLE_OWNER_METHANOGENESIS_C_TRANSFER_WITH_GROSS_DEBIT_INTERNAL_CREDIT_AND_NET_QJ_DT_CLOSURE`

The admitted scope is carbon only. For each TCD-033-qualified source-family methane production rate `Q_j`, accepted timestep `dt`, organic-matter carbon fraction `f_C`, and explicit effective internal-retention fraction `0<=a_j<1`, the scientific transfer contract is:

`G_j = Q_j*dt/(f_C*(1-a_j))`

`I_j = a_j*G_j`

`f_C*(G_j-I_j)=Q_j*dt`.

Humus/biomass uses `a_hu=0`. Every positive source-family methane transfer has exactly one source debit owner and every nonzero `I_j` has one matching internal humus/biomass credit. A duplicated DOM debit is forbidden. The TCD-033 parent/daughter identity remains a separate already-admitted dependency and is not reopened.

Historical revision-53 active-GHG behaviour remains `UNKNOWN_WITHOUT_B2`; the admission therefore uses the GOV03 historical-uncertainty route and GOV05 Tier-C same-agent adversarial review. The review is explicitly not genuinely independent.

Out of scope: production source, N/P transfer stoichiometry, `Rdas`/`Asfa` timing or construction, hidden task-state repair, CO2/subsidence accounting, whole-model C-balance closure, B4 and production migration.

Post-RG05N cadence: B3D40/TCD-033 is the first exact-final admission after RG05N. If B3D41 becomes exact-final green, TCD-032 is the second. The normal three-admission threshold is therefore not yet reached and RG05O must not be opened solely by this admission.
