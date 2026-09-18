# ANIMO-KT13 Qualification Rationale

KT13 is the first executable composition in which a selected hydrology packet can drive a bounded piece of real ANIMO science through the new transaction runtime.

The composition deliberately reuses KT06 as the binding authority rather than reproducing its time-mapping semantics. It then uses the exact KT05 projection function, the bounded source-derived HYDROEXEC01 equations, the typed HYDROQ01/HYDROQ02 outputs, the source-derived UBFORCE02 load resolver and the already B3-admitted TCD-042 algebra in KT12.

The external accepted TCD-042 state is modified only by KT02 after a successful science attempt.

The workunit also demonstrates why STATEQ08 matters operationally. On the detailed near-zero runoff branch, caller-provided `Runinu` can alter both the resolved upper hydrology and the upper solute load. KT13 therefore accepts this continuation explicitly. It does not hide the dependency or choose a first-call value.

Positive qualification would mean:

`A_SELECTED_KT05_HYDROLOGY_PACKET_PLUS_EXPLICIT_START_AND_CHEMISTRY_CONTEXT_CAN_DRIVE_ONE_BOUNDED_TCD042_INTERVAL_TO_AN_ATOMIC_KT02_COMMIT`.

It would not mean:

- the KT11 multi-packet provider is yet wired directly into this orchestrator;
- multi-interval hydrology continuation is solved;
- canonical Runinu state/restart ownership is admitted;
- the Tier D composition is independently reviewed or admitted;
- production is open.
