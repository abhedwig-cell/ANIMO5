# ANIMO-KT07 Same-Agent Adversarial Review Notes

Review mode: `same-agent / not genuinely independent`.

Assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

First green implementation head reviewed:

`90f1c9ba240da681033b6392d0843ddb131b6ef3`

Exact-head CI:

`35288669987 -> SUCCESS`

The earlier head `f43a52d7f5e883ccf9f92570f1b34ee7004ac4d8`
failed only because `-Werror=compare-reals` rejected exact-copy test syntax.
That was a tooling/test-expression failure, not a fixture or adapter failure.

## KT07-R1, medium: typed-step digest was self-referential in CI

The integrity test recomputed the typed-step digest and compared it with the
digest stored in the same mutable fixture. A coordinated change to both the
payload and its stored digest could therefore pass CI even though the frozen
real-packet identity had drifted.

The source-file SHA and dynamic-group SHA were independently hard-coded, but
the normalized typed-step identity was not.

Disposition: remediate before closeout.

The exact expected typed-step digest
`eeeb862839cce8111535fae86220d8574240804b9f6f029f7ec8e07ceb65da1c`
is now pinned independently in both:

- the fixture integrity test; and
- the local raw-source materializer.

A later change in parser normalization or fixture values must therefore fail
closed instead of merely updating the digest alongside the payload.

## Remaining evidence boundary

The fixture is still B1 diagnostic/derived evidence. The raw source bytes are
not committed and CI cannot independently rematerialize them. Regeneration
requires the externally supplied file whose SHA-256 is pinned in the
materializer.

The generated Fortran fixture is produced from JSON decimals. It verifies that
the frozen KT05 compiled carrier accepts and projects the same values represented
by that B1 fixture. It does not establish Intel/compiler B2 equivalence.

No scientific, runtime, restart, numerical or production semantics are changed.
