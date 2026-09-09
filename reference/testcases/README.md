# ANIMO testcase evidence

PREP01 analysed the supplied `ANIMO_testbank.zip` byte-for-byte and persists its exact archive identity and member-level manifest here. The binary ZIP itself is **not** stored in GitHub by PREP01 because the chat GitHub connector does not expose a byte-exact local-file upload path. This is a recorded blocker, not a completed freeze.

Archive identity:

- size: 7,659,314 bytes
- SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- files: 119
- testcase directories: 9

PREP01 found nine testcase directories. All nine contain an `animo.ini` identifying `Animo41`. Five contain Windows runner scripts that call either `..\animo41.exe` or `ANIMO` from PATH. No ANIMO executable is present in the supplied package.

All nine `Output/` directories are empty. Two cases contain an `initial.out` inside their input area, but PREP01 does not assume these are trusted expected results. They may be restart or carry-over state files.

Six cases contain one or more `animo.ini` path references for which no matching file is present in the package. Whether these paths are mandatory is `NOT_ASSESSED` because source/parser semantics are unavailable. Examples include `WAI`, `WAU`, `CHE`, and `CRU` entries.

When the original archive is available locally, run:

```text
python tools/audit_testbank.py /path/to/ANIMO_testbank.zip \
  --json reference/testcases/testbank_inventory.json \
  --manifest-csv reference/testcases/testbank_manifest.csv \
  --cases-csv docs/prep01/TESTCASE_INVENTORY.csv
```

The audit is an integrity/inventory check only. It is not a scientific testcase qualification.
