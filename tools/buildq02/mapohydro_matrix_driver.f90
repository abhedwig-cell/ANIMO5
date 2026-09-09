program mapohydro_matrix_driver
  implicit none
  include 'Param.inc'
  integer :: case_id
  do case_id=1,64
    call run_case(case_id)
  enddo
contains
  subroutine run_case(case_id)
    implicit none
    integer,intent(in)::case_id
    integer :: Flpn,LnBoMp(2),LnTpMpSr(2),Nl,Sqnu(0:Manl),TaskMp,Uoer
    real :: Badev,Flid(0:Manl),FlMpHlp(0:1),FlMpInPr(2),FlMpInRu(2),FlMpOuDr(Manl)
    real :: FrHeWeMpWl(2,Manl),FlMpOuIf(2,Manl),Flou(0:Manl),FrMpDrSo,FrMpRuRv
    real :: He(0:Manl),Mofr(0:Manl),MofrsaMp(0:Manl),Pr,SrWaMp(2),SrWaMpCp(2,Manl)
    real :: SrWaMpCpOld(Manl),SrWaMpOld(2),St,TiTo
    integer :: KBegMpReko,KEndMpReko,Nd,i,d
    logical :: CoStat(0:Manl)
    real :: FlMpInEf(2,Manl),FlMpInRuRv(2),FlMpInRuSo(2),FlMpOuDrMp(Manl),FlMpOuDrSo(Manl)
    real :: FlMpOuDrTo,FlMpOuSoTo(2,0:Manl),FlMpVt(2,Manl),MpWfps(Manl)
    real :: x

    Nl=4; Flpn=0; Uoer=6; St=0.25; TiTo=100.0+case_id
    Badev=0.; Flid=0.; FlMpHlp=0.; FlMpInPr=0.; FlMpInRu=0.; FlMpOuDr=0.
    FrHeWeMpWl=0.; FlMpOuIf=0.; Flou=0.; FrMpDrSo=0.2; FrMpRuRv=0.3
    He=0.2; Mofr=0.3; MofrsaMp=0.45; Pr=0.001; SrWaMp=0.; SrWaMpCp=0.; SrWaMpCpOld=0.; SrWaMpOld=0.
    Sqnu=0; do i=1,Nl; Sqnu(i)=i; enddo
    KBegMpReko=0; KEndMpReko=0; Nd=-1; CoStat=.true.; FlMpInEf=0.; FlMpInRuRv=0.; FlMpInRuSo=0.
    FlMpOuDrMp=0.; FlMpOuDrSo=0.; FlMpOuDrTo=0.; FlMpOuSoTo=0.; FlMpVt=0.; MpWfps=0.

    FrHeWeMpWl(1,mod(case_id-1,4)+1)=0.2
    FrHeWeMpWl(1,4)=0.2
    FrHeWeMpWl(2,4)=0.2
    if (mod(case_id,5)==0) FrHeWeMpWl(2,2)=0.15

    do d=1,2
      FlMpInPr(d)=1.0e-5*real(mod(case_id+d,4))
      FlMpInRu(d)=1.0e-5*real(mod(case_id+2*d,5))
      do i=1,Nl
        x=1.0e-5*real(mod(case_id+3*i+5*d,7))
        if (mod(case_id+i+d,6)==0) x=-x
        FlMpOuIf(d,i)=x
      enddo
    enddo
    do i=1,Nl
      FlMpOuDr(i)=1.0e-6*real(mod(case_id+i,3))
      SrWaMpCp(1,i)=1.0e-4*real(mod(case_id+i,4))
      SrWaMpCp(2,i)=1.0e-4*real(mod(case_id+2*i,3))
      SrWaMpCpOld(i)=1.0e-4*real(mod(case_id+3*i,2))
    enddo
    SrWaMp=(/1.0e-4*real(mod(case_id,3)),1.0e-4*real(mod(case_id+1,3))/)
    SrWaMpOld=(/1.0e-4*real(mod(case_id+2,3)),1.0e-4*real(mod(case_id+3,3))/)

    TaskMp=1
    call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer,Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl,FlMpOuIf,Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp,SrWaMpCp,SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko,Nd,CoStat,FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo,FlMpOuDrTo,FlMpOuSoTo,FlMpVt,MpWfps)
    if (Nd>0) then
      TaskMp=2
      call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer,Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl,FlMpOuIf,Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp,SrWaMpCp,SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko,Nd,CoStat,FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo,FlMpOuDrTo,FlMpOuSoTo,FlMpVt,MpWfps)
      TaskMp=3
      call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer,Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl,FlMpOuIf,Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp,SrWaMpCp,SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko,Nd,CoStat,FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo,FlMpOuDrTo,FlMpOuSoTo,FlMpVt,MpWfps)
      TaskMp=4
      call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer,Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl,FlMpOuIf,Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp,SrWaMpCp,SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko,Nd,CoStat,FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo,FlMpOuDrTo,FlMpOuSoTo,FlMpVt,MpWfps)
    endif
    write(*,'(I4,1X,5(I3,1X),18(ES24.16,1X),5(L1,1X))') case_id,LnBoMp(1),LnBoMp(2),LnTpMpSr(1),LnTpMpSr(2),Nd,Badev,(Flid(i),i=1,Nl),(Flou(i),i=0,Nl),(MpWfps(i),i=1,Nl),FlMpOuDrTo,Pr,FlMpHlp(0),FlMpHlp(1),SrWaMp(1),SrWaMp(2),(CoStat(i),i=0,Nl)
  end subroutine
end program
