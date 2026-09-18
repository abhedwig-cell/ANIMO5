module mod_animo_checkpoint_manifest_integrity
  use iso_fortran_env, only: int64, real64
  use mod_transient_time, only: TimeCoordinate
  use mod_animo_sha256, only: sha256_ascii
  use mod_animo_atomic_composite_application, only: &
    kt15_application_config_t, kt15_static_hydrology_config_t, &
    kt15_application_state_t, inspect_kt15_application_config, &
    validate_kt15_application_config, same_kt15_application_config
  use mod_animo_accepted_application_checkpoint, only: &
    kt16_application_checkpoint_t, encode_kt16_application_checkpoint, &
    validate_kt16_application_checkpoint, restore_kt16_application_checkpoint
  implicit none
  private

  character(len=*), parameter, public :: KT17_ENVELOPE_SCHEMA = &
    'ANIMO_KT17_ACCEPTED_CHECKPOINT_ENVELOPE_V1'
  character(len=*), parameter, public :: KT17_HASH_ALGORITHM = 'SHA-256'
  character(len=*), parameter, public :: KT17_CANONICALIZATION = &
    'ANIMO_KT17_CANON_ASCII_V1'
  character(len=*), parameter, public :: KT17_FEATURE_SET = &
    'BOUNDED_TCD042_STATIC_BOUNDARY_V1'
  character(len=*), parameter, public :: KT17_DIAGNOSTIC_POLICY = &
    'NO_DIAGNOSTIC_CONTINUATION_IN_BOUNDED_SCOPE'
  character(len=*), parameter, public :: KT17_SOURCE_ARCHIVE_SHA256 = &
    '183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566'
  character(len=*), parameter, public :: KT17_TESTBANK_SHA256 = &
    '44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84'
  character(len=*), parameter, public :: KT17_DOCUMENTATION_SHA256 = &
    'ae4cf81676e259c8974bb6c80d3d144d4dee42023bcb8dfa6a1553d98923e301'

  type, public :: kt17_checkpoint_envelope_t
    character(len=56) :: schema_id = ''
    character(len=16) :: hash_algorithm_id = ''
    character(len=48) :: canonicalization_id = ''
    character(len=48) :: feature_set_id = ''
    character(len=64) :: diagnostic_policy_id = ''
    character(len=40) :: producer_build_commit = ''
    character(len=64) :: source_archive_sha256 = ''
    character(len=64) :: testbank_sha256 = ''
    character(len=64) :: documentation_sha256 = ''
    character(len=64) :: application_config_sha256 = ''
    character(len=64) :: checkpoint_payload_sha256 = ''
    character(len=64) :: manifest_sha256 = ''
    type(kt16_application_checkpoint_t) :: checkpoint
  end type kt17_checkpoint_envelope_t

  public :: encode_kt17_checkpoint_envelope
  public :: verify_kt17_checkpoint_envelope
  public :: restore_kt17_checkpoint_envelope
  public :: canonical_kt15_config_hash
  public :: canonical_kt16_checkpoint_hash

