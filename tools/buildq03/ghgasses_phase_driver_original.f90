program phase_matrix
 implicit none
 integer,parameter::Manl=50
 integer :: c,Itask,Ioptmp,LnBoMp(2),LnTpMpSr(2),Nl,i
 real :: St
 real :: Flib(0:Manl+1),Flio(0:Manl),Flou(0:Manl),He(0:Manl),Mofr(0:Manl),Mofro(0:Manl),Mofrsa(0:Manl),Mofrt(0:Manl),Mofrox(0:Manl),MofrsaMp(0:Manl),SrWaMpCp(2,Manl),Mofrtx(0:Manl)
 real :: a(0:Manl),b(0:Manl),d(0:Manl),e(0:Manl),f(0:Manl),g(0:Manl),s
 Nl=3; St=0.25; LnBoMp=(/2,3/); LnTpMpSr=(/1,2/)
 do c=0,15
   Ioptmp=mod(c,2)
   Flib=0.;Flio=0.;Flou=0.;He=0.;Mofr=0.;Mofro=0.;Mofrsa=0.;Mofrt=0.;Mofrox=0.;MofrsaMp=0.;SrWaMpCp=0.;Mofrtx=0.;a=0.;b=0.;d=0.;e=0.;f=0.;g=0.;s=0.
   He(0)=0.01+0.003*mod(c/2,2); Mofr(0)=merge(1.0,0.6,mod(c/4,2)==1); Mofro(0)=0.4; Mofrt(0)=merge(0.5,0.1,mod(c/8,2)==1); Mofrsa(0)=1.; MofrsaMp(0)=1.
   do i=1,Nl
      He(i)=0.15+0.02*i; Mofro(i)=0.25+0.01*i; Mofrt(i)=Mofro(i)+0.01*(i-2); Mofr(i)=0.5*(Mofro(i)+Mofrt(i)); Mofrsa(i)=merge(0.52,Mofr(i),i==2 .and. mod(c/2,2)==1); MofrsaMp(i)=0.55; Mofrox(i)=Mofro(i)
      Flib(i)=0.002*i; Flio(i)=0.001*i; Flou(i)=0.0015*i; SrWaMpCp(1,i)=0.0002*i*Ioptmp; SrWaMpCp(2,i)=0.0001*i*Ioptmp
   enddo
   Itask=1; call ghg_phase_kernel(Itask,Ioptmp,LnBoMp,LnTpMpSr,Nl,St,Flib,Flio,Flou,He,Mofr,Mofro,Mofrsa,Mofrt,Mofrox,MofrsaMp,SrWaMpCp,Mofrtx,a,b,d,e,f,g,s)
   call clobber()
   Itask=2; call ghg_phase_kernel(Itask,Ioptmp,LnBoMp,LnTpMpSr,Nl,St,Flib,Flio,Flou,He,Mofr,Mofro,Mofrsa,Mofrt,Mofrox,MofrsaMp,SrWaMpCp,Mofrtx,a,b,d,e,f,g,s)
   write(*,'(I3,1X,I1,1X,7(ES23.15,1X))')c,Ioptmp,sum(a(0:Nl)),sum(b(0:Nl)),sum(d(0:Nl)),sum(e(0:Nl)),sum(f(0:Nl)),sum(g(0:Nl)),s
 enddo
contains
 subroutine clobber(); real::x(50000);integer::j;do j=1,size(x);x(j)=real(j)*2.71828;enddo;if(x(1)<0.)print*,x(size(x));end subroutine
end program
