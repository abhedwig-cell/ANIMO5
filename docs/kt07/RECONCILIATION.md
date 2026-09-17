# ANIMO-KT07 Reconciliation

KT07 branches from canonical KT05 closeout
`3319e57adbf6036a86684f8e26d9559454c07b82`.

It deliberately does not branch from or consume KT06 as qualified authority.
KT06 is still behind a GOV04 Tier C independent-review gate. KT07 is the safe
parallel evidence/tooling action explicitly allowed by the KT06 checkpoint.

No equivalent KT07 branch existed at workunit start.

The user-supplied frozen LWKM testbank provides the B0 source bytes outside the
repository. Their SHA-256 matches the KT03 frozen envelope:
`b48c6aaac1c3bdcac8883f227346a22eb97e60df0997f09080fa0fac9118c34c`.

Local materialization through the frozen PowerStation framing parser and KT03
typed adapter produced:

- Hlpimp=11;
- 30 layers;
- 30 horizons;
- 5 drainage systems;
- active soil temperature;
- first dynamic group: 13 logical records;
- group SHA-256
  `2e5e8ff7c088ddd94f91aeb663ea10abdecfda0ac4cd418a8bf90be955389ec7`;
- endpoint 10 d;
- duration 10 d;
- explicit interception storage endpoint 0 m;
- normalized typed-step digest
  `eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c`.

These are B1 derived/diagnostic facts. They do not promote the legacy
normalization path to B2 historical executable truth.
