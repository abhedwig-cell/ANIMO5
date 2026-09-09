program ghgasses_phase_projection_probe
  implicit none
  integer, parameter :: nmax=4
  integer :: c, nl, flpn, ioptmp, ln, d
  integer :: lnbomp(2), lntpmpsr(2)
  real(8) :: st
  real(8) :: flib(0:nmax),flio(0:nmax),flou(0:nmax),he(0:nmax)
  real(8) :: mofr(0:nmax),mofro(0:nmax),mofrsa(0:nmax),mofrt(0:nmax)
  real(8) :: mofrox(0:nmax),mofrsamp(0:nmax),srwampcp(2,nmax)
  real(8) :: floux1(0:nmax),mofrx1(0:nmax),mofrsax1(0:nmax),mofrtx1(0:nmax)
  real(8) :: flaiib1(0:nmax),flaiio1(0:nmax),flaiou1(0:nmax),flaiatmos1
  real(8) :: floux2(0:nmax),mofrx2(0:nmax),mofrsax2(0:nmax),mofrtx2(0:nmax)
  real(8) :: flaiib2(0:nmax),flaiio2(0:nmax),flaiou2(0:nmax),flaiatmos2
  logical :: ok

  nl=3
  do c=1,64
    flpn=mod(c,2)
    ioptmp=mod((c-1)/2,2)
    lnbomp=(/2,3/)
    lntpmpsr=(/1,2/)
    st=0.07d0+0.003d0*c
    flib=0.d0; flio=0.d0; flou=0.d0; he=0.d0
    mofr=0.d0; mofro=0.d0; mofrsa=0.d0; mofrt=0.d0
    mofrox=0.d0; mofrsamp=0.d0; srwampcp=0.d0
    do ln=0,nl
      he(ln)=0.08d0+0.025d0*ln+0.0002d0*c
      mofrsa(ln)=merge(1.d0,0.47d0+0.003d0*ln,ln==0)
      mofr(ln)=merge(0.35d0+0.003d0*c,0.28d0+0.018d0*ln+0.0001d0*c,ln==0)
      mofro(ln)=mofr(ln)-0.012d0
      mofrt(ln)=mofr(ln)+0.014d0
      mofrox(ln)=mofro(ln)+0.002d0
      mofrsamp(ln)=mofrsa(ln)+merge(0.d0,0.05d0,ln>0)
      flib(ln)=0.00015d0*(ln+1)+0.000001d0*c
      flio(ln)=0.00010d0*(nl-ln+1)+0.0000005d0*c
      flou(ln)=0.00020d0*(ln+1)+0.0000007d0*c
    enddo
    do d=1,2
      do ln=1,nl
        srwampcp(d,ln)=0.00020d0*d*ln+0.000001d0*c
      enddo
    enddo
    if (mod(c,4)==0) then
      ! force a shallow saturated barrier to exercise airflow stopping
      mofr(2)=mofrsa(2)-0.5d-8
      mofro(2)=mofr(2)-0.005d0
      mofrt(2)=mofr(2)+0.004d0
    endif

    call project_context(flpn,ioptmp,lnbomp,lntpmpsr,nl,st,flib,flio,flou,he,mofr,mofro,mofrsa,mofrt,mofrox,mofrsamp,srwampcp, &
         floux1,mofrx1,mofrsax1,mofrtx1,flaiib1,flaiio1,flaiou1,flaiatmos1)
    call clobber()
    call project_context(flpn,ioptmp,lnbomp,lntpmpsr,nl,st,flib,flio,flou,he,mofr,mofro,mofrsa,mofrt,mofrox,mofrsamp,srwampcp, &
         floux2,mofrx2,mofrsax2,mofrtx2,flaiib2,flaiio2,flaiou2,flaiatmos2)

    ok = all(floux1(0:nl)==floux2(0:nl)) .and. all(mofrx1(0:nl)==mofrx2(0:nl)) .and. &
         all(mofrsax1(0:nl)==mofrsax2(0:nl)) .and. all(mofrtx1(0:nl)==mofrtx2(0:nl)) .and. &
         all(flaiib1(0:nl)==flaiib2(0:nl)) .and. all(flaiio1(0:nl)==flaiio2(0:nl)) .and. &
         all(flaiou1(0:nl)==flaiou2(0:nl)) .and. flaiatmos1==flaiatmos2
    if (.not.ok) stop 91
    write(*,'(I3,1X,I1,1X,I1,1X,17(ES23.15,1X))') c,flpn,ioptmp, &
         floux1(0),floux1(1),floux1(2),floux1(3),mofrx1(0),mofrx1(1),mofrsax1(1),mofrtx1(1), &
         flaiib1(0),flaiib1(1),flaiio1(0),flaiio1(1),flaiou1(0),flaiou1(1),flaiatmos1,mofrtx1(2),mofrsax1(2)
  enddo
