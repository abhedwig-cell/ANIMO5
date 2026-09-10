# ANIMO-B3A01E — TCD-027 Frozen-B0 source evidence remediation

## Decision boundary

This workunit remediates source-evidence availability only. It does **not** perform the independent second-line re-review, does **not** change the ANIMO-B3A01R semantic result `INCOMPLETE`, does **not** apply the TCD-027 candidate correction, and does **not** admit TCD-027.

Base review authority: `ANIMO-B3A01R@510c9313926457cd9bfd8e71a551255297bdfbb3`, validated by GitHub Actions run `34451443377`. Formal route authority remains `ANIMO-B3D10@a7b11b334f8b2604d5036edc04365006800944e0` under `ANIMO-GOV03@cbd262bdabe92923113b7326f2f42822ce9a971c` and `ANIMO-B3Q01@846e0f4d02a38b9e02cc1419b1ca87e63aaedb54`.

ANIMO-B3A01R stopped `INCOMPLETE` because a GitHub-only reviewer could not independently inspect three exact frozen-source neighbourhoods: the local construction/meaning of `Dum` at TCD-027, the exact `Outbal_write.for` slot-24 through slot-27 mapping statements, and the exact organic-P slot-25/26/27 self-accumulator statements. B3A01E makes those exact frozen source bytes available for a new independent review. It does not reinterpret the old review into PASS.

## Frozen-B0 provenance

The uploaded source archive used for extraction was checked before extraction:

- display name: `ANIMO_4.1.5.53(3).zip`
- SHA-256: `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`
- size: `350696` bytes
- ZIP entries: `66`

The uploaded testbank identity was also rechecked as B0 context, but it was not used to derive these source excerpts:

- SHA-256: `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`
- size: `7659314` bytes

The exact reviewer-required source neighbourhoods are persisted inside `TCD027_FROZEN_B0_SOURCE_EVIDENCE_MANIFEST.json` as RFC 4648 Base64 of their unmodified CRLF-preserving bytes. Full source members are deliberately not duplicated in the repository; their archive-member SHA-256 and ZIP metadata are pinned as provenance identities:

- `ANIMO_4.1.5.53/Outbal_calc.for`: `4dc26a4b8a02896b26c9e3d4afd272a4adf7419e7e7738b11d65de51c07e4981`, `85845` bytes, 1682 CRLF-terminated lines.
- `ANIMO_4.1.5.53/Outbal_write.for`: `cdc0a9738216d8a97d3c35f9862b78fc94fec385aaf0691d6778a73031ac74ea`, `124202` bytes, 2316 CRLF-terminated lines.

The byte-authoritative review evidence is each manifest `source_neighbourhoods[*].exact_bytes_base64` value decoded to bytes and checked against its exact SHA-256, line range and byte offsets. The deterministic `--archive` mode additionally rebinds those bytes to the exact hash-matching ZIP and member paths. The line-numbered renderings below are human-readable views only. If any rendering conflicts with the Base64-decoded evidence, the decoded bytes and their hashes control.

## Gap 1 — local `Dum` construction at TCD-027

Frozen `Outbal_calc.for`, lines 1401-1444:

