module mod_animo_accepted_application_checkpoint
  use iso_fortran_env, only: int64, real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use mod_transient_time, only: TimeCoordinate, time_equal, time_is_valid
  use mod_transient_contracts, only: transient_payload_t, identity_argument_valid
  use mod_transient_transactions, only: accepted_store_t, reconstruct_accepted_store_trusted
  use mod_animo_tcd042_upper_boundary_client, only: tcd042_top_state_t
  use mod_animo_composite_accepted_continuation, only: &
    composite_accepted_continuation_t, validate_composite_continuation
  use mod_animo_atomic_composite_application, only: &
    kt15_application_config_t, kt15_application_state_t, &
    validate_kt15_application_state, validate_kt15_application_config, &
    same_kt15_application_config, initialize_kt15_application_state, &
    kt15_application_generation, kt15_application_time, &
    snapshot_kt15_science_payload, snapshot_kt15_continuation, &
    snapshot_kt15_application_config
  implicit none
  private

  character(len=*), parameter, public :: KT16_CHECKPOINT_SCHEMA = &
    'ANIMO_KT16_ACCEPTED_APPLICATION_CHECKPOINT_V1'
  character(len=*), parameter, public :: KT16_RECORD_KIND = &
    'ACCEPTED_BOUNDARY_ONLY'
  character(len=*), parameter, public :: KT16_PAYLOAD_SCHEMA = &
    'ANIMO_TCD042_TOP_STATE_V1'
  character(len=*), parameter, public :: KT16_PRODUCER_CONTRACT = &
    'ANIMO_KT15A_IMMUTABLE_APPLICATION_CONFIG_V1'

  type, public :: kt16_application_checkpoint_t
    character(len=56) :: schema_id = ''
    character(len=32) :: record_kind = ''
    character(len=48) :: payload_schema_id = ''
    character(len=56) :: producer_contract_id = ''
    character(len=64) :: lineage_id = ''
    integer(int64) :: generation = -1_int64
    type(TimeCoordinate) :: accepted_time
    integer :: layer_count = 0
    real(real64) :: tcd042_concentration = 0.0_real64
    type(kt15_application_config_t) :: config
    type(composite_accepted_continuation_t) :: continuation
  end type kt16_application_checkpoint_t

  public :: encode_kt16_application_checkpoint
  public :: validate_kt16_application_checkpoint
  public :: restore_kt16_application_checkpoint

