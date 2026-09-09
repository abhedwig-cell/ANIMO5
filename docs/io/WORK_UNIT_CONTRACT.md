# ANIMO-IO01 work-unit contract

Status target: `QUALIFIED_LEGACY_INPUT_CONTRACT_AND_TTUTIL_SUITABILITY_EVIDENCE`.

ANIMO-IO01 audits the revision-53 external input boundary. It does not redefine ANIMO science. The work unit separates three layers:

1. legacy parsing semantics, including labels, record ordering, tokenization, file routing and accept/reject behaviour;
2. normalization semantics, including explicit application of legacy defaults, aliases and conditional nullability;
3. scientific semantics, including units, parameter meaning, option meaning, process activation and state initialization.

TTUTIL may be used only in the first two layers. Scientific meaning comes from qualified ANIMO source, documentation and later scientific-admission work.

## Frozen evidence

- source archive SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- testbank SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`;
- supplied ANIMO 4.0 guide SHA-256: `ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301`.

Local source and testbank hashes were rechecked before source inspection. Frozen bytes were not modified.

## Authority anchors at work-unit start

- PREP01-05: `9df84bd0ab9bc4ef8e214f01da616aa257a24b13`;
- TQ01: `5c43ee16df37a0a1357614fdec527f25e5ca8c16`;
- ARCH05: `99b6098a19db405ce34928af89bb78b856dce7cd`;
- ARCH06: `ce3ea8089902dbc4bcbe3ff0224d30c2f8daf3a4`;
- ARCH07: `7e6f7bcb492cd36bf7a852235e93b796a6d2a8f6`;
- RG02 G5 branch head at start: `12ae76b23728d75fc6ca746ca1c67aa26e0ec005`.

No pre-existing `IO01` or TTUTIL branch/commit was found before reservation of this work unit.

## Hard boundaries

No frozen source or testcase modification. No scientific default, unit, parameter meaning or option meaning change. No parser relaxation may be called representation-only. No GHG schema blending. Unformatted hydrology remains a specialized exchange lineage. `INITIAL.out` and equivalent state files remain explicit state serialization, not ordinary configuration parsing. Final model-output equality is supporting evidence only and can never replace parser-level equivalence.

The pilot gate is separate from the audit gate. A successful audit does not imply a qualified TTUTIL runtime adapter and does not admit production migration.