```text
 1401: !           Redistribution (Ploughing; Tillage)
 1402: 
 1403:                 If (Pl(I) .Ge. 1) Then
 1404:                   If (Ln.Eq.0) Then
 1405:                     Bapp(Redi,Ly)  =bapp(Redi,Ly)  +Adpotoppl(I)    *Z
 1406: !                    Bapp(Finp_p,Ly)=bapp(Finp_p,Ly)+Adpotoppl(I)*Z
 1407:                   End If
 1408:                   If (Ln .Le. Pl(I)) Then
 1409:                     Bapp(Redi,Ly)   = Bapp(Redi,Ly) + Adpppl(I,Ln)  *Z
 1410:                     Bapp(Redi,Ly)   = Bapp(Redi,Ly) + Adpoprpl(I,Ln)*Z
 1411:                     Do J = 1,Ncxfa
 1412:                       Bapp(Redi,Ly)  =Bapp(Redi,Ly)  +                  &
 1413:      &                              Adpocxfapl(I,Ln,J)*Z
 1414: !                      Bapp(Finp_x,Ly)=bapp(Finp_x,Ly)+                  &
 1415: !     &                              Adpocxfapl(I,Ln,J)*Z
 1416:                     End Do
 1417:                     Do J = 1,Ncxsl
 1418:                       Bapp(Redi,Ly)  =Bapp(Redi,Ly)  +                  &
 1419:      &                              Adpocxslpl(I,Ln,J)*Z
 1420: !                      Bapp(Finp_x,Ly)=bapp(Finp_x,Ly)+                  &
 1421: !     &                              Adpocxslpl(I,Ln,J)*Z
 1422:                     End Do
 1423:                     Bapo(Redi,Ly) = Bapo(Redi,Ly) +Addiorpopl(I,Ln)*Z
 1424:                     Bafop(26,Ly)=bafop(26,Ly)+ Addiorpopl(I,Ln) * Z
 1425:                     If (Ln.Ne.0) Then
 1426:                       Dum = Adexpl(I,Ln)*Pofrex*Z
 1427:                       Bapo(Redi,Ly) = Bapo(Redi,Ly)   + Dum
 1428:                       Bafop(24,Ly)=bafop(25,Ly) + Dum
 1429:                       Dum = Adhuexpl(I,Ln) * Pofrhu(Ln) * Z
 1430:                       Bapo(Redi,Ly) = Bapo(Redi,Ly) + Dum
 1431:                       Bafop(27,Ly)=bafop(27,Ly) + Dum
 1432:                       Dum = Adhuospopl(I,Ln) * Z
 1433:                       Bapo(Redi,Ly) = Bapo(Redi,Ly) + Dum
 1434:                       Bafop(27,Ly)=bafop(27,Ly) + Dum                  
 1435:                       Do Fn = 1, Nf
 1436:                         Dum = Adospl(I,Ln,Fn) * Pofr(Fn) * Z
 1437:                         Bapo(Redi,Ly) = Bapo(Redi,Ly) + Dum
 1438:                         Bafop(25,Ly)=bafop(25,Ly) + Dum
 1439:                       End Do
 1440:                     End If
 1441:                   End If
 1442:                 End If
 1443:               End Do
 1444:             End Do
```

The frozen bytes show the exact local sequence around the disputed statement. In particular, line 1426 constructs `Dum` as `Adexpl(I,Ln)*Pofrex*Z`, line 1427 posts that same `Dum` to `Bapo(Redi,Ly)`, and line 1428 contains the legacy cross-slot statement `Bafop(24,Ly)=bafop(25,Ly) + Dum`. This sentence is an author description of the source evidence, not independent reviewer adjudication.

## Gap 2 — `Outbal_write.for` detailed organic-P mapping surface

Frozen `Outbal_write.for`, lines 608-638:

```text
  608: !      detailed transformations
  609: !
  610:             If(Outtransfom.Eq.1) Then
  611:               Call Unitnr(Uo)
  612:               Uob(14*(Ly-1)+10) = Uo
  613:               Open(Unit=uo,File='transfop'//chba(Ly)//'.Out',           &
  614:      &                              Status='unknown')
  615:               Write(Uo,'(2a40,/)')                                      &
  616:      &           ' Output from ANIMO   ---- Transformation',            &
  617:      &           's of organic phosphorus  ----             '
  618:               Write (Uo,12) Nint(Timi),Yrmi,Nint(Tima),Yrma,            &
  619:      &           Nl,Bo(Nl),Ln1,Ln2,Tplnmi,Bo(Ln2)
  620:               If (Nubati(Ly).Lt.1) Write (Uo,13) 
  621:               If (Nubati(Ly).Ge.1) Write (Uo,14) Nubati(Ly)
  622: 
  623:               Write (Uo,'(A60,A15/,A60/,6a60,A18)')                     &
  624:      &   ' Balance terms  in kg/ha org. phosphorus accumulated for the',&
  625:      &   ' balance period',                                             &
  626:      &   ' for each balance period the following items are given:',     &
  627:      &   ' yr      tito tiyr  grminerexP  incorexhuP  ntminerexP   tod',&
  628:      &   'issomP  grmineromP  incoromhuP  ntmineromP  grminerdoP  inco',&
  629:      &   'rdohuP  ntminerdoP   formomdoP  ntminerhuP   todisshuP   for',&
  630:      &   'mhuhuP  togrminerP  toincorhuP  tontminerP   P*expd*st    ad',&
  631:      &   'dRO_OP   addRO_DOP    addFr_OP   addFr_DOP   transpDOP   red',&
  632:      &   'is_EXP    redis_OP   redis_DOP   redis_HUP  huincorhuP    nt', &
  633:      &   'mindoP   sdoPincor'
  634: !                                                             initialise
  635:               Do I=1,30
  636:                  Bafop(I,Ly) = ze
  637:               End Do
  638:             End If
```

