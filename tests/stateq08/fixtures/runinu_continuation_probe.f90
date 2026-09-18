program stateq08_runinu_continuation_probe
  use iso_fortran_env, only: int64, real64
  implicit none

  real(real64) :: runinu_cont, runinu_split, runinu_missing, runinu_agg
  real(real64) :: rupr, rurv, ruso
  real(real64) :: checkpoint, load_cont, load_missing
  real(real64), parameter :: tiny = 2.0_real64**(-20)

  runinu_cont = 0.0_real64
  call detailed_partition(-tiny, runinu_cont, rupr, rurv, ruso)
  call assert_bits(runinu_cont, int(z'3EB0000000000000',int64), 'negative Ru assigns Runinu')
  checkpoint = runinu_cont

  call detailed_partition(0.0_real64, runinu_cont, rupr, rurv, ruso)
  call assert_bits(runinu_cont, int(z'3EB0000000000000',int64), &
    'detailed near-zero branch preserves call-entry Runinu')

  runinu_split = checkpoint
  call detailed_partition(0.0_real64, runinu_split, rupr, rurv, ruso)
  call assert_bits(runinu_split, transfer(runinu_cont,0_int64), &
    'split restore with Runinu reproduces continuous branch')

  runinu_missing = 0.0_real64
  call detailed_partition(0.0_real64, runinu_missing, rupr, rurv, ruso)
  if (transfer(runinu_missing,0_int64) == transfer(runinu_cont,0_int64)) then
    print *, 'ASSERTION FAILED: omitted Runinu continuation did not diverge'
    error stop 1
  end if

  load_cont = runinu_cont * 1.0_real64
  load_missing = runinu_missing * 1.0_real64
  call assert_bits(load_cont, int(z'3EB0000000000000',int64), &
    'Runinu changes UBoundconc run-in load contribution')
  call assert_bits(load_missing, 0_int64, 'omitted Runinu removes run-in load contribution')

  runinu_agg = 0.0_real64
  call aggregated_partition(-tiny, runinu_agg, rupr, rurv, ruso)
  call assert_bits(runinu_agg, int(z'3EB0000000000000',int64), &
    'aggregated negative Ru assigns Runinu')
  call aggregated_partition(0.0_real64, runinu_agg, rupr, rurv, ruso)
  call assert_bits(runinu_agg, 0_int64, &
    'aggregated nonnegative branch resets Runinu unlike detailed near-zero branch')

  print *, 'PASS_STATEQ08_RUNINU_EXECUTION_CONTINUATION'

contains

  subroutine assert_bits(value, expected, message)
    real(real64), intent(in) :: value
    integer(int64), intent(in) :: expected
    character(len=*), intent(in) :: message
    if (transfer(value,0_int64) /= expected) then
      print *, 'ASSERTION FAILED: ', trim(message)
      error stop 1
    end if
  end subroutine assert_bits

  subroutine detailed_partition(ru, runinu, rupr, rurv, ruso)
    real(real64), intent(in) :: ru
    real(real64), intent(inout) :: runinu
    real(real64), intent(out) :: rupr, rurv, ruso

    if (ru < 0.0_real64) then
      runinu = -ru
      rupr = 0.0_real64
      rurv = 0.0_real64
      ruso = 0.0_real64
    else if (ru > -1.0e-8_real64 .and. ru < 1.0e-8_real64) then
      ! Exact source property under test: no Runinu assignment here.
      rupr = 0.0_real64
      rurv = 0.0_real64
      ruso = 0.0_real64
    else
      ! This probe does not qualify the positive partition algebra.
      runinu = 0.0_real64
      rupr = 0.0_real64
      rurv = 0.0_real64
      ruso = ru
    end if
  end subroutine detailed_partition

  subroutine aggregated_partition(ru, runinu, rupr, rurv, ruso)
    real(real64), intent(in) :: ru
    real(real64), intent(inout) :: runinu
    real(real64), intent(out) :: rupr, rurv, ruso

    if (ru < 0.0_real64) then
      runinu = -ru
      rupr = 0.0_real64
      rurv = 0.0_real64
      ruso = 0.0_real64
    else
      runinu = 0.0_real64
      rupr = 0.0_real64
      rurv = 0.0_real64
      ruso = ru
    end if
  end subroutine aggregated_partition

end program stateq08_runinu_continuation_probe
