# ANIMO-KT08 Same-Agent Adversarial Review Notes

Review mode: `same-agent / not genuinely independent`.

Assurance: `PROCESS_SELF_REVIEWED_NOT_INDEPENDENT`.

First green implementation head reviewed:

`ca18712c0849ca1d3c5607df03abfcb5ee865230`

Exact-head CI:

`35291132020 -> SUCCESS`

## KT08-R1, medium: rematerializer did not reproduce committed anchor metadata exactly

The committed B1 summary assigns semantic `role` labels to its representative
anchors, but the raw-source rematerializer originally emitted the same anchor
indices and identities without those labels.

The scientific/evidence numbers were correct, and all three aggregate sequence
digests were independently pinned. However, a source rematerialization should
reconstruct the committed evidence artifact rather than a structurally similar
variant.

Disposition: remediate before closeout.

The materializer now owns the exact anchor-role map and emits the same role
labels as the committed summary. It also pins first origin, first endpoint and
minimum interception storage explicitly, in addition to the already pinned
aggregate sequence identities, duration histogram, final endpoint, nonzero
interception count and maximum interception storage.

## Evidence-boundary review

No runtime or scientific semantics are introduced. The materializer reads the
pinned legacy producer file, reconstructs each packet through the frozen KT03
adapter, validates each packet, requires explicit interception projection
capability and checks producer-coordinate continuity.

The aggregate sequence digests are compact commitments to all 1800 packets, not
a claim that CI contains the raw B0 file. CI validates the frozen B1 summary and
its independent pins. Raw-byte rematerialization remains an externally
reproducible step when the pinned B0 source is available.

KT06 is not consumed as qualified authority and its Tier C review gate is
unchanged.

## KT08-R1 completion check

A second parity inspection found one remaining non-scientific mismatch in the
same finding: the committed summary contained its workunit title while the
rematerializer omitted that descriptive field. The materializer now emits the
title as well. This does not alter any producer evidence, digest, packet value
or temporal claim; it completes exact artifact reconstruction for KT08-R1.
