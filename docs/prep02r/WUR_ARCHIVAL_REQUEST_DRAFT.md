# ANIMO-PREP02R — WUR Historical Artifact Request Draft

Status: `READY_FOR_HUMAN_SEND_NOT_SENT`.

## Contact evidence

Preferred institutional route:

- Leo Renaud is currently listed by WUR as an ANIMO expert and as the route for program-code/model-availability questions on the ANIMO product page.
- Leo Renaud's current WUR profile lists Sustainable Soil Use, Gaia building 101/C202, telephone `+31 317 486454` and secretary `+31 317 486669`.
- The supplied 2005 ANIMO 4.0 User's Guide gives historical address `leo.renaud@wur.nl` for program code/model availability. A 2007 OSPAR model inventory also gives `Leo.Renaud@wur.nl`. PREP02R has not independently proven from a current WUR page that this email address remains active.
- Piet Groenendijk is currently listed as an ANIMO expert. Current WUR material in 2026 still uses `piet.groenendijk@wur.nl`; this is a useful second contact for historical model/release context.

No message has been sent by PREP02R.

## Suggested subject

`Historical ANIMO 4.1.5 revision 53 executable / build archive for scientific reference qualification`

## Suggested message

Beste Leo,

Voor een gecontroleerde modernisering van ANIMO probeer ik eerst de historische gedragsreferentie van een oude ANIMO 4.1-lijn goed vast te leggen. Ik wil daarbij nadrukkelijk niet een moderne reconstructie of een GNU-build achteraf tot referentie verklaren.

De broncode die ik heb ontvangen is byte-voor-byte vastgelegd en identificeert zichzelf als:

```text
ANIMO 4.1.5
revision 53
Intel Visual Fortran Composer XE 12.1.0.233 [Intel(R) 64]
```

De meegeleverde historische testcases `CranGrass`, `CranMais`, `GrassPeat` en `RuurloGrass` verwijzen in hun runners naar `animo41.exe`, maar die executable ontbreekt. Ook de oorspronkelijke Visual Fortran projectbestanden en buildlog ontbreken.

Heb jij, of heeft WENR nog ergens in een historisch archief, een van de volgende zaken beschikbaar?

1. de ANIMO 4.1.5 revision-53 `animo41.exe`, liefst met informatie over release/build of de bijbehorende bronversie;
2. een oude `.vfproj`/`.sln`, buildlog, compiler- of linkercommandline, release-directory of gearchiveerde buildmachine/VM;
3. een complete historische output van bijvoorbeeld `RuurloGrass` die aantoonbaar met een bekende ANIMO 4.1 executable is gemaakt;
4. als revision 53 niet meer bestaat: de dichtstbijzijnde bewaarde ANIMO 4.1.x executable waarvan versie of revision nog bekend is.

De huidige WUR-pagina biedt ANIMO nog als executable op aanvraag aan, maar de huidige overeenkomst noemt Version 4.0. Daarom gaat mijn vraag specifiek over eventueel bewaard historisch 4.1.x materiaal, niet over de huidige standaarddistributie.

Ik hoef de executable niet openbaar te maken. Als er beperkingen op distributie zitten, kan het bestand in gecontroleerde opslag blijven. Voor de kwalificatie zijn een hash, provenance en gecontroleerde uitvoering voldoende.

Er zit nog één provenance-detail in de broncode dat historische buildinformatie extra nuttig maakt. `Version.inc` noemt tag `animo4.1.5` revision 53, terwijl file-level SVN-keywords in de ontvangen archive naar `tags/animo4.1.4` verwijzen. Dat kan eenvoudig oude/stale keyword-expansie zijn, maar zonder release- of buildinformatie wil ik daar geen conclusie aan verbinden.

Kun je aangeven of dergelijk historisch materiaal nog ergens bestaat, of wie binnen WENR mogelijk nog toegang heeft tot de oude ANIMO release- of SVN-archieven?

Met vriendelijke groet,

[naam]

## Why this wording is deliberately narrow

The request:

- asks for historical evidence rather than the newest/current ANIMO distribution;
- does not ask the recipient to validate ANIMO5;
- does not state that the supplied archive is proven to be a homogeneous canonical SVN checkout;
- accepts controlled access instead of public redistribution;
- keeps a nearest 4.1.x executable explicitly separate from revision-53 truth;
- gives the recipient several lower-effort alternatives if the exact executable is gone.

## Send gate

`HUMAN_SEND_REQUIRED`

Sending is an external action and is not part of the repository evidence update itself.
