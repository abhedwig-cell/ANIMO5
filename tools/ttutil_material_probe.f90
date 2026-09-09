program ttutil_material_probe
  implicit none
  character(len=512) :: input_file
  character(len=80) :: schema_version
  integer :: ipo, nm, nf
  double precision, allocatable :: fror(:), frnh(:), frni(:)
  double precision, allocatable :: recfav(:), hufros(:), ratio(:), asfa(:), nifr(:)
  double precision, allocatable :: fr(:), frca(:)
  double precision :: cfracom
  double precision :: recfexav,hufrosex,asfaex,nifrex,pofrex
  double precision :: recfcaav,sdofr,asfaca,recfsdoav,asfasdo
  double precision :: recfhuav,recfhusdoav,asfahu,nifrhuma,pofrhuma
  double precision :: recfntav,recfdeav,frhetero
  logical :: rdinqr

  if (command_argument_count() /= 1) then
    write(*,'(A)') 'ERROR=usage: ttutil_material_probe <TTUTIL-material-v1-file>'
    stop 2
  end if
  call get_command_argument(1,input_file)
  call messini(.false.,.false.,0)
  call rdinit(10,0,trim(input_file))

  if (.not. rdinqr('SchemaVersion')) then
    write(*,'(A)') 'ERROR=missing SchemaVersion'; stop 3
  end if
  call rdscha('SchemaVersion',schema_version)
  if (trim(schema_version) /= 'ANIMO5_TTUTIL_MATERIAL_V1') then
    write(*,'(A,A)') 'ERROR=unsupported SchemaVersion: ',trim(schema_version); stop 3
  end if
  call rdsint('IPO',ipo); call rdsint('Nm',nm); call rdsint('Nf',nf)
  if (ipo /= 0 .or. nm < 1 .or. nf < 1) then
    write(*,'(A)') 'ERROR=Pilot B requires IPO=0 and positive Nm/Nf'; stop 4
  end if
  allocate(fror(nm),frnh(nm),frni(nm),recfav(nf),hufros(nf),ratio(nf),asfa(nf),nifr(nf),fr(nm*nf),frca(nm*nf))

  call need_char_array_real8('Fror',fror,nm); call need_char_array_real8('Frnh',frnh,nm); call need_char_array_real8('Frni',frni,nm)
  call need_char_real8('Cfracom',cfracom)
  call need_char_array_real8('Recfav',recfav,nf); call need_char_array_real8('Hufros',hufros,nf)
  call need_char_array_real8('RatioRdSt',ratio,nf); call need_char_array_real8('Asfa',asfa,nf); call need_char_array_real8('Nifr',nifr,nf)
  call need_char_real8('Recfexav',recfexav); call need_char_real8('Hufrosex',hufrosex); call need_char_real8('Asfaex',asfaex)
  call need_char_real8('Nifrex',nifrex); call need_char_real8('Pofrex',pofrex)
  call need_char_real8('Recfcaav',recfcaav); call need_char_real8('SDOfr',sdofr); call need_char_real8('Asfaca',asfaca)
  call need_char_real8('RecfSDOav',recfsdoav); call need_char_real8('AsfaSDO',asfasdo)
  call need_char_real8('RecfHUav',recfhuav); call need_char_real8('RecfHUSDOav',recfhusdoav); call need_char_real8('AsfaHU',asfahu)
  call need_char_real8('Nifrhuma',nifrhuma); call need_char_real8('Pofrhuma',pofrhuma)
  call need_char_real8('Recfntav',recfntav); call need_char_real8('Recfdeav',recfdeav); call need_char_real8('Frhetero',frhetero)
  call need_char_array_real8('FR',fr,nm*nf); call need_char_array_real8('FRca',frca,nm*nf)

  write(*,'(A)') 'schema=MaterialParameterSet/v1'
  write(*,'(A)') 'adapter_id=TTUTILNativeMaterialAdapter/v1'
  write(*,'(A,I0)') 'IPO=',ipo; write(*,'(A,I0)') 'Nm=',nm; write(*,'(A,I0)') 'Nf=',nf
  call emit_scalar('Cfracom',cfracom)
  call emit_scalar('Recfexav',recfexav); call emit_scalar('Hufrosex',hufrosex); call emit_scalar('Asfaex',asfaex); call emit_scalar('Nifrex',nifrex); call emit_scalar('Pofrex',pofrex)
  call emit_scalar('Recfcaav',recfcaav); call emit_scalar('SDOfr',sdofr); call emit_scalar('Asfaca',asfaca)
  call emit_scalar('RecfSDOav',recfsdoav); call emit_scalar('AsfaSDO',asfasdo)
  call emit_scalar('RecfHUav',recfhuav); call emit_scalar('RecfHUSDOav',recfhusdoav); call emit_scalar('AsfaHU',asfahu); call emit_scalar('Nifrhuma',nifrhuma); call emit_scalar('Pofrhuma',pofrhuma)
  call emit_scalar('Recfntav',recfntav); call emit_scalar('Recfdeav',recfdeav); call emit_scalar('Frhetero',frhetero)
  call emit_array('Fror',fror,nm); call emit_array('Frnh',frnh,nm); call emit_array('Frni',frni,nm)
  call emit_array('Recfav',recfav,nf); call emit_array('Hufros',hufros,nf); call emit_array('RatioRdSt',ratio,nf); call emit_array('Asfa',asfa,nf); call emit_array('Nifr',nifr,nf)
  call emit_array('FR',fr,nm*nf); call emit_array('FRca',frca,nm*nf)

