program ttutil_direct_probe
  implicit none
  character(len=512) :: input_file
  character(len=80) :: schema_version
  character(len=80) :: value
  integer :: animo_version
  logical :: rdinqr

  if (command_argument_count() /= 1) then
     write(*,'(A)') 'ERROR=usage: ttutil_direct_probe <TTUTIL-direct-v1-file>'
     stop 2
  end if
  call get_command_argument(1, input_file)

  call messini(.false., .false., 0)
  call rdinit(10, 0, trim(input_file))

  if (.not. rdinqr('SchemaVersion')) then
     write(*,'(A)') 'ERROR=missing SchemaVersion'
     stop 3
  end if
  call rdscha('SchemaVersion', schema_version)
  if (trim(schema_version) /= 'ANIMO5_TTUTIL_DIRECT_V1') then
     write(*,'(A,A)') 'ERROR=unsupported SchemaVersion: ', trim(schema_version)
     stop 3
  end if

  if (.not. rdinqr('AnimoVersion')) then
     write(*,'(A)') 'ERROR=missing AnimoVersion'
     stop 4
  end if
  call rdsint('AnimoVersion', animo_version)
  if (animo_version /= 40 .and. animo_version /= 41) then
     write(*,'(A,I0)') 'ERROR=unsupported AnimoVersion: ', animo_version
     stop 4
  end if

  if (.not. rdinqr('GEN')) then
     write(*,'(A)') 'ERROR=missing mandatory GEN'
     stop 5
  end if

  write(*,'(A)') 'schema=LegacyInputBinding/v1'
  write(*,'(A)') 'adapter_id=TTUTILNativeTextAdapter/v1'
  write(*,'(A,I0)') 'animo_version=', animo_version

  call emit_binding('GEN')
  call emit_binding('MAT')
  call emit_binding('PLA')
  call emit_binding('SOI')
  call emit_binding('BOU')
  call emit_binding('INI')
  call emit_binding('MAN')
  call emit_binding('SWU')
  call emit_binding('WAI')
  call emit_binding('WAU')
  call emit_binding('CHE')
  call emit_binding('INO')
  call emit_binding('CRU')
  call emit_binding('STE')

  if (rdinqr('MES')) then
     call rdscha('MES', value)
     if (len_trim(value) == 0) then
        write(*,'(A)') 'ERROR=empty MES'
        stop 6
     end if
     write(*,'(A)') 'message_output.presence=EXPLICIT'
     write(*,'(A,A)') 'message_output.value=', trim(value)
  else
     write(*,'(A)') 'message_output.presence=DEFAULTED'
     write(*,'(A)') 'message_output.value=message.Out'
  end if

  if (rdinqr('CHE')) then
     write(*,'(A)') 'flag.chempar_selector_present=true'
  else
     write(*,'(A)') 'flag.chempar_selector_present=false'
  end if
  if (rdinqr('STE')) then
     write(*,'(A)') 'flag.soil_temperature_selector_present=true'
  else
     write(*,'(A)') 'flag.soil_temperature_selector_present=false'
  end if

contains

  subroutine emit_binding(name)
    implicit none
    character(len=*), intent(in) :: name
    character(len=80) :: local_value
    logical :: rdinqr
    if (rdinqr(name)) then
       call rdscha(name, local_value)
       write(*,'(A,A,A)') 'binding.', trim(name), '.presence=EXPLICIT'
       write(*,'(A,A,A,A)') 'binding.', trim(name), '.value=', trim(local_value)
    else
       write(*,'(A,A,A)') 'binding.', trim(name), '.presence=INACTIVE_NULL'
       write(*,'(A,A,A)') 'binding.', trim(name), '.value='
    end if
  end subroutine emit_binding

end program ttutil_direct_probe
