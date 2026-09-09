# Synthetic testcase evidence policy

Work unit: `ANIMO-TQ01`

Synthetic cases and controlled descendants are permitted only as diagnostic evidence. They never become B0 historical testcase bytes and never become B2 historical reference merely because they are deterministic.

## Permitted uses

A synthetic or transformed case may support:

- **branch reachability**, by making a source predicate true and instrumenting the selected path;
- **conservation identity tests**, when the pre-state, post-state and explicit transfer terms define a closed local identity;
- **causal defect proof**, through a minimal one-factor change with observer/non-interference controls;
- **non-interference**, by proving that an observer or correction candidate leaves unrelated outputs or state unchanged within the declared comparison contract;
- **bounds/index testing**, by selecting site counts, layer counts, boundary values or option combinations absent from the historical testbank.

Every transformed case must record its parent B0 member identities, exact transform, transform/tool hash where available, purpose, expected changed path, and evidence class. Frozen input bytes remain untouched.

## What synthetic evidence does not prove

It does not prove:

- that the historical executable produced the same behaviour;
- that the synthetic state is naturally reachable or representative;
- parameter realism or case prevalence;
- scientific correctness of a candidate formula merely because a conservation test closes;
- a numerical acceptance tolerance;
- B2 reference status;
- B3 admission;
- production suitability or B4 admission.

Large or small synthetic magnitudes are diagnostic observations only. They must not be converted into acceptance thresholds without a separate numerical/scientific qualification.

## Admission labels

Use `SYNTHETIC_DIAGNOSTIC_ONLY` for branch and causal evidence. If a synthetic descendant is derived from a historical case, retain both identities explicitly; do not call the descendant a historical testcase. A later B3 argument may cite synthetic evidence as supporting evidence only alongside the required provenance, theory/conservation argument and discrepancy disposition.
