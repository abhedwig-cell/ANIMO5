# ANIMO-BOUNDQ02 Frame Integrity Remediation

The first BOUNDQ02 qualification candidate passed its substantive compiled tests, but its interval-frame validator was too weak for downstream composition use.

The frame carried exact interval identity and chemistry, but a caller could mutate selected year/slot provenance, the UBFORCE02 forcing identifier or dry-deposition values after construction without the public frame validator detecting the inconsistency.

The pre-remediation freeze and same-agent review are therefore superseded.

The remediated frame now persists:

- simulation start year;
- BOUNDARY year count;
- selected source year and slot;
- exact origin and endpoint;
- boundary source identity;
- chemistry forcing identity;
- separate dry-deposition values.

Validation now fails closed unless:

- selected year equals `simulation_start_year + selected_slot - 1`;
- selected slot is inside the recorded BOUNDARY year count;
- the UBFORCE02 forcing identifier equals the deterministic boundary-source plus slot identity;
- the chemistry object reconstructs successfully through the UBFORCE02 constructor;
- dry-deposition values are finite;
- exact origin and endpoint match the expected interval.

This is a provenance/coherence repair only. It changes no source year-selection rule, chemistry value, scientific equation or production authority.

Requalification, refreeze and restarted review are required from the remediated head.
