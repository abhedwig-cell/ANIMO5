# ANIMO-KT06 Reconciliation

KT06 begins from branch head
`3319e57adbf6036a86684f8e26d9559454c07b82`, which already contains the
closed ANIMO-KT05 compiled explicit-state hydrology call-boundary adapter.

This supersedes the separately authored experimental branch
`work/animo-kt05-explicit-state-runtime-adapter` as the programme sequence:
the compiled carrier is KT05; runtime binding is KT06.

Consumed authorities:

- KT02 runtime:
  `ANIMO-KT02@1f88db4dc87fc4d93075884ac35a59711f0725bf`;
- KT02 frozen executable:
  `1909709e7a244b5d0ee53342a26bab74815c118c`;
- KT03 typed hydrology contract:
  `ANIMO-KT03@c5d4c14fbd4ce77ed5ef369bb8ecaee0709ea3b8`;
- KT05 closeout:
  `3319e57adbf6036a86684f8e26d9559454c07b82`;
- KT05 frozen implementation:
  `69dd607ba1efa28de3f83cc963526021352b3311`.

KT03F01 is not consumed as qualified authority.

A user-supplied frozen LWKM Hlpimp=11 producer file provides bounded B1 contact
for the first interval metadata: endpoint 10 d, duration 10 d and explicit
`Sict=0 m`. The KT06 test uses those interval facts and LWKM dimensions but
uses synthetic finite values for the remaining HydrologyStep fields. It does
not claim full real-record payload equivalence.
