module mod_transient_time
  use iso_fortran_env, only: int64
  implicit none
  private

  integer, parameter :: CALENDAR_ID_LEN = 48

  type, public :: TimeCoordinate
    character(len=CALENDAR_ID_LEN) :: calendar_contract_id = ''
    integer(int64) :: day_index = 0_int64
    integer(int64) :: subday_numerator = 0_int64
    integer(int64) :: subday_denominator = 1_int64
  end type TimeCoordinate

  public :: make_time_coordinate
  public :: time_equal
  public :: time_compare
  public :: time_add_fraction
  public :: time_is_valid

contains

  subroutine make_time_coordinate(calendar_contract_id, day_index, numerator, denominator, value, ok)
    character(len=*), intent(in) :: calendar_contract_id
    integer(int64), intent(in) :: day_index, numerator, denominator
    type(TimeCoordinate), intent(out) :: value
    logical, intent(out) :: ok
    integer(int64) :: whole, remainder, divisor, normalized_day
    integer :: calendar_length

    value = TimeCoordinate()
    ok = .false.

    calendar_length = len_trim(calendar_contract_id)
    if (calendar_length == 0 .or. calendar_length > CALENDAR_ID_LEN) return
    if (denominator <= 0_int64 .or. numerator < 0_int64) return

    whole = numerator / denominator
    remainder = modulo(numerator, denominator)
    if (.not. checked_add_nonnegative(day_index, whole, normalized_day)) return

    if (remainder == 0_int64) then
      divisor = 1_int64
    else
      divisor = gcd_nonnegative(remainder, denominator)
      if (divisor <= 0_int64) return
    end if

    value%calendar_contract_id = calendar_contract_id(:calendar_length)
    value%day_index = normalized_day
    value%subday_numerator = remainder / divisor
    value%subday_denominator = denominator / divisor
    ok = time_is_valid(value)
  end subroutine make_time_coordinate

  logical function time_is_valid(value)
    type(TimeCoordinate), intent(in) :: value
    integer(int64) :: divisor

    time_is_valid = .false.
    if (len_trim(value%calendar_contract_id) == 0) return
    if (value%subday_denominator <= 0_int64) return
    if (value%subday_numerator < 0_int64) return
    if (value%subday_numerator >= value%subday_denominator) return
    if (value%subday_numerator == 0_int64) then
      if (value%subday_denominator /= 1_int64) return
    else
      divisor = gcd_nonnegative(value%subday_numerator, value%subday_denominator)
      if (divisor /= 1_int64) return
    end if
    time_is_valid = .true.
  end function time_is_valid

  subroutine time_equal(left, right, equal, ok)
    type(TimeCoordinate), intent(in) :: left, right
    logical, intent(out) :: equal, ok
    integer :: ordering

    call time_compare(left, right, ordering, ok)
    equal = ok .and. ordering == 0
  end subroutine time_equal

  subroutine time_compare(left, right, ordering, ok)
    type(TimeCoordinate), intent(in) :: left, right
    integer, intent(out) :: ordering
    logical, intent(out) :: ok

    ordering = 0
    ok = .false.
    if (.not. time_is_valid(left) .or. .not. time_is_valid(right)) return
    if (trim(left%calendar_contract_id) /= trim(right%calendar_contract_id)) return

    if (left%day_index < right%day_index) then
      ordering = -1
      ok = .true.
      return
    else if (left%day_index > right%day_index) then
      ordering = 1
      ok = .true.
      return
    end if

    ordering = compare_nonnegative_ratios(left%subday_numerator, left%subday_denominator, &
      right%subday_numerator, right%subday_denominator)
    ok = .true.
  end subroutine time_compare

  subroutine time_add_fraction(base, add_numerator, add_denominator, result, ok)
    type(TimeCoordinate), intent(in) :: base
    integer(int64), intent(in) :: add_numerator, add_denominator
    type(TimeCoordinate), intent(out) :: result
    logical, intent(out) :: ok
    integer(int64) :: g, left_factor, right_factor
    integer(int64) :: left_term, right_term, sum_numerator, sum_denominator

    result = TimeCoordinate()
    ok = .false.
    if (.not. time_is_valid(base)) return
    if (add_denominator <= 0_int64 .or. add_numerator < 0_int64) return

    g = gcd_nonnegative(base%subday_denominator, add_denominator)
    if (g <= 0_int64) return
    left_factor = add_denominator / g
    right_factor = base%subday_denominator / g

    if (.not. checked_multiply_nonnegative(base%subday_numerator, left_factor, left_term)) return
    if (.not. checked_multiply_nonnegative(add_numerator, right_factor, right_term)) return
    if (.not. checked_add_nonnegative(left_term, right_term, sum_numerator)) return
    if (.not. checked_multiply_nonnegative(base%subday_denominator, left_factor, sum_denominator)) return

    call make_time_coordinate(trim(base%calendar_contract_id), base%day_index, &
      sum_numerator, sum_denominator, result, ok)
  end subroutine time_add_fraction

  pure integer(int64) function gcd_nonnegative(a_in, b_in) result(g)
    integer(int64), intent(in) :: a_in, b_in
    integer(int64) :: a, b, r
    a = a_in
    b = b_in
    if (a < 0_int64 .or. b < 0_int64) then
      g = 0_int64
      return
    end if
    do while (b /= 0_int64)
      r = modulo(a, b)
      a = b
      b = r
    end do
    g = a
  end function gcd_nonnegative

  logical function checked_add_nonnegative(a, b, result_value)
    integer(int64), intent(in) :: a, b
    integer(int64), intent(out) :: result_value
    result_value = 0_int64
    checked_add_nonnegative = .false.
    if (b < 0_int64) return
    if (a > huge(a) - b) return
    result_value = a + b
    checked_add_nonnegative = .true.
  end function checked_add_nonnegative

  logical function checked_multiply_nonnegative(a, b, result_value)
    integer(int64), intent(in) :: a, b
    integer(int64), intent(out) :: result_value
    result_value = 0_int64
    checked_multiply_nonnegative = .false.
    if (a < 0_int64 .or. b < 0_int64) return
    if (a == 0_int64 .or. b == 0_int64) then
      checked_multiply_nonnegative = .true.
      return
    end if
    if (a > huge(a) / b) return
    result_value = a * b
    checked_multiply_nonnegative = .true.
  end function checked_multiply_nonnegative

  pure integer function compare_nonnegative_ratios(a_in, b_in, c_in, d_in) result(ordering)
    integer(int64), intent(in) :: a_in, b_in, c_in, d_in
    integer(int64) :: a, b, c, d, q1, q2, r1, r2
    integer :: sense
    a = a_in
    b = b_in
    c = c_in
    d = d_in
    sense = 1
    ordering = 0
    do
      q1 = a / b
      q2 = c / d
      if (q1 < q2) then
        ordering = -sense
        return
      else if (q1 > q2) then
        ordering = sense
        return
      end if
      r1 = modulo(a, b)
      r2 = modulo(c, d)
      if (r1 == 0_int64 .and. r2 == 0_int64) then
        ordering = 0
        return
      else if (r1 == 0_int64) then
        ordering = -sense
        return
      else if (r2 == 0_int64) then
        ordering = sense
        return
      end if
      a = b
      b = r1
      c = d
      d = r2
      sense = -sense
    end do
  end function compare_nonnegative_ratios

end module mod_transient_time
