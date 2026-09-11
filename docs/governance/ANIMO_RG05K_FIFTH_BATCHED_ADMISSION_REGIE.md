# ANIMO-RG05K — Fifth Batched B3 Admission Integration

Source aggregate: `ANIMO-RG05J@624bbad35add93de29ac89649155d9fa086a73af`.

This is central-regie aggregation only. It does not repeat scientific admission, change production source, modify frozen B0, open B4 or authorize migration.

The normal GOV04 batching threshold is reached by three exact-final post-RG05J admissions:

- `ANIMO-B3D28@ce602528d075fc962b0b78759ed0082d1ec78a51`: `TCD-025-A1` bounded water ledger;
- `ANIMO-B3D29@97fd3274acd47bac74939d9dbd55b908043d1521`: `TCD-025-A2` bounded DOM ledger;
- `ANIMO-B3D30@5da4e4f38ca94630ff857deb66e86f974425f30c`: `TCD-025-A3` bounded N ledger with DON/NH4/NO3 identities preserved before aggregation.

All three are GOV05 Tier-C child admissions with historical uncertainty. Their same-agent reviews are explicitly `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

`ANIMO-B3I08@f4a3056087e5f7bac41b243be1f404739cde52b0` is now the current routing authority for the TCD-025 child partition. It defines A1-A4 as bounded candidates under the B3A10/MASSQ03 selected-profile predicate and A5 as the unresolved partial-saturated-reservoir blocker.

RG05K integrates A1-A3 only. A4 remains unadmitted. A5 remains `BLOCKED_NOT_SOURCE_CLOSED`. Parent TCD-025 remains unadmitted and must not be auto-admitted from child completion. No new top-level discrepancy is reserved and canonical top-level tail remains TCD-042.

Post-integration scientific admission count is 20, all with historical uncertainty, with zero normal-B2-route admissions. The top-level admitted TCD count remains 13. The admitted child-atom count becomes 7: TCD-037 A1-A4 plus TCD-025 A1-A3.

B3 remains incomplete. B4 and production remain closed.