contains
  subroutine need_char_real8(name,x)
    implicit none
    character(len=*),intent(in)::name
    double precision,intent(out)::x
    character(len=80)::token
    integer::ios
    logical::rdinqr
    if (.not. rdinqr(name)) then
      write(*,'(A,A)') 'ERROR=missing ',trim(name); stop 5
    end if
    call rdscha(name,token)
    read(token,*,iostat=ios) x
    if (ios /= 0) then
      write(*,'(A,A)') 'ERROR=invalid numeric token ',trim(name); stop 6
    end if
  end subroutine
  subroutine need_char_array_real8(name,x,n)
    implicit none
    character(len=*),intent(in)::name
    integer,intent(in)::n
    double precision,intent(out)::x(n)
    character(len=80),allocatable::token(:)
    integer::found,i,ios
    logical::rdinqr
    allocate(token(n))
    if (.not. rdinqr(name)) then
      write(*,'(A,A)') 'ERROR=missing ',trim(name); stop 5
    end if
    call rdacha(name,token,n,found)
    if (found /= n) then
      write(*,'(A,A,A,I0,A,I0)') 'ERROR=',trim(name),' count ',found,' expected ',n; stop 6
    end if
    do i=1,n
      read(token(i),*,iostat=ios) x(i)
      if (ios /= 0) then
        write(*,'(A,A,A,I0)') 'ERROR=invalid numeric token ',trim(name),' index ',i; stop 6
      end if
    end do
    deallocate(token)
  end subroutine
  subroutine emit_scalar(name,x)
    implicit none
    character(len=*),intent(in)::name
    double precision,intent(in)::x
    write(*,'(A,A,ES25.17E3)') trim(name),'=',x
  end subroutine
  subroutine emit_array(name,x,n)
    implicit none
    character(len=*),intent(in)::name
    integer,intent(in)::n
    double precision,intent(in)::x(n)
    integer::i
    write(*,'(A,A)',advance='no') 'array.',trim(name)//'='
    do i=1,n
      if (i>1) write(*,'(A)',advance='no') ' '
      write(*,'(ES25.17E3)',advance='no') x(i)
    end do
    write(*,*)
  end subroutine
end program
