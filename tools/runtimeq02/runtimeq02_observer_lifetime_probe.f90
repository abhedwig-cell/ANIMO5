program runtimeq02_observer_lifetime_probe
  use, intrinsic :: ieee_arithmetic
  implicit none

  real :: physical_state(3), baseline_state(3)
  real :: ch4_first, deni_first, nitr_first
  real :: ch4_seeded, deni_seeded, nitr_seeded
  real :: ch4_repeat, deni_repeat, nitr_repeat
  real :: saved_ch4_seeded, saved_deni_seeded, saved_nitr_seeded
  real :: saved_ch4_repeat, saved_deni_repeat, saved_nitr_repeat
  logical :: inactive_ok, first_read_exposed
  logical :: automatic_repeat_not_persistent
  logical :: persistence_stale_reuse, nitr_step_refresh
  logical :: physical_unchanged

  physical_state = (/ 1.25d0, 2.50d0, 3.75d0 /)
  baseline_state = physical_state

  call source_like_observer(0, .false., 1.0d0, physical_state, &
       ch4_first, deni_first, nitr_first)
  inactive_ok = all(physical_state == baseline_state) .and. &
       ch4_first == -999.0d0 .and. deni_first == -999.0d0 .and. &
       nitr_first == -999.0d0

  call source_like_observer(1, .false., 1.0d0, physical_state, &
       ch4_first, deni_first, nitr_first)
  first_read_exposed = ieee_is_nan(ch4_first) .and. &
       ieee_is_nan(deni_first) .and. (.not. ieee_is_nan(nitr_first))

  ! The seed is instrumentation only. It demonstrates that a value made finite
  ! in one call does not create source ownership for a later automatic call.
  call source_like_observer(1, .true., 1.0d0, physical_state, &
       ch4_seeded, deni_seeded, nitr_seeded)
  call source_like_observer(1, .false., 2.0d0, physical_state, &
       ch4_repeat, deni_repeat, nitr_repeat)
  automatic_repeat_not_persistent = (.not. ieee_is_nan(ch4_seeded)) .and. &
       (.not. ieee_is_nan(deni_seeded)) .and. ieee_is_nan(ch4_repeat) .and. &
       ieee_is_nan(deni_repeat)

  ! Counterfactual only: explicit SAVE is deliberately added here to show that
  ! persistence without a fresh producer merely reuses stale observer values.
  call saved_counterfactual_observer(1, .true., 1.0d0, physical_state, &
       saved_ch4_seeded, saved_deni_seeded, saved_nitr_seeded)
  call saved_counterfactual_observer(1, .false., 2.0d0, physical_state, &
       saved_ch4_repeat, saved_deni_repeat, saved_nitr_repeat)
  persistence_stale_reuse = (saved_ch4_repeat == saved_ch4_seeded) .and. &
       (saved_deni_repeat == saved_deni_seeded)
  nitr_step_refresh = (saved_nitr_repeat == 2.0d0 * saved_nitr_seeded)

  physical_unchanged = all(physical_state == baseline_state)

  write(*,'(A,1X,L1)') 'INACTIVE_OK', inactive_ok
  write(*,'(A,1X,L1)') 'FIRST_READ_EXPOSED', first_read_exposed
  write(*,'(A,1X,L1)') 'AUTOMATIC_REPEAT_NOT_PERSISTENT', &
       automatic_repeat_not_persistent
  write(*,'(A,1X,L1)') 'PERSISTENCE_STALE_REUSE', persistence_stale_reuse
  write(*,'(A,1X,L1)') 'NITR_STEP_REFRESH', nitr_step_refresh
  write(*,'(A,1X,L1)') 'PHYSICAL_UNCHANGED', physical_unchanged

contains

  subroutine source_like_observer(ioptghg, seed_hidden, st, physical_state, &
       obs_ch4, obs_deni, obs_nitr)
    implicit none
    integer, intent(in) :: ioptghg
    logical, intent(in) :: seed_hidden
    real, intent(in) :: st
    real, intent(inout) :: physical_state(3)
    real, intent(out) :: obs_ch4, obs_deni, obs_nitr
    real :: AmCH4(0:2), AmN2Odeni(0:2), AmN2Onitr(0:2)
    integer :: ln

    obs_ch4 = -999.0d0
    obs_deni = -999.0d0
    obs_nitr = -999.0d0
    if (ioptghg < 1) return

    do ln = 1, 2
      AmN2Onitr(ln) = 1.0d-5 * dble(ln) * st
    end do
    AmN2Onitr(0) = AmN2Onitr(1) + AmN2Onitr(2)

    if (seed_hidden) then
      AmCH4 = (/ 101.0d0, 102.0d0, 103.0d0 /)
      AmN2Odeni = (/ 201.0d0, 202.0d0, 203.0d0 /)
    end if

    obs_ch4 = AmCH4(1)
    obs_deni = AmN2Odeni(1)
    obs_nitr = AmN2Onitr(0)
  end subroutine source_like_observer

  subroutine saved_counterfactual_observer(ioptghg, seed_hidden, st, &
       physical_state, obs_ch4, obs_deni, obs_nitr)
    implicit none
    integer, intent(in) :: ioptghg
    logical, intent(in) :: seed_hidden
    real, intent(in) :: st
    real, intent(inout) :: physical_state(3)
    real, intent(out) :: obs_ch4, obs_deni, obs_nitr
    real, save :: AmCH4(0:2), AmN2Odeni(0:2)
    real :: AmN2Onitr(0:2)
    integer :: ln

    obs_ch4 = -999.0d0
    obs_deni = -999.0d0
    obs_nitr = -999.0d0
    if (ioptghg < 1) return

    do ln = 1, 2
      AmN2Onitr(ln) = 1.0d-5 * dble(ln) * st
    end do
    AmN2Onitr(0) = AmN2Onitr(1) + AmN2Onitr(2)

    if (seed_hidden) then
      AmCH4 = (/ 101.0d0, 102.0d0, 103.0d0 /)
      AmN2Odeni = (/ 201.0d0, 202.0d0, 203.0d0 /)
    end if

    obs_ch4 = AmCH4(1)
    obs_deni = AmN2Odeni(1)
    obs_nitr = AmN2Onitr(0)
  end subroutine saved_counterfactual_observer

end program runtimeq02_observer_lifetime_probe
