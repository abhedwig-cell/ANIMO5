# TCD-042-E1 independent numerical review handoff

Work unit: `ANIMO-NQ03`

Review target: `NQ03_RESTRICTED_NATURAL_ENVELOPE_QUADRATIC_DIMENSIONLESS_POLICY`.

This handoff is for independent numerical review only. It authorizes no production patch and no B3, parent-TCD or corrected-legacy admission.

## Reviewer must independently verify

1. Reconstruct `Hetop*dC/dt = Load - Flux*C` and the exact positive-flow end-state and time-average coefficients without using the NQ03 implementation as the authority.
2. Confirm that `P=St*Flux/Hetop` is the correct conditioning coordinate and that a raw Flux threshold is insufficient to characterize cancellation.
3. Reproduce the UBQ02 natural envelope pin: `4.2351647362715017e-20 <= P <= 3.8510200002999744e-7`, with 1,238 finite-positive records across six traced cases.
4. Reproduce a high-precision reference for `f=(1-exp(-P))/P` and `g=(P-1+exp(-P))/P^2` using an implementation independent from the candidate polynomial.
5. Confirm that raw nested binary64 evaluation is numerically unacceptable and that `expm1` fixes `f` but does not by itself fix the second-order cancellation in `g`.
6. Re-derive the alternating-series remainder bounds. In particular, verify that degree 1 is not below binary64 unit roundoff at the observed P maximum, while degree 2 is.
7. Challenge the selection of degree 2 as the minimal canonical order for the restricted natural envelope. A higher order may be mathematically valid, but should not be preferred without a numerical reason.
8. Reproduce the binary32 sensitivity axis and confirm that NQ03 does not admit binary32 as canonical policy.
9. Re-derive the conservation identity `C1-C0=Lbar-P*Cavg` and independently inspect the persisted conservation probe. Do not turn the observed residual into an acceptance tolerance.
10. Check the equal-subinterval semigroup test and confirm that the reported differences are consistent with binary64 operation accumulation rather than a timestep-dependent model change.
11. Verify the one-sided limit `P -> 0+`: `A1->1`, `A2->St/Hetop`, `B1->1`, `B2->St/(2*Hetop)`. Confirm that this matches UBQ01 but does not reopen or redefine TCD-042-B1.
12. Confirm that events with `P>3.8510200002999744e-7` are outside the NQ03 qualification. The observed upper envelope is not a physical validity threshold and must not silently become one in production.
13. Confirm branch scope: no production source, canonical TCD register, B3 admission record or TCD-042-B1 artifact may be modified by NQ03.

## Evidence pins

- B3I05 start head: `7fa0162415e02a6f0167e71b48ae38177a9e06e0`.
- UBQ02 qualified head: `bb572bb5d431f91d780018a1acbb345fbcfced37`.
- UBQ02 characterization blob: `b65a0d05d9a314e8d6dcecc008ee6e4eaa2ba321`.
- UBQ01 boundary head: `6895b67799f26888025eced7188e7190b2a0d07d`.
- Frozen source SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`.
- Frozen testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

## Review outcome vocabulary

Use one of:

- `INDEPENDENT_REVIEW_PASS_RESTRICTED_POLICY`;
- `INDEPENDENT_REVIEW_REQUIRES_REVISION`;
- `INDEPENDENT_REVIEW_FAIL_POLICY_NOT_SUFFICIENTLY_UNIQUE_OR_SUPPORTED`.

A review pass is still not B3 admission or authorization to modify production code.
