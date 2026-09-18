# ANIMO-STATEQ08 Qualification Rationale

A two-step source-branch probe demonstrates the continuation hazard without inventing a tolerance.

Step 1 uses negative runoff, which deterministically assigns a nonzero `Runinu`.

Step 2 uses detailed-mode near-zero runoff. The source branch does not assign `Runinu`, so uninterrupted execution retains the prior value.

A split run that restores that value is bitwise identical at this branch. A split run that omits it diverges immediately. The same value also changes the run-in contribution to the upper-boundary solute load.

The probe is source-semantic evidence, not B2 historical runtime evidence.

The correct bounded conclusion is therefore that `Runinu` is continuation-critical for exact source-faithful detailed execution, while its canonical owner and any corrected deterministic near-zero rule remain unadmitted.
