# ANIMO-PREP02R — WUR Historical Artifact Request Draft

Status: `READY_FOR_HUMAN_SEND_NOT_SENT`.

## Contact evidence

Preferred institutional route:

- Leo Renaud is currently listed by WUR as an ANIMO expert and as the route for program-code/model-availability questions on the ANIMO product page.
- Leo Renaud's current WUR profile lists Sustainable Soil Use, Gaia building 101/C202, telephone `+31 317 486454` and secretary `+31 317 486669`.
- The supplied 2005 ANIMO 4.0 User's Guide gives historical address `leo.renaud@wur.nl` for program code/model availability. PREP02R has not independently proven from a current WUR page that this email address remains active.
- Piet Groenendijk is currently listed as an ANIMO expert. Current WUR material in 2026 still uses `piet.groenendijk@wur.nl`; this is a useful second contact for historical model/release context.

No message has been sent by PREP02R.

## New evidence that changes the request

On 2026-09-09, three additional artifacts were received:

- `animo41.sln`, SHA-256 `206dd6cc23b7d53c117131e16f15a22c4c97afc1c81febb3c73d789cdb9551f2`;
- `animo41.vfproj`, SHA-256 `f8ac40ea91df926a035396b0afe8584ea0d9c19711535a12b4f12634ce688b2a`;
- `animo41.exe`, SHA-256 `40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d`.

The project files materially improve the build-contract evidence. The executable, however, is demonstrably a modern x64 Debug rebuild: its PE timestamp is 2026-05-27, its PDB path is under `x64\Debug`, and embedded source paths include `src_develop_for_20260519`. It therefore cannot be treated as the missing historical release executable.

The request below is narrowed accordingly. Project settings are no longer the main gap. Historical behavioural provenance remains the gap.

## Suggested subject

`Historical ANIMO 4.1.x executable or executable-linked output for reference qualification`

## Suggested message

Beste Leo,

Voor een gecontroleerde modernisering van ANIMO probeer ik de historische gedragsreferentie van de ANIMO 4.1-lijn zo goed mogelijk vast te leggen. Ik wil daarbij nadrukkelijk niet een moderne reconstructie achteraf tot historische referentie verklaren.

De broncode die ik heb ontvangen is byte-voor-byte vastgelegd en identificeert zichzelf als:

```text
ANIMO 4.1.5
revision 53
Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]
```

Inmiddels heb ik ook een `animo41.sln`, `animo41.vfproj` en een `animo41.exe` ontvangen. De projectbestanden geven nuttige compilerinstellingen, maar de executable zelf blijkt een x64 Debug-build uit 2026 te zijn en is dus geen historische release-binary.

De oude testcases `CranGrass`, `CranMais`, `GrassPeat` en `RuurloGrass` verwijzen in hun runners naar `animo41.exe`. Voor wetenschappelijke referentiekwalificatie zoek ik daarom nog één van de volgende vormen van historische evidence:

1. een bewaarde ANIMO 4.1.5 revision-53 `animo41.exe`, liefst met informatie over release/build of bijbehorende bronversie;
2. een andere provenance-gekoppelde ANIMO 4.1.x executable waarvan versie/revision bekend is;
3. complete historische output van bijvoorbeeld `RuurloGrass` die aantoonbaar met een bekende ANIMO 4.1 executable is gemaakt;
4. een release- of archiefmanifest, buildlog of andere provenance-informatie waaruit blijkt welke executable bij de revision-53 of nabije 4.1.x bronlijn hoorde.

Daarnaast zou één provenance-bevestiging over de recent ontvangen projectbestanden al nuttig zijn: weet je of `animo41.vfproj`/`.sln` rechtstreeks uit de oude ANIMO 4.1 releaseomgeving stammen, of later zijn bewaard/omgezet voor modernere builds?

De huidige WUR-pagina biedt ANIMO nog als executable op aanvraag aan, maar de huidige overeenkomst noemt Version 4.0. Mijn vraag gaat daarom specifiek over eventueel bewaard historisch 4.1.x materiaal en niet over de huidige standaarddistributie.

Ik hoef een historische executable niet openbaar te maken. Als er distributiebeperkingen zijn, kan het bestand in gecontroleerde opslag blijven; voor de kwalificatie zijn hash, provenance en gecontroleerde uitvoering voldoende.

Er zit nog één provenance-detail in de ontvangen broncode: `Version.inc` noemt tag `animo4.1.5` revision 53, terwijl file-level SVN-keywords in de archive naar `tags/animo4.1.4` verwijzen. Dat kan stale keyword-expansie zijn, maar zonder release- of archiefinformatie wil ik daar geen conclusie aan verbinden.

Kun je aangeven of dergelijk historisch materiaal nog ergens bestaat, of wie binnen WENR mogelijk toegang heeft tot de oude ANIMO release- of SVN-archieven?

Met vriendelijke groet,

[naam]

## Why this wording is deliberately narrow

The request:

- incorporates the newly received project/build evidence instead of asking for artifacts already obtained;
- distinguishes the 2026 executable from historical behavioural truth;
- asks for historical evidence rather than the newest/current ANIMO distribution;
- does not ask the recipient to validate ANIMO5;
- does not state that the supplied archive is proven to be a homogeneous canonical SVN checkout;
- accepts controlled access instead of public redistribution;
- keeps a nearest provenance-qualified 4.1.x executable explicitly separate from revision-53 truth;
- asks a low-effort provenance question about the received `.vfproj`/`.sln`, which may strengthen lineage even if no old executable survives.

## Send gate

`HUMAN_SEND_REQUIRED`

Sending is an external action and is not part of the repository evidence update itself.