contains
  subroutine project_context(flpn,ioptmp,lnbomp,lntpmpsr,nl,st,flib,flio,flou,he0,mofr0,mofro0,mofrsa0,mofrt0,mofrox0,mofrsamp,srwampcp, &
      floux,mofrx,mofrsax,mofrtx,flaiib,flaiio,flaiou,flaiatmos)
    integer,intent(in)::flpn,ioptmp,nl,lnbomp(2),lntpmpsr(2)
    real(8),intent(in)::st,flib(0:nmax),flio(0:nmax),flou(0:nmax),he0(0:nmax),mofr0(0:nmax),mofro0(0:nmax),mofrsa0(0:nmax),mofrt0(0:nmax)
    real(8),intent(in)::mofrox0(0:nmax),mofrsamp(0:nmax),srwampcp(2,nmax)
    real(8),intent(out)::floux(0:nmax),mofrx(0:nmax),mofrsax(0:nmax),mofrtx(0:nmax),flaiib(0:nmax),flaiio(0:nmax),flaiou(0:nmax),flaiatmos
    real(8)::he(0:nmax),mofr(0:nmax),mofro(0:nmax),mofrsa(0:nmax),mofrt(0:nmax),mofrox(0:nmax),flair(nmax+1)
    real(8)::heorig,mofrorig,mofrtorig,mofrorig_av,rest
    integer::ln,la,lntp
    he=he0; mofr=mofr0; mofro=mofro0; mofrsa=mofrsa0; mofrt=mofrt0; mofrox=mofrox0
    floux=0.d0; mofrx=0.d0; mofrsax=0.d0; mofrtx=0.d0; flaiib=0.d0; flaiio=0.d0; flaiou=0.d0; flair=0.d0

    ! Exact Task-1 GHGponding view needed by the projection.
    if (flpn==1) then
      heorig=he(0); mofrorig_av=mofr(0); mofrorig=mofro(0); mofrtorig=mofrt(0)
      he(0)=mofrorig_av*heorig
      mofr(0)=1.d0
      mofro(0)=max(mofrorig/mofrorig_av,1.d-3)
      mofrt(0)=max(mofrtorig/mofrorig_av,1.d-3)
      mofrsa(0)=1.d0
    endif

    if (ioptmp/=1) then
      do ln=0,nl
        floux(ln)=flou(ln); mofrx(ln)=mofr(ln); mofrox(ln)=mofro(ln); mofrsax(ln)=mofrsa(ln); mofrtx(ln)=mofrt(ln)
      enddo
    else
      do ln=0,nl
        floux(ln)=flou(ln); mofrx(ln)=mofr(ln); mofrsax(ln)=mofrsamp(ln); mofrtx(ln)=mofrt(ln)
      enddo
      lntp=max(1,min(lntpmpsr(1),lntpmpsr(2)))
      do ln=lntp,max(lnbomp(1),lnbomp(2))
        mofrtx(ln)=mofrt(ln)+(srwampcp(1,ln)+srwampcp(2,ln))/he(ln)
        mofrx(ln)=0.5d0*(mofrox(ln)+mofrtx(ln))
        rest=flib(ln)+flio(ln)-(mofrtx(ln)-mofrox(ln))*he(ln)
        floux(ln)=flou(ln)+max(0.d0,rest)
      enddo
      mofrox(0)=mofro(0)
    endif

    la=1
    if (mofro(0)*he(0)>2.d-3 .and. mofrt(0)*he(0)>2.d-3) la=0
    do while (la>0 .and. la<nl .and. mofrsax(la)-mofrx(la)>1.d-7)
      la=la+1
    enddo
    la=max(0,la-1)
    flair(la+1)=0.d0
    do ln=la,1,-1
      flair(ln)=flair(ln+1)+(mofrox(ln)-mofrtx(ln))*he(ln)*st
    enddo
    do ln=la+2,nl
      flair(ln)=0.d0
    enddo
    do ln=1,nl
      flaiib(ln)=max(0.d0,flair(ln))
      flaiio(ln)=-min(0.d0,flair(ln+1))
      flaiou(ln)=max(0.d0,flair(ln+1))
      flaiou(ln)=flaiou(ln)-min(0.d0,flair(ln))
    enddo
    flaiatmos=-min(0.d0,flair(1))
    if (mofr(0)<0.99d0) then
      flaiib(0)=flaiib(1); flaiio(0)=flaiatmos; flaiou(0)=flaiib(1)+flaiatmos
    else
      flaiib(0)=0.d0; flaiio(0)=0.d0; flaiou(0)=0.d0
    endif
  end subroutine
  subroutine clobber()
    real(8)::x(50000)
    integer::j
    do j=1,size(x); x(j)=dble(j)*1.234567890123d0; enddo
    if (x(1)<0.d0) print *,x(size(x))
  end subroutine
end program
