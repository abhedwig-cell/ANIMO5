program stateq01_rc12_probe
  implicit none
  include 'Param.inc'
  integer :: Iopthyvs,Ipo,Iwa,Flpn,Errornumber
  real :: Avcodiormatop,Avcodiornitop,Avcodiorpotop,Avconhtop,Avconitop,Avcopotop
  real :: Codiormaid,Codiormairr,Codiormarunon,Codiormatop
  real :: Codiorniid,Codiorniirr,Codiornirunon,Codiornitop
  real :: Codiorpoid,Codiorpoirr,Codiorporunon,Codiorpotop
  real :: Coidnh,Coidni,Coidpo,Coirrnh,Coirrni,Coirrpo
  real :: Conh(0:manl),Conhtop,Coni(0:manl),Conitop,Copotop
  real :: Coprnhyn,Coprniyn,Coprpoyn,Corunonnh,Corunonni,Corunonpo
  real :: Cxnh(0:manl),Drdepnhyn,Drdepniyn,Flib(0:manl+1),He(0:manl),Hetop
  real :: Mofro(0:manl),Pn,Snla,Pr,Prirr,Prr,Rhbd(0:manl)
  real :: Rscodiormatop,Rscodiornitop,Rscodiorpotop,Rsconhtop,Rsconitop,Rscopotop
  real :: Runinu,Runon,Rupr,Socfnh(0:manl),St
  real :: Corurvnh,Corurvni,CorurvDOM,CorurvDON,Corurvpo,CorurvDOP,Prsn,Rurv
  real :: init_top(6), cp_top(6), cont_final(6), split_final(6), omitted_final(6)

  init_top = (/ 2.0, 3.0, 4.0, 5.0, 6.0, 7.0 /)

  call setup_common()
  call set_top(init_top)
  call step_once()
  call capture_result(cp_top)
  call promote_result()
  call step_once()
  call capture_result(cont_final)

  call setup_common()
  call set_top(init_top)
  call step_once()
  call capture_result(cp_top)
  call set_top(cp_top)
  call clear_results()
  call step_once()
  call capture_result(split_final)

  call setup_common()
  call set_top(init_top)
  call step_once()
  call set_top((/0.0,0.0,0.0,0.0,0.0,0.0/))
  call clear_results()
  call step_once()
  call capture_result(omitted_final)

  write(*,'(a,6es24.16)') 'CONT_FINAL ', cont_final
  write(*,'(a,6es24.16)') 'SPLIT_FINAL ', split_final
  write(*,'(a,6es24.16)') 'OMITTED_FINAL ', omitted_final
  write(*,'(a,l1)') 'CONT_EQ_SPLIT ', all(cont_final == split_final)
  write(*,'(a,l1)') 'OMITTED_DIFFERS ', any(omitted_final /= cont_final)
  if (.not. all(cont_final == split_final)) stop 21
  if (.not. any(omitted_final /= cont_final)) stop 22

contains

  subroutine setup_common()
    Iopthyvs=1; Ipo=1; Iwa=2; Flpn=0
    Codiormaid=0.2; Codiormairr=0.3; Codiormarunon=0.4
    Codiorniid=0.25; Codiorniirr=0.35; Codiornirunon=0.45
    Codiorpoid=0.15; Codiorpoirr=0.22; Codiorporunon=0.31
    Coidnh=0.7; Coidni=0.8; Coidpo=0.5
    Coirrnh=0.9; Coirrni=1.0; Coirrpo=0.6
    Coprnhyn=1.1; Coprniyn=1.2; Coprpoyn=0.75
    Corunonnh=1.3; Corunonni=1.4; Corunonpo=0.85
    Drdepnhyn=0.0; Drdepniyn=0.0
    Flib=0.0; Flib(1)=0.010
    He=0.2; Hetop=0.05; Mofro=0.25; Rhbd=1.3; Socfnh=0.8
    Pn=0.0; Snla=0.0
    Pr=0.004; Prirr=0.0015; Prr=0.005; Prsn=0.0004
    Runinu=0.0007; Runon=0.0009; Rupr=0.0002; Rurv=0.002
    St=1.0
    Conh=0.0; Coni=0.0; Cxnh=0.0
    Corurvnh=0.0; Corurvni=0.0; CorurvDOM=0.0; CorurvDON=0.0; Corurvpo=0.0; CorurvDOP=0.0
    call clear_results()
  end subroutine setup_common

  subroutine clear_results()
    Avcodiormatop=0.0; Avcodiornitop=0.0; Avcodiorpotop=0.0
    Avconhtop=0.0; Avconitop=0.0; Avcopotop=0.0
    Rscodiormatop=0.0; Rscodiornitop=0.0; Rscodiorpotop=0.0
    Rsconhtop=0.0; Rsconitop=0.0; Rscopotop=0.0
    Errornumber=0
  end subroutine clear_results

  subroutine set_top(v)
    real, intent(in) :: v(6)
    Conhtop=v(1); Conitop=v(2); Codiormatop=v(3); Codiornitop=v(4); Copotop=v(5); Codiorpotop=v(6)
  end subroutine set_top

  subroutine capture_result(v)
    real, intent(out) :: v(6)
    v = (/ Rsconhtop, Rsconitop, Rscodiormatop, Rscodiornitop, Rscopotop, Rscodiorpotop /)
  end subroutine capture_result

  subroutine promote_result()
    Conhtop=Rsconhtop; Conitop=Rsconitop; Codiormatop=Rscodiormatop
    Codiornitop=Rscodiornitop; Copotop=Rscopotop; Codiorpotop=Rscodiorpotop
    call clear_results()
  end subroutine promote_result

  subroutine step_once()
    call UBoundconc(Iopthyvs,Ipo,Iwa,Flpn,Avcodiormatop,Avcodiornitop,Avcodiorpotop, &
      Avconhtop,Avconitop,Avcopotop,Codiormaid,Codiormairr,Codiormarunon,Codiormatop, &
      Codiorniid,Codiorniirr,Codiornirunon,Codiornitop,Codiorpoid,Codiorpoirr, &
      Codiorporunon,Codiorpotop,Coidnh,Coidni,Coidpo,Coirrnh,Coirrni,Coirrpo,Conh, &
      Conhtop,Coni,Conitop,Copotop,Coprnhyn,Coprniyn,Coprpoyn,Corunonnh,Corunonni, &
      Corunonpo,Cxnh,Drdepnhyn,Drdepniyn,Flib,He,Hetop,Mofro,Pn,Snla,Pr,Prirr,Prr, &
      Rhbd,Rscodiormatop,Rscodiornitop,Rscodiorpotop,Rsconhtop,Rsconitop,Rscopotop, &
      Runinu,Runon,Rupr,Socfnh,St,Corurvnh,Corurvni,CorurvDOM,CorurvDON,Corurvpo, &
      CorurvDOP,Prsn,Rurv,Errornumber)
    if (Errornumber /= 0) stop 20
  end subroutine step_once
end program stateq01_rc12_probe
