# Source provenance keyword audit

Status: `ARCHIVE_IDENTITY_PINNED_INTERNAL_SVN_METADATA_HETEROGENEOUS`.

This audit concerns only provenance metadata embedded in the supplied source archive. It does not alter any source file and does not infer behavioural differences from version strings alone.

## Archive identity

- archive: `ANIMO_4.1.5.53(3).zip`;
- SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`;
- files: 65.

`Version.inc` contains:

```text
Rcstemp='file:///V:/svn_Animo/tags/animo4.1.5'
Rcsrev='53'
Built='Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]'
```

This remains the strongest archive-level self-identification available in PREP01.

## File-level SVN keyword inventory

A source-wide static scan found:

- 55 files containing an `$Id`-style keyword string;
- 53 `$Id` strings with a parseable numeric revision and date;
- 53 files containing `$HeadURL`;
- all 53 observed `$HeadURL` values point to `file:///V:/svn_Animo/tags/animo4.1.4/...`, not `animo4.1.5`.

The parseable `$Id` metadata ranges from revision 7 to revision 53 and from 2013-02-28 through 2016-08-26.

Examples:

```text
input1.for
  $Id: input1.for 53 2013-06-04 10:23:17Z renau001 $
  $HeadURL: file:///V:/svn_Animo/tags/animo4.1.4/input1.for $

Input_addit.for
  $Id: Input_addit.for 46 2013-06-03 14:45:20Z renau001 $
  $HeadURL: file:///V:/svn_Animo/tags/animo4.1.4/Input_addit.for $

Animo.for
  Rcsid='$Id: Animo.for 41 2016-08-26 15:14:46Z renau001 $'
  Rcstemp='$HeadURL: file:///V:/svn_Animo/tags/animo4.1.4/Animo.for $'
```

The two supplied `input1.for` variants carry the same revision-53/2013-06-04 `Id` and the same `animo4.1.4` HeadURL, despite differing source content.

## Interpretation boundary

This metadata establishes **internal provenance heterogeneity**. It does not establish which of the following explanations is correct:

- a 4.1.5 package assembled from a 4.1.4-tag working copy plus later files;
- stale SVN keyword expansion retained during a later release/export;
- a manually assembled maintenance snapshot;
- another release procedure not represented in the supplied evidence.

PREP01 must therefore distinguish:

- **byte identity of the supplied archive**, which is fully pinned;
- **archive self-identification as 4.1.5/revision 53**, which is observed;
- **exact homogeneous SVN tag provenance**, which is not yet proven.

No source filename, keyword or version string is normalized or rewritten.

## GHG testcase relevance

The GHG source files contain implementation comments dating the process work to 2007/2008 and file-level SVN metadata from 2013. The supplied `GHGMais` material file reports creation on 2010-06-17 and uses an input schema that does not match the supplied revision-53 `input1.for` parser.

Those dates are consistent with the testcase potentially belonging to a different development-stage input contract, but dates alone do not identify the exact matching source revision. The testcase remains a provenance blocker rather than being translated to fit the supplied parser.

## Qualification consequence

The immutable B0 baseline may safely be defined as **the exact supplied archive bytes** once controlled retention is resolved. Calling that B0 an exact canonical SVN `animo4.1.5` checkout would require additional evidence.

Reference-build qualification should therefore record both:

1. the archive SHA-256 and per-file hashes;
2. the unresolved archive-versus-SVN-keyword lineage discrepancy.
