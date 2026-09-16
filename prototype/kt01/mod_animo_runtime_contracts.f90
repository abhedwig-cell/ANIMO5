! ANIMO-KT01 nonproduction prototype.
! Authority: ARCH01/ARCH03/ARCH05 under ANIMO-GOV06.
! Structural derivation only from SWAP5 mod_canonical_contracts.f90
! @50346642bd565f79134ea17d5462e544b354998c blob 3962c270a7579b7403764674302445fe15ef5f72, classified DESIGN_ONLY.
module mod_animo_runtime_contracts
  use iso_fortran_env, only: int64
  use mod_animo_time_coordinate, only: TimeCoordinate
  implicit none
  private

  integer, parameter, public :: ID_LEN = 48
  integer, parameter, public :: MAX_TRANSFER_EVENTS = 32
  integer, parameter, public :: MAX_ASSESSMENTS = 16

  type, public :: TransferEvent
    character(len=ID_LEN) :: quantity_id = ''
    character(len=ID_LEN) :: source_id = ''
    character(len=ID_LEN) :: sink_id = ''
    integer(int64) :: amount = 0_int64
  end type TransferEvent

  type, public :: TransferJournal
    integer :: count = 0
    type(TransferEvent) :: events(MAX_TRANSFER_EVENTS)
  end type TransferJournal

  type, public :: AcceptedState
    character(len=ID_LEN) :: lineage_id = ''
    integer(int64) :: generation = 0_int64
    type(TimeCoordinate) :: accepted_time
    integer(int64) :: synthetic_storage = 0_int64
    type(TransferJournal) :: committed_journal
  end type AcceptedState

  type, public :: TrialState
    character(len=ID_LEN) :: origin_lineage_id = ''
    integer(int64) :: origin_generation = 0_int64
    type(TimeCoordinate) :: origin_time
    type(TimeCoordinate) :: endpoint_time
    integer(int64) :: synthetic_storage = 0_int64
    type(TransferJournal) :: trial_journal
  end type TrialState

  type, public :: ConservationAssessment
    character(len=ID_LEN) :: quantity_id = ''
    character(len=ID_LEN) :: control_volume_id = ''
    integer(int64) :: beginning_storage = 0_int64
    integer(int64) :: ending_storage = 0_int64
    integer(int64) :: inbound_transfer = 0_int64
    integer(int64) :: outbound_transfer = 0_int64
    integer(int64) :: diagnostic_nonclosure = 0_int64
    logical :: complete = .false.
    logical :: admissible = .false.
  end type ConservationAssessment

  type, public :: TrialResult
    type(TrialState) :: candidate
    integer :: n_assessments = 0
    type(ConservationAssessment) :: assessments(MAX_ASSESSMENTS)
    character(len=ID_LEN) :: provenance_id = ''
    integer(int64) :: diagnostic_counter = 0_int64
  end type TrialResult

  public :: clear_journal
  public :: append_transfer_event
  public :: assessments_allow_commit

contains

  subroutine clear_journal(journal)
    type(TransferJournal), intent(out) :: journal
    integer :: i

    journal%count = 0
    do i = 1, MAX_TRANSFER_EVENTS
      journal%events(i) = TransferEvent()
    end do
  end subroutine clear_journal

  subroutine append_transfer_event(journal, quantity_id, source_id, sink_id, amount, ok)
    type(TransferJournal), intent(inout) :: journal
    character(len=*), intent(in) :: quantity_id, source_id, sink_id
    integer(int64), intent(in) :: amount
    logical, intent(out) :: ok
    integer :: slot

    ok = .false.
    if (journal%count < 0 .or. journal%count >= MAX_TRANSFER_EVENTS) return
    if (len_trim(quantity_id) == 0 .or. len_trim(source_id) == 0 .or. len_trim(sink_id) == 0) return
    if (len_trim(quantity_id) > ID_LEN .or. len_trim(source_id) > ID_LEN .or. len_trim(sink_id) > ID_LEN) return

    slot = journal%count + 1
    journal%events(slot)%quantity_id = trim(quantity_id)
    journal%events(slot)%source_id = trim(source_id)
    journal%events(slot)%sink_id = trim(sink_id)
    journal%events(slot)%amount = amount
    journal%count = slot
    ok = .true.
  end subroutine append_transfer_event

  logical function assessments_allow_commit(result)
    type(TrialResult), intent(in) :: result
    integer :: i

    assessments_allow_commit = .false.
    if (result%n_assessments <= 0 .or. result%n_assessments > MAX_ASSESSMENTS) return
    do i = 1, result%n_assessments
      if (.not. result%assessments(i)%complete) return
      if (.not. result%assessments(i)%admissible) return
      if (len_trim(result%assessments(i)%quantity_id) == 0) return
      if (len_trim(result%assessments(i)%control_volume_id) == 0) return
    end do
    assessments_allow_commit = .true.
  end function assessments_allow_commit

end module mod_animo_runtime_contracts
