module mod_transient_persistence
  use iso_fortran_env, only: int64
  use mod_transient_time, only: TimeCoordinate, time_is_valid
  use mod_transient_contracts, only: accepted_store_t, transient_payload_t, &
    accepted_store_ready, identity_argument_valid, TRANSIENT_ID_LEN
  implicit none
  private

  type, public :: accepted_checkpoint_t
    private
    logical :: valid = .false.
    character(len=TRANSIENT_ID_LEN) :: checkpoint_schema_id = ''
    character(len=TRANSIENT_ID_LEN) :: state_layout_id = ''
    character(len=TRANSIENT_ID_LEN) :: configuration_id = ''
    character(len=TRANSIENT_ID_LEN) :: feature_layout_id = ''
    character(len=TRANSIENT_ID_LEN) :: lineage_id = ''
    integer(int64) :: accepted_generation = 0_int64
    type(TimeCoordinate) :: accepted_time
    class(transient_payload_t), allocatable :: payload
  end type accepted_checkpoint_t

  public :: make_checkpoint
  public :: restore_checkpoint

contains

  subroutine make_checkpoint(accepted, checkpoint_schema_id, state_layout_id, configuration_id, &
      feature_layout_id, checkpoint, ok)
    type(accepted_store_t), intent(in) :: accepted
    character(len=*), intent(in) :: checkpoint_schema_id, state_layout_id
    character(len=*), intent(in) :: configuration_id, feature_layout_id
    type(accepted_checkpoint_t), intent(out) :: checkpoint
    logical, intent(out) :: ok

    checkpoint = accepted_checkpoint_t()
    ok = .false.
    if (.not. accepted_store_ready(accepted)) return
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
    call accepted%payload%clone_payload(checkpoint%payload)
    if (.not. allocated(checkpoint%payload)) return
    if (.not. checkpoint%payload%is_valid()) then
      deallocate(checkpoint%payload)
      return
    end if
    checkpoint%valid = .true.
    ok = .true.
  end subroutine make_checkpoint

  subroutine restore_checkpoint(checkpoint, expected_checkpoint_schema_id, expected_state_layout_id, &
      expected_configuration_id, expected_feature_layout_id, restored, ok, reason)
    type(accepted_checkpoint_t), intent(in) :: checkpoint
    character(len=*), intent(in) :: expected_checkpoint_schema_id, expected_state_layout_id
    character(len=*), intent(in) :: expected_configuration_id, expected_feature_layout_id
    type(accepted_store_t), intent(out) :: restored
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    class(transient_payload_t), allocatable :: payload_copy

    restored = accepted_store_t()
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
    if (.not. identity_argument_valid(checkpoint%lineage_id) .or. checkpoint%accepted_generation < 0_int64) then
      reason = 'INVALID_ACCEPTED_PROVENANCE'
      return
    end if
    if (.not. time_is_valid(checkpoint%accepted_time)) then
      reason = 'INVALID_ACCEPTED_TIME'
      return
    end if
    if (.not. allocated(checkpoint%payload) .or. .not. checkpoint%payload%is_valid()) then
      reason = 'INVALID_CHECKPOINT_PAYLOAD'
      return
    end if

    call checkpoint%payload%clone_payload(payload_copy)
    if (.not. allocated(payload_copy) .or. .not. payload_copy%is_valid()) then
      reason = 'CHECKPOINT_PAYLOAD_CLONE_FAILED'
      return
    end if

    restored%lineage_id = checkpoint%lineage_id
    restored%generation = checkpoint%accepted_generation
    restored%accepted_time = checkpoint%accepted_time
    call move_alloc(payload_copy, restored%payload)
    ok = .true.
    reason = 'RESTORED'
  end subroutine restore_checkpoint

end module mod_transient_persistence