Frozen write/reset block, lines 1742-1752:

```text
 1742: !     detailed organic transformations
 1743: 
 1744:             If(Outtransfom.Eq.1) Then
 1745:               Uo = Uob(14*(Ly-1)+10)
 1746:               Write(Uo,'(1x,I4,I8,I5,1p,99e12.4:)')                     &
 1747:      &            Yr,Nint(Tito),Nint(Tiyr),(Bafop(I,Ly),I=1,30)
 1748: !                                                             Initialise
 1749:               Do I=1,30
 1750:                  Bafop(I,Ly) = ze
 1751:               End Do
 1752:             End If
```

A deterministic mechanical derivation implemented by the validator concatenates the Fortran character literals in lines 623-633, takes the 30 labels following `yr tito tiyr`, and enumerates them against `(Bafop(I,Ly),I=1,30)` at line 1747. That derivation yields slots 24=`redis_EXP`, 25=`redis_OP`, 26=`redis_DOP`, 27=`redis_HUP`. This mapping is retained in the manifest as `AUTHOR_INTERPRETATION_MECHANICALLY_DERIVED_FROM_FROZEN_SOURCE_EVIDENCE`; the next reviewer must rederive it rather than accept the author label as review authority.

## Gap 3 — neighbouring organic-P self-accumulators

The same frozen P redistribution neighbourhood above contains:

- slot 26 self-accumulation at line 1424;
- slot 27 self-accumulation at lines 1431 and 1434;
- slot 25 self-accumulation at line 1438.

No corrected slot-24 statement is written into any frozen or production source by B3A01E.

## Orthogonal source context

These contexts are persisted only as index cross-check evidence and do not expand the TCD scope.

Frozen organic-matter redistribution, lines 419-443:

```text
  419: !           Redistribution (Ploughing; Tillage)
  420: 
  421: 
  422:               If(Pl(I) .Ge. 1) Then
  423:                 If(Ln.Eq.0)Then
  424:                    Bdom(Redi,Ly) = Bdom(Redi,Ly) + Addiormatoppl(I) *Z
  425:                 End If
  426:                 If (Ln .Le. Pl(I)) Then
  427:                   Bdom(Redi,Ly) = Bdom(Redi,Ly)+                        &
  428:      &                         (Addiormapl(I,Ln)+AdStdiormapl(I,Ln)) * Z
  429:                   Bafom(26,Ly) = Bafom(26,Ly)  +                        &
  430:      &                         (Addiormapl(I,Ln)+AdStdiormapl(I,Ln)) * Z
  431:                   If (Ln.Ne.0) Then
  432:                     Bfom(Redi,Ly) =bfom(Redi,Ly)  +Adexpl(I,Ln)  * Z
  433:                     Bafom(24,Ly)  =bafom(24,Ly)   +Adexpl(I,Ln)  * Z
  434:                     Bahu(Redi,Ly) =bahu(Redi,Ly)  +Adhuexpl(I,Ln)* Z
  435:                     Bafom(27,Ly)  =bafom(27,Ly)   +Adhuexpl(I,Ln)* Z
  436:                     Bahu(Redi,Ly) =bahu(Redi,Ly)  +Adhuospl(I,Ln)* Z
  437:                     Bafom(27,Ly)  =bafom(27,Ly)   +Adhuospl(I,Ln)* Z
  438:                     Do Fn = 1,Nf
  439:                       Bfom(Redi,Ly) =bfom(Redi,Ly)+Adospl(I,Ln,Fn) * Z
  440:                       Bafom(25,Ly)  =bafom(25,Ly) +Adospl(I,Ln,Fn) * Z
  441:                     End Do
  442:                   End If
  443:                 End If
```

