program stateq01_rc5_nh4_adsorption_probe
  implicit none
  include 'param.inc'
  integer :: Errornumber, Flpn, Nl, Uoer, Ioptmp, Ipo, KBegMpReko, KEndMpReko, Nd
  integer :: Sqnu(0:manl), LnBoMp(2), LnTpMpSr(2), ItRec(6,50)
  real :: Avco(0:manl+1), Co(0:manl), Cx(0:manl), Flev(0:manl), Flib(0:manl+1), Flid(0:manl), Flio(0:manl), Flou(0:manl)
  real :: He(0:manl), Mofr(0:manl), Mofro(0:manl), Mofrt(0:manl), Rekico(0:manl), Rekicx(0:manl), Rekiso(0:manl)
  real :: Reko(0:manl), Rhbd(0:manl), Rsco(0:manl), Rscx(0:manl), Se(0:manl), Socf(0:manl), Toin(0:manl), Toou(0:manl)
  real :: Coaq, Coid, Cotop, St, Tito, Evicpr, Evicirr, Evsn, Evpn, Rupr, Prsn, Runon, Runinu
  real :: Coirr, CoMp(2), Copryn, FlMpInEf(2,Manl), FlMpInPr(2), FlMpInRuRv(2), FlMpOuDrMp(Manl)
  real :: FlMpOuSoTo(2,0:Manl), FlMpVt(2,Manl), Prirr, Prr, SrWaMp(2), SrWaMpOld(2), TimSwi
  real :: AvCoML(2,Manl), AvCoMp(2), RsCoMp(2)
  logical :: CoStat(0:Manl)
  real :: cp_co, cp_cx, recon_cx
  real :: cont_rsco, cont_rscx, cont_avco, cont_toin, cont_toou
  real :: recon_rsco, recon_rscx, recon_avco, recon_toin, recon_toou
  real :: omit_rsco, omit_rscx, omit_avco, omit_toin, omit_toou
  character(len=12) :: subst, caller

  Sqnu=0; LnBoMp=0; LnTpMpSr=0; ItRec=0
  Avco=0.; Co=0.; Cx=0.; Flev=0.; Flib=0.; Flid=0.; Flio=0.; Flou=0.; He=0.; Mofr=0.; Mofro=0.; Mofrt=0.
  Rekico=0.; Rekicx=0.; Rekiso=0.; Reko=0.; Rhbd=0.; Rsco=0.; Rscx=0.; Se=0.; Socf=0.; Toin=0.; Toou=0.
  CoMp=0.; FlMpInEf=0.; FlMpInPr=0.; FlMpInRuRv=0.; FlMpOuDrMp=0.; FlMpOuSoTo=0.; FlMpVt=0.; SrWaMp=0.; SrWaMpOld=0.
  AvCoML=0.; AvCoMp=0.; RsCoMp=0.; CoStat=.false.
  Flpn=0; Nl=1; Sqnu(1)=1; Ioptmp=0; Ipo=0; KBegMpReko=0; KEndMpReko=0; Nd=0
  He(1)=0.2; Mofr(1)=0.3; Mofro(1)=0.3; Mofrt(1)=0.3; Rhbd(1)=1300.; Socf(1)=0.001
  Flib(1)=0.01; Flou(1)=0.01
  Coaq=0.; Coid=0.; St=1.; Evicpr=0.; Evicirr=0.; Evsn=0.; Evpn=0.; Rupr=0.; Prsn=0.; Runon=0.; Runinu=0.
  Coirr=0.; Copryn=0.; Prirr=0.; Prr=0.; TimSwi=0.
  subst='AMMONIUM    '; caller='ANIMO-act   '

  Co=0.; Cx=0.; Rsco=0.; Rscx=0.; Avco=0.; Toin=0.; Toou=0.
  Co(1)=0.010; Cx(1)=He(1)*Rhbd(1)*Socf(1)*Co(1); Cotop=0.020; Tito=1.0
  open(unit=91,file='step1.log',status='replace',action='write'); Uoer=91
  call Transport(subst,caller,Flpn,Nl,Sqnu,Uoer,Avco,Co,Coaq,Coid,Cotop,Cx,Flev,Flib,Flid,Flio,Flou,He,Mofr,Mofro,Mofrt,Rekico,Rekicx,Rekiso,Reko,Rhbd,Rsco,Rscx,Se,Socf,St,Tito,Toin,Toou,Evicpr,Evicirr,Evsn,Evpn,Rupr,Prsn,Runon,Runinu,Ioptmp,Ipo,KBegMpReko,KEndMpReko,LnBoMp,LnTpMpSr,Nd,CoStat,Coirr,CoMp,Copryn,FlMpInEf,FlMpInPr,FlMpInRuRv,FlMpOuDrMp,FlMpOuSoTo,FlMpVt,Prirr,Prr,SrWaMp,SrWaMpOld,TimSwi,ItRec,AvCoML,AvCoMp,RsCoMp,Errornumber)
  close(91)
  if (Errornumber.ne.0) stop 11
  cp_co=Rsco(1); cp_cx=Rscx(1)
  recon_cx=He(1)*Rhbd(1)*Socf(1)*cp_co

  Co=0.; Cx=0.; Rsco=0.; Rscx=0.; Avco=0.; Toin=0.; Toou=0.
  Co(1)=cp_co; Cx(1)=cp_cx; Cotop=0.015; Tito=2.0
  open(unit=92,file='continuous.log',status='replace',action='write'); Uoer=92
  call Transport(subst,caller,Flpn,Nl,Sqnu,Uoer,Avco,Co,Coaq,Coid,Cotop,Cx,Flev,Flib,Flid,Flio,Flou,He,Mofr,Mofro,Mofrt,Rekico,Rekicx,Rekiso,Reko,Rhbd,Rsco,Rscx,Se,Socf,St,Tito,Toin,Toou,Evicpr,Evicirr,Evsn,Evpn,Rupr,Prsn,Runon,Runinu,Ioptmp,Ipo,KBegMpReko,KEndMpReko,LnBoMp,LnTpMpSr,Nd,CoStat,Coirr,CoMp,Copryn,FlMpInEf,FlMpInPr,FlMpInRuRv,FlMpOuDrMp,FlMpOuSoTo,FlMpVt,Prirr,Prr,SrWaMp,SrWaMpOld,TimSwi,ItRec,AvCoML,AvCoMp,RsCoMp,Errornumber)
  close(92)
  if (Errornumber.ne.0) stop 12
  cont_rsco=Rsco(1); cont_rscx=Rscx(1); cont_avco=Avco(1); cont_toin=Toin(1); cont_toou=Toou(1)

  Co=0.; Cx=0.; Rsco=0.; Rscx=0.; Avco=0.; Toin=0.; Toou=0.
  Co(1)=cp_co; Cx(1)=recon_cx; Cotop=0.015; Tito=2.0
  open(unit=93,file='reconstructed.log',status='replace',action='write'); Uoer=93
  call Transport(subst,caller,Flpn,Nl,Sqnu,Uoer,Avco,Co,Coaq,Coid,Cotop,Cx,Flev,Flib,Flid,Flio,Flou,He,Mofr,Mofro,Mofrt,Rekico,Rekicx,Rekiso,Reko,Rhbd,Rsco,Rscx,Se,Socf,St,Tito,Toin,Toou,Evicpr,Evicirr,Evsn,Evpn,Rupr,Prsn,Runon,Runinu,Ioptmp,Ipo,KBegMpReko,KEndMpReko,LnBoMp,LnTpMpSr,Nd,CoStat,Coirr,CoMp,Copryn,FlMpInEf,FlMpInPr,FlMpInRuRv,FlMpOuDrMp,FlMpOuSoTo,FlMpVt,Prirr,Prr,SrWaMp,SrWaMpOld,TimSwi,ItRec,AvCoML,AvCoMp,RsCoMp,Errornumber)
  close(93)
  if (Errornumber.ne.0) stop 13
  recon_rsco=Rsco(1); recon_rscx=Rscx(1); recon_avco=Avco(1); recon_toin=Toin(1); recon_toou=Toou(1)

  Co=0.; Cx=0.; Rsco=0.; Rscx=0.; Avco=0.; Toin=0.; Toou=0.
  Co(1)=cp_co; Cx(1)=0.0; Cotop=0.015; Tito=2.0
  open(unit=94,file='omitted.log',status='replace',action='write'); Uoer=94
  call Transport(subst,caller,Flpn,Nl,Sqnu,Uoer,Avco,Co,Coaq,Coid,Cotop,Cx,Flev,Flib,Flid,Flio,Flou,He,Mofr,Mofro,Mofrt,Rekico,Rekicx,Rekiso,Reko,Rhbd,Rsco,Rscx,Se,Socf,St,Tito,Toin,Toou,Evicpr,Evicirr,Evsn,Evpn,Rupr,Prsn,Runon,Runinu,Ioptmp,Ipo,KBegMpReko,KEndMpReko,LnBoMp,LnTpMpSr,Nd,CoStat,Coirr,CoMp,Copryn,FlMpInEf,FlMpInPr,FlMpInRuRv,FlMpOuDrMp,FlMpOuSoTo,FlMpVt,Prirr,Prr,SrWaMp,SrWaMpOld,TimSwi,ItRec,AvCoML,AvCoMp,RsCoMp,Errornumber)
  close(94)
  if (Errornumber.ne.0) stop 14
  omit_rsco=Rsco(1); omit_rscx=Rscx(1); omit_avco=Avco(1); omit_toin=Toin(1); omit_toou=Toou(1)

  write(*,'(A,1X,ES24.16)') 'CHECKPOINT_RSCO',cp_co
  write(*,'(A,1X,ES24.16)') 'CHECKPOINT_RSCX',cp_cx
  write(*,'(A,1X,ES24.16)') 'RECONSTRUCTED_CX',recon_cx
  write(*,'(A,1X,L1)') 'CHECKPOINT_EQ_RECONSTRUCTED_CX',cp_cx.eq.recon_cx
  write(*,'(A,5(1X,ES24.16))') 'CONT_FINAL',cont_rsco,cont_rscx,cont_avco,cont_toin,cont_toou
  write(*,'(A,5(1X,ES24.16))') 'RECON_FINAL',recon_rsco,recon_rscx,recon_avco,recon_toin,recon_toou
  write(*,'(A,5(1X,ES24.16))') 'OMIT_FINAL',omit_rsco,omit_rscx,omit_avco,omit_toin,omit_toou
  write(*,'(A,1X,L1)') 'CONT_EQ_RECON',(cont_rsco.eq.recon_rsco .and. cont_rscx.eq.recon_rscx .and. cont_avco.eq.recon_avco .and. cont_toin.eq.recon_toin .and. cont_toou.eq.recon_toou)
  write(*,'(A,1X,L1)') 'CONT_EQ_OMIT_PHYSICAL',(cont_rsco.eq.omit_rsco .and. cont_rscx.eq.omit_rscx .and. cont_avco.eq.omit_avco .and. cont_toin.eq.omit_toin .and. cont_toou.eq.omit_toou)
end program stateq01_rc5_nh4_adsorption_probe
subroutine MapoTransport()
  implicit none
end subroutine MapoTransport
