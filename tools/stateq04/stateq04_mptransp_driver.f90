program stateq04_mptransp_driver
  implicit none
  include 'param.inc'
  character(len=32) :: mode, species_arg
  character(len=256) :: checkpoint_path, trace_path
  character(len=12) :: substname, callsubr
  integer :: argc, split_step, start_step, end_step, s, ucp, utr, ios
  integer :: ipo, k, kbeg, kend, maxiter, nd, nl, uoer, flpn
  integer :: lnbomp(2), lntpmpsr(2), sqnu(0:Manl), itrec(6,50)
  logical :: costat(0:Manl)
  real :: avco(0:Manl), coirr, comp(2), copryn, cotemp(0:Manl), cotop
  real :: flmpinef(2,Manl), flmpinpr(2), flmpinrurv(2)
  real :: flmpoudrmp(Manl), flmpousoto(2,0:Manl), flmpvt(2,Manl)
  real :: he(0:Manl), prirr, prr, reko(0:Manl), srwamp(2), srwampold(2)
  real :: st, timswi, tito, avcomp(2), avcoml(2,Manl), mpreko(0:Manl)
  real :: rscomp(2), toin(0:Manl), basec, basetop
  integer(8) :: magic
  integer :: cp_version, cp_step

  argc = command_argument_count()
  if (argc < 4) then
    write(*,*) 'usage: driver MODE SPECIES CHECKPOINT TRACE'
    stop 2
  endif
  call get_command_argument(1, mode)
  call get_command_argument(2, species_arg)
  call get_command_argument(3, checkpoint_path)
  call get_command_argument(4, trace_path)

  call configure_species(trim(species_arg), substname, basec, basetop)
  callsubr = 'ANIMO-act   '
  ipo = 1
  nd = 2
  nl = 2
  uoer = 99
  flpn = 0
  kbeg = 1
  kend = 2
  maxiter = 50
  lnbomp = (/2,2/)
  lntpmpsr = (/1,1/)
  sqnu = 0
  sqnu(1)=1
  sqnu(2)=2
  costat = .true.
  he = 0.1d0
  st = 1.0d0
  prirr = 0.0d0
  cotop = 0.0d0
  coirr = 0.0d0
  timswi = -999.0d0
  itrec = 0
  split_step = 5
  magic = int(z'5354513034544344', kind=8)  ! STQ04TCD
  cp_version = 1

  open(unit=uoer, file='stateq04_mptransp_warnings.log', status='replace', action='write')
  open(newunit=utr, file=trim(trace_path), access='stream', form='unformatted', &
       status='replace', action='write')

  select case (trim(mode))
  case ('continuous')
    comp = (/basec, basec*1.35d0/)
    rscomp = comp
    srwampold = (/0.010d0, 0.008d0/)
    start_step = 1
    end_step = 10
  case ('stageA')
    comp = (/basec, basec*1.35d0/)
    rscomp = comp
    srwampold = (/0.010d0, 0.008d0/)
    start_step = 1
    end_step = split_step
  case ('stageB-good','stageB-nativebad')
    open(newunit=ucp, file=trim(checkpoint_path), access='stream', form='unformatted', &
         status='old', action='read', iostat=ios)
    if (ios /= 0) stop 20
    read(ucp) magic
    if (magic /= int(z'5354513034544344', kind=8)) stop 21
    read(ucp) cp_version
    if (cp_version /= 1) stop 22
    read(ucp) cp_step
    if (cp_step /= split_step) stop 23
    read(ucp) comp
    read(ucp) srwampold
    close(ucp)
    if (trim(mode) == 'stageB-good') then
      ! Candidate restore transaction: accepted owner is restored first and the
      ! non-owner result alias is initialized from that accepted coordinate.
      rscomp = comp
    else
      ! Causal negative: emulate the revision-53 first resumed Init promotion
      ! when RsCoMp has no restart representation.
      rscomp = 0.0d0
      comp = rscomp
    endif
    timswi = dble(split_step)
    start_step = split_step + 1
    end_step = 10
  case ('inactive')
    comp = (/basec, basec*1.35d0/)
    rscomp = comp
    srwampold = (/0.010d0, 0.008d0/)
    do s=1,10
      call write_trace(utr, s, comp, rscomp, srwampold, (/0.0d0,0.0d0/), &
                       (/0.0d0,0.0d0/), (/0.0d0,0.0d0/))
    enddo
    close(utr); close(uoer)
    stop 0
  case default
    stop 3
  end select

  do s = start_step, end_step
    call configure_step(s, basec, basetop, nl, avco, cotemp, copryn, prr, &
         flmpinef, flmpinpr, flmpinrurv, flmpoudrmp, flmpousoto, flmpvt, &
         srwampold, srwamp)
    reko = 0.0d0
    toin = 0.0d0
    mpreko = 0.0d0
    avcomp = 0.0d0
    avcoml = 0.0d0
    k = kbeg
    tito = dble(s)

    call MPTRANSP(1,substname,callsubr,flpn,ipo,k,kbeg,kend,lnbomp, &
         lntpmpsr,maxiter,nd,nl,sqnu,uoer,costat,avco,coirr,comp,copryn, &
         cotemp,cotop,flmpinef,flmpinpr,flmpinrurv,flmpoudrmp,flmpousoto, &
         flmpvt,he,prirr,prr,reko,srwamp,srwampold,st,timswi,tito, &
         itrec,avcomp,avcoml,mpreko,rscomp,toin)

    call MPTRANSP(2,substname,callsubr,flpn,ipo,k,kbeg,kend,lnbomp, &
         lntpmpsr,maxiter,nd,nl,sqnu,uoer,costat,avco,coirr,comp,copryn, &
         cotemp,cotop,flmpinef,flmpinpr,flmpinrurv,flmpoudrmp,flmpousoto, &
         flmpvt,he,prirr,prr,reko,srwamp,srwampold,st,timswi,tito, &
         itrec,avcomp,avcoml,mpreko,rscomp,toin)

    k = kbeg
    call MPTRANSP(3,substname,callsubr,flpn,ipo,k,kbeg,kend,lnbomp, &
         lntpmpsr,maxiter,nd,nl,sqnu,uoer,costat,avco,coirr,comp,copryn, &
         cotemp,cotop,flmpinef,flmpinpr,flmpinrurv,flmpoudrmp,flmpousoto, &
         flmpvt,he,prirr,prr,reko,srwamp,srwampold,st,timswi,tito, &
         itrec,avcomp,avcoml,mpreko,rscomp,toin)

    ! Accepted boundary promotion.
    comp = rscomp
    srwampold = srwamp
    call write_trace(utr, s, comp, rscomp, srwampold, avcomp, &
                     (/mpreko(1),mpreko(2)/), (/toin(1),toin(2)/))
  enddo

  if (trim(mode) == 'stageA') then
    open(newunit=ucp, file=trim(checkpoint_path), access='stream', form='unformatted', &
         status='replace', action='write')
    write(ucp) magic
    write(ucp) cp_version
    write(ucp) split_step
    write(ucp) comp
    write(ucp) srwampold
    close(ucp)
  endif

  close(utr)
  close(uoer)
