# ANIMO-KT04 Reconciliation

KT04 starts from the exact KT03F01 closeout head `0bd8e3f2fe84837e85c45c44ec2e8201f81cef12`. Its closeout workflow run `35283894975` completed successfully.

The predecessor chain is now coherent:

`KT02 model-neutral runtime -> KT03 file-independent HydrologyStep -> KT03F01 Hlpimp=1 absent interception-state disposition -> KT04 guarded downstream projection`.

KT04 does not reopen the KT03 payload schema. It adds a separate projection layer so the scientific distinction between "state absent" and "state explicitly supplied" survives into downstream transformation.

The first implementation head `7111ebc969fff927240a3c5532a2e322402814c9` passed exact-head CI run `35284103015`. Adversarial pre-close inspection identified two contract-hardening items: the projection carrier must be structurally immutable, and a typed provider must present a pinned semantic authority rather than a free policy string. Both are remediated before review.

## Supplementary supplied build artifacts

Additional user-supplied local artifacts were inspected during reconciliation:

- `animo41.vfproj` SHA-256 `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`;
- `animo41.exe` SHA-256 `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`.

The project declares `LocalVariableStorage="localStorageSave"` in all four configurations. Only `Debug|x64` explicitly declares `LocalSavedScalarsZero="true"`; the other three configurations do not explicitly set that property, so no false/default value is inferred for them.

The supplied executable embeds the PDB path `D:\USR\5200048928_SWAP_ANIMO\ANIMO\x64\Debug\animo41.pdb`, is PE32+ x86-64, and carries a 2026 linker timestamp. This is consistent with the supplied Debug|x64 project profile.

This evidence is supplementary only. The executable is a modern rebuild, not a recovered revision-53 historical reference. KT04 therefore does not use it to replace the KT03F01 scientific/source disposition or to claim B2 historical behaviour.

Current phase: `QUALIFY`.
