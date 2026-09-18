module mod_animo_static_boundary_chemistry_adapter
  use iso_fortran_env, only: real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  private

  integer, parameter, public :: BOUNDQ01_OK = 0
  integer, parameter, public :: BOUNDQ01_ERR_OPEN = 1
  integer, parameter, public :: BOUNDQ01_ERR_LABEL = 2
  integer, parameter, public :: BOUNDQ01_ERR_READ = 3
  integer, parameter, public :: BOUNDQ01_ERR_OPTION = 4
  integer, parameter, public :: BOUNDQ01_ERR_RANGE = 5
  integer, parameter, public :: BOUNDQ01_ERR_ARGUMENT = 6

  character(len=*), parameter, public :: BOUNDQ01_SCHEMA = &
    'ANIMO_REV53_STATIC_BOUNDARY_CHEMISTRY_V1'

  type, public :: four_channel_chemistry_t
    real(real64) :: nh = 0.0_real64
    real(real64) :: ni = 0.0_real64
    real(real64) :: doma = 0.0_real64
    real(real64) :: don = 0.0_real64
  end type four_channel_chemistry_t

  type, extends(four_channel_chemistry_t), public :: six_channel_chemistry_t
    real(real64) :: po = 0.0_real64
    real(real64) :: dop = 0.0_real64
  end type six_channel_chemistry_t

  type, public :: static_boundary_chemistry_t
    character(len=48) :: schema_id = ''
    integer :: nuyr = 0
    logical :: phosphorus_enabled = .false.
    integer :: ioptidti = -1
    integer :: ioptirti = -1
    real(real64), allocatable :: precipitation_nh(:)
    real(real64), allocatable :: precipitation_ni(:)
    real(real64), allocatable :: precipitation_po(:)
    real(real64), allocatable :: dry_deposition_nh(:)
    real(real64), allocatable :: dry_deposition_ni(:)
    type(six_channel_chemistry_t) :: runon
    type(six_channel_chemistry_t) :: irrigation
    type(six_channel_chemistry_t) :: runin
  end type static_boundary_chemistry_t

  public :: read_rev53_static_boundary_chemistry
  public :: validate_rev53_static_boundary_chemistry

