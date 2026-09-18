# ANIMO-KT15A Work Unit Contract

Workunit: `ANIMO-KT15A - Immutable Application Configuration Binding Remediation`.

KT15A remediates one coherence gap discovered after KT15 qualified logical atomic publication.

## Finding

KT15 kept science state and cross-module continuation inside the accepted application aggregate, but interval-invariant execution configuration was still supplied anew on every call:

- runtime calendar contract;
- producer day offset;
- top-layer hydrology geometry/partition parameters;
- declared boundary content SHA-256;
- simulation start year;
- selected TCD-042 load channel.

That meant a caller could legally drive generation N and generation N+1 with different configuration arguments while the accepted application state itself carried no identity proving which configuration governed the run. This is incompatible with robust checkpoint/restart identity.

## Remediation

KT15A introduces a private-component `kt15_application_config_t` and stores it inside `kt15_application_state_t`.

The configuration contains:

- runtime calendar contract id;
- producer day offset;
- `he_top`, `lefrrv`, `lefrso`;
- declared canonical lowercase 64-character boundary content SHA-256;
- simulation start year;
- legacy load channel.

The configuration is created once, validated, bound to the accepted state's calendar, copied with the application aggregate and no longer supplied to each interval execution.

## Runtime rule

`execute_kt15_atomic_interval` receives only:

- accepted application state;
- selected hydrology packet;
- endpoint time;
- interval execution id;
- boundary chemistry object.

Every interval-invariant configuration coordinate is read from the accepted application's immutable configuration.

This prevents accidental parameter drift between accepted generations.

## Boundary-content limitation

The SHA-256 is a declared identity already governed by BOUNDQ02B.

KT15A does not hash the source file and cannot prove that a caller supplied chemistry matching that declared digest. Source-byte verification remains outside scope.

## Equality

Configuration equality is exact:

- identifiers and integers compare exactly;
- binary64 hydrology configuration fields compare by bit identity.

No tolerance is introduced.

## Checkpoint consequence

KT15A makes future checkpoint materialization structurally possible because the accepted application aggregate now contains the configuration identity needed to interpret its continuation.

It does not itself define a checkpoint schema or persistence format.

## Authorities

- `ANIMO-KT15@d3a51aad084969a753cb5b54c604ebefba4b26c6`, exact-final CI run `35375951746 -> success`;
- `ANIMO-STATEQ11@c2bd0d17ac6921fcd9f22d6289a510cae454153d`;
- `ANIMO-BOUNDQ02B@de6eef3122354e74405ff9c92286794714bdee82`;
- `ANIMO-KT14B@46e9e7397be751f245069033bae655b4382b63bd`;
- program authority `ANIMO-RG06@8efdd151d89e1cff131d4b21e2acf559ca1828d6`.

## Hard boundaries

No source-byte hash verification.
No boundary chemistry parser change.
No new hydrology science.
No TCD-042 change.
No first-call Runinu rule.
No canonical state admission.
No checkpoint schema admission.
No B3 mutation.
No TB7.
No B4.
No production.
No Status A or AA.

## Governance

This changes cross-module accepted application identity and therefore remains a GOV04 Tier D candidate. Same-agent review is not independent admission.
