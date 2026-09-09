# TTUTIL 4.27 source provenance checkpoint

## Purpose

This note records the source-provenance state for the TTUTIL dependency considered by ANIMO-IO01. It does **not** admit a TTUTIL-backed ANIMO adapter and it does not alter any frozen ANIMO B0 material.

## Official SWAP/WUR distribution evidence

The Wageningen SWAP download page states that SWAP uses TTUTIL and that the TTUTIL source is included in the latest SWAP download. The current development release is SWAP 4.3.1 (June 2026).

Official SWAP pages used for this checkpoint:

- https://swap.wur.nl/downloads.html
- https://swap.wur.nl/faq.html
- https://swap.wur.nl/DownloadRecentDevelopment/swap4.3.1/form.html

The SWAP FAQ identifies TTUTIL427.LIB as distributed under LGPL 2.1 in the SWAP distribution.

A previously supplied official SWAP 4.3.1 development source package in the project was pinned as:

- package: `SWAP_4.3.1.zip` / previously supplied copy `SWAP_4.3.1(6).zip`
- SHA-256: `2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`
- bundled TTUTIL baseline: 4.27
- previously audited TTUTIL source extent: approximately 153 Fortran source files

The current chat runtime does not expose the bytes of that previously supplied ZIP, so the bundled TTUTIL subtree cannot yet be extracted and re-hashed here.

## WUR download boundary

The current SWAP 4.3.1 download is behind the WUR registration form. The form requires an e-mail address, country selection and explicit acceptance of the license agreement. This workunit must not invent registration details or silently accept a license agreement on behalf of the user.

Consequently, the official package identity is known, but a fresh server download was not executed from this chat.

## Public `SWAP-model/ttutil` repository

A public repository exists at:

- repository: `SWAP-model/ttutil`
- inspected commit: `bd8601dca3cfb449a79accddd39a566811f1a75e`
- source version declared by `ttuver.for`: 4.27
- build metadata version: 4.2.7
- source tree: 153 Fortran files in the build list

Its current source tree is unchanged from its initial import commit `0703e930274b603a09aed3b3407b064004147886`; the initial commit says it was created to separate TTUTIL for SWAP distribution/build automation.

However, the repository README explicitly calls the repository **unofficial**. It is therefore a useful candidate mirror and transport/reference source, but it is **not** being treated as a substitute for the official SWAP/WUR distribution without byte-level equivalence evidence.

The repository also carries a historical TTUTIL license text that is not worded identically to the current SWAP FAQ licensing statement. This is another reason not to collapse mirror provenance into official-distribution provenance.

## Qualification consequence

ANIMO-IO01 can now pin:

1. the official SWAP distribution identity;
2. TTUTIL version 4.27 as the bundled baseline;
3. the public mirror commit as a non-authoritative candidate source;
4. the current public licensing statements.

ANIMO-IO01 still cannot claim `QUALIFIED_REPRESENTATION_ONLY_TTUTIL_ADAPTER_CANDIDATE` until one of these fail-closed conditions is met:

- the official `SWAP_4.3.1` package bytes are made available again, the package SHA-256 matches `2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360`, and the bundled TTUTIL 4.27 subtree is extracted and individually manifested; or
- independent byte-level evidence proves that the candidate mirror source tree is identical to the TTUTIL subtree in that official package.

No TTUTIL source is vendored into ANIMO5 by this checkpoint. No parser behaviour is changed. No production migration is admitted.