Frozen organic-N redistribution, lines 912-943:

```text
  912: !           Redistribution (Ploughing; Tillage)
  913: 
  914:               If (Pl(I) .Ge. 1)Then
  915: 
  916:                 If(Ln.Eq.0)Then
  917:                   Banh(Redi,Ly) = Banh(Redi,Ly) + Adnhtoppl(I)   *Z
  918:                   Bani(Redi,Ly) = Bani(Redi,Ly) + Adnitoppl(I)   *Z
  919:                   Bano(Redi,Ly) = Bano(Redi,Ly) +Addiornitoppl(I)*Z
  920:                 End If
  921:                 If (Ln .Le. Pl(I)) Then
  922:                   Banh(Redi,Ly) = Banh(Redi,Ly) + Adnhpl(I,Ln)   *Z
  923:                   Bani(Redi,Ly) = Bani(Redi,Ly) + Adnipl(I,Ln)   *Z
  924:                   Bano(Redi,Ly) = Bano(Redi,Ly) +(Addiornipl(I,Ln) +    &
  925:      &                                            AdStdiornipl(I,Ln))*Z
  926:                   Bafon(26,Ly)=bafon(26,Ly)     +(Addiornipl(I,Ln) +    &
  927:      &                                            AdStdiornipl(I,Ln))*Z
  928:                   If (Ln.Ne.0) Then
  929:                     Dum = Adexpl(I,Ln)*Nifrex*Z
  930:                     Bano(Redi,Ly) = Bano(Redi,Ly) + Dum
  931:                     Bafon(24,Ly)  = Bafon(24,Ly)  + Dum
  932:                     Dum = Adhuexpl(I,Ln) * Nifrhu(Ln) * Z
  933:                     Bano(Redi,Ly) = Bano(Redi,Ly) + Dum
  934:                     Bafon(27,Ly)  = Bafon(27,Ly)  + Dum
  935:                     Dum = Adhuosnipl(I,Ln) * Z
  936:                     Bano(Redi,Ly) = Bano(Redi,Ly) + Dum
  937:                     Bafon(27,Ly)  = Bafon(27,Ly)  + Dum
  938:                     Do Fn = 1,Nf
  939:                       Dum = Adospl(I,Ln,Fn) * Nifr(Fn) * Z
  940:                       Bano(Redi,Ly) = Bano(Redi,Ly) + Dum
  941:                       Bafon(25,Ly)  = Bafon(25,Ly)  + Dum
  942:                     End Do
  943:                   End If
```

They contain the organic-matter and organic-N slot-24 self-accumulation analogues previously cited by the readiness/disposition work. B3A01E does not promote those analogues to a scientific review conclusion.

## Reproducibility contract

`tools/extract_verify_tcd027_frozen_b0.py` has two roles. In repository/CI mode it decodes every committed Base64 source neighbourhood and checks exact excerpt SHA-256, size, CRLF line identity, source-line assertions and the mechanical 30-label mapping. With `--archive <path>` it additionally hashes the supplied ZIP, requires the exact frozen-B0 archive SHA-256, reads the exact member paths from that ZIP, checks their pinned full-member SHA-256 identities, and requires every persisted neighbourhood to equal the corresponding archive byte slice.

The latter mode is the provenance re-extraction check. A mismatching archive, member, excerpt, line mapping or evidence copy fails closed.

## Review history and handoff

The retained result remains:

`ANIMO-B3A01R = INCOMPLETE`

B3A01E can qualify only that the previously unavailable frozen-source evidence is now persisted and mechanically checkable. It cannot issue `PASS`, `FAIL`, or a replacement review result.

After B3A01E validation, the next required workunit is a **new genuinely separate** second-line re-review, recommended as `ANIMO-B3A01R2`, against this evidence packet plus the retained readiness/disposition/review authorities. The new reviewer must independently inspect and rederive the three formerly missing source-bound checks.

Hard boundaries remain: no production source change, no frozen-B0 change, no candidate patch, no composition, no B4, no central-regie update, and no TCD-027 admission.
