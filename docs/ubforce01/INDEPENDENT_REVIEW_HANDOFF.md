# ANIMO-UBFORCE01 Tier D Review Handoff

Independent review should verify:

1. ARCH05 separation of hydrology and solute composition is preserved.
2. IO01 does not already qualify BOUNDARY migration.
3. the detailed `UBoundconc` source mapping for Load1 through Load6 is exact at the pinned source identity;
4. the carrier represents already-resolved loads only;
5. dry deposition is correctly excluded as a separate state pulse;
6. optional phosphorus channels follow `Ipo=1` presence;
7. the unit derivation is dimensionally consistent with pinned KT03/IO01 units;
8. interval and forcing-execution provenance are explicit;
9. no parser, raw load resolver, B3, B4 or production authority is created;
10. hydrology is not promoted to chemistry owner.

Same-agent assurance is only `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.