contains

  subroutine encode_kt16_application_checkpoint(state, checkpoint, ok, reason)
    type(kt15_application_state_t), intent(in) :: state
    type(kt16_application_checkpoint_t), intent(out) :: checkpoint
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    class(transient_payload_t), allocatable :: payload
    type(TimeCoordinate) :: accepted_time
    type(kt15_application_config_t) :: config
    type(composite_accepted_continuation_t) :: continuation
    integer(int64) :: generation
    character(len=128) :: local_reason
    logical :: state_ok, time_ok, config_ok, continuation_ok, payload_ok

    checkpoint = kt16_application_checkpoint_t()
    ok = .false.
    reason = 'UNSET'

    call validate_kt15_application_state(state, state_ok, local_reason)
    if (.not. state_ok) then
      reason = 'KT16_SOURCE_APPLICATION_STATE_INVALID'
      return
    end if

    generation = kt15_application_generation(state)
    if (generation < 0_int64) then
      reason = 'KT16_SOURCE_GENERATION_INVALID'
      return
    end if
    call kt15_application_time(state, accepted_time, time_ok)
    if (.not. time_ok) then
      reason = 'KT16_SOURCE_ACCEPTED_TIME_UNAVAILABLE'
      return
    end if
    call snapshot_kt15_application_config(state, config, config_ok)
    if (.not. config_ok) then
      reason = 'KT16_SOURCE_CONFIG_UNAVAILABLE'
      return
    end if
    call snapshot_kt15_continuation(state, continuation, continuation_ok)
    if (.not. continuation_ok) then
      reason = 'KT16_SOURCE_CONTINUATION_UNAVAILABLE'
      return
    end if
    call snapshot_kt15_science_payload(state, payload, payload_ok)
    if (.not. payload_ok .or. .not. allocated(payload)) then
      reason = 'KT16_SOURCE_SCIENCE_PAYLOAD_UNAVAILABLE'
      return
    end if

    checkpoint%schema_id = KT16_CHECKPOINT_SCHEMA
    checkpoint%record_kind = KT16_RECORD_KIND
    checkpoint%payload_schema_id = KT16_PAYLOAD_SCHEMA
    checkpoint%producer_contract_id = KT16_PRODUCER_CONTRACT
    checkpoint%lineage_id = continuation%lineage_id
    checkpoint%generation = generation
    checkpoint%accepted_time = accepted_time
    checkpoint%layer_count = size(continuation%hydrology_origin%mofro)
    checkpoint%config = config
    checkpoint%continuation = continuation

    select type(typed => payload)
    type is (tcd042_top_state_t)
      checkpoint%tcd042_concentration = typed%concentration
    class default
      reason = 'KT16_UNSUPPORTED_ACCEPTED_SCIENCE_PAYLOAD'
      return
    end select

    call validate_kt16_application_checkpoint(checkpoint, ok, local_reason)
    if (.not. ok) then
      reason = trim(local_reason)
      return
    end if

    reason = 'KT16_ACCEPTED_APPLICATION_CHECKPOINT_ENCODED'
  end subroutine encode_kt16_application_checkpoint

  subroutine validate_kt16_application_checkpoint(checkpoint, ok, reason)
    type(kt16_application_checkpoint_t), intent(in) :: checkpoint
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    logical :: config_ok, continuation_ok, equal, compare_ok
    character(len=128) :: local_reason

    ok = .false.
    reason = 'UNSET'

    if (trim(checkpoint%schema_id) /= KT16_CHECKPOINT_SCHEMA) then
      reason = 'KT16_CHECKPOINT_SCHEMA_MISMATCH'
      return
    end if
    if (trim(checkpoint%record_kind) /= KT16_RECORD_KIND) then
      reason = 'KT16_CHECKPOINT_NOT_ACCEPTED_BOUNDARY_ONLY'
      return
    end if
    if (trim(checkpoint%payload_schema_id) /= KT16_PAYLOAD_SCHEMA) then
      reason = 'KT16_PAYLOAD_SCHEMA_MISMATCH'
      return
    end if
    if (trim(checkpoint%producer_contract_id) /= KT16_PRODUCER_CONTRACT) then
      reason = 'KT16_PRODUCER_CONTRACT_MISMATCH'
      return
    end if
    if (.not. identity_argument_valid(checkpoint%lineage_id)) then
      reason = 'KT16_INVALID_LINEAGE'
      return
    end if
    if (checkpoint%generation < 0_int64) then
      reason = 'KT16_INVALID_GENERATION'
      return
    end if
    if (.not. time_is_valid(checkpoint%accepted_time)) then
      reason = 'KT16_INVALID_ACCEPTED_TIME'
      return
    end if
    if (checkpoint%layer_count <= 0) then
      reason = 'KT16_INVALID_LAYER_COUNT'
      return
    end if
    if (.not. ieee_is_finite(checkpoint%tcd042_concentration)) then
      reason = 'KT16_NONFINITE_TCD042_CONCENTRATION'
      return
    end if

    call validate_kt15_application_config(checkpoint%config, config_ok, local_reason)
    if (.not. config_ok) then
      reason = 'KT16_INVALID_APPLICATION_CONFIG'
      return
    end if
    call validate_composite_continuation(checkpoint%continuation, continuation_ok, local_reason)
    if (.not. continuation_ok) then
      reason = 'KT16_INVALID_COMPOSITE_CONTINUATION'
      return
    end if
    if (.not. allocated(checkpoint%continuation%hydrology_origin%mofro) .or. &
        size(checkpoint%continuation%hydrology_origin%mofro) /= checkpoint%layer_count) then
      reason = 'KT16_LAYER_COUNT_CONTINUATION_MISMATCH'
      return
    end if
    if (trim(checkpoint%lineage_id) /= trim(checkpoint%continuation%lineage_id)) then
      reason = 'KT16_LINEAGE_CONTINUATION_MISMATCH'
      return
    end if
    if (checkpoint%generation /= checkpoint%continuation%generation) then
      reason = 'KT16_GENERATION_CONTINUATION_MISMATCH'
      return
    end if
    call time_equal(checkpoint%accepted_time, checkpoint%continuation%accepted_time, &
      equal, compare_ok)
    if (.not. compare_ok .or. .not. equal) then
      reason = 'KT16_TIME_CONTINUATION_MISMATCH'
      return
    end if

    ok = .true.
    reason = 'VALID_KT16_ACCEPTED_APPLICATION_CHECKPOINT'
  end subroutine validate_kt16_application_checkpoint

  subroutine restore_kt16_application_checkpoint(checkpoint, expected_config, state, ok, reason)
    type(kt16_application_checkpoint_t), intent(in) :: checkpoint
    type(kt15_application_config_t), intent(in) :: expected_config
    type(kt15_application_state_t), intent(out) :: state
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    type(tcd042_top_state_t) :: payload
    type(accepted_store_t) :: store
    character(len=128) :: local_reason
    logical :: checkpoint_ok, config_ok, store_ok

    state = kt15_application_state_t()
    ok = .false.
    reason = 'UNSET'

    call validate_kt16_application_checkpoint(checkpoint, checkpoint_ok, local_reason)
    if (.not. checkpoint_ok) then
      reason = trim(local_reason)
      return
    end if

    call validate_kt15_application_config(expected_config, config_ok, local_reason)
    if (.not. config_ok) then
      reason = 'KT16_EXPECTED_CONFIG_INVALID'
      return
    end if
    if (.not. same_kt15_application_config(checkpoint%config, expected_config)) then
      reason = 'KT16_EXPECTED_CONFIG_MISMATCH'
      return
    end if

    payload%concentration = checkpoint%tcd042_concentration
    call reconstruct_accepted_store_trusted(checkpoint%lineage_id, checkpoint%generation, &
      checkpoint%accepted_time, payload, store, store_ok)
    if (.not. store_ok) then
      reason = 'KT16_ACCEPTED_STORE_RECONSTRUCTION_FAILED'
      return
    end if

    call initialize_kt15_application_state(store, checkpoint%continuation, checkpoint%config, &
      state, ok, local_reason)
    if (.not. ok) then
      reason = 'KT16_APPLICATION_RESTORE_COHERENCE_FAILED'
      return
    end if

    reason = 'KT16_ACCEPTED_APPLICATION_CHECKPOINT_RESTORED'
  end subroutine restore_kt16_application_checkpoint

end module mod_animo_accepted_application_checkpoint
