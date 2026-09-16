program test_kt01_identity_envelope
  use iso_fortran_env, only: int64
  use mod_animo_time_coordinate
  use mod_animo_runtime_contracts
  use mod_animo_kernel_transactions
  use mod_animo_committed_persistence
  use mod_animo_worker_context
  implicit none

  type(TimeCoordinate) :: t0, t1
  type(AcceptedState) :: accepted
  type(TrialState) :: trial
  type(TrialResult) :: result
  type(AcceptedCheckpoint) :: checkpoint
  type(WorkerContext) :: worker
  logical :: ok
  character(len=96) :: overlong
  character(len=80) :: reason
  integer :: failures

  failures = 0
  overlong = repeat('X', len(overlong))

  call make_time_coordinate(overlong, 0_int64, 0_int64, 1_int64, t0, ok)
  call assert_true(.not. ok, '30 overlong calendar identity fails closed', failures)

  call make_time_coordinate('BAD|CALENDAR', 0_int64, 0_int64, 1_int64, t0, ok)
  call assert_true(.not. ok, '31 delimiter-ambiguous calendar identity fails closed', failures)

  call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1', 300_int64, 0_int64, 1_int64, t0, ok)
  if (.not. ok) error stop 'fixture t0'
  call make_time_coordinate('ANIMO_PG_86400_NOLEAPSECONDS_V1', 301_int64, 0_int64, 1_int64, t1, ok)
  if (.not. ok) error stop 'fixture t1'

  accepted = AcceptedState()
  accepted%lineage_id = 'LINEAGE-A'
  accepted%generation = 2_int64
  accepted%accepted_time = t0
  accepted%synthetic_storage = 10_int64

  call make_accepted_checkpoint(accepted, overlong, 'LAYOUT', 'CONFIG', 'FEATURE', checkpoint, ok)
  call assert_true(.not. ok, '32 overlong checkpoint identity fails closed', failures)

  call initialize_worker_context(worker, overlong, ok)
  call assert_true(.not. ok, '33 overlong worker identity fails closed', failures)

  call begin_trial(accepted, t1, trial, ok)
  if (.not. ok) error stop 'fixture trial'
  result = TrialResult()
  result%candidate = trial
  result%n_assessments = 1
  result%assessments(1)%quantity_id = 'SYNTHETIC_Q'
  result%assessments(1)%control_volume_id = 'CV'
  result%assessments(1)%complete = .true.
  result%assessments(1)%admissible = .true.
  call commit_trial(accepted, result, ok, reason)
  call assert_true(.not. ok .and. trim(reason) == 'MISSING_TRIAL_PROVENANCE', &
    '34 provenance-free candidate cannot commit', failures)

  if (failures /= 0) then
    write(*,'(A,I0)') 'KT01 IDENTITY ENVELOPE TEST FAILURES: ', failures
    error stop 1
  end if
  write(*,'(A)') 'KT01 IDENTITY ENVELOPE TESTS 30-34: PASS'

contains

  subroutine assert_true(condition, label, failures)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: label
    integer, intent(inout) :: failures
    if (condition) then
      write(*,'(A)') 'PASS '//trim(label)
    else
      write(*,'(A)') 'FAIL '//trim(label)
      failures = failures + 1
    end if
  end subroutine assert_true

end program test_kt01_identity_envelope
