program buildq04_uninit_probe
  implicit none
  integer :: nl
  do nl=1,4
    call one(nl)
  enddo
contains
subroutine one(nl)
  integer, parameter :: maxl=8
  integer, intent(in) :: nl
  integer :: la,ln
  real :: flair(maxl+1),flaiio(maxl),flaiou(maxl)
  real :: mofrsax(maxl),mofrx(maxl),mofrox(maxl),mofrtx(maxl),he(maxl),st
  mofrsax=.5; mofrx=.3; mofrox=.3; mofrtx=.28; he=.25; st=1.0
  la=1
  do while(la.gt.0.and.la.lt.nl.and.mofrsax(la)-mofrx(la).gt.1.e-7)
    la=la+1
  enddo
  la=max(0,la-1)
  flair(la+1)=0.0
  do ln=la,1,-1
    flair(ln)=flair(ln+1)+(mofrox(ln)-mofrtx(ln))*he(ln)*st
  enddo
  do ln=la+2,nl
    flair(ln)=0.0
  enddo
  do ln=1,nl
    flaiio(ln)=-min(0.0,flair(ln+1))
    flaiou(ln)=max(0.0,flair(ln+1))-min(0.0,flair(ln))
  enddo
  write(*,'(A,I0,A,I0,A,ES24.16,A,ES24.16,A,ES24.16)') &
    'NL=',nl,' LA=',la,' SLOT=',flair(nl+1),' FIO=',flaiio(nl),' FOU=',flaiou(nl)
end subroutine
end program