contains

  pure subroutine lowercase_hex(value)
    character(len=*), intent(inout) :: value
    integer :: i,c
    do i=1,len(value)
      c=iachar(value(i:i))
      if(c>=iachar('A') .and. c<=iachar('F')) value(i:i)=achar(c+32)
    end do
  end subroutine lowercase_hex

  logical function canonical_hex(value,expected_length)
    character(len=*), intent(in) :: value
    integer, intent(in) :: expected_length
    integer :: i,c
    canonical_hex=.false.
    if(len_trim(value)/=expected_length) return
    do i=1,expected_length
      c=iachar(value(i:i))
      if(.not.((c>=iachar('0').and.c<=iachar('9')).or. &
               (c>=iachar('a').and.c<=iachar('f')))) return
    end do
    canonical_hex=.true.
  end function canonical_hex

  function hex_i64(value) result(text)
    integer(int64), intent(in) :: value
    character(len=16) :: text
    write(text,'(Z16.16)') value
    call lowercase_hex(text)
  end function hex_i64

  function hex_real64(value) result(text)
    real(real64), intent(in) :: value
    character(len=16) :: text
    integer(int64) :: bits
    bits=transfer(value,bits)
    text=hex_i64(bits)
  end function hex_real64

  subroutine append_raw(buffer,token)
    character(len=:), allocatable, intent(inout) :: buffer
    character(len=*), intent(in) :: token
    if(allocated(buffer)) then
      buffer=buffer//token
    else
      buffer=token
    end if
  end subroutine append_raw

  subroutine append_string(buffer,value)
    character(len=:), allocatable, intent(inout) :: buffer
    character(len=*), intent(in) :: value
    character(len=16) :: nhex
    nhex=hex_i64(int(len_trim(value),int64))
    call append_raw(buffer,'S'//nhex//':'//trim(value)//';')
  end subroutine append_string

  subroutine append_i64(buffer,value)
    character(len=:), allocatable, intent(inout) :: buffer
    integer(int64), intent(in) :: value
    call append_raw(buffer,'I'//hex_i64(value)//';')
  end subroutine append_i64

  subroutine append_integer(buffer,value)
    character(len=:), allocatable, intent(inout) :: buffer
    integer, intent(in) :: value
    call append_i64(buffer,int(value,int64))
  end subroutine append_integer

  subroutine append_real64(buffer,value)
    character(len=:), allocatable, intent(inout) :: buffer
    real(real64), intent(in) :: value
    call append_raw(buffer,'R'//hex_real64(value)//';')
  end subroutine append_real64

  subroutine append_logical(buffer,value)
    character(len=:), allocatable, intent(inout) :: buffer
    logical, intent(in) :: value
    if(value) then
      call append_raw(buffer,'B1;')
    else
      call append_raw(buffer,'B0;')
    end if
  end subroutine append_logical

  subroutine append_time(buffer,value)
    character(len=:), allocatable, intent(inout) :: buffer
    type(TimeCoordinate), intent(in) :: value
    call append_raw(buffer,'T{')
    call append_string(buffer,value%calendar_contract_id)
    call append_i64(buffer,value%day_index)
    call append_i64(buffer,value%subday_numerator)
    call append_i64(buffer,value%subday_denominator)
    call append_raw(buffer,'};')
  end subroutine append_time

  subroutine canonical_config_preimage(config,text,ok,reason)
    type(kt15_application_config_t), intent(in) :: config
    character(len=:), allocatable, intent(out) :: text
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    character(len=64) :: calendar_id,boundary_sha
    integer(int64) :: producer_offset
    type(kt15_static_hydrology_config_t) :: hydro
    integer :: start_year,load_channel
    character(len=128) :: local_reason

    ok=.false.
    reason='UNSET'
    if(allocated(text)) deallocate(text)

    call inspect_kt15_application_config(config,calendar_id,producer_offset,hydro, &
      boundary_sha,start_year,load_channel,ok,local_reason)
    if(.not.ok) then
      reason='KT17_CONFIG_INSPECTION_FAILED'
      return
    end if

    call append_raw(text,'KT15CFG{')
    call append_string(text,calendar_id)
    call append_i64(text,producer_offset)
    call append_real64(text,hydro%he_top)
    call append_real64(text,hydro%lefrrv)
    call append_real64(text,hydro%lefrso)
    call append_string(text,boundary_sha)
    call append_integer(text,start_year)
    call append_integer(text,load_channel)
    call append_raw(text,'}')
    ok=.true.
    reason='KT17_CANONICAL_CONFIG_PREIMAGE_READY'
  end subroutine canonical_config_preimage

  subroutine canonical_kt15_config_hash(config,hash,ok,reason)
    type(kt15_application_config_t), intent(in) :: config
    character(len=64), intent(out) :: hash
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    character(len=:), allocatable :: text

    hash=''
    call canonical_config_preimage(config,text,ok,reason)
    if(.not.ok) return
    hash=sha256_ascii(text)
    if(.not.canonical_hex(hash,64)) then
      ok=.false.
      reason='KT17_CONFIG_HASH_FAILED'
      return
    end if
    reason='KT17_CANONICAL_CONFIG_HASH_READY'
  end subroutine canonical_kt15_config_hash

  subroutine canonical_checkpoint_preimage(checkpoint,text,ok,reason)
    type(kt16_application_checkpoint_t), intent(in) :: checkpoint
    character(len=:), allocatable, intent(out) :: text
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    character(len=:), allocatable :: config_text
    character(len=128) :: local_reason
    integer :: i

    ok=.false.
    reason='UNSET'
    if(allocated(text)) deallocate(text)

    call validate_kt16_application_checkpoint(checkpoint,ok,local_reason)
    if(.not.ok) then
      reason='KT17_INVALID_KT16_CHECKPOINT'
      return
    end if

    call canonical_config_preimage(checkpoint%config,config_text,ok,local_reason)
    if(.not.ok) then
      reason='KT17_CHECKPOINT_CONFIG_CANONICALIZATION_FAILED'
      return
    end if

    call append_raw(text,'KT16CHK{')
    call append_string(text,checkpoint%schema_id)
    call append_string(text,checkpoint%record_kind)
    call append_string(text,checkpoint%payload_schema_id)
    call append_string(text,checkpoint%producer_contract_id)
    call append_string(text,checkpoint%lineage_id)
    call append_i64(text,checkpoint%generation)
    call append_time(text,checkpoint%accepted_time)
    call append_integer(text,checkpoint%layer_count)
    call append_real64(text,checkpoint%tcd042_concentration)
    call append_string(text,config_text)

    call append_raw(text,'CONT{')
    call append_string(text,checkpoint%continuation%schema_id)
    call append_string(text,checkpoint%continuation%lineage_id)
    call append_i64(text,checkpoint%continuation%generation)
    call append_time(text,checkpoint%continuation%accepted_time)
    call append_string(text,checkpoint%continuation%hydrology_origin%schema_id)
    call append_string(text,checkpoint%continuation%hydrology_origin%transfer_contract_id)
    call append_real64(text,checkpoint%continuation%hydrology_origin%pn)
    call append_real64(text,checkpoint%continuation%hydrology_origin%sic)
    call append_real64(text,checkpoint%continuation%hydrology_origin%snla)
    call append_integer(text,size(checkpoint%continuation%hydrology_origin%mofro))
    do i=1,size(checkpoint%continuation%hydrology_origin%mofro)
      call append_real64(text,checkpoint%continuation%hydrology_origin%mofro(i))
    end do
    call append_real64(text,checkpoint%continuation%runinu_call_entry)
    call append_string(text,checkpoint%continuation%boundary_cursor%schema_id)
    call append_logical(text,checkpoint%continuation%boundary_cursor%initialized)
    call append_integer(text,checkpoint%continuation%boundary_cursor%active_year)
    call append_integer(text,checkpoint%continuation%boundary_cursor%active_slot)
    call append_raw(text,'};')
    call append_raw(text,'}')

    ok=.true.
    reason='KT17_CANONICAL_CHECKPOINT_PREIMAGE_READY'
  end subroutine canonical_checkpoint_preimage

  subroutine canonical_kt16_checkpoint_hash(checkpoint,hash,ok,reason)
    type(kt16_application_checkpoint_t), intent(in) :: checkpoint
    character(len=64), intent(out) :: hash
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    character(len=:), allocatable :: text

    hash=''
    call canonical_checkpoint_preimage(checkpoint,text,ok,reason)
    if(.not.ok) return
    hash=sha256_ascii(text)
    if(.not.canonical_hex(hash,64)) then
      ok=.false.
      reason='KT17_CHECKPOINT_HASH_FAILED'
      return
    end if
    reason='KT17_CANONICAL_CHECKPOINT_HASH_READY'
  end subroutine canonical_kt16_checkpoint_hash

  subroutine manifest_preimage(envelope,text)
    type(kt17_checkpoint_envelope_t), intent(in) :: envelope
    character(len=:), allocatable, intent(out) :: text
    if(allocated(text)) deallocate(text)
    call append_raw(text,'KT17MAN{')
    call append_string(text,envelope%schema_id)
    call append_string(text,envelope%hash_algorithm_id)
    call append_string(text,envelope%canonicalization_id)
    call append_string(text,envelope%feature_set_id)
    call append_string(text,envelope%diagnostic_policy_id)
    call append_string(text,envelope%producer_build_commit)
    call append_string(text,envelope%source_archive_sha256)
    call append_string(text,envelope%testbank_sha256)
    call append_string(text,envelope%documentation_sha256)
    call append_string(text,envelope%application_config_sha256)
    call append_string(text,envelope%checkpoint_payload_sha256)
    call append_raw(text,'}')
  end subroutine manifest_preimage

  subroutine encode_kt17_checkpoint_envelope(state,producer_build_commit,envelope,ok,reason)
    type(kt15_application_state_t), intent(in) :: state
    character(len=*), intent(in) :: producer_build_commit
    type(kt17_checkpoint_envelope_t), intent(out) :: envelope
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    character(len=:), allocatable :: manifest_text
    character(len=128) :: local_reason

    envelope=kt17_checkpoint_envelope_t()
    ok=.false.
    reason='UNSET'

    if(.not.canonical_hex(producer_build_commit,40)) then
      reason='KT17_INVALID_BUILD_COMMIT_ID'
      return
    end if

    call encode_kt16_application_checkpoint(state,envelope%checkpoint,ok,local_reason)
    if(.not.ok) then
      reason='KT17_KT16_CHECKPOINT_ENCODE_FAILED'
      return
    end if

    envelope%schema_id=KT17_ENVELOPE_SCHEMA
    envelope%hash_algorithm_id=KT17_HASH_ALGORITHM
    envelope%canonicalization_id=KT17_CANONICALIZATION
    envelope%feature_set_id=KT17_FEATURE_SET
    envelope%diagnostic_policy_id=KT17_DIAGNOSTIC_POLICY
    envelope%producer_build_commit=producer_build_commit(1:40)
    envelope%source_archive_sha256=KT17_SOURCE_ARCHIVE_SHA256
    envelope%testbank_sha256=KT17_TESTBANK_SHA256
    envelope%documentation_sha256=KT17_DOCUMENTATION_SHA256

    call canonical_kt15_config_hash(envelope%checkpoint%config, &
      envelope%application_config_sha256,ok,local_reason)
    if(.not.ok) then
      reason='KT17_CONFIG_HASH_CONSTRUCTION_FAILED'
      return
    end if
    call canonical_kt16_checkpoint_hash(envelope%checkpoint, &
      envelope%checkpoint_payload_sha256,ok,local_reason)
    if(.not.ok) then
      reason='KT17_PAYLOAD_HASH_CONSTRUCTION_FAILED'
      return
    end if
    call manifest_preimage(envelope,manifest_text)
    envelope%manifest_sha256=sha256_ascii(manifest_text)

    call verify_kt17_checkpoint_envelope(envelope,producer_build_commit, &
      envelope%checkpoint%config,ok,local_reason)
    if(.not.ok) then
      reason='KT17_SELF_VERIFICATION_FAILED'
      return
    end if

    reason='KT17_ACCEPTED_CHECKPOINT_ENVELOPE_ENCODED'
  end subroutine encode_kt17_checkpoint_envelope

  subroutine verify_kt17_checkpoint_envelope(envelope,expected_build_commit,expected_config,ok,reason)
    type(kt17_checkpoint_envelope_t), intent(in) :: envelope
    character(len=*), intent(in) :: expected_build_commit
    type(kt15_application_config_t), intent(in) :: expected_config
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason

    character(len=64) :: config_hash,payload_hash,manifest_hash
    character(len=:), allocatable :: manifest_text
    character(len=128) :: local_reason
    logical :: config_ok

    ok=.false.
    reason='UNSET'

    if(trim(envelope%schema_id)/=KT17_ENVELOPE_SCHEMA) then
      reason='KT17_ENVELOPE_SCHEMA_MISMATCH'
      return
    end if
    if(trim(envelope%hash_algorithm_id)/=KT17_HASH_ALGORITHM) then
      reason='KT17_HASH_ALGORITHM_MISMATCH'
      return
    end if
    if(trim(envelope%canonicalization_id)/=KT17_CANONICALIZATION) then
      reason='KT17_CANONICALIZATION_MISMATCH'
      return
    end if
    if(trim(envelope%feature_set_id)/=KT17_FEATURE_SET) then
      reason='KT17_FEATURE_SET_MISMATCH'
      return
    end if
    if(trim(envelope%diagnostic_policy_id)/=KT17_DIAGNOSTIC_POLICY) then
      reason='KT17_DIAGNOSTIC_POLICY_MISMATCH'
      return
    end if

    if(.not.canonical_hex(expected_build_commit,40) .or. &
       .not.canonical_hex(envelope%producer_build_commit,40)) then
      reason='KT17_BUILD_ID_INVALID'
      return
    end if
    if(trim(envelope%producer_build_commit)/=trim(expected_build_commit)) then
      reason='KT17_EXPECTED_BUILD_ID_MISMATCH'
      return
    end if
    if(trim(envelope%source_archive_sha256)/=KT17_SOURCE_ARCHIVE_SHA256 .or. &
       trim(envelope%testbank_sha256)/=KT17_TESTBANK_SHA256 .or. &
       trim(envelope%documentation_sha256)/=KT17_DOCUMENTATION_SHA256) then
      reason='KT17_EVIDENCE_IDENTITY_MISMATCH'
      return
    end if
    if(.not.canonical_hex(envelope%application_config_sha256,64) .or. &
       .not.canonical_hex(envelope%checkpoint_payload_sha256,64) .or. &
       .not.canonical_hex(envelope%manifest_sha256,64)) then
      reason='KT17_INTEGRITY_HASH_SYNTAX_INVALID'
      return
    end if

    call validate_kt15_application_config(expected_config,config_ok,local_reason)
    if(.not.config_ok) then
      reason='KT17_EXPECTED_CONFIG_INVALID'
      return
    end if
    if(.not.same_kt15_application_config(envelope%checkpoint%config,expected_config)) then
      reason='KT17_EXPECTED_CONFIG_MISMATCH'
      return
    end if

    call canonical_kt15_config_hash(envelope%checkpoint%config,config_hash,ok,local_reason)
    if(.not.ok .or. config_hash/=envelope%application_config_sha256) then
      ok=.false.
      reason='KT17_APPLICATION_CONFIG_INTEGRITY_MISMATCH'
      return
    end if

    call canonical_kt16_checkpoint_hash(envelope%checkpoint,payload_hash,ok,local_reason)
    if(.not.ok .or. payload_hash/=envelope%checkpoint_payload_sha256) then
      ok=.false.
      reason='KT17_CHECKPOINT_PAYLOAD_INTEGRITY_MISMATCH'
      return
    end if

    call manifest_preimage(envelope,manifest_text)
    manifest_hash=sha256_ascii(manifest_text)
    if(manifest_hash/=envelope%manifest_sha256) then
      ok=.false.
      reason='KT17_MANIFEST_INTEGRITY_MISMATCH'
      return
    end if

    call validate_kt16_application_checkpoint(envelope%checkpoint,ok,local_reason)
    if(.not.ok) then
      reason='KT17_EMBEDDED_KT16_CHECKPOINT_INVALID'
      return
    end if

    ok=.true.
    reason='VALID_KT17_ACCEPTED_CHECKPOINT_ENVELOPE'
  end subroutine verify_kt17_checkpoint_envelope

  subroutine restore_kt17_checkpoint_envelope(envelope,expected_build_commit, &
      expected_config,state,ok,reason)
    type(kt17_checkpoint_envelope_t), intent(in) :: envelope
    character(len=*), intent(in) :: expected_build_commit
    type(kt15_application_config_t), intent(in) :: expected_config
    type(kt15_application_state_t), intent(out) :: state
    logical, intent(out) :: ok
    character(len=*), intent(out) :: reason
    character(len=128) :: local_reason

    call verify_kt17_checkpoint_envelope(envelope,expected_build_commit,expected_config,ok,local_reason)
    if(.not.ok) then
      reason=trim(local_reason)
      return
    end if

    call restore_kt16_application_checkpoint(envelope%checkpoint,expected_config,state,ok,local_reason)
    if(.not.ok) then
      reason='KT17_KT16_RESTORE_FAILED'
      return
    end if

    reason='KT17_ACCEPTED_CHECKPOINT_ENVELOPE_RESTORED'
  end subroutine restore_kt17_checkpoint_envelope

end module mod_animo_checkpoint_manifest_integrity
