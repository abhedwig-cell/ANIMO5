# ANIMO-B3B02 - HETOP=0 runtime reconciliation for TCD-042-B1

Date: 2026-09-09

Status impact: no change to the domain-refined B3B02 decision. The full parser-admitted trigger remains fail closed; the positive-`Hetop` exact-zero subdomain remains scientifically qualified.

This note adds executable evidence for the `Hetop = 0` domain discovered during B3B02 closeout. It does not admit a correction, does not change `SOIL.INP` grammar, and does not reserve a new TCD.

## Frozen identities

- source archive SHA256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- testbank SHA256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- ANIMO user-guide/documentation SHA256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`

The runtime probe reused the GNU diagnostic-build and testcase-adapter contracts already qualified as diagnostic tooling upstream:

- `tools/build_gnu_diagnostic.py`, blob `484a876f06926ab48d863383a28171936a4b09c6`;
- `tools/prepare_gnu_case.py`, blob `c85e37d3849f71aba9bd0b11d6357ad577016f75`.

Evidence class is `B0_HASH_PINNED_DIAGNOSTIC_EXECUTION_NOT_B2`.

## Parser and documentation boundary

Frozen `input1.for:1826-1829` accepts `Hetop = 0` because the declared lower bound is zero and `Checkrea` rejects only values strictly less than the lower bound.

The ANIMO user guide independently documents HETOP as the thickness of the virtual reservoir for fertilizer additions and gives range `[0.0 ... 0.2] m` in Table 6 for `SOIL.INP`.

No authoritative zero-thickness operational semantics were found in B3B02.

## Source-wide positive-HETOP dependencies

The exact-zero candidate is not the only code that requires positive `Hetop`.

Hash-pinned revision-53 source contains at least these divisions:

- `UBoundconc.for:114`: `P = St*Flux/Hetop` on the ordinary positive-flow branch;
- `Addit.for:361-370`: dissolved additions to the top reservoir divide by `Hetop`;
- `Uptpar_Grass.for:92,194`: `Help = Flab(1)/Hetop`;
- `Uptpar_Plant.for:110,283`: `Help = Flab(1)/Hetop`.

This already shows that defining `Hetop=0` inside TCD-042-B1 would silently solve a broader input/runtime contract problem.

## Executable Ruurlo zero-thickness probe

A GNU Fortran 14.2.0 diagnostic Ruurlo case was prepared from the frozen testbank. The only scientific-input change was

```diff
- 0.02 0.2
+ 0.0 0.2
```

at the `>profil:` HETOP/HE(0) pair in `Input/SOIL.INP`. Thus `Hetop` changed from `0.02` to `0.0` while `He(0)` remained `0.2`.

The adapted input hashes are:

- positive-HETOP baseline `SOIL.INP`: `97881a83a8da46c6ac28694bfc6e2a5540584b1af9d753603e66d1c4deb36da4`;
- zero-HETOP probe `SOIL.INP`: `10c03e7ceb99b2552d5ea04d97ab423c13db4199ca2c1f9aaf2f15f70bba813f`.

### Ordinary diagnostic execution

Executable SHA256:

`0cfb020136d58b1f03fb75db0ec166b3c5f05021b5020b96bd36a7e48056417e`

The positive-HETOP baseline emitted no textual NaNs in the checked output.

The zero-HETOP variant continued without an immediate hard stop but reported both `IEEE_INVALID_FLAG` and `IEEE_DIVIDE_BY_ZERO`. Its `initial.out` already contained 185 `NaN` values. This is numerical corruption, not a valid zero-thickness semantic result.

### Trap execution

A second diagnostic build added only instrumentation flags

```text
-g
-fbacktrace
-ffpe-trap=zero,invalid,overflow
```

Executable SHA256:

`981bce0cbdfd9119ab5696f1a49752826195835e6935b7c23fafe587ea092568`

The unmodified Ruurlo case with `Hetop=0.02` completed normally under the trap build.

The zero-HETOP variant terminated with `SIGFPE`, process return code `136`. The first trapped legacy source location was

```text
UBoundconc.for:114
P = St*Flux/Hetop
```

called from `Animo.for:517`.

The branch was the existing no-ponding ordinary positive-flow path, `Flpn=0` and `Flux>=1.0d-8`. Therefore the modified case fails in pre-existing legacy positive-flow algebra before the later exact-zero Ruurlo witness used by TCD-042-B1.

## Interpretation

The executable result materially sharpens the domain finding:

1. parser and documentation acceptance of `Hetop=0` does not establish a well-posed runtime configuration;
2. `Hetop=0` can fail in existing legacy behaviour independently of the proposed exact-zero Class-B correction;
3. the zero-thickness problem therefore spans input validation/runtime semantics beyond TCD-042-B1;
4. B3B02 must not insert an unqualified `Hetop>0` production guard or invent a no-reservoir policy;
5. the existing positive-`Hetop` TCD-042-B1 derivation and Ruurlo exact-zero evidence remain intact.

The probe does not prove that every possible `Hetop=0` configuration follows the same runtime path. It does prove that the parser-admitted zero value is not generally safe under frozen revision-53 and that a natural Ruurlo variant reaches a hard divide-by-zero in legacy code.

## Governance consequence

B3B02 remains:

`PARTIAL_TCD042_B1_CLASS_B_READINESS_HETOP_ZERO_DOMAIN_UNRESOLVED_ROUTE_AND_REVIEW_FAIL_CLOSED`

Qualified inside B3B02:

- exact-zero Class-B algebra for `Hetop>0`;
- conservation and expected-difference contract for that subdomain;
- natural Ruurlo mineral-N activation and negative controls;
- proof that zero-thickness semantics are broader than the TCD-042-B1 local correction.

Still fail closed:

- the full parser-admitted `Flpn=0 AND Flux=0` domain because `Hetop=0` has no qualified semantic treatment;
- any change to the HETOP input lower bound;
- any zero-thickness fallback or redirection policy;
- corrected-legacy admission;
- historical B2 route;
- GOV02 historical-uncertainty route;
- independent second-line review;
- production migration;
- parent TCD-042 admission.

No `TCD-043` is reserved. Any later intake of the HETOP parser/runtime mismatch must be classified separately rather than smuggled into the TCD-042-B1 algebra atom.
