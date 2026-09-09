program rc5_probe
  implicit none
  integer, parameter :: manl=50
  integer :: sqnu(0:manl), ioptmp, ipo, kbeg, kend, lnbomp(2), lntp(2), nd
  integer :: itrec(6,50), uoer, err
  real :: avco(0:manl+1), co(0:manl), coaq, coid, cotop, cx(0:manl)
  real :: flev(0:manl), flib(0:manl+1), flid(0:manl), flio(0:manl), flou(0:manl)
  real :: he(0:manl), mofr(0:manl), mofro(0:manl), mofrt(0:manl)
  real :: rekico(0:manl), rekicx(0:manl), rekiso(0:manl), reko(0:manl), rhbd(0:manl)
  real :: rsco(0:manl), rscx(0:manl), se(0:manl), socf(0:manl), st, tito, toin(0:manl), toou(0:manl)
  real :: evicpr, evicirr, evsn, evpn, rupr, prsn, runon, runinu
  logical :: costat(0:manl)
  real :: coirr, comp(2), copryn, flmpinef(2,manl), flmpinpr(2), flmpinrurv(2)
  real :: flmpoudrmp(manl), flmpousoto(2,0:manl), flmpvt(2,manl), prirr, prr
  real :: srwamp(2), srwampold(2), timswi, avcoml(2,manl), avcomp(2), rscomp(2)
  real :: checkpoint_rsco, checkpoint_rscx, reconstructed_cx
  logical :: correct_diag_empty, split_diag_empty, omitted_diag_present

  call reset_all()
  co(1)=2.0e-3
  he(1)=0.25
  rhbd(1)=1300.0
  socf(1)=2.5e-4
  mofro(1)=0.30
  mofrt(1)=0.30
  mofr(1)=0.30
  cx(1)=he(1)*rhbd(1)*socf(1)*co(1)

  ! Step 1: original frozen Transport produces accepted aqueous and adsorbed result.
  open(newunit=uoer,status='scratch',action='readwrite',form='formatted')
  call run_transport('ANIMO-act   ')
  close(uoer)
  checkpoint_rsco=rsco(1)
  checkpoint_rscx=rscx(1)

  ! Uninterrupted continuation: legacy Init-equivalent Cx <- Rscx.
  co(1)=checkpoint_rsco
  cx(1)=checkpoint_rscx
  open(newunit=uoer,status='scratch',action='readwrite',form='formatted')
  call run_transport('ANIMO-act   ')
  correct_diag_empty = stream_empty(uoer)
  close(uoer)

  ! Split continuation: reconstruct Cx from checkpointed aqueous state + immutable inputs.
  co(1)=checkpoint_rsco
  reconstructed_cx=he(1)*rhbd(1)*socf(1)*checkpoint_rsco
  cx(1)=reconstructed_cx
  open(newunit=uoer,status='scratch',action='readwrite',form='formatted')
  call run_transport('ANIMO-act   ')
  split_diag_empty = stream_empty(uoer)
  close(uoer)

  ! Sensitivity: omit reconstructed adsorbed amount.
  co(1)=checkpoint_rsco
  cx(1)=0.0
  open(newunit=uoer,status='scratch',action='readwrite',form='formatted')
  call run_transport('ANIMO-act   ')
  omitted_diag_present = .not. stream_empty(uoer)
  close(uoer)

  print '(A,ES24.16)', 'CHECKPOINT_RSCO=', checkpoint_rsco
  print '(A,ES24.16)', 'CHECKPOINT_RSCX=', checkpoint_rscx
  print '(A,ES24.16)', 'RECONSTRUCTED_CX=', reconstructed_cx
  print '(A,L1)', 'EXACT_RECONSTRUCTION=', reconstructed_cx == checkpoint_rscx
  print '(A,L1)', 'UNINTERRUPTED_DIAGNOSTIC_EMPTY=', correct_diag_empty
  print '(A,L1)', 'SPLIT_DIAGNOSTIC_EMPTY=', split_diag_empty
  print '(A,L1)', 'OMITTED_CX_DIAGNOSTIC_PRESENT=', omitted_diag_present
  if (.not.(reconstructed_cx == checkpoint_rscx .and. correct_diag_empty .and. split_diag_empty .and. omitted_diag_present)) error stop 2

contains
  subroutine reset_all()
    sqnu=0; sqnu(1)=1
    ioptmp=0; ipo=0; kbeg=0; kend=0; lnbomp=0; lntp=0; nd=0; itrec=0
    avco=0.0; co=0.0; coaq=0.0; coid=0.0; cotop=0.0; cx=0.0
    flev=0.0; flib=0.0; flid=0.0; flio=0.0; flou=0.0
    he=0.0; mofr=0.0; mofro=0.0; mofrt=0.0
    rekico=0.0; rekicx=0.0; rekiso=0.0; reko=0.0; rhbd=0.0
    rsco=0.0; rscx=0.0; se=0.0; socf=0.0; st=1.0; tito=1.0; toin=0.0; toou=0.0
    evicpr=0.0; evicirr=0.0; evsn=0.0; evpn=0.0; rupr=0.0; prsn=0.0; runon=0.0; runinu=0.0
    costat=.false.; coirr=0.0; comp=0.0; copryn=0.0; flmpinef=0.0; flmpinpr=0.0; flmpinrurv=0.0
    flmpoudrmp=0.0; flmpousoto=0.0; flmpvt=0.0; prirr=0.0; prr=0.0
    srwamp=0.0; srwampold=0.0; timswi=0.0; avcoml=0.0; avcomp=0.0; rscomp=0.0
  end subroutine

  subroutine run_transport(callsubr)
    character(len=12), intent(in) :: callsubr
    call Transport('AMMONIUM    ',callsubr,0,1,sqnu,uoer,avco,co,coaq,coid,cotop,cx, &
      flev,flib,flid,flio,flou,he,mofr,mofro,mofrt,rekico,rekicx,rekiso,reko,rhbd,rsco,rscx, &
      se,socf,st,tito,toin,toou,evicpr,evicirr,evsn,evpn,rupr,prsn,runon,runinu, &
      ioptmp,ipo,kbeg,kend,lnbomp,lntp,nd,costat,coirr,comp,copryn,flmpinef,flmpinpr,flmpinrurv, &
      flmpoudrmp,flmpousoto,flmpvt,prirr,prr,srwamp,srwampold,timswi,itrec,avcoml,avcomp,rscomp,err)
    if (err /= 0) error stop 3
  end subroutine

  logical function stream_empty(unit)
    integer, intent(in) :: unit
    character(len=512) :: line
    integer :: ios
    rewind(unit)
    read(unit,'(A)',iostat=ios) line
    stream_empty = ios /= 0
  end function
end program

! Dependency stubs deliberately isolate original revision-53 TRANSPORT.FOR.
! MapoTransport is unreachable because Ioptmp=0 and Nd=0 in this probe.
subroutine MapoTransport()
end subroutine MapoTransport

! The concentration solver is replaced by a neutral pass-through so the probe
! tests only Transport's adsorbed-state reconstruction and balance diagnostic.
subroutine Transsub(Substname,Callsubr,Optneg,Ln,Uoer,avc,cb,co,coid,con,fev,fid,flb,flo,fu,ld,mt,mto,rd,reki,reko,rhbd,rsc,socf,st,tito)
  implicit none
  character(len=12) :: Substname, Callsubr
  integer :: Optneg, Ln, Uoer
  real :: avc,cb,co,coid,con,fev,fid,flb,flo,fu,ld,mt,mto,rd,reki,reko,rhbd,rsc,socf,st,tito
  avc = co
  rsc = co
end subroutine Transsub
