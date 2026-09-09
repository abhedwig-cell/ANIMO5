program mapohydro_driver
  implicit none
  include 'Param.inc'
  integer :: case_id, ios
  character(len=32) :: arg
  call get_command_argument(1,arg)
  if (len_trim(arg) > 0) then
     read(arg,*,iostat=ios) case_id
     if (ios /= 0 .or. case_id < 1 .or. case_id > 4) stop 2
     call run_case(case_id)
  else
     do case_id = 1, 4
        call run_case(case_id)
     end do
  endif
contains
  subroutine run_case(case_id)
    implicit none
    integer, intent(in) :: case_id
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
    integer :: i
    real :: expected1, expected2

    Nl = 2
    Flpn = 0
    Uoer = 6
    Badev = 0.0
    Flid = 0.0
    FlMpHlp = 0.0
    FlMpInPr = 0.0
    FlMpInRu = 0.0
    FlMpOuDr = 0.0
    FrHeWeMpWl = 0.0
    FlMpOuIf = 0.0
    Flou = 0.0
    FrMpDrSo = 0.0
    FrMpRuRv = 0.0
    He = 0.25
    Mofr = 0.30
    MofrsaMp = 0.45
    Pr = 0.0
    SrWaMp = 0.0
    SrWaMpCp = 0.0
    SrWaMpCpOld = 0.0
    SrWaMpOld = 0.0
    St = 1.0
    TiTo = real(case_id)
    Sqnu = 0
    do i=1,Nl
      Sqnu(i)=i
    end do
    KBegMpReko = 0
    KEndMpReko = 0
    Nd = -1
    CoStat = .true.
    FlMpInEf = 0.0
    FlMpInRuRv = 0.0
    FlMpInRuSo = 0.0
    FlMpOuDrMp = 0.0
    FlMpOuDrSo = 0.0
    FlMpOuDrTo = 0.0
    FlMpOuSoTo = 0.0
    FlMpVt = 0.0
    MpWfps = 0.0
    LnBoMp = 0
    LnTpMpSr = 0

    select case(case_id)
    case(1)
      FrHeWeMpWl(1,1)=0.2
      FrHeWeMpWl(1,2)=0.2
      FrHeWeMpWl(2,2)=0.2
      FlMpOuIf(1,1)=0.10
      FlMpOuIf(2,1)=0.20
      FlMpOuIf(1,2)=0.05
      FlMpOuIf(2,2)=0.07
    case(2)
      FrHeWeMpWl(1,1)=0.2
      FrHeWeMpWl(2,2)=0.2
      FlMpOuIf(1,1)=0.11
      FlMpOuIf(2,1)=0.03
      FlMpOuIf(1,2)=0.02
      FlMpOuIf(2,2)=0.09
    case(3)
      FrHeWeMpWl(1,1)=0.2
      FrHeWeMpWl(1,2)=0.2
      FlMpOuIf(1,1)=0.04
      FlMpOuIf(1,2)=0.06
    case(4)
    end select

    TaskMp=1
    call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer, &
      Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl, &
      FlMpOuIf,Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp, &
      SrWaMpCp,SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko, &
      Nd,CoStat,FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo, &
      FlMpOuDrTo,FlMpOuSoTo,FlMpVt,MpWfps)

    write(*,'(A,I0,A,2(I0,1X),A,2(I0,1X),A,I0)') 'CASE=',case_id,' LNB=', &
      LnBoMp(1),LnBoMp(2),' LNT=',LnTpMpSr(1),LnTpMpSr(2),' ND=',Nd

    if (Nd > 0) then
      Flid(1)=1.0 + FlMpOuSoTo(1,1)+FlMpOuSoTo(2,1)
      Flid(2)=1.0 + FlMpOuSoTo(1,2)+FlMpOuSoTo(2,2)
      expected1=1.0
      expected2=1.0
      call clobber_stack(case_id)
      TaskMp=4
      call Mapohydro(TaskMp,Flpn,LnBoMp,LnTpMpSr,Nl,Sqnu,Uoer, &
        Badev,Flid,FlMpHlp,FlMpInPr,FlMpInRu,FlMpOuDr,FrHeWeMpWl, &
        FlMpOuIf,Flou,FrMpDrSo,FrMpRuRv,He,Mofr,MofrsaMp,Pr,SrWaMp, &
        SrWaMpCp,SrWaMpCpOld,SrWaMpOld,St,TiTo,KBegMpReko,KEndMpReko, &
        Nd,CoStat,FlMpInEf,FlMpInRuRv,FlMpInRuSo,FlMpOuDrMp,FlMpOuDrSo, &
        FlMpOuDrTo,FlMpOuSoTo,FlMpVt,MpWfps)
      write(*,'(A,I0,A,2(ES24.16,1X),A,2(ES24.16,1X))') 'RESET=',case_id,' FLID=', &
        Flid(1),Flid(2),' EXPECT=',expected1,expected2
    endif
  end subroutine

  subroutine clobber_stack(seed)
    implicit none
    integer, intent(in) :: seed
    integer :: i
    real :: a(20000)
    do i=1,size(a)
      a(i)=real(seed)+real(i)*0.000001
    end do
    if (a(size(a)) < 0.0) print *, a(1)
  end subroutine
end program