contains

  subroutine read_rev53_static_boundary_chemistry(path, nuyr, ipo, value, status)
    character(len=*), intent(in) :: path
    integer, intent(in) :: nuyr, ipo
    type(static_boundary_chemistry_t), intent(out) :: value
    integer, intent(out) :: status

    integer :: unit, ios
    real(real64) :: run_nh, run_ni, run_po, run_doma, run_don, run_dop
    real(real64) :: irr_nh, irr_ni, irr_po, irr_doma, irr_don, irr_dop
    real(real64) :: in_nh, in_ni, in_po, in_doma, in_don, in_dop

    value = static_boundary_chemistry_t()
    status = BOUNDQ01_OK

    if (nuyr <= 0 .or. (ipo /= 0 .and. ipo /= 1)) then
      status = BOUNDQ01_ERR_ARGUMENT
      return
    end if

    value%schema_id = BOUNDQ01_SCHEMA
    value%nuyr = nuyr
    value%phosphorus_enabled = ipo == 1
    allocate(value%precipitation_nh(nuyr), value%precipitation_ni(nuyr))
    allocate(value%dry_deposition_nh(nuyr), value%dry_deposition_ni(nuyr))
    if (ipo == 1) then
      allocate(value%precipitation_po(nuyr))
    else
      allocate(value%precipitation_po(0))
    end if

    open(newunit=unit, file=path, status='old', action='read', iostat=ios)
    if (ios /= 0) then
      status = BOUNDQ01_ERR_OPEN
      return
    end if

    call find_first_label(unit, '>optibc:', status)
    if (status /= BOUNDQ01_OK) then
      close(unit)
      return
    end if
    read(unit, *, iostat=ios) value%ioptidti, value%ioptirti
    if (ios /= 0) then
      status = BOUNDQ01_ERR_READ
      close(unit)
      return
    end if
    if (value%ioptidti /= 0 .or. value%ioptirti /= 0) then
      status = BOUNDQ01_ERR_OPTION
      close(unit)
      return
    end if

    call find_first_label(unit, '>topbou:', status)
    if (status /= BOUNDQ01_OK) then
      close(unit)
      return
    end if

    read(unit, *, iostat=ios) value%precipitation_nh
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    read(unit, *, iostat=ios) value%precipitation_ni
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    if (ipo == 1) then
      read(unit, *, iostat=ios) value%precipitation_po
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if

    read(unit, *, iostat=ios) value%dry_deposition_nh
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    read(unit, *, iostat=ios) value%dry_deposition_ni
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if

    read(unit, *, iostat=ios) run_nh, run_ni
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    run_po = 0.0_real64
    if (ipo == 1) then
      read(unit, *, iostat=ios) run_po
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if
    read(unit, *, iostat=ios) run_doma, run_don
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    run_dop = 0.0_real64
    if (ipo == 1) then
      read(unit, *, iostat=ios) run_dop
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if

    read(unit, *, iostat=ios) irr_nh, irr_ni
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    irr_po = 0.0_real64
    if (ipo == 1) then
      read(unit, *, iostat=ios) irr_po
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if
    read(unit, *, iostat=ios) irr_doma, irr_don
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    irr_dop = 0.0_real64
    if (ipo == 1) then
      read(unit, *, iostat=ios) irr_dop
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if

    call find_first_label(unit, '>latbou:', status)
    if (status /= BOUNDQ01_OK) then
      close(unit)
      return
    end if

    read(unit, *, iostat=ios) in_nh, in_ni
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    in_po = 0.0_real64
    if (ipo == 1) then
      read(unit, *, iostat=ios) in_po
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if
    read(unit, *, iostat=ios) in_doma, in_don
    if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    in_dop = 0.0_real64
    if (ipo == 1) then
      read(unit, *, iostat=ios) in_dop
      if (ios /= 0) then; status=BOUNDQ01_ERR_READ; close(unit); return; end if
    end if

    close(unit)

    value%runon%nh = run_nh
    value%runon%ni = run_ni
    value%runon%doma = run_doma
    value%runon%don = run_don
    value%runon%po = run_po
    value%runon%dop = run_dop

    value%irrigation%nh = irr_nh
    value%irrigation%ni = irr_ni
    value%irrigation%doma = irr_doma
    value%irrigation%don = irr_don
    value%irrigation%po = irr_po
    value%irrigation%dop = irr_dop

    value%runin%nh = in_nh
    value%runin%ni = in_ni
    value%runin%doma = in_doma
    value%runin%don = in_don
    value%runin%po = in_po
    value%runin%dop = in_dop

    call validate_rev53_static_boundary_chemistry(value, status)
  end subroutine read_rev53_static_boundary_chemistry

  subroutine find_first_label(unit, label, status)
    integer, intent(in) :: unit
    character(len=8), intent(in) :: label
    integer, intent(out) :: status
    character(len=512) :: line
    integer :: ios

    rewind(unit)
    status = BOUNDQ01_ERR_LABEL
    do
      read(unit, '(A)', iostat=ios) line
      if (ios /= 0) return
      if (line(1:8) == label) then
        status = BOUNDQ01_OK
        return
      end if
    end do
  end subroutine find_first_label

  subroutine validate_rev53_static_boundary_chemistry(value, status)
    type(static_boundary_chemistry_t), intent(in) :: value
    integer, intent(out) :: status

    status = BOUNDQ01_ERR_RANGE

    if (trim(value%schema_id) /= BOUNDQ01_SCHEMA) return
    if (value%nuyr <= 0) return
    if (value%ioptidti /= 0 .or. value%ioptirti /= 0) return
    if (.not. allocated(value%precipitation_nh) .or. &
        .not. allocated(value%precipitation_ni) .or. &
        .not. allocated(value%precipitation_po) .or. &
        .not. allocated(value%dry_deposition_nh) .or. &
        .not. allocated(value%dry_deposition_ni)) return
    if (size(value%precipitation_nh) /= value%nuyr .or. &
        size(value%precipitation_ni) /= value%nuyr .or. &
        size(value%dry_deposition_nh) /= value%nuyr .or. &
        size(value%dry_deposition_ni) /= value%nuyr) return
    if (value%phosphorus_enabled) then
      if (size(value%precipitation_po) /= value%nuyr) return
    else
      if (size(value%precipitation_po) /= 0) return
    end if

    if (.not. all(ieee_is_finite(value%precipitation_nh)) .or. &
        .not. all(ieee_is_finite(value%precipitation_ni)) .or. &
        .not. all(ieee_is_finite(value%precipitation_po)) .or. &
        .not. all(ieee_is_finite(value%dry_deposition_nh)) .or. &
        .not. all(ieee_is_finite(value%dry_deposition_ni))) return

    if (.not. within(value%precipitation_nh,0.0_real64,1.0_real64)) return
    if (.not. within(value%precipitation_ni,0.0_real64,1.0_real64)) return
    if (value%phosphorus_enabled) then
      if (.not. within(value%precipitation_po,0.0_real64,1.0_real64)) return
    end if
    if (.not. within(value%dry_deposition_nh,0.0_real64,100.0_real64)) return
    if (.not. within(value%dry_deposition_ni,0.0_real64,100.0_real64)) return

    if (.not. six_valid(value%runon, value%phosphorus_enabled, &
        999.0_real64,10.0_real64,10.0_real64)) return
    if (.not. six_valid(value%irrigation, value%phosphorus_enabled, &
        999.0_real64,10.0_real64,10.0_real64)) return
    if (.not. six_valid(value%runin, value%phosphorus_enabled, &
        1.0_real64,10.0_real64,0.1_real64)) return
    ! Legacy lateral DON has the tighter 0..1 source bound.
    if (value%runin%don < 0.0_real64 .or. value%runin%don > 1.0_real64) return

    status = BOUNDQ01_OK
  end subroutine validate_rev53_static_boundary_chemistry

  logical function six_valid(value, phosphorus_enabled, mineral_max, doma_max, dop_max)
    type(six_channel_chemistry_t), intent(in) :: value
    logical, intent(in) :: phosphorus_enabled
    real(real64), intent(in) :: mineral_max, doma_max, dop_max
    real(real64) :: core(4), pvals(2)

    core = [value%nh,value%ni,value%doma,value%don]
    pvals = [value%po,value%dop]
    six_valid = .false.
    if (.not. all(ieee_is_finite(core)) .or. .not. all(ieee_is_finite(pvals))) return
    if (value%nh < 0.0_real64 .or. value%nh > mineral_max) return
    if (value%ni < 0.0_real64 .or. value%ni > mineral_max) return
    if (value%doma < 0.0_real64 .or. value%doma > doma_max) return
    if (value%don < 0.0_real64 .or. value%don > doma_max) return
    if (phosphorus_enabled) then
      if (value%po < 0.0_real64 .or. value%po > mineral_max) return
      if (value%dop < 0.0_real64 .or. value%dop > dop_max) return
    else
      if (.not. exact_zero(value%po) .or. .not. exact_zero(value%dop)) return
    end if
    six_valid = .true.
  end function six_valid

  logical function within(values, lower, upper)
    real(real64), intent(in) :: values(:)
    real(real64), intent(in) :: lower, upper
    within = all(values >= lower .and. values <= upper)
  end function within

  logical function exact_zero(value)
    real(real64), intent(in) :: value
    integer(kind=8) :: bits
    bits = transfer(value,bits)
    exact_zero = iand(bits,int(z'7FFFFFFFFFFFFFFF',kind=8)) == 0_8
  end function exact_zero

end module mod_animo_static_boundary_chemistry_adapter
