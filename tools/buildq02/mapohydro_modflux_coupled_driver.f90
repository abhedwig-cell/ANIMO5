program mapohydro_modflux_driver
  implicit none
  include 'Param.inc'
  integer :: mode, ios
  character(len=16) :: arg
  integer :: Flpn, LnBoMp(2), LnTpMpSr(2), Nl, Sqnu(0:Manl), TaskMp, Uoer
  real :: Badev, Flid(0:Manl), FlMpHlp(0:1), FlMpInPr(2), FlMpInRu(2)
  real :: FlMpOuDr(Manl), FrHeWeMpWl(2,Manl), FlMpOuIf(2,Manl)
  real :: Flou(0:Manl), FrMpDrSo, FrMpRuRv, He(0:Manl), Mofr(0:Manl)
  real :: MofrsaMp(0:Manl), Pr, SrWaMp(2), SrWaMpCp(2,Manl)
  real :: SrWaMpCpOld(Manl), SrWaMpOld(2), St, TiTo
  integer :: KBegMpReko, KEndMpReko, Nd
  logical :: CoStat(0:Manl)
  real :: FlMpInEf(2,Manl), FlMpInRuRv(2), FlMpInRuSo(2)
  real :: FlMpOuDrMp(Manl), FlMpOuDrSo(Manl), FlMpOuDrTo
  real :: FlMpOuSoTo(2,0:Manl), FlMpVt(2,Manl), MpWfps(Manl)
  integer :: Nudr, Ioptmp
  real :: Flab(0:Manl+1), Fldr(Madr,0:Manl), Flib(0:Manl+1), Flio(0:Manl)
  real :: Rurv, Ruso

  mode=1
  call get_command_argument(1,arg)
  if (len_trim(arg)>0) then
    read(arg,*,iostat=ios) mode
    if (ios/=0 .or. mode<1 .or. mode>2) stop 2
  endif

  Nl=2; Flpn=1; Uoer=6; St=1.0; TiTo=1.0
  Badev=0.; Flid=0.; FlMpHlp=0.; FlMpInPr=0.; FlMpInRu=0.; FlMpOuDr=0.
  FrHeWeMpWl=0.; FlMpOuIf=0.; Flou=0.; FrMpDrSo=0.; FrMpRuRv=0.; He=0.25
  Mofr=0.30; MofrsaMp=0.45; Pr=0.; SrWaMp=0.; SrWaMpCp=0.; SrWaMpCpOld=0.; SrWaMpOld=0.
  Sqnu=0; KBegMpReko=0; KEndMpReko=0; Nd=-1; CoStat=.true.; FlMpInEf=0.
  FlMpInRuRv=0.; FlMpInRuSo=0.; FlMpOuDrMp=0.; FlMpOuDrSo=0.; FlMpOuDrTo=0.
  FlMpOuSoTo=0.; FlMpVt=0.; MpWfps=0.

  ! Mode 1: no macropore outgoing flux, exposing the Task-2 backward-scan Ln=0 seam.
  ! Mode 2: outgoing flux in both layers, making the CoStat range include Ln=0.
  FrHeWeMpWl(1,1)=0.2; FrHeWeMpWl(1,2)=0.2; FrHeWeMpWl(2,2)=0.2
  if (mode==2) then
    FlMpOuIf(1,1)=0.1
    FlMpOuIf(1,2)=0.1
  endif

  TaskMp=1
  call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer, &
    Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl,FlMpOuIf, &
    Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp,SrWaMpCp, &
    SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko,Nd,CoStat, &
    FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo,FlMpOuDrTo, &
    FlMpOuSoTo,FlMpVt,MpWfps)
  write(*,'(A,2(I0,1X),A,I0)') 'TASK1 LNB=',LnBoMp(1),LnBoMp(2),' ND=',Nd

  Nudr=0; Ioptmp=1; Fldr=0.; Flib=0.; Flio=0.; Rurv=0.; Ruso=0.
  Flab=0.; Flab(0)=-1.; Flab(1)=-1.; Flab(2)=0.; Flab(3)=-1.
  call Modflux(Flpn,Nl,Nudr,Sqnu,Flab,Fldr,Flib,Flid,Flio,Flou,Rurv,Ruso,Ioptmp,FlMpOuSoTo)
  write(*,'(A,3(I0,1X))') 'MODFLUX SQNU=',Sqnu(0),Sqnu(1),Sqnu(2)

  TaskMp=2
  call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer, &
    Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl,FlMpOuIf, &
    Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp,SrWaMpCp, &
    SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko,Nd,CoStat, &
    FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo,FlMpOuDrTo, &
    FlMpOuSoTo,FlMpVt,MpWfps)
  write(*,'(A,2(I0,1X))') 'TASK2 K=',KBegMpReko,KEndMpReko
end program
