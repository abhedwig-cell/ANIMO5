program ttutil_material_probe_typed_double
  implicit none
  character(len=512) :: input_file
  character(len=80) :: schema_version
  integer :: ipo,nm,nf,ifnd
  double precision,allocatable :: fror(:),frnh(:),frni(:),recfav(:),hufros(:),ratio(:),asfa(:),nifr(:),fr(:),frca(:)
  double precision :: cfracom,recfexav,hufrosex,asfaex,nifrex,pofrex,recfcaav,sdofr,asfaca
  double precision :: recfsdoav,asfasdo,recfhuav,recfhusdoav,asfahu,nifrhuma,pofrhuma,recfntav,recfdeav,frhetero
  logical :: rdinqr

  if (command_argument_count()/=1) stop 2
  call get_command_argument(1,input_file)
  call messini(.false.,.false.,0)
  call rdinit(10,0,trim(input_file))
  if (.not.rdinqr('SchemaVersion')) stop 3
  call rdscha('SchemaVersion',schema_version)
  if (trim(schema_version)/='ANIMO5_TTUTIL_MATERIAL_V1') stop 3
  call rdsint('IPO',ipo); call rdsint('Nm',nm); call rdsint('Nf',nf)
  allocate(fror(nm),frnh(nm),frni(nm),recfav(nf),hufros(nf),ratio(nf),asfa(nf),nifr(nf),fr(nm*nf),frca(nm*nf))
  call need('Fror',fror,nm); call need('Frnh',frnh,nm); call need('Frni',frni,nm)
  call rdsdou('Cfracom',cfracom)
  call need('Recfav',recfav,nf); call need('Hufros',hufros,nf); call need('RatioRdSt',ratio,nf); call need('Asfa',asfa,nf); call need('Nifr',nifr,nf)
  call rdsdou('Recfexav',recfexav); call rdsdou('Hufrosex',hufrosex); call rdsdou('Asfaex',asfaex); call rdsdou('Nifrex',nifrex); call rdsdou('Pofrex',pofrex)
  call rdsdou('Recfcaav',recfcaav); call rdsdou('SDOfr',sdofr); call rdsdou('Asfaca',asfaca)
  call rdsdou('RecfSDOav',recfsdoav); call rdsdou('AsfaSDO',asfasdo)
  call rdsdou('RecfHUav',recfhuav); call rdsdou('RecfHUSDOav',recfhusdoav); call rdsdou('AsfaHU',asfahu); call rdsdou('Nifrhuma',nifrhuma); call rdsdou('Pofrhuma',pofrhuma)
  call rdsdou('Recfntav',recfntav); call rdsdou('Recfdeav',recfdeav); call rdsdou('Frhetero',frhetero)
  call need('FR',fr,nm*nf); call need('FRca',frca,nm*nf)

  write(*,'(A)') 'schema=MaterialParameterSet/v1'; write(*,'(A)') 'adapter_id=TTUTILNativeMaterialAdapter/v1'
  write(*,'(A,I0)') 'IPO=',ipo; write(*,'(A,I0)') 'Nm=',nm; write(*,'(A,I0)') 'Nf=',nf
  call emits('Cfracom',cfracom); call emits('Recfexav',recfexav); call emits('Hufrosex',hufrosex); call emits('Asfaex',asfaex); call emits('Nifrex',nifrex); call emits('Pofrex',pofrex)
  call emits('Recfcaav',recfcaav); call emits('SDOfr',sdofr); call emits('Asfaca',asfaca); call emits('RecfSDOav',recfsdoav); call emits('AsfaSDO',asfasdo)
  call emits('RecfHUav',recfhuav); call emits('RecfHUSDOav',recfhusdoav); call emits('AsfaHU',asfahu); call emits('Nifrhuma',nifrhuma); call emits('Pofrhuma',pofrhuma)
  call emits('Recfntav',recfntav); call emits('Recfdeav',recfdeav); call emits('Frhetero',frhetero)
  call emita('Fror',fror,nm); call emita('Frnh',frnh,nm); call emita('Frni',frni,nm); call emita('Recfav',recfav,nf); call emita('Hufros',hufros,nf)
  call emita('RatioRdSt',ratio,nf); call emita('Asfa',asfa,nf); call emita('Nifr',nifr,nf); call emita('FR',fr,nm*nf); call emita('FRca',frca,nm*nf)
contains
  subroutine need(name,x,n)
    character(len=*),intent(in)::name; integer,intent(in)::n; double precision,intent(out)::x(n); integer::found
    call rdadou(name,x,n,found)
    if(found/=n) stop 6
  end subroutine
  subroutine emits(name,x)
    character(len=*),intent(in)::name; double precision,intent(in)::x
    write(*,'(A,A,ES25.17E3)') trim(name),'=',x
  end subroutine
  subroutine emita(name,x,n)
    character(len=*),intent(in)::name; integer,intent(in)::n; double precision,intent(in)::x(n); integer::i
    write(*,'(A,A)',advance='no') 'array.',trim(name)//'='
    do i=1,n
      if(i>1) write(*,'(A)',advance='no') ' '
      write(*,'(ES25.17E3)',advance='no') x(i)
    end do
    write(*,*)
  end subroutine
end program
