! ANIMO-KT01 nonproduction prototype.
! Adapted control-structure provenance: SWAP5 src/kernel/mod_kernel_committed_persistence.f90
! @50346642bd565f79134ea17d5462e544b354998c blob ffd886c3401fc12739a456fe60a8741c12b9848b, classified PORT_WITH_ANIMO_ADAPTATION.
! ANIMO ARCH02/04/06 identities replace SWAP persistence layout assumptions.
module mod_animo_committed_persistence
  use iso_fortran_env, only: int64
  use mod_animo_time_coordinate, only: TimeCoordinate, time_is_valid
  use mod_animo_runtime_contracts, only: AcceptedState, ID_LEN
  implicit none
  private

  type, public :: AcceptedCheckpoint
    private
    logical :: valid = .false.
    character(len=ID_LEN) :: checkpoint_schema_id = ''
    character(len=ID_LEN) :: state_layout_id = ''
    character(len=ID_LEN) :: configuration_id = ''
    character(len=ID_LEN) :: feature_layout_id = ''
    character(len=ID_LEN) :: lineage_id = ''
    integer(int64) :: accepted_generation = 0_int64
    type(TimeCoordinate) :: accepted_time
    integer(int64) :: synthetic_storage = 0_int64
  end type AcceptedCheckpoint

  public :: make_accepted_checkpoint
  public :: restore_accepted_checkpoint

contains

  logical function identity_argument_valid(value)
    character(len=*), intent(in) :: value
    integer :: n

    n = len_trim(value)
    identity_argument_valid = n > 0 .and. n <= ID_LEN
  end function identity_argument_valid

  subroutine make_accepted_checkpoint(accepted, checkpoint_schema_id, state_layout_id, &
      configuration_id, feature_layout_id, checkpoint, ok)
    type(AcceptedState), intent(in) :: accepted
    character(len=*), intent(in) :: checkpoint_schema_id, state_layout_id
    character(len=*), intent(in) :: configuration_id, feature_layout_id
    type(AcceptedCheckpoint), intent(out) :: checkpoint
    logical, intent(out) :: ok

    checkpoint = AcceptedCheckpoint()
    ok = .false.
    if (len_trim(accepted%lineage_id) == 0) return
    if (accepted%generation < 0_int64) return
    if (.not. time_is_valid(accepted%accepted_time)) return
    if (.not. identity_argument_valid(checkpoint_schema_id)) return
    if (.not. identity_argument_valid(state_layout_id)) return
    if (.not. identity_argument_valid(configuration_id)) return
    if (.not. identity_argument_valid(feature_layout_id)) return

    checkpoint%checkpoint_schema_id = trim(checkpoint_schema_id)
    checkpoint%state_layout_id = trim(state_layout_id)
    checkpoint%configuration_id = trim(configuration_id)
    checkpoint%feature_layout_id = trim(feature_layout_id)
    checkpoint%lineage_id = accepted%lineage_id
    checkpoint%accepted_generation = accepted%generation
    checkpoint%accepted_time = accepted%accepted_time
    checkpoint%synthetic_storage = accepted%synthetic_storage
    checkpoint%valid = .true.
    ok = .true.
  end subroutine make_accepted_checkpoint

  subroutine restore_accepted_checkpoint(checkpoint, expected_checkpoint_schema_id, &
      expected_state_layout_id, expected_configuration_id, expected_feature_layout_id, &
      restored, ok, reason)
    type(AcceptedCheckpoint), intent(in) :: checkpoint
    character(len=*), intent(in) :: expected_checkpoint_schema_id, expected_state_layout_id
    character(len=*), intent(in) :: expected_configuration_id, expected_feature_layout_id
    type(AcceptedState), intent(out) :: restored
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    restored = AcceptedState()
    ok = .false.
    reason = 'UNSET'

    if (.not. checkpoint%valid) then
      reason = 'INVALID_CHECKPOINT'
      return
    end if
    if (.not. identity_argument_valid(expected_checkpoint_schema_id) .or. &
        .not. identity_argument_valid(expected_state_layout_id) .or. &
        .not. identity_argument_valid(expected_configuration_id) .or. &
        .not. identity_argument_valid(expected_feature_layout_id)) then
      reason = 'INVALID_EXPECTED_IDENTITY'
      return
    end if
    if (trim(checkpoint%checkpoint_schema_id) /= trim(expected_checkpoint_schema_id)) then
      reason = 'CHECKPOINT_SCHEMA_MISMATCH'
      return
    end if
    if (trim(checkpoint%state_layout_id) /= trim(expected_state_layout_id)) then
      reason = 'STATE_LAYOUT_MISMATCH'
      return
    end if
    if (trim(checkpoint%configuration_id) /= trim(expected_configuration_id)) then
      reason = 'CONFIGURATION_MISMATCH'
      return
    end if
    if (trim(checkpoint%feature_layout_id) /= trim(expected_feature_layout_id)) then
      reason = 'FEATURE_LAYOUT_MISMATCH'
      return
    end if
    if (len_trim(checkpoint%lineage_id) == 0 .or. checkpoint%accepted_generation < 0_int64) then
      reason = 'INVALID_ACCEPTED_PROVENANCE'
      return
    end if
    if (.not. time_is_valid(checkpoint%accepted_time)) then
      reason = 'INVALID_ACCEPTED_TIME'
      return
    end if

    restored%lineage_id = checkpoint%lineage_id
    restored%generation = checkpoint%accepted_generation
    restored%accepted_time = checkpoint%accepted_time
    restored%synthetic_storage = checkpoint%synthetic_storage
    ok = .true.
    reason = 'RESTORED'
  end subroutine restore_accepted_checkpoint

end module mod_animo_committed_persistence