contains
  subroutine configure_species(arg, name, c0, ctop)
    character(len=*), intent(in) :: arg
    character(len=12), intent(out) :: name
    real, intent(out) :: c0, ctop
    select case (trim(arg))
    case ('DOM'); name='Sol.Org.Mat '; c0=1.10d0; ctop=0.75d0
    case ('DON'); name='Sol.Org.Nit '; c0=0.12d0; ctop=0.08d0
    case ('NH4'); name='AMMONIUM    '; c0=0.045d0; ctop=0.025d0
    case ('NO3'); name='NITRATE     '; c0=0.090d0; ctop=0.055d0
    case ('DOP'); name='Sol.Org.Pho '; c0=0.018d0; ctop=0.010d0
    case ('PO4'); name='PHOSPHORUS  '; c0=0.030d0; ctop=0.016d0
    case default; stop 4
    end select
  end subroutine

  subroutine configure_step(step, c0, ctop0, nl_, avco_, cotemp_, copryn_, prr_, &
       fin, fpr, fru, fdr, fout, fvt, sold, snew)
    integer, intent(in) :: step, nl_
    real, intent(in) :: c0, ctop0, sold(2)
    real, intent(out) :: avco_(0:Manl), cotemp_(0:Manl), copryn_, prr_
    real, intent(out) :: fin(2,Manl), fpr(2), fru(2), fdr(Manl)
    real, intent(out) :: fout(2,0:Manl), fvt(2,Manl), snew(2)
    real :: in1, out1, in2, out2, scale
    avco_ = 0.0d0
    cotemp_ = 0.0d0
    fin = 0.0d0; fpr=0.0d0; fru=0.0d0; fdr=0.0d0
    fout=0.0d0; fvt=0.0d0
    scale = 1.0d0 + 0.015d0*dble(step)
    avco_(1) = c0*(0.60d0 + 0.01d0*dble(step))
    avco_(2) = c0*(1.20d0 - 0.005d0*dble(step))
    cotemp_ = avco_
    copryn_ = ctop0*scale
    prr_ = 0.002d0

    fpr(1) = 0.00042d0 + 0.00001d0*dble(mod(step,3))
    fru(1) = 0.00003d0
    fin(1,2) = 0.00004d0 + 0.000005d0*dble(mod(step,2))
    fout(1,1) = 0.00014d0
    fout(1,2) = 0.00011d0
    fdr(1) = 0.00005d0
    fvt(1,1) = fpr(1) + fru(1)
    in1 = fvt(1,1) + fin(1,1) + fin(1,2)
    out1 = fout(1,1) + fout(1,2) + fdr(1) + fdr(2)
    snew(1) = sold(1) + in1 - out1

    fpr(2) = 0.00024d0 + 0.000005d0*dble(mod(step,4))
    fru(2) = 0.00002d0
    fin(2,1) = 0.000035d0
    fout(2,1) = 0.00010d0
    fout(2,2) = 0.00008d0
    fvt(2,1) = fpr(2) + fru(2)
    in2 = fvt(2,1) + fin(2,1) + fin(2,2)
    out2 = fout(2,1) + fout(2,2)
    snew(2) = sold(2) + in2 - out2
  end subroutine

  subroutine write_trace(unit, step, cacc, cres, sw, avc, mr, ti)
    integer, intent(in) :: unit, step
    real, intent(in) :: cacc(2), cres(2), sw(2), avc(2), mr(2), ti(2)
    write(unit) step
    write(unit) cacc
    write(unit) cres
    write(unit) sw
    write(unit) avc
    write(unit) mr
    write(unit) ti
  end subroutine
end program
