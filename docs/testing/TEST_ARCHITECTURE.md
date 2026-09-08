# ANIMO5 test architecture baseline

## Test levels

- `UT`: unit test
- `CT`: contract test
- `IT`: integration test
- `INV`: invariant test
- `RR`: reference regression
- `QG`: qualification gate

## Cost classes

- `FAST`: cheap developer checks
- `FOCUSED`: bounded component/work-unit checks
- `BROAD`: wider regression/integration checks
- `QUALIFICATION`: pinned, evidence-producing admission gates

## Expected-value provenance

Every numerical expectation must declare one of:

- `ANALYTICAL`
- `THEORY`
- `FROZEN_LEGACY`
- `CORRECTED_LEGACY_REFERENCE`
- `QUALIFIED_GOLDEN_CASE`
- `INVARIANT`
- `UNKNOWN`

`UNKNOWN` expectations may be captured for investigation but may not silently become qualification oracles.

## Traceability chain

```text
requirement/invariant
  -> test id
  -> exact source commit
  -> input/evidence identity
  -> result artifact
  -> qualification decision
```

## PREP01 tests

PREP01 only admits evidence-integrity checks:

- archive SHA-256 identity;
- member manifest reproducibility;
- testcase count and steering inventory;
- unresolved path references reported without assuming mandatory semantics.

No `RR` or `QG` testcase is qualified yet because executable/source and trusted expected outputs are unavailable.
