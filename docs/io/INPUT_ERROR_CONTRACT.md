# Input error contract

The target is semantic accept/reject equivalence for the `LegacyRevision53TextAdapter`, not byte-identical error messages.

For every parser family a negative case records: input mutation, legacy expected class, target expected class, failure stage and whether the legacy behaviour itself is considered a quirk rather than a desirable native-schema rule.

## Required fail-closed cases

| Error class | Legacy-adapter rule | Native TTUTIL-schema rule |
| --- | --- | --- |
| missing required section/key | reject before physical execution | reject |
| malformed number | reject | reject |
| invalid option/range | reject using source-authorized bounds | reject using same scientific bounds for the same schema version |
| too few/too many rows | reject when cardinality is fixed or driver-dependent | reject |
| inconsistent cardinality | reject | reject |
| missing active conditional section | reject | reject |
| active-only field supplied while feature inactive | preserve family-specific legacy behaviour in legacy adapter; native schema should reject unless its version contract explicitly permits it | normally reject |
| unknown sequential ANIMO41 key | reject because next expected key mismatches | reject unknown key in native schema |
| reordered sequential ANIMO41 keys | reject in legacy adapter | native TTUTIL schema may define order-free behaviour, but that is a new representation and not legacy-equivalent |
| duplicate direct-file selector | preserve revision-53 last-assignment-wins semantics in compatibility mode and report provenance | native schema should reject duplicates |
| unknown direct-file selector | preserve observed ignore behaviour only in exact legacy mode; surface diagnostic | native schema should reject |
| duplicate `Findadr` section | preserve first-occurrence-wins if exact legacy compatibility is claimed | native schema should reject |
| GHGMais under revision-53 adapter | reject as lineage mismatch | only accept under separately identified versioned adapter after provenance closure |
| binary hydrology passed to TTUTIL text adapter | reject as wrong adapter class | reject |
| restart/state file passed to ordinary config adapter | reject as wrong owner/adapter class | reject |

## Failure stage

Parser/schema failures must occur before creation of an executable physical trial. No invalid-data fallback may cross the kernel boundary. A normalized-object constructor may only run after lexical parsing and structural schema checks succeed.

A legacy default is not an error fallback. It is allowed only when the revision-53 source demonstrably defines that default for the exact condition and when the normalized dump records the default rule id.

## Range checks

The supplied ANIMO 4.0 guide is useful for units and expected ranges, but it also states that code-side checks can be wider than the guide's indicative ranges. Therefore source checks, not the printed indicative range alone, govern revision-53 accept/reject evidence. A future native schema may choose tighter validation only through a separately admitted contract change, not under representation-only qualification.
