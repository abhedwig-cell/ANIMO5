program buildq04_boundary_probe
  implicit none
  integer :: nl, scenario
  real :: bvals(5)
  bvals = (/ -1.0e-3, -1.0e-6, 0.0, 1.0e-6, 1.0e-3 /)
  do nl=1,4
    do scenario=1,3
      call run_case(nl, scenario, bvals)
    enddo
  enddo
contains
subroutine run_case(nl, scenario, bvals)
  integer, intent(in) :: nl, scenario
  real, intent(in) :: bvals(5)
  integer, parameter :: maxl=8
  real :: he(0:maxl), mofrox(0:maxl), mofrtx(0:maxl), mofrsax(0:maxl), mofrx(0:maxl)
  real :: flair(maxl+1), flaiib(0:maxl), flaiio(0:maxl), flaiou(0:maxl)
  real :: avca(0:maxl), rebuav(0:maxl), st, tofl, y3
  integer :: la, ln, i
  he=0.25; mofrox=0.30; mofrtx=0.28; mofrsax=0.45; mofrx=0.30
  avca=0.0; rebuav=2.0; st=1.0
  do ln=0,nl
    avca(ln)=0.01+0.005*ln
  enddo
  select case(scenario)
  case(1)
    do ln=1,nl
      mofrsax(ln)=0.50; mofrx(ln)=0.30
    enddo
  case(2)
    mofrsax(1)=0.30; mofrx(1)=0.30
  case(3)
    mofrox(0)=0.5; mofrtx(0)=0.5; he(0)=0.01
  end select
  do i=1,5
    flair = -999.0
    la=1
    if (scenario==3) la=0
    do while (la.gt.0 .and. la.lt.nl .and. mofrsax(la)-mofrx(la).gt.1.e-7)
      la=la+1
    enddo
    la=max(0,la-1)
    flair(nl+1)=bvals(i)
    flair(la+1)=0.0
    do ln=la,1,-1
      flair(ln)=flair(ln+1)+(mofrox(ln)-mofrtx(ln))*he(ln)*st
    enddo
    do ln=la+2,nl
      flair(ln)=0.0
    enddo
    flaiib=0.0; flaiio=0.0; flaiou=0.0
    do ln=1,nl
      flaiib(ln)=max(0.0,flair(ln))
      flaiio(ln)=-min(0.0,flair(ln+1))
      flaiou(ln)=max(0.0,flair(ln+1))
      flaiou(ln)=flaiou(ln)-min(0.0,flair(ln))
    enddo
    if (nl.eq.1) then
      tofl = -avca(nl)*flaiou(nl)*st
    else
      tofl = (avca(nl-1)*flaiib(nl)-avca(nl)*flaiou(nl))*st
    endif
    y3 = (rebuav(nl)*flaiou(nl))/he(nl)
    write(*,'(A,I0,A,I0,A,I0,A,ES13.5,A,ES13.5,A,ES13.5,A,ES13.5,A,ES13.5)') &
      'NL=',nl,' SC=',scenario,' LA=',la,' B=',bvals(i),' FIO=',flaiio(nl),' FOU=',flaiou(nl), &
      ' TOFL=',tofl,' Y3=',y3
  enddo
end subroutine
end program
