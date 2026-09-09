subroutine ghg_phase_kernel(Itask,Ioptmp,LnBoMp,LnTpMpSr,Nl,St,Flib,Flio,Flou,He,Mofr,Mofro,Mofrsa,Mofrt,Mofrox,MofrsaMp,SrWaMpCp,Mofrtx,CapFloux,CapMofrx,CapMofrsax,CapFlaiib,CapFlaiio,CapFlaiou,CapFlaiAtmos)
  implicit none
  integer, parameter :: Manl=50
  integer :: Itask,Ioptmp,LnBoMp(2),LnTpMpSr(2),Nl,La,Ln
  real :: St
  real :: Flib(0:Manl+1),Flio(0:Manl),Flou(0:Manl),He(0:Manl),Mofr(0:Manl),Mofro(0:Manl),Mofrsa(0:Manl),Mofrt(0:Manl)
  real :: Mofrox(0:Manl),MofrsaMp(0:Manl),SrWaMpCp(2,Manl),Mofrtx(0:Manl)
  real :: CapFloux(0:Manl),CapMofrx(0:Manl),CapMofrsax(0:Manl),CapFlaiib(0:Manl),CapFlaiio(0:Manl),CapFlaiou(0:Manl),CapFlaiAtmos
  real :: FlaiAtmos,Flaiib(0:Manl),Flaiio(0:Manl),Flaiou(0:Manl),Flair(Manl+1)
  real :: Floux(0:Manl),Mofrx(0:Manl),Mofrsax(0:Manl)
  goto (1000,2000) Itask
1000 continue
  if (Ioptmp.ne.1) then
    do Ln=0,Nl
      Floux(Ln)=Flou(Ln); Mofrx(Ln)=Mofr(Ln); Mofrox(Ln)=Mofro(Ln); Mofrsax(Ln)=Mofrsa(Ln); Mofrtx(Ln)=Mofrt(Ln)
    enddo
  else
    call GHGMapohydro_k(LnBoMp,LnTpMpSr,Nl,Flib,Flio,Flou,He,Mofr,Mofrox,MofrsaMp,Mofrt,SrWaMpCp,Floux,Mofrx,Mofrsax,Mofrtx)
    Mofrox(0)=Mofro(0)
  endif
  Flair(Nl+1)=0.0
  La=1
  if (Mofro(0)*He(0).gt.2.e-3 .and. Mofrt(0)*He(0).gt.2.e-3) La=0
  do while (La.gt.0.and.La.lt.Nl.and.Mofrsax(La)-Mofrx(La).gt.1.e-7)
    La=La+1
  enddo
  La=max(0,La-1)
  Flair(La+1)=0.0
  do Ln=La,1,-1
    Flair(Ln)=Flair(Ln+1)+(Mofrox(Ln)-Mofrtx(Ln))*He(Ln)*St
  enddo
  do Ln=La+2,Nl
    Flair(Ln)=0.0
  enddo
  do Ln=1,Nl
    Flaiib(Ln)=max(0.0,Flair(Ln)); Flaiio(Ln)=-min(0.0,Flair(Ln+1)); Flaiou(Ln)=max(0.0,Flair(Ln+1)); Flaiou(Ln)=Flaiou(Ln)-min(0.0,Flair(Ln))
  enddo
  FlaiAtmos=-min(0.0,Flair(1))
  if (Mofr(0).lt.0.99) then
    Flaiib(0)=Flaiib(1); Flaiio(0)=FlaiAtmos; Flaiou(0)=Flaiib(1)+FlaiAtmos
  else
    Flaiib(0)=0.0; Flaiio(0)=0.0; Flaiou(0)=0.0
  endif
  return
2000 continue
  CapFloux(0:Nl)=Floux(0:Nl); CapMofrx(0:Nl)=Mofrx(0:Nl); CapMofrsax(0:Nl)=Mofrsax(0:Nl)
  CapFlaiib(0:Nl)=Flaiib(0:Nl); CapFlaiio(0:Nl)=Flaiio(0:Nl); CapFlaiou(0:Nl)=Flaiou(0:Nl); CapFlaiAtmos=FlaiAtmos
end subroutine

subroutine GHGMapohydro_k(LnBoMp,LnTpMpSr,Nl,Flib,Flio,Flou,He,Mofr,Mofrox,MofrsaMp,Mofrt,SrWaMpCp,Floux,Mofrx,Mofrsax,Mofrtx)
  implicit none
  integer, parameter :: Manl=50
  integer :: LnBoMp(2),LnTpMpSr(2),Nl,Ln,LnTp
  real :: Flib(0:Manl+1),Flio(0:Manl),Flou(0:Manl),He(0:Manl),Mofr(0:Manl),Mofrox(0:Manl),MofrsaMp(0:Manl),Mofrt(0:Manl),SrWaMpCp(2,Manl)
  real :: Floux(0:Manl),Mofrx(0:Manl),Mofrsax(0:Manl),Mofrtx(0:Manl),Rest
  do Ln=0,Nl
    Floux(Ln)=Flou(Ln); Mofrx(Ln)=Mofr(Ln); Mofrsax(Ln)=MofrsaMp(Ln); Mofrtx(Ln)=Mofrt(Ln)
  enddo
  LnTp=max(1,min(LnTpMpSr(1),LnTpMpSr(2)))
  do Ln=LnTp,max(LnBoMp(1),LnBoMp(2))
    Mofrtx(Ln)=Mofrt(Ln)+(SrWaMpCp(1,Ln)+SrWaMpCp(2,Ln))/He(Ln)
    Mofrx(Ln)=0.5*(Mofrox(Ln)+Mofrtx(Ln))
    Rest=Flib(Ln)+Flio(Ln)-(Mofrtx(Ln)-Mofrox(Ln))*He(Ln)
    Floux(Ln)=Flou(Ln)+max(0.0,Rest)
  enddo
end subroutine
