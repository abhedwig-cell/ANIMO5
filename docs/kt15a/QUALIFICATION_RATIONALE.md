# ANIMO-KT15A Qualification Rationale

KT15 proved logical atomic publication, but a reproducible accepted state is insufficient if the configuration that gives that state meaning can silently change between intervals.

KT15A moves the interval-invariant configuration into the accepted application aggregate. Once initialized, interval execution can no longer receive an alternative load channel, calendar, producer-day mapping, declared boundary identity or top hydrology configuration.

The two-interval tests still exercise the KT15 atomic path, while additional tests verify invalid configuration is rejected before application initialization and that the exact accepted configuration is unchanged after multiple commits.

This is a runtime identity remediation only. The process equations and scientific scope are unchanged.

A positive qualification means:

`THE_BOUNDED_KT15_APPLICATION_STATE_CARRIES_THE_IMMUTABLE_EXECUTION_CONFIGURATION_REQUIRED_TO_INTERPRET_AND_CONTINUE_ITS_ACCEPTED_STATE`.

It does not mean the declared boundary SHA-256 has been cryptographically checked against source bytes.
