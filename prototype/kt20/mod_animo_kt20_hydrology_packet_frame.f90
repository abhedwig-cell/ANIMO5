module mod_animo_kt20_hydrology_packet_frame
  use iso_fortran_env, only: int64, real64
  use mod_animo_hydrology_adapter, only: hydrology_step_t, &
    validate_hydrology_step_explicit, KT05_OK
  implicit none
  private

  character(len=*), parameter, public :: KT20_FRAME_SCHEMA = &
    'ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1'
  character(len=*), parameter, public :: KT20_FRAME_ROLE = &
    'NONPRODUCTION_ADAPTER_INTERCHANGE_NOT_CANONICAL_FORCING_ABI'

  public :: read_kt20_hydrology_packet_frame

contains

  logical function canonical_sha256(value)
    character(len=*), intent(in) :: value
    integer :: i, c
    canonical_sha256 = .false.
    if (len_trim(value) /= 64) return
    do i = 1, 64
      c = iachar(value(i:i))
      if (.not. ((c >= iachar('0') .and. c <= iachar('9')) .or. &
                 (c >= iachar('a') .and. c <= iachar('f')))) return
    end do
    canonical_sha256 = .true.
  end function canonical_sha256

  subroutine read_required_line(unit, value, ok)
    integer, intent(in) :: unit
    character(len=*), intent(out) :: value
    logical, intent(out) :: ok
    integer :: ios
    value = ''
    read(unit,'(A)',iostat=ios) value
    ok = ios == 0
  end subroutine read_required_line

  subroutine read_integer_line(unit, value, ok)
    integer, intent(in) :: unit
    integer, intent(out) :: value
    logical, intent(out) :: ok
    character(len=128) :: line
    integer :: ios
    call read_required_line(unit,line,ok)
    if (.not.ok) return
    read(line,*,iostat=ios) value
    ok = ios == 0
  end subroutine read_integer_line

  subroutine read_real_bits_line(unit, value, ok)
    integer, intent(in) :: unit
    real(real64), intent(out) :: value
    logical, intent(out) :: ok
    character(len=128) :: line
    integer(int64) :: bits
    integer :: ios, i, c
    value = 0.0_real64
    call read_required_line(unit,line,ok)
    if (.not.ok) return
    if (len_trim(line) /= 16) then
      ok = .false.
      return
    end if
    do i=1,16
      c=iachar(line(i:i))
      if (.not. ((c>=iachar('0') .and. c<=iachar('9')) .or. &
                 (c>=iachar('a') .and. c<=iachar('f')))) then
        ok=.false.
        return
      end if
    end do
    read(line,'(Z16)',iostat=ios) bits
    if (ios /= 0) then
      ok=.false.
      return
    end if
    value=transfer(bits,value)
    ok=.true.
  end subroutine read_real_bits_line

  subroutine read_kt20_hydrology_packet_frame(path, packet, typed_step_sha256, ok, reason)
    character(len=*), intent(in) :: path
    type(hydrology_step_t), intent(out) :: packet
    character(len=*), intent(out) :: typed_step_sha256
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    integer :: unit, ios, i, j, flag, status
    character(len=160) :: line
    logical :: line_ok

    packet = hydrology_step_t()
    typed_step_sha256 = ''
    ok = .false.
    reason = 'UNSET'

    open(newunit=unit,file=path,status='old',action='read',iostat=ios)
    if (ios /= 0) then
      reason='KT20_FRAME_OPEN_FAILED'
      return
    end if

    call read_required_line(unit,line,line_ok)
    if (.not.line_ok .or. trim(line)/=KT20_FRAME_SCHEMA) then
      reason='KT20_FRAME_SCHEMA_MISMATCH'; close(unit); return
    end if
    call read_required_line(unit,line,line_ok)
    if (.not.line_ok .or. trim(line)/=KT20_FRAME_ROLE) then
      reason='KT20_FRAME_ROLE_MISMATCH'; close(unit); return
    end if
    call read_required_line(unit,line,line_ok)
    if (.not.line_ok .or. .not.canonical_sha256(trim(line))) then
      reason='KT20_FRAME_INVALID_TYPED_DIGEST'; close(unit); return
    end if
    if (len_trim(line)>len(typed_step_sha256)) then
      reason='KT20_FRAME_DIGEST_OUTPUT_TOO_SHORT'; close(unit); return
    end if
    typed_step_sha256=trim(line)

    call read_required_line(unit,line,line_ok)
    if (.not.line_ok .or. len_trim(line)>len(packet%schema_id)) then
      reason='KT20_FRAME_HYDROLOGY_SCHEMA_INVALID'; close(unit); return
    end if
    packet%schema_id=trim(line)
    call read_required_line(unit,line,line_ok)
    if (.not.line_ok .or. len_trim(line)>len(packet%unit_contract_id)) then
      reason='KT20_FRAME_UNIT_CONTRACT_INVALID'; close(unit); return
    end if
    packet%unit_contract_id=trim(line)

    call read_integer_line(unit,packet%layer_count,line_ok)
    if (.not.line_ok .or. packet%layer_count<=0) then
      reason='KT20_FRAME_LAYER_COUNT_INVALID'; close(unit); return
    end if
    call read_integer_line(unit,packet%drainage_count,line_ok)
    if (.not.line_ok .or. packet%drainage_count<0) then
      reason='KT20_FRAME_DRAINAGE_COUNT_INVALID'; close(unit); return
    end if

    call read_real_bits_line(unit,packet%producer_endpoint_day,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%producer_step_days,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%prr,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%prsn,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%prirr,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evicpr,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evicirr,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evsn,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evso,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evpn,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evsoma,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%evtrma,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%runon,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%runoff,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%groundwater_level,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%ponding_end,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%snow_storage_end,line_ok); if(.not.line_ok) goto 900
    call read_real_bits_line(unit,packet%water_balance_aeration,line_ok); if(.not.line_ok) goto 900

    call read_integer_line(unit,flag,line_ok)
    if(.not.line_ok .or. (flag/=0 .and. flag/=1)) goto 900
    packet%has_interception_storage_end=flag==1
    call read_real_bits_line(unit,packet%interception_storage_end,line_ok); if(.not.line_ok) goto 900
    if(.not.packet%has_interception_storage_end) packet%interception_storage_end=0.0_real64

    call read_integer_line(unit,flag,line_ok)
    if(.not.line_ok .or. (flag/=0 .and. flag/=1)) goto 900
    packet%has_soil_temperature=flag==1

    allocate(packet%sc(packet%layer_count),packet%mofrt(packet%layer_count), &
      packet%flev(packet%layer_count),packet%flab(packet%layer_count+1), &
      packet%fldr(packet%drainage_count,packet%layer_count))
    if(packet%has_soil_temperature) then
      allocate(packet%soil_temperature(packet%layer_count))
    else
      allocate(packet%soil_temperature(0))
    end if

    do i=1,packet%layer_count
      call read_real_bits_line(unit,packet%sc(i),line_ok); if(.not.line_ok) goto 900
    end do
    do i=1,packet%layer_count
      call read_real_bits_line(unit,packet%mofrt(i),line_ok); if(.not.line_ok) goto 900
    end do
    do i=1,packet%layer_count
      call read_real_bits_line(unit,packet%flev(i),line_ok); if(.not.line_ok) goto 900
    end do
    do i=1,packet%layer_count+1
      call read_real_bits_line(unit,packet%flab(i),line_ok); if(.not.line_ok) goto 900
    end do
    do i=1,packet%drainage_count
      do j=1,packet%layer_count
        call read_real_bits_line(unit,packet%fldr(i,j),line_ok); if(.not.line_ok) goto 900
      end do
    end do
    if(packet%has_soil_temperature) then
      do i=1,packet%layer_count
        call read_real_bits_line(unit,packet%soil_temperature(i),line_ok); if(.not.line_ok) goto 900
      end do
    end if

    call read_required_line(unit,line,line_ok)
    if(.not.line_ok .or. trim(line)/='END_ANIMO_KT20_HYDROLOGY_PACKET_FRAME_V1') then
      reason='KT20_FRAME_FOOTER_MISMATCH'; close(unit); return
    end if
    read(unit,'(A)',iostat=ios) line
    if(ios==0) then
      reason='KT20_FRAME_TRAILING_CONTENT'; close(unit); return
    end if
    close(unit)

    call validate_hydrology_step_explicit(packet,status)
    if(status/=KT05_OK) then
      reason='KT20_FRAME_DECODED_PACKET_INVALID'
      return
    end if

    ok=.true.
    reason='KT20_HYDROLOGY_PACKET_FRAME_DECODED'
    return

900 continue
    reason='KT20_FRAME_BINARY_PAYLOAD_INVALID'
    close(unit)
  end subroutine read_kt20_hydrology_packet_frame

end module mod_animo_kt20_hydrology_packet_frame
